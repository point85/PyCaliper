from enum import Enum, auto


class MeasurementType(Enum):
    """
    An enumeration of the basic types of units of measure
    """
    
    SCALAR = auto() 
    PRODUCT = auto() 
    QUOTIENT = auto() 
    POWER = auto()
