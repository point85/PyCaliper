from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.localizer import Localizer
import math
from builtins import staticmethod


class Quantity(Symbolic):
    def __init__(self, amount, uom):
        super().__init__(None, None, None)
        
        self.amount = amount
        self.uom = uom
        
    def __hash__(self):
        return hash(str(self.amount) + self.uom.symbol)
        
    def __eq__(self, other):
        answer = False
    
        if (other is not None and isinstance(other, Quantity)):
            # same amount and same unit of measures
            if (math.isclose(self.amount, other.amount) and self.uom == other.uom):
                answer = True
        return answer
        
    def __str__(self):
        return str(self.amount) + ", [" + str(self.uom) + "] " + super().__str__()
   
    @staticmethod
    def createAmountFromString(value):
        if (value is None):
            msg = Localizer.instance().messageStr("amount.cannot.be.null")
            raise Exception(msg) 

        return float(value)
    """    
    def fromPrefixedUnit(self, amount, prefix, unit):
        uom = MeasurementSystem.instance().getUOM(prefix, unit)
        self(amount, uom)
    """
        
    def fromStringUOM(self, amount, uom):
        value = Quantity.createAmountFromString(amount)
        self(value, uom)
    
    """    
    def fromUnit(self, amount, unit): 
        uom = MeasurementSystem.instance().getUOM(unit)
        self(amount, uom)
        
    def fromStringUnit(self, strAmount, unit):
        value = Quantity.createAmountFromString(strAmount)
        uom = MeasurementSystem.instance().getUOM(unit)
        self(value, uom)
    """
        
    def convert(self, toUOM):
        multiplier = self.uom.getConversionFactor(toUOM)
        thisOffset = self.uom.offset
        targetOffset = toUOM.offset

        # adjust for a non-zero "this" offset
        offsetAmount = self.amount + thisOffset

        # new path amount
        newAmount = offsetAmount * multiplier

        # adjust for non-zero target offset
        newAmount = newAmount - targetOffset

        # create the quantity now
        return Quantity(newAmount, toUOM)
    
    """
    def convertToUnit(self, unit):
        return self.convert(MeasurementSystem.instance().getUOM(unit))
    
    def convertToPrefixUnit(self, prefix, unit):
        return self.convert(MeasurementSystem.instance().getUOM(prefix, unit))
    """
    
    def convertToPowerProduct(self, uom1, uom2):
        newUOM = self.uom.clonePowerProduct(uom1, uom2)
        return self.convert(newUOM)
    
    def convertToPower(self, uom):
        newUOM = self.uom.clonePower(uom)
        return self.convert(newUOM)
        
    def subtract(self, other):
        toSubtract = other.convert(self.uom)
        amount = self.amount - toSubtract.amount
        return Quantity(amount, self.uom)
    
    def add(self, other):
        toAdd = other.convert(self.uom)
        amount = self.amount + toAdd.amount
        return Quantity(amount, self.uom)
    
    def divide(self, other):
        if (other.amount == 0.0):
            msg = Localizer.instance().messageStr("divisor.cannot.be.zero")
            raise Exception(msg)

        amount = self.amount / other.amount
        newUOM = self.uom.divide(other.uom)
        return Quantity(amount, newUOM)
    
    def divideByAmount(self, divisor):
        return  Quantity(self.amount / divisor, self.uom)
    
    def multiply(self, other):
        amount = self.amount * other.amount
        newUOM = self.uom.multiply(other.uom)
        return Quantity(amount, newUOM)
    
    def multiplyByAmount(self, multiplier):
        return Quantity(self.amount * multiplier, self.uom)
    
    """
    def power(self, exponent: int):
        amount = math.pow(self.amount, exponent)
        newUOM = MeasurementSystem.instance().createPowerUOM(self.uom, exponent)
        return Quantity(amount, newUOM) 
    """
    
    def invert(self):
        amount = 1.0 / self.amount
        uom = self.uom.invert()
        return Quantity(amount, uom)  
    
    def compare(self, other):
        toCompare = other
        
        if (self.uom != other.uom):
            # first try converting the units
            toCompare = other.convert(self.uom)
        
        if (math.isclose(self.amount, toCompare.amount)):
            return 0
        elif (self.amount < toCompare.amount):
            return -1
        else:
            return 1

    def classify(self):
        self.uom.classify()
        return self    
