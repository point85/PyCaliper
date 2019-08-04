
class Prefix:
    """
    The Prefix class defines SI unit of measure prefixes as well as those found in computer science.
    """
    
    __prefixes = []
    
    @classmethod
    def yotta(cls):
        cls.YOTTA = cls("yotta", "Y", 1.0E+24)
        return cls.YOTTA
    
    @classmethod
    def zetta(cls):
        cls.ZETTA = cls("zetta", "Z", 1.0E+21)
        return cls.ZETTA
    
    def __init__(self, name : str, symbol : str, factor : float): 
        """
        Construct a prefix
         
        parameter name
                    Name
        parameter symbol
                    Symbol
        parameter factor
                    Numerical factor
        """
        self.name = name
        self.symbol = symbol
        self.factor = factor

        Prefix.__prefixes.append(self)
    
    @classmethod    
    def fromName(cls, name: str):
        """
        Find the prefix with the specified name
        
        parameter name
                   Name of prefix
        return Prefix
        """
     
        for p in cls.__prefixes:
            if p.name == name:
                prefix = p
                break

        return prefix
    
    def __str__(self):
        return self.name + ", " + self.symbol + ", " + str(self.factor)