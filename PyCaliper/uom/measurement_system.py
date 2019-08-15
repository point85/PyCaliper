import gettext
import locale
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.unit_type import UnitType
from PyCaliper.uom.unit_of_measure import UnitOfMeasure

# get the default locale and the language code
thisLocale = locale.getdefaultlocale('LANG)')
langCC = thisLocale[0]

# translated text with error messages for this locale
messages = gettext.translation('messages', localedir='locales', languages=[langCC[0:2]])
messages.install()
_M = messages.gettext

"""
# translated user-visible text for this locale
units = gettext.translation('units', localedir='locales', languages=[langCC[0:2]])
units.install()
_U = units.gettext
"""

class MeasurementSystem:
    # name of resource bundle with translatable strings for exception messages
    __MESSAGE_BUNDLE_NAME = "Message"
    
    # single instance
    __unifiedSystem = None

    @staticmethod
    def instance():
        if MeasurementSystem.__unifiedSystem == None:
            MeasurementSystem()
        return MeasurementSystem.__unifiedSystem 

    def __init__(self):
            MeasurementSystem.__unifiedSystem = self
            self.__unitTypeRegistry = {}
            
    @staticmethod
    def getMessage(msgId: str) -> str :
        """ Get an error message by its id """
        return messages.gettext(msgId)
    
    @staticmethod
    def getUnitString(msgId: str) -> str :
        """ Get a unit name, symbol or description by its id """
        #return units.gettext(msgId)
        pass
    
    def area(self, cachedMap):
        cachedMap[UnitType.LENGTH] = 2
    
    def getTypeMap(self, unitType: UnitType):            
        if (self.__unitTypeRegistry.get(unitType) is not None):
            return self.__unitTypeRegistry[unitType]
        
        cachedMap = {}
        self.__unitTypeRegistry[unitType] = cachedMap
        
        if (unitType == UnitType.AREA):
            cachedMap[UnitType.LENGTH] = 2
        elif (unitType == UnitType.VOLUME):
            cachedMap[UnitType.LENGTH] = 3;
        elif (unitType ==  UnitType.DENSITY):
            cachedMap[UnitType.MASS] = 1;
            cachedMap[UnitType.LENGTH] = -3;
        elif (unitType ==  UnitType.VELOCITY):
            cachedMap[UnitType.LENGTH] = 1;
            cachedMap[UnitType.TIME] = -1;
        else:
            pass
        
        return cachedMap;
    
    def getUOM(self, unit: Unit) -> UnitOfMeasure:
        uom = self.cacheManager.getUOM(unit)

        if (uom is None):
            uom = createUOMForUnit(unit)
        return uom
        

class CacheManager:

    def __init__(self):
        self.symbolRegistry = {}
        self.baseRegistry = {}
        self.unitRegistry = {}
    
    def getUOMBySymbol(self, symbol: str) -> UnitOfMeasure:
        return self.symbolRegistry[symbol]
        
    def getUOMByUnit(self, unit: Unit) -> UnitOfMeasure:
        return self.unitRegistry[unit]
    
    def getBaseUOM(self, baseSymbol: str) -> UnitOfMeasure:
        return self.baseRegistry[baseSymbol]
        
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
    
    def unregisterUnit(self, uom: UnitOfMeasure):
        # remove by enumeration
        if (uom.unitType is not None):
            del self.unitRegistry[uom.unit] 
            
        # remove by symbol and base symbol
        del self.symbolRegistry[uom.symbol]
        del self.baseRegistry[uom.getBaseSymbol()]
        
    def getOne(self):
        return self.getUOMByUnit(Unit.ONE)
    
    def createScalarUOM(self, unitType: UnitType, unit: Unit, name: str, symbol: str, description:str) -> UnitOfMeasure:
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setEnumeration(unit)
        self.registerUnit(uom)

        return uom;
    
    def createSIUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.ONE):
            # unity
            uom = self.createScalarUOM(UnitType.UNITY, unit, \
                MeasurementSystem.getUnitString("one.name"), MeasurementSystem.getUnitString("one.symbol"), MeasurementSystem.getUnitString("one.desc"))
        """
                case ONE:
            // unity
            uom = createScalarUOM(UnitType.UNITY, Unit.ONE, units.getString("one.name"), units.getString("one.symbol"),
                    units.getString("one.desc"));
            break;
        """
        
        return uom
    
    def createCustomaryUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.RANKINE):
            # Rankine (base) 
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, \
                MeasurementSystem.getUnitString("rankine.name"), MeasurementSystem.getUnitString("rankine.symbol"), MeasurementSystem.getUnitString("rankine.desc"))
            
            # create bridge to SI
            uom.setBridgeConversion(5.0/9.0, self.getUOM(Unit.KELVIN), 0.0)
            """
                    case RANKINE:
            // Rankine (base)
            uom = createScalarUOM(UnitType.TEMPERATURE, Unit.RANKINE, units.getString("rankine.name"),
                    units.getString("rankine.symbol"), units.getString("rankine.desc"));

            // create bridge to SI
            uom.setBridgeConversion(5d / 9d, getUOM(Unit.KELVIN), 0.0d);
            break;
            """
        return uom
    
    def createUSUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.US_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.getUnitString("us_gallon.name"), MeasurementSystem.getUnitString("us_gallon.symbol"), MeasurementSystem.getUnitString("us_gallon.desc"))
            uom.setConversion(231.0, self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        return uom
        
    def createBRUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.BR_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.getUnitString("br_gallon.name"), MeasurementSystem.getUnitString("br_gallon.symbol"), MeasurementSystem.getUnitString("br_gallon.desc"))
            uom.setConversion(277.4194327916215, self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        return uom
    
    def createFinancialUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.US_DOLLAR):
            # dollar 
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, \
                MeasurementSystem.getUnitString("us_dollar.name"), MeasurementSystem.getUnitString("us_dollar.symbol"), MeasurementSystem.getUnitString("us_dollar.desc"))
            
        return uom
    
    def createUOMForUnit(self, unit: Unit) -> UnitOfMeasure:
        # SI
        uom = self.createSIUnit(unit)
        
        if (uom is not None):
            return uom
        
        # Customary
        uom = self.createCustomaryUnit(unit)
        
        if (uom is not None):
            return uom
        
        # US
        uom = self.createUSUnit(unit)
        
        if (uom is not None):
            return uom
        
        # British
        uom = self.createBRUnit(unit)
        
        if (uom is not None):
            return uom
        
        return self.createFinancialUnit(unit)
"""

"""