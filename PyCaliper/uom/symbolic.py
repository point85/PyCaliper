from abc import ABC

##
# This class represents an object that is identified by a name and symbol with
# an optional description. Units of measure are such objects.
#
class Symbolic(ABC):
    def __init__(self, name, symbol, description):
        self.name = name
        self.symbol = symbol
        self.description = description
        
        super().__init__()
    
    def __str__(self):
        value = ""
        
        if (self.symbol is not None):
            value = value + " (" + self.symbol
            
        if (self.name is not None):
            value = value + ", " + self.name
            
        if (self.description is not None):
            value = value + ", " + self.description + ')'
                   
        return value
