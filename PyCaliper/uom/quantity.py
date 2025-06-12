import math
from PyCaliper.uom.symbolic import Symbolic
from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.caliper_exception import PyCaliperException

##
# The Quantity class represents an amount and UnitOfMeasure. A constant
# quantity can be named and given a symbol, e.g. the speed of light.
# 
class Quantity(Symbolic):
    ##
    # Create a quantity with an amount and unit of measure
    # 
    # @param amount
    #            Amount
    # @param uom
    #            {@link UnitOfMeasure}
    #
    def __init__(self, amount, uom):
        super().__init__(None, None, None)
        
        self.amount = amount
        self.uom = uom
        
    def __hash__(self):
        return hash((round(self.amount, 10), self.uom.symbol))
        
    def __eq__(self, other):
        answer = False
    
        if (other is not None and isinstance(other, Quantity)):
            # same amount and same unit of measures
            if (math.isclose(self.amount, other.amount) and self.uom == other.uom):
                answer = True
        return answer
        
    def __str__(self):
        return str(self.amount) + ", [" + str(self.uom) + "] " + super().__str__()

    ##
    # Create an amount of a quantity that adheres to precision and rounding
    # settings from a Number
    # 
    # @param number
    #            Value
    # @return Amount
    #   
    @staticmethod
    def createAmountFromString(value):
        if (value is None):
            msg = Localizer.instance().messageStr("amount.cannot.be.null")
            raise PyCaliperException(msg) 

        return float(value)

    ##
    # Convert this quantity to the target UOM
    # 
    # @param toUOM
    #            {@link UnitOfMeasure}
    # @return Converted quantity
    #        
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

    ##
    # Convert this quantity with a product or quotient unit of measure to the
    # specified units of measure.
    # 
    # @param uom1
    #            Multiplier or dividend {@link UnitOfMeasure}
    # @param uom2
    #            Multiplicand or divisor {@link UnitOfMeasure}
    # @return Converted quantity
    #    
    def convertToPowerProduct(self, uom1, uom2):
        newUOM = self.uom.clonePowerProduct(uom1, uom2)
        return self.convert(newUOM)

    ##
    # Convert this quantity of a power unit using the specified base unit of
    # measure.
    # 
    # @param uom
    #            Base {@link UnitOfMeasure}
    # @return Converted quantity
    #    
    def convertToPower(self, uom):
        newUOM = self.uom.clonePower(uom)
        return self.convert(newUOM)

    ##
    # Subtract a quantity from this quantity
    # 
    # @param other
    #            quantity
    # @return New quantity
    #        
    def subtract(self, other):
        toSubtract = other.convert(self.uom)
        amount = self.amount - toSubtract.amount
        return Quantity(amount, self.uom)

    ##
    # Add two quantities
    # 
    # @param other
    #            {@link Quantity}
    # @return Sum {@link Quantity}
    #    
    def add(self, other):
        toAdd = other.convert(self.uom)
        amount = self.amount + toAdd.amount
        return Quantity(amount, self.uom)

    ##
    # Divide two quantities to create a third quantity
    # 
    # @param other
    #            {@link Quantity}
    # @return Quotient {@link Quantity}
    #    
    def divide(self, other):
        if (other.amount == 0.0):
            msg = Localizer.instance().messageStr("divisor.cannot.be.zero")
            raise PyCaliperException(msg)

        amount = self.amount / other.amount
        newUOM = self.uom.divide(other.uom)
        return Quantity(amount, newUOM)

    ##
    # Divide this quantity by the specified amount
    # 
    # @param divisor
    #            Amount
    # @return Quantity {@link Quantity}
    #    
    def divideByAmount(self, divisor):
        if (divisor == 0.0):
            msg = Localizer.instance().messageStr("divisor.cannot.be.zero")
            raise PyCaliperException(msg)
        return Quantity(self.amount / divisor, self.uom)

    ##
    # Multiply this quantity by another quantity to create a third quantity
    # 
    # @param other
    #            Quantity
    # @return Multiplied quantity
    #    
    def multiply(self, other):
        amount = self.amount * other.amount
        newUOM = self.uom.multiply(other.uom)
        return Quantity(amount, newUOM)

    ##
    # Multiply this quantity by the specified amount
    # 
    # @param multiplier
    #            Amount
    # @return Quantity {@link Quantity}
    #     
    def multiplyByAmount(self, multiplier):
        return Quantity(self.amount * multiplier, self.uom)
    
    ##
    # Invert this quantity, i.e. 1 divided by this quantity to create another
    # quantity
    # 
    # @return {@link Quantity}
    #    
    def invert(self):
        if self.amount == 0.0:
            msg = Localizer.instance().messageStr("divisor.cannot.be.zero")
            raise PyCaliperException(msg)
        amount = 1.0 / self.amount
        uom = self.uom.invert()
        return Quantity(amount, uom)

    ##
    # Compare this quantity to the other quantity
    # 
    # @param other
    #            Quantity
    # @return -1 if less than, 0 if equal and 1 if greater than
    #    
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

    ##
    # Find a matching unit type for the quantity's unit of measure.
    # 
    # @return {@link Quantity}
    #
    def classify(self):
        self.uom.classify()
        return self    
