from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.unit_type import UnitType
from PyCaliper.uom.measurement_type import MeasurementType
import math
from builtins import staticmethod
import time

class PathParameters:
    # UOM, scaling factor and power cumulative along a conversion path
    def __init__(self, pathUOM: UnitOfMeasure, pathFactor: float):
        self.pathUOM = pathUOM
        self.pathFactor = pathFactor
          
class Reducer:
    def __init__(self):
        self.MAX_RECURSIONS = 100
        self.STARTING_LEVEL = -1
        self.terms = {}
        self.mapScalingFactor = 1
        self.pathExponents = []
        self.counter = 0
    
    def explode(self, unit: UnitOfMeasure):
        self.explodeRecursively(unit, self.STARTING_LEVEL)
        
    def explodeRecursively(self, unit: UnitOfMeasure, level: int):
        self.counter = self.counter + 1
        if (self.counter > self.MAX_RECURSIONS):
            args = unit.symbol
            msg = MeasurementSystem.getMessage("circular.references").format(*args)
            raise Exception(msg)
        
        # down a level
        level = level + 1
        
        # scaling factor to abscissa unit
        scalingFactor = unit.scalingFactor
        
        # explode the abscissa unit
        abscissaUnit = unit.abscissaUnit
        
        uom1 = abscissaUnit.uom1
        uom2 = abscissaUnit.uom2
        
        exp1 = abscissaUnit.exponent1
        exp2 = abscissaUnit.exponent2
        
        # scaling
        if (len(self.pathExponents) > 0):
            lastExponent = self.pathExponents[len(self.pathExponents) - 1]

            # compute the overall scaling factor
            factor = 1
            
            i = 0
            while (i < abs(lastExponent)):
                factor = factor * scalingFactor

                if (lastExponent < 0):
                    self.mapScalingFactor = self.mapScalingFactor / factor;
                else:
                    self.mapScalingFactor = self.mapScalingFactor * factor;
                i = i + 1
        else:
            self.mapScalingFactor = scalingFactor    
            
        if (uom1 is None):
            if (abscissaUnit.isTerminal() == False):
                # keep exploding down the conversion path
                currentMapFactor = self.mapScalingFactor
                self.mapScalingFactor = 1
                self.explodeRecursively(abscissaUnit, self.STARTING_LEVEL)
                self.mapScalingFactor = self.mapScalingFactor * currentMapFactor
            else:
                # multiply out all of the exponents down the path
                pathExponent = 1
                
                for exp in self.pathExponents:
                    pathExponent = pathExponent * exp
                
                # variable = 1 if something == 1 else 0
                invert = True if pathExponent < 0 else False
                
                i = 0
                while (i < abs(pathExponent)):
                    self.addTerm(abscissaUnit, invert)
        else:
            # explode UOM #1
            self.pathExponents.append(exp1)
            self.explodeRecursively(uom1, level)
            del self.pathExponents[level];  
            
        if (uom2 is not None):
            # explode UOM #2
            self.pathExponents.append(exp2)
            self.explodeRecursively(uom2, level)
            del self.pathExponents[level];     
            
        # up a level
        level = level - 1    
        
              
    def addTerm(self, uom: UnitOfMeasure, invert: bool):
        # add a UOM and exponent pair to the map of reduced Terms
        unitPower = 1
        power = 0

        if (not invert):
            # get existing power
            if (uom not in self.terms):
                # add first time
                power = unitPower
            else:
                # increment existing power                    
                if (uom != MeasurementSystem.instance().getOne()):
                    power = self.terms[uom] + unitPower
        else:
            # denominator with negative powers
            if (uom not in self.terms):
                # add first time
                power = -unitPower
            else:
                # decrement existing power
                if (uom != MeasurementSystem.instance().getOne()):
                    power = self.terms[uom] - unitPower

        if (power == 0):
            del self.terms[uom]
        else:
            if (uom != MeasurementSystem.instance().getOne()):
                self.terms[uom] = power
                
    def buildBaseString(self):
        numerator = ""
        denominator = ""
        
        numeratorCount = 0
        denominatorCount = 0
        
        # sort units by symbol (ascending)
        for unit in sorted(self.terms.keys()):
            power = self.terms[unit]
        
            if (power < 0):
                # negative, put in denominator
                if (len(denominator) > 0):
                        denominator = denominator + UnitOfMeasure.__MULT
                        
                if (unit != MeasurementSystem.instance().getOne()):
                        denominator = denominator + unit.getSymbol()
                        denominatorCount = denominatorCount + 1

                if (power < -1):
                    if (power == -2):
                        denominator = denominator + UnitOfMeasure.__SQ
                    elif (power == -3):
                        denominator = denominator + UnitOfMeasure.__CUBED
                    else:
                        denominator = denominator + UnitOfMeasure.__POW + abs(power)
            elif (power >= 1 and unit != MeasurementSystem.instance().getOne()):
                # positive, put in numerator
                if (len(numerator) > 0):
                    numerator = numerator + UnitOfMeasure.__MULT + unit.getSymbol()
                    numeratorCount = numeratorCount + 1

                if (power > 1):
                    if (power == 2):
                        numerator = numerator + UnitOfMeasure.__SQ
                    elif (power == 3):
                        numerator = numerator + UnitOfMeasure.__CUBED
                    else:
                        numerator = numerator + UnitOfMeasure.__POW + power
            else:
                # unary, don't add a '1'
                pass
            
        if (numeratorCount == 0):
            numerator = numerator + UnitOfMeasure.__ONE_CHAR

            result = None

            if (denominatorCount == 0):
                result = numerator
            else:
                if (denominatorCount == 1):
                    result = numerator + UnitOfMeasure.__DIV + denominator
                else:
                    result = numerator + UnitOfMeasure.__DIV + UnitOfMeasure.__LP + denominator + UnitOfMeasure.__RP

            return result       

