import math
import time
from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.enums import MeasurementType
from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit

##
# This class reduces a unit of measure to its most basic scalar units of measure.
#
class Reducer:
    # operators    
    MULT = '\xB7'
    DIV = '/'
    POW = '^'
    SQ = '\xB2'
    CUBED = '\xB3'
    LP = '('
    RP = ')'
    ONE = '1'
        
    def __init__(self):
        self.MAX_RECURSIONS = 100
        self.STARTING_LEVEL = -1
        self.terms = {}
        self.mapScalingFactor = 1.0
        self.pathExponents = []
        self.counter = 0
    
    def explode(self, uom):
        self.explodeRecursively(uom, self.STARTING_LEVEL)
        
    def explodeRecursively(self, uom, level):
        self.counter = self.counter + 1
        if (self.counter > self.MAX_RECURSIONS):
            msg = Localizer.instance().messageStr("circular.references").format(uom.symbol)
            raise Exception(msg)
        
        # down a level
        level = level + 1
        
        # scaling
        if (len(self.pathExponents) > 0):
            lastExponent = self.pathExponents[len(self.pathExponents) - 1]

            # compute the overall scaling factor
            factor = 1.0
            
            for _ in range(abs(lastExponent)):
                factor = factor * uom.scalingFactor

            if (lastExponent < 0):
                self.mapScalingFactor = self.mapScalingFactor / factor
            else:
                self.mapScalingFactor = self.mapScalingFactor * factor
        else:
            self.mapScalingFactor = uom.scalingFactor    
            
        if (uom.abscissaUnit.uom1 is None):
            if (not uom.abscissaUnit.isTerminal()):
                # keep exploding down the conversion path
                currentMapFactor = self.mapScalingFactor
                self.mapScalingFactor = 1.0
                self.explodeRecursively(uom.abscissaUnit, self.STARTING_LEVEL)
                self.mapScalingFactor = self.mapScalingFactor * currentMapFactor
            else:
                # multiply out all of the exponents down the path
                pathExponent = 1
                
                for exp in self.pathExponents:
                    pathExponent = pathExponent * exp
                
                invert = True if pathExponent < 0 else False
                
                for _ in range(abs(pathExponent)):
                    self.addTerm(uom.abscissaUnit, invert)
        else:
            # explode UOM #1
            self.pathExponents.append(uom.abscissaUnit.exponent1)
            self.explodeRecursively(uom.abscissaUnit.uom1, level)
            del self.pathExponents[level]  
            
        if (uom.abscissaUnit.uom2 is not None):
            # explode UOM #2
            self.pathExponents.append(uom.abscissaUnit.exponent2)
            self.explodeRecursively(uom.abscissaUnit.uom2, level)
            del self.pathExponents[level]     
            
        # up a level
        level = level - 1   
                 
    def addTerm(self, uom, invert):        
        # add a UOM and exponent pair to the map of reduced Terms
        unitPower = 1
        power = 0

        if (not invert):
            # get existing power
            if (uom not in self.terms.keys()):
                # add first time
                power = unitPower
            else:
                # increment existing power                    
                if (uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                    power = self.terms[uom] + unitPower
        else:
            # denominator with negative powers
            if (uom not in self.terms.keys()):
                # add first time
                power = -unitPower
            else:
                # decrement existing power
                if (uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                    power = self.terms[uom] - unitPower

        if (power == 0):
            del self.terms[uom]
        else:
            if (uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                self.terms[uom] = power
                
    def buildBaseString(self):
        numerator = ""
        denominator = ""
        
        numeratorCount = 0
        denominatorCount = 0
        
        # sort units by symbol (ascending)
        sortedTerms = sorted(self.terms.keys())
        for uom in sortedTerms:
            power = self.terms[uom]
        
            if (power < 0):
                # negative, put in denominator
                if (len(denominator) > 0):
                    denominator = denominator + Reducer.MULT
                        
                if (uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                    denominator = denominator + uom.symbol
                    denominatorCount = denominatorCount + 1

                if (power < -1):
                    if (power == -2):
                        denominator = denominator + Reducer.SQ
                    elif (power == -3):
                        denominator = denominator + Reducer.CUBED
                    else:
                        denominator = denominator + Reducer.POW + str(abs(power))
            elif (power >= 1 and uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                # positive, put in numerator
                if (len(numerator) > 0):
                    numerator = numerator + Reducer.MULT
                numerator = numerator + uom.symbol
                numeratorCount = numeratorCount + 1

                if (power > 1):
                    if (power == 2):
                        numerator = numerator + Reducer.SQ
                    elif (power == 3):
                        numerator = numerator + Reducer.CUBED
                    else:
                        numerator = numerator + Reducer.POW + str(power)
            else:
                # unary, don't add a '1'
                pass
            
        if (numeratorCount == 0):
            numerator = numerator + Reducer.ONE

        result = None

        if (denominatorCount == 0):
            result = numerator
        else:
            if (denominatorCount == 1):
                result = numerator + Reducer.DIV + denominator
            else:
                result = numerator + Reducer.DIV + Reducer.LP + denominator + Reducer.RP

        return result       

    def __str__(self):
        return str(self.mapScalingFactor) + str(self.terms)
    
##
# This class holds the unit of measure and cumulative scaling factor along a conversion path
#
class PathParameters:
    # UOM, scaling factor and power cumulative along a conversion path
    def __init__(self, pathUOM, pathFactor):
        self.pathUOM = pathUOM
        self.pathFactor = pathFactor

##
# The UnitOfMeasure class represents a unit of measure.
# <p>
# A UnitOfMeasure can have a linear conversion (y = ax + b) to another unit of
# measure in the same internationally recognized measurement system of
# International Customary, SI, US or British Imperial. Or, the unit of measure
# can have a conversion to another custom unit of measure. It is owned by the
# unified {@link MeasurementSystem} defined by this project.
# </p>
# 
# <p>
# A unit of measure is categorized by scalar (simple unit), quotient (divisor
# and dividend units), product (multiplier and multiplicand units) or power
# (unit with an integral exponent). More than one representation of a unit of
# measure is possible. For example, a unit of "per second" could be a quotient
# of "1/s" (e.g. an inverted second) or a power of s^-1.
# </p>
# 
# <p>
# A unit of measure also has an enumerated {@link UnitType} (for example LENGTH
# or MASS) and a unique {@link Unit} discriminator (for example METRE). <br>
# A basic unit (a.k.a fundamental unit in the SI system) can have a bridge
# conversion to another basic unit in another recognized measurement system.
# This conversion is defined unidirectionally. For example, an International
# Customary foot is 0.3048 SI metres. The conversion from metre to foot is just
# the inverse of this relationship.
# </p>
# 
# <p>
# A unit of measure has a base symbol, for example 'm' for metre. A base symbol
# is one that consists only of the symbols for the base units of measure. In
# the SI system, the base units are well-defined. The derived units such as
# Newton all have base symbols expressed in the fundamental units of length
# (metre), mass (kilogram), time (second), temperature (Kelvin), plane angle
# (radian), electric charge (Coulomb) and luminous intensity (candela). In the
# US and British systems, base units are not defined. Caliper uses foot for
# length, pound mass for mass and Rankine for temperature. This base symbol is
# used in unit of measure conversions to uniquely identify the target unit.
# </p>
# <p>
# The SI system has defined prefixes (e.g. "centi") for 1/100th of another unit
# (e.g. metre). Instead of defining all the possible unit of measure
# combinations, the {@link MeasurementSystem} is able to create units by
# specifying the {@link Prefix} and target unit of measure. Similarly, computer
# science has defined prefixes for bytes (e.g. "mega").
#        
class UnitOfMeasure(Symbolic):  
    MAX_SYMBOL_LENGTH = 16
             
    def __init__(self, unitType=UnitType.UNCLASSIFIED, name=None, symbol=None, description=None):
        super().__init__(name, symbol, description)
        
        self.conversionRegistry = {}
        self.category = Localizer.instance().langStr("default.category.text")
        self.unit = None
        self.unitType = unitType    
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

    ##
    # Check to see if the exponent is valid
    # 
    # @param exponent
    #            Power exponent
    # @return True if it is a valid exponent  
    @staticmethod
    def isValidExponent(exponent):
        return False if exponent is None else True
 
    def __hash__(self):
        return hash(str(self.unitType) + self.symbol)
        
    def __eq__(self, other):
        # same type
        if (other is None or self.unitType != other.unitType):
            return False
        
        # same unit enumeration
        if (self.unit is not None and other.unit is not None and self.unit != other.unit):
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
    
    def __lt__(self, other):
        return self.symbol < other.symbol

    def __gt__(self, other):
        return self.symbol > other.symbol
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        # type
        value = Localizer.instance().langStr("unit.type.text") + " " + str(self.unitType) + ", "
        
        # enumeration
        if (self.unit is not None):
            value = value + Localizer.instance().langStr("enum.text") + " " + str(self.unit) + ", "
            
        # symbol
        value = value + Localizer.instance().langStr("symbol.text") + " " + self.symbol + ", "
        value = value + Localizer.instance().langStr("conversion.text") + " "
        
        # scaling factor
        if (not math.isclose(self.scalingFactor, 1.0)):
            value = value + str(self.scalingFactor) + Reducer.MULT
            
        # abscissa unit
        if (self.abscissaUnit is not None):
            value = value + self.abscissaUnit.symbol
            
        # offset
        if (not math.isclose(self.offset, 0.0)):   
            value = value + " + " + str(self.offset) 
            
        # base symbol
        value = value + ", " + Localizer.instance().langStr("base.text") + " " + self.getBaseSymbol()
            
        return value
    
    def setBaseSymbol(self, symbol):
        self.baseSymbol = symbol
        
    def setPowerProduct(self, uom1, exponent1, uom2, exponent2):
        self.uom1 = uom1
        self.exponent1 = exponent1
        self.uom2 = uom2
        self.exponent2 = exponent2
     
    ##
    # Set the multiplier and multiplicand
    # 
    # @param multiplier
    #            Multiplier
    # @param multiplicand
    #            Multiplicand  
    def setProductUnits(self, multiplier, multiplicand):
        if (multiplier is None):
            msg = Localizer.instance().messageStr("multiplier.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        if (multiplicand is None):
            msg = Localizer.instance().messageStr("multiplicand.cannot.be.null").format(self.symbol)
            raise Exception(msg)            

        self.setPowerProduct(multiplier, 1, multiplicand, 1)

    ##
    # Set the dividend and divisor
    # 
    # @param dividend
    #            Dividend
    # @param divisor
    #            Divisor  
    def setQuotientUnits(self, dividend, divisor):
        if (dividend is None):
            msg = Localizer.instance().messageStr("dividend.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        if (divisor is None):
            msg = Localizer.instance().messageStr("divisor.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        self.setPowerProduct(dividend, 1, divisor, -1)

    ##
    # Get the measurement type
    # 
    # @return {@link MeasurementType} 
    def getMeasurementType(self):
        measurementType = MeasurementType.SCALAR
        
        if (self.exponent2 is not None and self.exponent2 < 0):
            measurementType = MeasurementType.QUOTIENT
        elif (self.exponent2 is not None and self.exponent2 > 0):
            measurementType = MeasurementType.PRODUCT
        elif (self.uom1 is not None and self.exponent1 is not None):
            measurementType = MeasurementType.POWER
            
        return measurementType
    
    def getReducer(self):
        reducer = Reducer()
        reducer.explode(self)
        return reducer

    ##
    # Get the most reduced units of measure
    # 
    # @return Map of {@link UnitOfMeasure} and exponent
    def getBaseUnitsOfMeasure(self):
        return self.getReducer().terms

    ##
    # Check to see if this unit of measure has a conversion to another unit of
    # measure other than itself.
    # 
    # @return True if it does not
    def isTerminal(self):
        return True if self == self.abscissaUnit else False
    
    def setBridgeConversion(self, scalingFactor, abscissaUnit, offset):
        self.bridgeScalingFactor = scalingFactor
        self.bridgeAbscissaUnit = abscissaUnit
        self.bridgeOffset = offset

    ##
    # Define a conversion with the specified scaling factor, abscissa unit of
    # measure and scaling factor.
    # 
    # @param scalingFactor
    #            Factor
    # @param abscissaUnit
    #            {@link UnitOfMeasure}
    # @param offset
    #            Offset
    def setConversion(self, scalingFactor, abscissaUnit, offset=0.0):
        if (abscissaUnit is None):
            msg = Localizer.instance().messageStr("unit.cannot.be.null")
            raise Exception(msg)

        # self conversion is special
        if (self == abscissaUnit):
            if (scalingFactor != 1.0 or offset != 0.0):
                msg = Localizer.instance().messageStr("conversion.not.allowed")
                raise Exception(msg)

        # unit has been previously cached, so first remove it, then cache again
        CacheManager.instance().unregisterUOM(self)
        
        self.baseSymbol = None
        self.scalingFactor = scalingFactor
        self.abscissaUnit = abscissaUnit
        self.offset = offset

        # re-cache
        CacheManager.instance().registerUOM(self)

    ##
    # Get the exponent of a power unit
    # 
    # @return Exponent
    def getPowerExponent(self):
        return self.exponent1

    ##
    # Get the dividend unit of measure
    # 
    # @return {@link UnitOfMeasure}
    def getDividend(self):
        return self.uom1
    
    ##
    # Get the divisor unit of measure
    # 
    # @return {@link UnitOfMeasure}
    def getDivisor(self):
        return self.uom2 

    ##
    # Get the multiplier
    # 
    # @return {@link UnitOfMeasure}
    def getMultiplier(self):
        return self.uom1 
    
    ##
    # Get the multiplicand
    # 
    # @return {@link UnitOfMeasure}
    def getMultiplicand(self):
        return self.uom2 

    ##
    # Set the base unit of measure and exponent
    # 
    # @param base
    #            Base unit of measure
    # @param exponent
    #            Exponent
    #
    def setPowerUnit(self, base, exponent):
        if (base is None):
            msg = Localizer.instance().messageStr("base.cannot.be.null").format(self.symbol)
            raise Exception(msg)

        # special cases
        if (exponent == -1):
            self.setPowerProduct(CacheManager.instance().getUOMByUnit(Unit.ONE), 1, base, -1)
        else:
            self.setPowerProduct(base, exponent, None, None)
    
    @staticmethod    
    def generateIntermediateSymbol():
        # generate a symbol for units of measure created as the result of
        # intermediate multiplication and division operations. These symbols are
        # not cached.
        ns = str(time.time_ns())
        return ns[:UnitOfMeasure.MAX_SYMBOL_LENGTH]

    @staticmethod 
    def generatePowerSymbol(base, exponent):
        return base.symbol + Reducer.POW + str(exponent)

    @staticmethod
    def generateProductSymbol(multiplier, multiplicand):
        symbol = None
        if (multiplier == multiplicand):
            symbol = multiplier.symbol + Reducer.SQ
        else:
            symbol = multiplier.symbol + Reducer.MULT + multiplicand.symbol
        return symbol

    @staticmethod
    def generateQuotientSymbol(dividend, divisor):
        return dividend.symbol + Reducer.DIV + divisor.symbol   
    
    def clonePower(self, uom):
        newUOM = UnitOfMeasure()
        newUOM.unitType = self.unitType

        # check if quotient
        exponent = 1
        if (UnitOfMeasure.isValidExponent(self.getPowerExponent())):
            exponent = self.getPowerExponent()

        one = CacheManager.instance().getUOMByUnit(Unit.ONE)
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
   
    ##
    # If the unit of measure is unclassified, from its base unit map find a
    # matching unit type.
    # 
    # @return {@link UnitOfMeasure}
    #
    def classify(self):        
        if (self.unitType is not None and self.unitType != UnitType.UNCLASSIFIED):
            # already classified
            return self

        # base unit map
        uomBaseMap = self.getReducer().terms

        # try to find this map in the unit types
        matchedType = UnitType.UNCLASSIFIED

        for unitType in UnitType:
            unitTypeMap = CacheManager.instance().getTypeMap(unitType)

            if (len(unitTypeMap) != len(uomBaseMap)):
                # not a match
                continue

            match = True

            # same size, now check base unit types and exponents
            for uomBaseEntry in uomBaseMap.items():
                uomBaseType = uomBaseEntry[0].unitType
                
                unitValue = None
                if (uomBaseType in unitTypeMap):
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
    def checkTypes(uom1, uom2):
        thisType = uom1.unitType
        targetType = uom2.unitType

        if (thisType != UnitType.UNCLASSIFIED and targetType != UnitType.UNCLASSIFIED and thisType != UnitType.UNITY and targetType != UnitType.UNITY and thisType != targetType):
            msg = Localizer.instance().messageStr("must.be.same.as").format(uom1, thisType, uom2, targetType)
            raise Exception(msg)

    ##
    # Get the unit of measure symbol in the fundamental units for that system.
    # For example a Newton is a kg.m/s2.
    # 
    # @return Base symbol
    #
    def getBaseSymbol(self):
        if (self.baseSymbol is None):
            powerMap = self.getReducer()
            self.baseSymbol = powerMap.buildBaseString()
            
        return self.baseSymbol
    
    def traversePath(self):
        pathUOM = self
        pathFactor = 1.0
        
        while (True):
            scalingFactor = pathUOM.scalingFactor
            abscissa = pathUOM.abscissaUnit

            pathFactor = pathFactor * scalingFactor

            if (pathUOM == abscissa):
                break

            # next UOM on path
            pathUOM = abscissa
            
        return PathParameters(pathUOM, pathFactor)
    
    def checkOffset(self, other):
        if (not math.isclose(other.offset, 0.0)):
            msg = Localizer.instance().messageStr("offset.not.supported").format(str(other))
            raise Exception(msg)
        
    def clearCache(self):
        self.conversionRegistry.clear()
        
    def clonePowerProduct(self, uom1, uom2):        
        invert = False
        one = CacheManager.instance().getUOMByUnit(Unit.ONE)
    
        # check if quotient
        if (self.getMeasurementType() == MeasurementType.QUOTIENT):
            if (uom2 == one): 
                msg = Localizer.instance().messageStr("incompatible.units").format(self, one)
                raise Exception(msg)
            
            invert = True
        else: 
            if (uom1 == one or uom2 == one): 
                msg = Localizer.instance().messageStr("incompatible.units").format(self, one)
                raise Exception(msg)

        newUOM = uom1.multiplyOrDivide(uom2, invert)
        newUOM.unitType = self.unitType

        return newUOM 
    
    def multiplyOrDivide(self, other, invert): 
        if (other is None):
            msg = Localizer.instance().messageStr("unit.cannot.be.null")
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
            
            otherPower = None
            
            if (thisUOM in otherMap):
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
        result = UnitOfMeasure()

        if (not invert):
            result.setProductUnits(self, other)
            result.symbol = self.generateProductSymbol(result.getMultiplier(), result.getMultiplicand())
        else:
            result.setQuotientUnits(self, other)
            result.symbol = self.generateQuotientSymbol(result.getDividend(), result.getDivisor())
            
        # constrain symbol to a maximum length
        if (len(result.symbol) > UnitOfMeasure.MAX_SYMBOL_LENGTH):
            result.symbol = self.generateIntermediateSymbol()
            
        baseSymbol = resultReducer.buildBaseString()
        baseUOM = CacheManager.instance().getBaseUOM(baseSymbol)
        
        if (baseUOM is not None):
            # there is a conversion to the base UOM
            thisFactor = thisReducer.mapScalingFactor
            otherFactor = otherReducer.mapScalingFactor

            resultFactor = 0.0
            if (not invert):
                resultFactor = thisFactor * otherFactor
            else:
                resultFactor = thisFactor / otherFactor
            
            result.scalingFactor = resultFactor
            result.abscissaUnit = baseUOM
            result.unitType = baseUOM.unitType

        return result
    
    def convertScalarToScalar(self, targetUOM):
        scalingFactor = 0.0
        
        if (self.abscissaUnit == targetUOM):
            # direct conversion
            scalingFactor = self.scalingFactor
        else:
            # indirect conversion
            scalingFactor = self.convertUnit(targetUOM)
        
        return scalingFactor
    
    def getBridgeFactor(self, uom):
        factor = 0.0
        
        # check for our bridge
        if (self.bridgeAbscissaUnit is not None):
            factor = self.bridgeScalingFactor
        else:
            # try other side
            if (uom.bridgeAbscissaUnit is not None):
                toUOM = uom.bridgeAbscissaUnit

                if (toUOM == self):
                    factor = 1.0 / uom.bridgeScalingFactor
        
        return factor
    
    ##
    # Divide two units of measure to create a third one.
    # 
    # @param divisor
    #            {@link UnitOfMeasure}
    # @return {@link UnitOfMeasure}
    #
    def divide(self, divisor):
        return self.multiplyOrDivide(divisor, True)
    
    def getBaseUOM(self):
        baseSymbol = self.getBaseSymbol()
        return CacheManager.instance().getBaseUOM(baseSymbol)
    
    def convertUnit(self, targetUOM):
        # get path factors in each system
        thisParameters = self.traversePath()
        targetParameters = targetUOM.traversePath()

        thisPathFactor = thisParameters.pathFactor
        thisBase = thisParameters.pathUOM

        targetPathFactor = targetParameters.pathFactor
        targetBase = targetParameters.pathUOM

        # check for a base conversion unit bridge
        bridgeFactor = thisBase.getBridgeFactor(targetBase)

        if (bridgeFactor != 0.0):
            thisPathFactor = thisPathFactor * bridgeFactor

        # new path amount
        scalingFactor = thisPathFactor / targetPathFactor

        return scalingFactor

    ##
    # Get the factor to convert to the unit of measure
    # 
    # @param targetUOM
    #            Target {@link UnitOfMeasure}
    # @return conversion factor
    #
    def getConversionFactor(self, targetUOM):
        if (targetUOM is None):
            msg = Localizer.instance().messageStr("unit.cannot.be.null")
            raise Exception(msg)
        
        # first check the cache
        cachedFactor = None
        if targetUOM in self.conversionRegistry: 
            cachedFactor = self.conversionRegistry[targetUOM]

        if (cachedFactor is not None):
            return cachedFactor
        
        UnitOfMeasure.checkTypes(self, targetUOM)
        
        fromReducer = self.getReducer()
        toReducer = targetUOM.getReducer()

        fromMap = fromReducer.terms
        toMap = toReducer.terms

        if (len(fromMap) != len(toMap)):
            msg = Localizer.instance().messageStr("incompatible.units").format(self, targetUOM)
            raise Exception(msg)
        
        fromFactor = fromReducer.mapScalingFactor
        toFactor = toReducer.mapScalingFactor

        factor = 1.0

        # compute map factor
        matchCount = 0
        
        for fromEntry in fromMap.items():
            fromUOM = fromEntry[0]
            fromType = fromUOM.unitType
            fromPower = fromEntry[1]

            for toEntry in toMap.items():
                toType = toEntry[0].unitType

                if (fromType == toType):
                    matchCount = matchCount + 1
                    toUOM = toEntry[0]
                    bd = fromUOM.convertScalarToScalar(toUOM)
                    bd = math.pow(bd, fromPower)
                    factor = factor * bd
                    break

        if (matchCount != len(fromMap)):
            msg = Localizer.instance().messageStr("incompatible.units").format(self, targetUOM)
            raise Exception(msg)

        scaling = fromFactor / toFactor
        cachedFactor = factor * scaling

        # cache it
        self.conversionRegistry[targetUOM] = cachedFactor

        return cachedFactor
    
    ##
    # Get the base unit of measure for the power
    # 
    # @return {@link UnitOfMeasure}
    def getPowerBase(self):
        return self.uom1

    ##
    # Invert a unit of measure to create a new one
    # 
    # @return {@link UnitOfMeasure}
    #
    def invert(self):
        inverted = None

        if (UnitOfMeasure.isValidExponent(self.exponent2) and self.exponent2 < 0):
            inverted = self.getDivisor().divide(self.getDividend())
        else:
            inverted = CacheManager.instance().getUOMByUnit(Unit.ONE).divide(self)

        return inverted

    ##
    # Multiply two units of measure to create a third one.
    # 
    # @param multiplicand
    #            {@link UnitOfMeasure}
    # @return {@link UnitOfMeasure}
    #
    def multiply(self, multiplicand):
        return self.multiplyOrDivide(multiplicand, False)
