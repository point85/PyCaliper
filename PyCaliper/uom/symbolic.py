##
# This class represents an object that is identified by a name and symbol with
# a description. Units of measure are such objects.
#
class Symbolic():
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
    
    def __eq__(self, other):
        if not isinstance(other, Symbolic):
            return False
        return (self.name == other.name and 
                self.symbol == other.symbol and 
                self.description == other.description)

    def __hash__(self):
        return hash((self.name, self.symbol, self.description))
