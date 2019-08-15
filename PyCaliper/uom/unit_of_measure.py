from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.unit_type import UnitType
from PyCaliper.uom.measurement_type import MeasurementType
from math import isclose

class UnitOfMeasure(Symbolic):
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
    
    def initialize(self):
        self.__conversionRegistry = {}
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
       
    def __init__(self, unitType: UnitType, name: str, symbol: str, description: str):
        super(name, symbol, description)
        self.initialize()
        self.unitType = unitType
    
    def __hash__(self):
        return hash(self.args)
    """
    """
    
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
        if (not isclose(self.scalingFactor, other.scalingFactor)):
            return False
        
        # similar offsets
        if (not isclose(self.offset, other.offset)):
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
    
    def setPowerProduct(self, uom: UnitOfMeasure, exponent: int):
        self.uom1 = uom
        self.exponent1 = exponent
        
    def setPowerProduct2(self, uom1: UnitOfMeasure, exponent1: int, uom2: UnitOfMeasure, exponent2: int):
        self.setPowerProduct(uom1, exponent1)
        self.uom2 = uom2
        self.exponent2 = exponent2
        
    def getMeasurementType(self) -> "MeasurementType":
        measurementType = MeasurementType.SCALAR
        
        if (self.exponent2 is not None and self.exponent2 < 0):
            measurementType = MeasurementType.QUOTIENT
        elif (self.exponent2 is not None and self.exponent2 > 0):
            measurementType = MeasurementType.PRODUCT
        elif (self.uom1 is not None and self.exponent1 is not None):
            measurementType = MeasurementType.POWER
            
        return measurementType
    
    def isTerminal(self):
        return True if self == self.abscissaUnit else False
    
    def setBridgeConversion(self, scalingFactor: float, abscissaUnit: UnitOfMeasure, offset: float):
        self.bridgeScalingFactor = scalingFactor
        self.bridgeAbscissaUnit = abscissaUnit
        self.bridgeOffset = offset

"""
    public void setConversion(double scalingFactor, UnitOfMeasure abscissaUnit, double offset) throws Exception {
        if (abscissaUnit == null) {
            throw new Exception(MeasurementSystem.getMessage("unit.cannot.be.null"));
        }

        // self conversion is special
        if (this.equals(abscissaUnit)) {
            if (Double.valueOf(scalingFactor).compareTo(1.0d) != 0 || Double.valueOf(offset).compareTo(0.0d) != 0) {
                throw new Exception(MeasurementSystem.getMessage("conversion.not.allowed"));
            }
        }

        // unit has been previously cached, so first remove it, then cache again
        MeasurementSystem.getSystem().unregisterUnit(this);
        baseSymbol = null;

        this.scalingFactor = scalingFactor;
        this.abscissaUnit = abscissaUnit;
        this.offset = offset;

        // re-cache
        MeasurementSystem.getSystem().registerUnit(this);
    }
"""        
        
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
                
"""

"""        
        