class UnitOfMeasure(Symbolic):
    ## maximum number of characters in the symbol
    __MAX_SYMBOL_LENGTH = 16
       
    # operators    
    __MULT = '\xB7'
    __DIV = '/'
    __POW = '^'
    __SQ = '\xB2'
    __CUBED ='\xB3'
    __LP = '('
    __RP = ')'
    __ONE_CHAR = '1'
    
    def __init__(self, unitType: UnitType, name: str, symbol: str, description: str):
        super(name, symbol, description)
        self.initialize()
        self.unitType = unitType
            
    def initialize(self):
        self.conversionRegistry = {}
        self.category = MeasurementSystem.getUnitString("default.category.text")
        self.unit = None
        self.unitType = UnitType.UNCLASSIFIED     
        self.abscissaUnit = self
        self.scalingFactor = 1.0
        self.offset = 0.0
        self.uom1 = None
        self.uom2 = None
        self.exponent1 = None
        self.exponent2 = None
        self.bridgeScalingFactor = None
        self.bridgeOffset = None
        self.bridgeAbscissaUnit = None
        
    @staticmethod
    def isValidExponent(exponent: int) -> bool:
        return False if exponent is None else True
 
    def __hash__(self):
        return hash(self.args)
        
    def __eq__(self, other):
        # same type
        if (other == None or self.unitType != other.unitType):
            return False
        
        # same unit enumeration
        if (self.unit != None and other.unit != None and self.unit != other.unit):
            return False
        
        # same abscissa unit symbols            
        if (self.abscissaUnit.symbol != other.abscissaUnit.symbol):
            return False
        
        # similar factors
        if (not math.isclose(self.scalingFactor, other.scalingFactor)):
            return False
        
        # similar offsets
        if (not math.isclose(self.offset, other.offset)):
            return False

        return True;
    
    def __lt__ (self, other):
        return self.__symbol < other.__symbol

    def __gt__ (self, other):
        return self.__symbol > other.__symbol
    
    def __ne__ (self, other):
        return not self.__eq__(other)
    
    def setBaseSymbol(self, symbol: str):
            self.baseSymbol = symbol
        
    def setPowerProduct(self, uom1: UnitOfMeasure, exponent1: int, uom2: UnitOfMeasure, exponent2: int):
        self.setPowerProduct(uom1, exponent1)
        self.uom2 = uom2
        self.exponent2 = exponent2
        
    def setProductUnits(self, multiplier: UnitOfMeasure, multiplicand: UnitOfMeasure):
        if (multiplier is None):
            args = self.symbol
            msg = MeasurementSystem.getMessage("multiplier.cannot.be.null").format(*args)
            raise Exception(msg)

        if (multiplicand is None):
            args = self.symbol
            msg = MeasurementSystem.getMessage("multiplicand.cannot.be.null").format(*args)
            raise Exception(msg)            

        self.setPowerProduct(multiplier, 1, multiplicand, 1)
        
    def setQuotientUnits(self, dividend: UnitOfMeasure, divisor: UnitOfMeasure):
        if (dividend is None):
            args = self.symbol
            msg = MeasurementSystem.getMessage("dividend.cannot.be.null").format(*args)
            raise Exception(msg)

        if (divisor is None):
            args = self.symbol
            msg = MeasurementSystem.getMessage("divisor.cannot.be.null").format(*args)
            raise Exception(msg)

        self.setPowerProduct(dividend, 1, divisor, -1)
        
    def getMeasurementType(self) -> MeasurementType:
        measurementType = MeasurementType.SCALAR
        
        if (self.exponent2 is not None and self.exponent2 < 0):
            measurementType = MeasurementType.QUOTIENT
        elif (self.exponent2 is not None and self.exponent2 > 0):
            measurementType = MeasurementType.PRODUCT
        elif (self.uom1 is not None and self.exponent1 is not None):
            measurementType = MeasurementType.POWER
            
        return measurementType
    
    def getReducer(self) -> Reducer:
        reducer = Reducer()
        reducer.explode(self)
        return reducer
    
    def getBaseUnitsOfMeasure(self):
        return self.getReducer().terms
    
    def power(self, exponent: int) -> UnitOfMeasure:
        return MeasurementSystem.instance().createPowerUOM(self, exponent)
    
    def isTerminal(self):
        return True if self == self.abscissaUnit else False
    
    def setBridgeConversion(self, scalingFactor: float, abscissaUnit: UnitOfMeasure, offset: float):
        self.bridgeScalingFactor = scalingFactor
        self.bridgeAbscissaUnit = abscissaUnit
        self.bridgeOffset = offset


    def setConversion(self, scalingFactor: float, abscissaUnit: UnitOfMeasure, offset: float):
        if (abscissaUnit is None):
            msg = MeasurementSystem.getMessage("unit.cannot.be.null")
            raise Exception(msg)

        # self conversion is special
        if (self == abscissaUnit):
            if (scalingFactor != 1.0 or offset != 0.0):
                msg = MeasurementSystem.getMessage("conversion.not.allowed")
                raise Exception(msg)

        # unit has been previously cached, so first remove it, then cache again
        MeasurementSystem.instance().unregisterUnit(self)
        
        self.baseSymbol = None
        self.scalingFactor = scalingFactor
        self.abscissaUnit = abscissaUnit
        self.offset = offset

        # re-cache
        MeasurementSystem.instance().registerUnit(self)
        
    def getPowerExponent(self) -> int:
        return self.exponent1
    
    def getDividend(self) -> UnitOfMeasure:
        return self.uom1;
    
    def getDivisor(self) -> UnitOfMeasure:
        return self.uom2; 
    
    def getMultiplier(self) -> UnitOfMeasure:
        return self.uom1; 
    
    def getMultiplicand(self) -> UnitOfMeasure:
        return self.uom2; 
    
    def setPowerUnit(self, base: UnitOfMeasure, exponent: int):
        if (base is None):
            args = self.symbol
            msg = MeasurementSystem.getMessage("base.cannot.be.null").format(*args)
            raise Exception(msg)

        # special cases
        if (exponent == -1):
            self.setPowerProduct(MeasurementSystem.instance().getOne(), 1, base, -1)
        else:
            self.setPowerProduct(base, exponent, None, None)
    
    @staticmethod    
    def generateIntermediateSymbol() -> str:
        ms = time.time_ns() // 1000000 
        return str(ms)

    @staticmethod 
    def generatePowerSymbol(base: UnitOfMeasure, exponent: int) -> str:
        return base.symbol + UnitOfMeasure.__POW + str(exponent)

    @staticmethod
    def generateProductSymbol(multiplier: UnitOfMeasure, multiplicand: UnitOfMeasure) -> str:
        symbol = None
        if (multiplier == multiplicand):
            symbol = multiplier.symbol + UnitOfMeasure.__SQ
        else:
            symbol = multiplier.symbol + UnitOfMeasure.__MULT + multiplicand.symbol
        return symbol

    @staticmethod
    def generateQuotientSymbol(dividend: UnitOfMeasure, divisor: UnitOfMeasure) -> str:
        return dividend.symbol + UnitOfMeasure.__DIV + divisor.symbol   
    
    def clonePower(self, uom: UnitOfMeasure) -> UnitOfMeasure:
        newUOM = UnitOfMeasure()
        newUOM.setUnitType(self.unitType);

        # check if quotient
        exponent = 1
        if (UnitOfMeasure.isValidExponent(self.getPowerExponent())):
            exponent = self.getPowerExponent()

        one = MeasurementSystem.instance().getOne()
        if (self.getMeasurementType() == MeasurementType.QUOTIENT):
            if (self.getDividend() == one):
                exponent = self.exponent2
            elif (self.getDivisor() == one):
                exponent = self.exponent1
               
        newUOM.setPowerUnit(uom, exponent)
        symbol = UnitOfMeasure.generatePowerSymbol(uom, exponent)
        newUOM.symbol = symbol
        newUOM.name = symbol

        return newUOM
   
    def classify(self):
        if (self.unitType != UnitType.UNCLASSIFIED):
            # already classified
            return self

        # base unit map
        uomBaseMap = self.getReducer().terms

        # try to find this map in the unit types
        matchedType = UnitType.UNCLASSIFIED

        for unitType in UnitType:
            unitTypeMap = MeasurementSystem.instance().getTypeMap(unitType)

            if (len(unitTypeMap) != len(uomBaseMap)):
                # not a match
                continue

            match = True

            # same size, now check base unit types and exponents
            for uomBaseEntry in uomBaseMap.items():
                uomBaseType = uomBaseEntry[0].unitType;
                unitValue = unitTypeMap[uomBaseType]

                if (unitValue is None or unitValue != uomBaseEntry[1]):
                    # not a match
                    match = False
                    break

            if (match):
                matchedType = unitType
                break

        if (matchedType != UnitType.UNCLASSIFIED):
            self.unitType = matchedType

        return self
