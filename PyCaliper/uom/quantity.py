from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.measurement_system import MeasurementSystem
from builtins import staticmethod
import math

class Quantity(Symbolic):
    def __init__(self, amount: float, uom: UnitOfMeasure):
        super(None, None, None)
        
        self.amount = amount
        self.uom = uom
        
    def __hash__(self):
        return hash(self.args)
        
    def __eq__(self, other):
        answer = False
        
        return answer
    
        if (other is not None and isinstance(other, Quantity)):
            # same amount and same unit of measure
            if (self.amount == other.amount and self.uom == other.uom):
                answer = True
            return answer
        
    def __str__(self):
        return self.amount + ", [" + str(self.uom) + "] " + str(super)
   
    @staticmethod
    def createAmount(self, value) -> float:
        if (value is None):
            msg = MeasurementSystem.getMessage("amount.cannot.be.null")
            raise Exception(msg) 

        return float(value)
        
    def fromPrefixedUnit(self, amount: float, prefix: Prefix, unit: Unit):
        uom = MeasurementSystem.instance().getUOM(prefix, unit)
        self(amount, uom)
        
    def fromStringUOM(self, amount: str, uom: UnitOfMeasure):
        value = self.createAmountFromString(amount)
        self(value, uom)
        
    def fromUnit(self, amount: float, unit: Unit): 
        uom = MeasurementSystem.instance().getUOM(unit)
        self(amount, uom)
        
    def fromStringUnit(self, amount: str, unit: Unit):
        value = self.createAmountFromString(amount)
        uom = MeasurementSystem.instance().getUOM(unit)
        self(value, uom)
        
    def convert(self, toUOM: UnitOfMeasure) -> Quantity:
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
    
    def convertToUnit(self, unit: Unit) -> Quantity:
        return self.convert(MeasurementSystem.instance().getUOM(unit))
    
    def convertToPrefixUnit(self, prefix: Prefix, unit: Unit) -> Quantity:
        return self.convert(MeasurementSystem.instance().getUOM(prefix, unit))
    
    def convertToPowerProduct(self, uom1: UnitOfMeasure, uom2: UnitOfMeasure) -> Quantity:
        newUOM = self.uom.clonePowerProduct(uom1, uom2)
        return self.convert(newUOM)
    
    def convertToPower(self, uom: UnitOfMeasure) -> Quantity:
        newUOM = self.uom.clonePower(uom)
        return self.convert(newUOM)
        
    def subtract(self, other: Quantity) -> Quantity:
        toSubtract = other.convert(self.uom)
        amount = self.amount - toSubtract.amount
        return Quantity(amount, self.uom)
    
    def add(self, other: Quantity) -> Quantity:
        toAdd = other.convert(self.uom)
        amount = self.amount + toAdd.amount
        return Quantity(amount, self.uom)
    
    def divide(self, other: Quantity) -> Quantity:
        if (other.amount == 0.0):
            msg = MeasurementSystem.getMessage("divisor.cannot.be.zero")
            raise Exception(msg)

        amount = self.amount / other.amount
        newUOM = self.uom.divide(other.uom)
        return Quantity(amount, newUOM)
    
    def divideByAmount(self, divisor: float) -> Quantity:
        return  Quantity(self.amount / divisor, self.uom)
    
    def multiply(self, other: Quantity) -> Quantity:
        amount = self.amount * other.amount
        newUOM = self.uom.multiply(other.uom)
        return Quantity(amount, newUOM)
    
    def multiplyByAmount(self, multiplier: float) -> Quantity:
        return Quantity(self.amount * multiplier, self.uom)
    
    def power(self, exponent: int) -> Quantity:
        amount = math.pow(self.amount, exponent)
        newUOM = MeasurementSystem.instance().createPowerUOM(self.uom, exponent)
        return Quantity(amount, newUOM) 
    
    def invert(self) -> Quantity:
        amount = 1.0 / self.amount
        uom = self.uom.invert()
        return Quantity(amount, uom)  
    
    def compare(self, other: Quantity) -> int:
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

    def classify(self) -> Quantity:
        self.uom.classify()
        return self
"""

"""    