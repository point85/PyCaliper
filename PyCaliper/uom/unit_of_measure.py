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
            msg = MeasurementSystem.messageStr("circular.references").format(unit.symbol)
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
                    self.mapScalingFactor = self.mapScalingFactor / factor
                else:
                    self.mapScalingFactor = self.mapScalingFactor * factor
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
            del self.pathExponents[level]  
            
        if (uom2 is not None):
            # explode UOM #2
            self.pathExponents.append(exp2)
            self.explodeRecursively(uom2, level)
            del self.pathExponents[level]     
            
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
        
        self.conversionRegistry = {}
        self.category = MeasurementSystem.unitStr("default.category.text")
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
        self.unitType = unitType
        self.baseSymbol = None
        
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

        return True
    
    def __lt__ (self, other):
        return self.__symbol < other.__symbol

    def __gt__ (self, other):
        return self.__symbol > other.__symbol
    
    def __ne__ (self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        # type
        value = MeasurementSystem.unitStr("unit.type.text") + " " + str(self.unitType) + ", "
        
        # enumeration
        if (self.unit is not None):
            value = value + MeasurementSystem.unitStr("enum.text") + " " + str(self.unit) + ", "
            
        # symbol
        value = value + MeasurementSystem.unitStr("symbol.text") + " " + self.symbol + ", "
        value = value + MeasurementSystem.unitStr("conversion.text") + " "
        
        # scaling factor
        if (not math.isclose(self.scalingFactor, 1.0)):
            value = value + str(self.scalingFactor) + UnitOfMeasure.__MULT
            
        # abscissa unit
        if (self.abscissaUnit is not None) :
            value = value + self.abscissaUnit.symbol
            
        # offset
        if (not math.isclose(self.offset, 0.0)):   
            value = value + " + " + str(self.offset) + ", " + MeasurementSystem.unitStr("base.text") + " "
            
        # base symbol
        value = value + self.getBaseSymbol()
            
        return value
    
    def setBaseSymbol(self, symbol: str):
            self.baseSymbol = symbol
        
    def setPowerProduct(self, uom1: UnitOfMeasure, exponent1: int, uom2: UnitOfMeasure, exponent2: int):
        self.setPowerProduct(uom1, exponent1)
        self.uom2 = uom2
        self.exponent2 = exponent2
        
    def setProductUnits(self, multiplier: UnitOfMeasure, multiplicand: UnitOfMeasure):
        if (multiplier is None):
            msg = MeasurementSystem.messageStr("multiplier.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        if (multiplicand is None):
            msg = MeasurementSystem.messageStr("multiplicand.cannot.be.null").format(self.symbol)
            raise Exception(msg)            

        self.setPowerProduct(multiplier, 1, multiplicand, 1)
        
    def setQuotientUnits(self, dividend: UnitOfMeasure, divisor: UnitOfMeasure):
        if (dividend is None):
            msg = MeasurementSystem.messageStr("dividend.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        if (divisor is None):
            msg = MeasurementSystem.messageStr("divisor.cannot.be.null").format(self.symbol)
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
        with self.lock:
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
            msg = MeasurementSystem.messageStr("unit.cannot.be.null")
            raise Exception(msg)

        # self conversion is special
        if (self == abscissaUnit):
            if (scalingFactor != 1.0 or offset != 0.0):
                msg = MeasurementSystem.messageStr("conversion.not.allowed")
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
        return self.uom1
    
    def getDivisor(self) -> UnitOfMeasure:
        return self.uom2 
    
    def getMultiplier(self) -> UnitOfMeasure:
        return self.uom1 
    
    def getMultiplicand(self) -> UnitOfMeasure:
        return self.uom2 
    
    def setPowerUnit(self, base: UnitOfMeasure, exponent: int):
        if (base is None):
            msg = MeasurementSystem.messageStr("base.cannot.be.null").format(self.symbol)
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
        newUOM.setUnitType(self.unitType)

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
                uomBaseType = uomBaseEntry[0].unitType
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

    @staticmethod
    def checkTypes(uom1: UnitOfMeasure,  uom2: UnitOfMeasure):
        thisType = uom1.getUnitType()
        targetType = uom2.getUnitType()

        if (thisType != UnitType.UNCLASSIFIED and targetType != UnitType.UNCLASSIFIED and thisType != UnitType.UNITY \
            and targetType != UnitType.UNITY and  thisType != targetType):
            msg = MeasurementSystem.messageStr("must.be.same.as").format(uom1, uom1.getUnitType(), uom2, uom2.getUnitType())
            raise Exception(msg)
    
    def getBaseSymbol(self) -> str:
        with self.lock:
            if (self.baseSymbol is None):
                powerMap = self.getReducer()
                baseSymbol = powerMap.buildBaseString()
            
        return baseSymbol
    
    def traversePath(self) -> PathParameters:
        pathUOM = self
        pathFactor = 1.0
        
        while (True):
            scalingFactor = pathUOM.getScalingFactor()
            abscissa = pathUOM.getAbscissaUnit()

            pathFactor = pathFactor * scalingFactor

            if (pathUOM == abscissa):
                break

            # next UOM on path
            pathUOM = abscissa
            
        return PathParameters(pathUOM, pathFactor)
    
    def checkOffset(self, other: UnitOfMeasure):
        if (math.isclose(other.offset, 0.0)):
            msg = MeasurementSystem.messageStr("offset.not.supported").format(str(other))
            raise Exception(msg)
        
    def clearCache(self):
        self.conversionRegistry.clear()
        
    def clonePowerProduct(self, uom1: UnitOfMeasure, uom2: UnitOfMeasure) -> UnitOfMeasure:
        invert = False
        one = MeasurementSystem.instance().getOne()
    
            # check if quotient
        if (self.getMeasurementType() == MeasurementType.QUOTIENT):
            if (uom2 == one): 
                msg = MeasurementSystem.messageStr("incompatible.units").format(self, one)
                raise Exception(msg)
            
            invert = True
        else: 
            if (uom1 == one or uom2 == one): 
                msg = MeasurementSystem.messageStr("incompatible.units").format(self, one)
                raise Exception(msg)


        newUOM = uom1.multiplyOrDivide(uom2, invert)
        newUOM.unitType = self.unitType

        return newUOM 
    
    def multiplyOrDivide(self, other: UnitOfMeasure, invert: bool) -> UnitOfMeasure: 
        if (other is None):
            msg = MeasurementSystem.messageStr("unit.cannot.be.null")
            raise Exception(msg)
        
        self.checkOffset(self)
        self.checkOffset(other)
        
        # self base symbol map
        thisReducer = self.getReducer()
        thisMap = thisReducer.terms
        
        # other base symbol map
        otherReducer = other.getReducer()
        otherMap = otherReducer.terms
        
        # create a map of the unit of measure powers
        resultMap = {}
        
        # iterate over the multiplier's unit map
        for thisEntry in thisMap.items():
            thisUOM = thisEntry[0]
            thisPower = thisEntry[1]
            otherPower = otherMap[thisUOM]
            
            if (otherPower is not None):
                if (not invert):
                    # add to multiplier's power
                    thisPower = thisPower + otherPower
                else:
                    # subtract from dividend's power
                    thisPower = thisPower - otherPower

                # remove multiplicand or divisor UOM
                del otherMap[thisUOM]

            if (thisPower != 0):
                resultMap[thisUOM] = thisPower
    
        # add any remaining multiplicand terms and invert any remaining divisor terms
        for otherEntry in otherMap.items():
            otherUOM = otherEntry[0]
            otherPower = otherEntry[1]

            if (not invert):
                resultMap[otherUOM] = otherPower
            else:
                resultMap[otherUOM] = -otherPower
                
        # get the base symbol and possibly base UOM
        resultReducer = Reducer()
        resultReducer.terms = resultMap

        # product or quotient
        result = UnitOfMeasure(None, None, None, None)

        if (not invert):
            result.setProductUnits(self, other)
            result.symbol = self.generateProductSymbol(result.getMultiplier(), result.getMultiplicand())
        else:
            result.setQuotientUnits(self, other)
            result.symbol = self.generateQuotientSymbol(result.getDividend(), result.getDivisor())
            
        # constrain symbol to a maximum length
        if (len(result.symbol) > UnitOfMeasure.__MAX_SYMBOL_LENGTH):
            result.symbol = self.generateIntermediateSymbol()
            
        baseSymbol = resultReducer.buildBaseString()
        baseUOM = MeasurementSystem.instance().getBaseUOM(baseSymbol)
        
        if (baseUOM is not None):
            # there is a conversion to the base UOM
            thisFactor = thisReducer.scalingFactor
            otherFactor = otherReducer.scalingFactor

            resultFactor = 0.0
            if (not invert):
                resultFactor = thisFactor * otherFactor
            else:
                resultFactor = thisFactor / otherFactor
            
            result.scalingFactor = resultFactor
            result.abscissaUnit = baseUOM
            result.unitType = baseUOM.unitType

        return result

    """

    """