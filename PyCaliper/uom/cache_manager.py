from PyCaliper.uom.enums import UnitType


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
          
    def getCachedUOMs(self):
        return self.symbolRegistry.values()
    
    def getSymbolCache(self):
        return self.symbolRegistry
        
    def getBaseSymbolCache(self):
        return self.baseRegistry
    
    def getEnumerationCache(self):
        return self.unitRegistry  
    
    def unregisterUOM(self, uom):
        if (uom is None):
            return
        
        # remove by enumeration
        if (uom.unit is not None and uom.unit in self.unitRegistry):
            del self.unitRegistry[uom.unit] 
            
        # remove by symbol and base symbol
        if (uom.symbol in self.symbolRegistry):
            del self.symbolRegistry[uom.symbol]
            
        key = uom.getBaseSymbol()
        if (key in self.baseRegistry):
            del self.baseRegistry[key]
        
    def registerUOM(self, uom):
        if (uom is None):
            return
        
        # get first by symbol
        current = self.getUOMBySymbol(uom.symbol)

        if (current is not None):
            # already cached
            return

        #print("+++registering uom " + uom.symbol)
        # cache it by symbol
        self.symbolRegistry[uom.symbol] = uom

        # next by unit enumeration
        if (uom.unit is not None):
            self.unitRegistry[uom.unit] = uom

        # TODO finally cache by base symbol
        key = uom.getBaseSymbol()
        
        if (key not in self.baseRegistry):
            self.baseRegistry[key] = uom

    def getTypeMap(self, unitType):            
        if (unitType in self.unitTypeRegistry):
            return self.unitTypeRegistry[unitType]
        
        cachedMap = {}
        self.unitTypeRegistry[unitType] = cachedMap
        
        if (unitType == UnitType.AREA):
            cachedMap[UnitType.LENGTH] = 2
            
        elif (unitType == UnitType.VOLUME):
            cachedMap[UnitType.LENGTH] = 3
            
        elif (unitType == UnitType.DENSITY):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = -3
            
        elif (unitType == UnitType.VELOCITY):
            cachedMap[UnitType.LENGTH] = 1
            cachedMap[UnitType.TIME] = -1
            
        elif (unitType == UnitType.VOLUMETRIC_FLOW):
            cachedMap[UnitType.LENGTH] = 3
            cachedMap[UnitType.TIME] = -1
            
        elif (unitType == UnitType.MASS_FLOW):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.FREQUENCY):
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.ACCELERATION):
            cachedMap[UnitType.LENGTH] = 1
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.FORCE):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 1
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.PRESSURE):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = -1
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.ENERGY):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.POWER):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -3
                    
        elif (unitType == UnitType.ELECTRIC_CHARGE):
            cachedMap[UnitType.ELECTRIC_CURRENT] = 1
            cachedMap[UnitType.TIME] = 1
                    
        elif (unitType == UnitType.ELECTROMOTIVE_FORCE):
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.ELECTRIC_CURRENT] = -1
            cachedMap[UnitType.TIME] = -3
                    
        elif (unitType == UnitType.ELECTRIC_RESISTANCE):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = -3
            cachedMap[UnitType.ELECTRIC_CURRENT] = 2
            cachedMap[UnitType.TIME] = 4
                    
        elif (unitType == UnitType.ELECTRIC_CAPACITANCE):
            cachedMap[UnitType.MASS] = -1
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.ELECTRIC_CURRENT] = -2
            cachedMap[UnitType.TIME] = -3
                    
        elif (unitType == UnitType.ELECTRIC_PERMITTIVITY):
            cachedMap[UnitType.MASS] = -1
            cachedMap[UnitType.LENGTH] = -3
            cachedMap[UnitType.ELECTRIC_CURRENT] = 2
            cachedMap[UnitType.TIME] = 4
                    
        elif (unitType == UnitType.ELECTRIC_FIELD_STRENGTH):
            cachedMap[UnitType.ELECTRIC_CURRENT] = 1
            cachedMap[UnitType.LENGTH] = -1
                    
        elif (unitType == UnitType.MAGNETIC_FLUX):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.ELECTRIC_CURRENT] = -1
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.MAGNETIC_FLUX_DENSITY):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.ELECTRIC_CURRENT] = -1
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.ELECTRIC_INDUCTANCE):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.ELECTRIC_CURRENT] = -2
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.ELECTRIC_CONDUCTANCE):
            cachedMap[UnitType.MASS] = -1
            cachedMap[UnitType.LENGTH] = -2
            cachedMap[UnitType.ELECTRIC_CURRENT] = 2
            cachedMap[UnitType.TIME] = 3
                    
        elif (unitType == UnitType.LUMINOUS_FLUX):
            cachedMap[UnitType.LUMINOSITY] = 1
                    
        elif (unitType == UnitType.ILLUMINANCE):
            cachedMap[UnitType.LUMINOSITY] = 1
            cachedMap[UnitType.LENGTH] = -2
                    
        elif (unitType == UnitType.RADIATION_DOSE_ABSORBED):
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.RADIATION_DOSE_EFFECTIVE):
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -2
                    
        elif (unitType == UnitType.RADIATION_DOSE_RATE):
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -3
                    
        elif (unitType == UnitType.RADIOACTIVITY):
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.CATALYTIC_ACTIVITY):
            cachedMap[UnitType.SUBSTANCE_AMOUNT] = 1
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.DYNAMIC_VISCOSITY):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.LENGTH] = 1
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.KINEMATIC_VISCOSITY):
            cachedMap[UnitType.LENGTH] = 2
            cachedMap[UnitType.TIME] = -1
                    
        elif (unitType == UnitType.RECIPROCAL_LENGTH):
            cachedMap[UnitType.LENGTH] = -1
                    
        elif (unitType == UnitType.TIME_SQUARED):
            cachedMap[UnitType.TIME] = 2
                    
        elif (unitType == UnitType.MOLAR_CONCENTRATION):
            cachedMap[UnitType.SUBSTANCE_AMOUNT] = 1
            cachedMap[UnitType.LENGTH] = -3
                    
        elif (unitType == UnitType.IRRADIANCE):
            cachedMap[UnitType.MASS] = 1
            cachedMap[UnitType.TIME] = -3
                            
        else:
            pass
        
        return cachedMap
