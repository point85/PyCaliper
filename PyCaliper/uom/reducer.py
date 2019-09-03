from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.operands import Operands
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.unit import Unit


class Reducer:
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
            msg = Localizer.messageStr("circular.references").format(uom.symbol)
            raise Exception(msg)
        
        # down a level
        level = level + 1
        
        # scaling factor to abscissa unit
        scalingFactor = uom.scalingFactor
        
        # explode the abscissa unit
        abscissaUnit = uom.abscissaUnit
        
        uom1 = abscissaUnit.uom1
        uom2 = abscissaUnit.uom2
        
        exp1 = abscissaUnit.exponent1
        exp2 = abscissaUnit.exponent2
        
        # scaling
        if (len(self.pathExponents) > 0):
            lastExponent = self.pathExponents[len(self.pathExponents) - 1]

            # compute the overall scaling factor
            factor = 1.0
            
            for _ in range(abs(lastExponent)):
                factor = factor * scalingFactor

                if (lastExponent < 0):
                    self.mapScalingFactor = self.mapScalingFactor / factor
                else:
                    self.mapScalingFactor = self.mapScalingFactor * factor
        else:
            self.mapScalingFactor = scalingFactor    
            
        if (uom1 is None):
            if (not abscissaUnit.isTerminal()):
                # keep exploding down the conversion path
                currentMapFactor = self.mapScalingFactor
                self.mapScalingFactor = 1.0
                self.explodeRecursively(abscissaUnit, self.STARTING_LEVEL)
                self.mapScalingFactor = self.mapScalingFactor * currentMapFactor
            else:
                # multiply out all of the exponents down the path
                pathExponent = 1
                
                for exp in self.pathExponents:
                    pathExponent = pathExponent * exp
                
                # variable = 1 if something == 1 else 0
                invert = True if pathExponent < 0 else False
                
                for _ in range(abs(pathExponent)):
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
                    denominator = denominator + Operands.MULT
                        
                if (uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                    denominator = denominator + uom.symbol
                    denominatorCount = denominatorCount + 1

                if (power < -1):
                    if (power == -2):
                        denominator = denominator + Operands.SQ
                    elif (power == -3):
                        denominator = denominator + Operands.CUBED
                    else:
                        denominator = denominator + Operands.POW + abs(power)
            elif (power >= 1 and uom != CacheManager.instance().getUOMByUnit(Unit.ONE)):
                # positive, put in numerator
                if (len(numerator) > 0):
                    numerator = numerator + Operands.MULT
                numerator = numerator + uom.symbol
                numeratorCount = numeratorCount + 1

                if (power > 1):
                    if (power == 2):
                        numerator = numerator + Operands.SQ
                    elif (power == 3):
                        numerator = numerator + Operands.CUBED
                    else:
                        numerator = numerator + Operands.POW + power
            else:
                # unary, don't add a '1'
                pass
            
        if (numeratorCount == 0):
            numerator = numerator + Operands.ONE

        result = None

        if (denominatorCount == 0):
            result = numerator
        else:
            if (denominatorCount == 1):
                result = numerator + Operands.DIV + denominator
            else:
                result = numerator + Operands.DIV + Operands.LP + denominator + Operands.RP

        return result       

    def __str__(self):
        return str(self.mapScalingFactor) + str(self.terms)