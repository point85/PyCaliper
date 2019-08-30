from PyCaliper.uom.unit_type import UnitType

class CacheManager:
        # single instance
    manager = None
    
    def __init__(self):
        CacheManager.manager = self
        
        self.symbolRegistry = {}
        self.baseRegistry = {}
        self.unitRegistry = {}
        self.unitTypeRegistry = {}
        
    @staticmethod
    def instance():
        if (CacheManager.manager is None):
            CacheManager()
        return CacheManager.manager 
    
    def getUOMBySymbol(self, symbol):
        uom = None
        if (symbol in self.symbolRegistry):
            uom = self.symbolRegistry[symbol]
        return uom
        
    def getUOMByUnit(self, unit):
        uom = None
        if (unit in self.unitRegistry):
            uom = self.unitRegistry[unit]
        return uom
    
    def getBaseUOM(self, baseSymbol):
        uom = None
        if (baseSymbol in self.baseRegistry):
            uom = self.baseRegistry[baseSymbol]
        return uom
    
    def clearCache(self):
        self.symbolRegistry.clear()
        self.baseRegistry.clear()
        self.unitRegistry.clear()
          
    def getCachedUnits(self):
        return self.symbolRegistry.values()
    
    def getSymbolCache(self):
        return self.symbolRegistry
        
    def getBaseSymbolCache(self):
        return self.baseRegistry
    
    def getEnumerationCache(self):
        return self.unitRegistry  
    
    def unregisterUnit(self, uom):
        # remove by enumeration
        if (uom.unitType is not None):
            del self.unitRegistry[uom.unit] 
            
        # remove by symbol and base symbol
        del self.symbolRegistry[uom.symbol]
        del self.baseRegistry[uom.getBaseSymbol()]
        
    def registerUnit(self, uom):
        # get first by symbol
        current = self.getUOMBySymbol(uom.symbol)

        if (current is not None):
            # already cached
            return

        # cache it by symbol
        self.symbolRegistry[uom.symbol] = uom

        # next by unit enumeration
        if (uom.unit is not None):
            self.unitRegistry[uom.unit] = uom

        # finally cache by base symbol
        key = uom.getBaseSymbol()
        uom = self.getBaseUOM(key)
        
        if (uom is None):
            self.baseRegistry[key] = uom

    def getTypeMap(self, unitType):            
        if (self.unitTypeRegistry.get(unitType) is not None):
            return self.unitTypeRegistry[unitType]
        
        cachedMap = {}
        self.unitTypeRegistry[unitType] = cachedMap
        
        if (unitType == UnitType.AREA):
            cachedMap[UnitType.LENGTH] = 2
        elif (unitType == UnitType.VOLUME):
            cachedMap[UnitType.LENGTH] = 3
        elif (unitType ==  UnitType.DENSITY):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = -3
        elif (unitType ==  UnitType.VELOCITY):
            cachedMap[UnitType.LENGTH] = 1
            cachedMap[UnitType.TIME] = -1
        else:
            pass
        
        return cachedMap