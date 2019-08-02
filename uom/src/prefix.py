
class Prefix:
    """
    The Prefix class defines SI unit of measure prefixes as well as those found in computer science.
    """
    
    __prefixes = []
    
    @classmethod
    def yotta(cls):
        cls.YOTTA = cls("yotta", "Y", 1.0E+24)
        return cls.YOTTA
    
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
    
    def __str__(self):
        return self.__name + ", " + self.__symbol + ", " + str(self.__factor)