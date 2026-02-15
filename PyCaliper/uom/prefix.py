##
# The Prefix class defines SI unit of measure prefixes as well as those found in computer science.
#
class Prefix:  
    # floating point precision equality
    EPSILON = 1e-10
    
    # list of cached prefixes  
    prefixes = []
    
    # Cached prefix instances
    _cached_prefixes = {}
        
    @classmethod
    def yotta(cls):
        # SI prefix 10^24
        if 'yotta' not in cls._cached_prefixes:
            cls._cached_prefixes['yotta'] = cls("yotta", "Y", 1.0E+24)
        return cls._cached_prefixes['yotta']
    
    @classmethod
    def zetta(cls):
        # SI prefix 10^21
        if 'zetta' not in cls._cached_prefixes:
            cls._cached_prefixes['zetta'] = cls("zetta", "Z", 1.0E+21)
        return cls._cached_prefixes['zetta']
    
    @classmethod
    def exa(cls):
        # SI prefix 10^18
        if 'exa' not in cls._cached_prefixes:
            cls._cached_prefixes['exa'] = cls("exa", "E", 1.0E+18)
        return cls._cached_prefixes['exa']
    
    @classmethod
    def peta(cls):
        # SI prefix 10^15
        if 'peta' not in cls._cached_prefixes:
            cls._cached_prefixes['peta'] = cls("peta", "P", 1.0E+15)
        return cls._cached_prefixes['peta']
    
    @classmethod
    def tera(cls):
        # SI prefix 10^12
        if 'tera' not in cls._cached_prefixes:
            cls._cached_prefixes['tera'] = cls("tera", "T", 1.0E+12)
        return cls._cached_prefixes['tera']
    
    @classmethod
    def giga(cls):
        # SI prefix 10^9
        if 'giga' not in cls._cached_prefixes:
            cls._cached_prefixes['giga'] = cls("giga", "G", 1.0E+09)
        return cls._cached_prefixes['giga']
    
    @classmethod
    def mega(cls):
        # SI prefix 10^6
        if 'mega' not in cls._cached_prefixes:
            cls._cached_prefixes['mega'] = cls("mega", "M", 1.0E+06)
        return cls._cached_prefixes['mega']
    
    @classmethod
    def kilo(cls):
        # SI prefix 10^3
        if 'kilo' not in cls._cached_prefixes:
            cls._cached_prefixes['kilo'] = cls("kilo", "k", 1.0E+03)
        return cls._cached_prefixes['kilo']
    
    @classmethod
    def hecto(cls):
        # SI prefix 10^2
        if 'hecto' not in cls._cached_prefixes:
            cls._cached_prefixes['hecto'] = cls("hecto", "h", 1.0E+02)
        return cls._cached_prefixes['hecto']
    
    @classmethod
    def deka(cls):
        # SI prefix 10^1
        if 'deka' not in cls._cached_prefixes:
            cls._cached_prefixes['deka'] = cls("deka", "da", 1.0E+01)
        return cls._cached_prefixes['deka']
    
    @classmethod
    def deci(cls):
        # SI prefix 10^-1
        if 'deci' not in cls._cached_prefixes:
            cls._cached_prefixes['deci'] = cls("deci", "d", 1.0E-01)
        return cls._cached_prefixes['deci']
    
    @classmethod
    def centi(cls):
        # SI prefix 10^-2
        if 'centi' not in cls._cached_prefixes:
            cls._cached_prefixes['centi'] = cls("centi", "c", 1.0E-02)
        return cls._cached_prefixes['centi']
    
    @classmethod
    def milli(cls):
        # SI prefix 10^-3
        if 'milli' not in cls._cached_prefixes:
            cls._cached_prefixes['milli'] = cls("milli", "m", 1.0E-03)
        return cls._cached_prefixes['milli']
    
    @classmethod
    def micro(cls):
        # SI prefix 10^-6
        if 'micro' not in cls._cached_prefixes:
            cls._cached_prefixes['micro'] = cls("micro", "\u03BC", 1.0E-06)
        return cls._cached_prefixes['micro']
    
    @classmethod
    def nano(cls):
        # SI prefix 10^-9
        if 'nano' not in cls._cached_prefixes:
            cls._cached_prefixes['nano'] = cls("nano", "n", 1.0E-09)
        return cls._cached_prefixes['nano']
    
    @classmethod
    def pico(cls):
        # SI prefix 10^-12
        if 'pico' not in cls._cached_prefixes:
            cls._cached_prefixes['pico'] = cls("pico", "p", 1.0E-12)
        return cls._cached_prefixes['pico']

    @classmethod
    def femto(cls):
        # SI prefix 10^-15
        if 'femto' not in cls._cached_prefixes:
            cls._cached_prefixes['femto'] = cls("femto", "f", 1.0E-15)
        return cls._cached_prefixes['femto']

    @classmethod
    def atto(cls):
        # SI prefix 10^-18
        if 'atto' not in cls._cached_prefixes:
            cls._cached_prefixes['atto'] = cls("atto", "a", 1.0E-18)
        return cls._cached_prefixes['atto']
            
    @classmethod
    def zepto(cls):
        # SI prefix 10^-21
        if 'zepto' not in cls._cached_prefixes:
            cls._cached_prefixes['zepto'] = cls("zepto", "z", 1.0E-21)
        return cls._cached_prefixes['zepto']
    
    @classmethod
    def yocto(cls):
        # SI prefix 10^-24
        if 'yocto' not in cls._cached_prefixes:
            cls._cached_prefixes['yocto'] = cls("yocto", "y", 1.0E-24)
        return cls._cached_prefixes['yocto']
    
    """
    Digital information prefixes for bytes established by the International
    Electrotechnical Commission (IEC) in 1998
    """    
    @classmethod
    def kibi(cls):
        if 'kibi' not in cls._cached_prefixes:
            cls._cached_prefixes['kibi'] = cls("kibi", "Ki", 1024)
        return cls._cached_prefixes['kibi']
    
    @classmethod
    def mebi(cls):
        if 'mebi' not in cls._cached_prefixes:
            cls._cached_prefixes['mebi'] = cls("mebi", "Mi", 1024**2)
        return cls._cached_prefixes['mebi']
    
    @classmethod
    def gibi(cls):
        if 'gibi' not in cls._cached_prefixes:
            cls._cached_prefixes['gibi'] = cls("gibi", "Gi", 1024**3)
        return cls._cached_prefixes['gibi']       

    ##
    # Construct a prefix
    # 
    # @param name
    #            Name
    # @param symbol
    #            Symbol
    # @param factor
    #            Numerical factor
    #
    def __init__(self, name, symbol, factor): 
        self.name = name
        self.symbol = symbol
        self.factor = factor

        if self not in Prefix.prefixes:
            Prefix.prefixes.append(self)
    
    ##
    # Find the prefix with the specified name
    # 
    # @param name
    #            Name of prefix
    # @return {@link Prefix}  
    # 
    @classmethod    
    def fromName(cls, name):
        for p in cls.prefixes:
            if p.name == name:
                return p

        return None
    
    ##
    # Find the prefix with the specified scaling factor
    # 
    # @param factor
    #            Scaling factor
    # @return {@link Prefix}
    #    
    @classmethod
    def fromFactor(cls, factor):
        for p in cls.prefixes:
            if abs(p.factor - factor) < cls.EPSILON:
                return p

        return None
    
    def __str__(self):
        return self.name + ", " + self.symbol + ", " + str(self.factor)
    
    def __eq__(self, other):
        # same name
        if (other is None or self.name != other.name):
            return False
        
        # same symbol
        if (self.symbol != other.symbol):
            return False

        # same factor
        if (abs(self.factor - other.factor) > Prefix.EPSILON):
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.name, self.symbol, self.factor))    
