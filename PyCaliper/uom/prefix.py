class Prefix:
    """
    The Prefix class defines SI unit of measure prefixes as well as those found in computer science.
    """
    @classmethod
    def yotta(cls):
        # SI prefix 10^24
        return cls("yotta", "Y", 1.0E+24)
    
    @classmethod
    def zetta(cls):
        # SI prefix 10^21
        return cls("zetta", "Z", 1.0E+21)
    
    @classmethod
    def exa(cls):
        # SI prefix 10^18
        return cls("exa", "E", 1.0E+18)
    
    @classmethod
    def peta(cls):
        # SI prefix 10^15
        return cls("peta", "P", 1.0E+15)
    
    @classmethod
    def tera(cls):
        # SI prefix 10^12
        return cls("tera", "T", 1.0E+12)
    
    @classmethod
    def giga(cls):
        # SI prefix 10^9
        return cls("giga", "G", 1.0E+09)  
    
    @classmethod
    def mega(cls):
        # SI prefix 10^6
        return cls("mega", "M", 1.0E+06)   
    
    @classmethod
    def kilo(cls):
        # SI prefix 10^3
        return cls("kilo", "k", 1.0E+03)   
    
    @classmethod
    def hecto(cls):
        # SI prefix 10^2
        return cls("hecto", "h", 1.0E+02)  
    
    @classmethod
    def deka(cls):
        # SI prefix 10^1
        return cls("deka", "da", 1.0E+01)    
    
    @classmethod
    def deci(cls):
        # SI prefix 10^-1
        return cls("deci", "d", 1.0E-01)  
    
    @classmethod
    def centi(cls):
        # SI prefix 10^-2
        return cls("centi", "c", 1.0E-02) 
    
    @classmethod
    def milli(cls):
        # SI prefix 10^-3
        return cls("milli", "m", 1.0E-03)  
    
    @classmethod
    def micro(cls):
        # SI prefix 10^-6
        return cls("micro", "\u03BC", 1.0E-06)   
    
    @classmethod
    def nano(cls):
        # SI prefix 10^-9
        return cls("nano", "n", 1.0E-09)     
    
    @classmethod
    def pico(cls):
        # SI prefix 10^-12
        return cls("pico", "p", 1.0E-12)                         

    @classmethod
    def femto(cls):
        # SI prefix 10^-15
        return cls("femto", "f", 1.0E-15)

    @classmethod
    def atto(cls):
        # SI prefix 10^-18
        return cls("atto", "a", 1.0E-18)
            
    @classmethod
    def zepto(cls):
        # SI prefix 10^-21
        return cls("zepto", "z", 1.0E-21)
    
    @classmethod
    def yocto(cls):
        # SI prefix 10^-24
        return cls("yocto", "y", 1.0E-24)
    
    """
    Digital information prefixes for bytes established by the International
    Electrotechnical Commission (IEC) in 1998
    """    
    @classmethod
    def kibi(cls):
        return cls("kibi", "Ki", 1024)
    
    @classmethod
    def mebi(cls):
        return cls("mebi", "Mi", 1.048576E+06) 
    
    @classmethod
    def gibi(cls):
        return cls("gibi", "Gi", 1.073741824E+09)       
    
    def __init__(self, name, symbol, factor): 
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
    def fromName(cls, name):
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
    
    @classmethod
    def fromFactor(cls, factor):
        
        for p in cls.__prefixes:
            if p.factor == factor:
                prefix = p
                break

        return prefix
    
    def __str__(self):
        return self.name + ", " + self.symbol + ", " + str(self.factor)
