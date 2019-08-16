from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.measurement_system import MeasurementSystem
from builtins import staticmethod

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
        
    def subtract(self, other: Quantity) -> Quantity:
        toSubtract = other.convert(self.uom)
        amount = self.amount - toSubtract.amount
        return Quantity(amount, self.uom)
    
    def add(self, other: Quantity) -> Quantity:
        toAdd = other.convert(self.uom)
        amount = self.amount + toAdd.amount
        return Quantity(amount, self.uom)
    
"""

"""    