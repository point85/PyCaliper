import gettext
import locale
import math
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.unit_type import UnitType
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.constant import Constant

# get the default locale and the language code
thisLocale = locale.getdefaultlocale('LANG)')
langCC = thisLocale[0]

# translated text with error messages for this locale
messages = gettext.translation('messages', localedir='locales', languages=[langCC[0:2]])
messages.install()
_M = messages.gettext

# translated user-visible text for this locale
units = gettext.translation('units', localedir='locales', languages=[langCC[0:2]])
units.install()
_U = units.gettext

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
        
    def registerUnit(self, uom: UnitOfMeasure):
        # get first by symbol
        current = self.symbolRegistry[uom.symbol]

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

        if (self.baseRegistry[key] is None):
            self.baseRegistry[key] = uom

class MeasurementSystem:
    # name of resource bundle with translatable strings for exception messages
    __MESSAGE_BUNDLE_NAME = "Message"
    
    # single instance
    unifiedSystem = None
    
    def __init__(self):
        MeasurementSystem.unifiedSystem = self
        self.unitTypeRegistry = {}
        self.cacheManager = CacheManager()

    @staticmethod
    def instance():
        if MeasurementSystem.unifiedSystem == None:
            MeasurementSystem()
        return MeasurementSystem.unifiedSystem 
            
    @staticmethod
    def messageStr(msgId: str) -> str :
        """ Get an error message by its id """
        return messages.gettext(msgId)
    
    @staticmethod
    def unitStr(msgId: str) -> str :
        """ Get a unit name, symbol or description by its id """
        return units.gettext(msgId)
    
    def area(self, cachedMap):
        cachedMap[UnitType.LENGTH] = 2
    
    def getTypeMap(self, unitType: UnitType):            
        if (self.unitTypeRegistry.get(unitType) is not None):
            return self.unitTypeRegistry[unitType]
        
        cachedMap = {}
        self.unitTypeRegistry[unitType] = cachedMap
        
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
        uom = self.cacheManager.self.getUOM(unit)

        if (uom is None):
            uom = self.createUOMForUnit(unit)
        return uom
        
    def getOne(self):
        return self.self.getUOMByUnit(Unit.ONE)
    
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
                MeasurementSystem.unitStr("one.name"), MeasurementSystem.unitStr("one.symbol"), MeasurementSystem.unitStr("one.desc"))
        
        elif (unit == Unit.PERCENT):
            uom = self.createScalarUOM(UnitType.UNITY, Unit.PERCENT, MeasurementSystem.unitStr("percent.name"), \
                    MeasurementSystem.unitStr("percent.symbol"), MeasurementSystem.unitStr("percent.desc"))
            uom.setConversion(0.01, self.self.getOne())

        elif (unit == Unit.SECOND):
            # second
            uom = self.createScalarUOM(UnitType.TIME, Unit.SECOND, MeasurementSystem.unitStr("sec.name"), \
                    MeasurementSystem.unitStr("sec.symbol"), MeasurementSystem.unitStr("sec.desc"))

        elif (unit == Unit.MINUTE):
            # minute
            uom = self.createScalarUOM(UnitType.TIME, Unit.MINUTE, MeasurementSystem.unitStr("min.name"), \
                    MeasurementSystem.unitStr("min.symbol"), MeasurementSystem.unitStr("min.desc"))
            uom.setConversion(60, self.self.getUOM(Unit.SECOND))

        elif (unit == Unit.HOUR):
            # hour
            uom = self.createScalarUOM(UnitType.TIME, Unit.HOUR, MeasurementSystem.unitStr("hr.name"), MeasurementSystem.unitStr("hr.symbol"), \
                    MeasurementSystem.unitStr("hr.desc"))
            uom.setConversion(3600, self.getUOM(Unit.SECOND))
        
        elif (unit == Unit.DAY):
            # day
            uom = self.createScalarUOM(UnitType.TIME, Unit.DAY, MeasurementSystem.unitStr("day.name"), MeasurementSystem.unitStr("day.symbol"), \
                    MeasurementSystem.unitStr("day.desc"))
            uom.setConversion(86400, self.getUOM(Unit.SECOND))

        elif (unit == Unit.WEEK):
            # week
            uom = self.createScalarUOM(UnitType.TIME, Unit.WEEK, MeasurementSystem.unitStr("week.name"), \
                    MeasurementSystem.unitStr("week.symbol"), MeasurementSystem.unitStr("week.desc"))
            uom.setConversion(604800, self.getUOM(Unit.SECOND))

        elif (unit == Unit.JULIAN_YEAR):
            # Julian year
            uom = self.createScalarUOM(UnitType.TIME, Unit.JULIAN_YEAR, MeasurementSystem.unitStr("jyear.name"), \
                    MeasurementSystem.unitStr("jyear.symbol"), MeasurementSystem.unitStr("jyear.desc"))
            uom.setConversion(3.1557600E+07, self.self.getUOM(Unit.SECOND))

        elif (unit == Unit.SQUARE_SECOND):
            # square second
            uom = self.self.createPowerUOM(UnitType.TIME_SQUARED, Unit.SQUARE_SECOND, MeasurementSystem.unitStr("s2.name"), \
                    MeasurementSystem.unitStr("s2.symbol"), MeasurementSystem.unitStr("s2.desc"), self.getUOM(Unit.SECOND), 2)

        elif (unit == Unit.MOLE):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, Unit.MOLE, MeasurementSystem.unitStr("mole.name"), \
                    MeasurementSystem.unitStr("mole.symbol"), MeasurementSystem.unitStr("mole.desc"))

        elif (unit == Unit.EQUIVALENT):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, Unit.EQUIVALENT, MeasurementSystem.unitStr("equivalent.name"), \
                    MeasurementSystem.unitStr("equivalent.symbol"), MeasurementSystem.unitStr("equivalent.desc"))

        elif (unit == Unit.DECIBEL):
            # decibel
            uom = self.createScalarUOM(UnitType.INTENSITY, Unit.DECIBEL, MeasurementSystem.unitStr("db.name"), \
                    MeasurementSystem.unitStr("db.symbol"), MeasurementSystem.unitStr("db.desc"))

        elif (unit == Unit.RADIAN):
            # plane angle radian (rad)
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, Unit.RADIAN, MeasurementSystem.unitStr("radian.name"), \
                    MeasurementSystem.unitStr("radian.symbol"), MeasurementSystem.unitStr("radian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.STERADIAN):
            # solid angle steradian (sr)
            uom = self.createScalarUOM(UnitType.SOLID_ANGLE, Unit.STERADIAN, MeasurementSystem.unitStr("steradian.name"), \
                    MeasurementSystem.unitStr("steradian.symbol"), MeasurementSystem.unitStr("steradian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.DEGREE):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, Unit.DEGREE, MeasurementSystem.unitStr("degree.name"), \
                    MeasurementSystem.unitStr("degree.symbol"), MeasurementSystem.unitStr("degree.desc"))
            uom.setConversion(math.pi / 180, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.ARC_SECOND):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, Unit.ARC_SECOND, MeasurementSystem.unitStr("arcsec.name"), \
                    MeasurementSystem.unitStr("arcsec.symbol"), MeasurementSystem.unitStr("arcsec.desc"))
            uom.setConversion(math.pi / 648000, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.METRE):
            # fundamental length
            uom = self.createScalarUOM(UnitType.LENGTH, Unit.METRE, MeasurementSystem.unitStr("m.name"), MeasurementSystem.unitStr("m.symbol"), \
                    MeasurementSystem.unitStr("m.desc"))

        elif (unit == Unit.DIOPTER):
            # per metre
            uom = self.self.createQuotientUOM(UnitType.RECIPROCAL_LENGTH, Unit.DIOPTER, MeasurementSystem.unitStr("diopter.name"), \
                    MeasurementSystem.unitStr("diopter.symbol"), MeasurementSystem.unitStr("diopter.desc"), self.getOne(), self.getUOM(Unit.METRE))

        elif (unit == Unit.KILOGRAM):
            # fundamental mass
            uom = self.createScalarUOM(UnitType.MASS, Unit.KILOGRAM, MeasurementSystem.unitStr("kg.name"), \
                    MeasurementSystem.unitStr("kg.symbol"), MeasurementSystem.unitStr("kg.desc"))

        elif (unit == Unit.TONNE):
            # mass
            uom = self.createScalarUOM(UnitType.MASS, Unit.TONNE, MeasurementSystem.unitStr("tonne.name"), \
                    MeasurementSystem.unitStr("tonne.symbol"), MeasurementSystem.unitStr("tonne.desc"))
            uom.setConversion(Prefix.kilo().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.KELVIN):
            # fundamental temperature
            uom = self.createScalarUOM(UnitType.TEMPERATURE, Unit.KELVIN, MeasurementSystem.unitStr("kelvin.name"), \
                    MeasurementSystem.unitStr("kelvin.symbol"), MeasurementSystem.unitStr("kelvin.desc"))

        elif (unit == Unit.AMPERE):
            # electric current
            uom = self.createScalarUOM(UnitType.ELECTRIC_CURRENT, Unit.AMPERE, MeasurementSystem.unitStr("amp.name"), \
                    MeasurementSystem.unitStr("amp.symbol"), MeasurementSystem.unitStr("amp.desc"))

        elif (unit == Unit.CANDELA):
            # luminosity
            uom = self.createScalarUOM(UnitType.LUMINOSITY, Unit.CANDELA, MeasurementSystem.unitStr("cd.name"), \
                    MeasurementSystem.unitStr("cd.symbol"), MeasurementSystem.unitStr("cd.desc"))

        elif (unit == Unit.MOLARITY):
            # molar concentration
            uom = self.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, Unit.MOLARITY, MeasurementSystem.unitStr("molarity.name"), \
                    MeasurementSystem.unitStr("molarity.symbol"), MeasurementSystem.unitStr("molarity.desc"), self.getUOM(Unit.MOLE), \
                    self.getUOM(Unit.LITRE))

        elif (unit == Unit.GRAM): # gram
            uom = self.createScalarUOM(UnitType.MASS, Unit.GRAM, MeasurementSystem.unitStr("gram.name"), \
                    MeasurementSystem.unitStr("gram.symbol"), MeasurementSystem.unitStr("gram.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.CARAT):
            # carat
            uom = self.createScalarUOM(UnitType.MASS, Unit.CARAT, MeasurementSystem.unitStr("carat.name"), \
                    MeasurementSystem.unitStr("carat.symbol"), MeasurementSystem.unitStr("carat.desc"))
            uom.setConversion(0.2, self.getUOM(Unit.GRAM))

        elif (unit == Unit.SQUARE_METRE):
            # square metre
            uom = self.createPowerUOM(UnitType.AREA, Unit.SQUARE_METRE, MeasurementSystem.unitStr("m2.name"), \
                    MeasurementSystem.unitStr("m2.symbol"), MeasurementSystem.unitStr("m2.desc"), self.getUOM(Unit.METRE), 2)

        elif (unit == Unit.HECTARE):
            # hectare
            uom = self.createScalarUOM(UnitType.AREA, Unit.HECTARE, MeasurementSystem.unitStr("hectare.name"), \
                    MeasurementSystem.unitStr("hectare.symbol"), MeasurementSystem.unitStr("hectare.desc"))
            uom.setConversion(10000, self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.METRE_PER_SEC):
            # velocity
            uom = self.createQuotientUOM(UnitType.VELOCITY, Unit.METRE_PER_SEC, MeasurementSystem.unitStr("mps.name"), \
                    MeasurementSystem.unitStr("mps.symbol"), MeasurementSystem.unitStr("mps.desc"), self.getUOM(Unit.METRE), self.getSecond())

        elif (unit == Unit.METRE_PER_SEC_SQUARED):
            # acceleration
            uom = self.createQuotientUOM(UnitType.ACCELERATION, Unit.METRE_PER_SEC_SQUARED, MeasurementSystem.unitStr("mps2.name"), \
                    MeasurementSystem.unitStr("mps2.symbol"), MeasurementSystem.unitStr("mps2.desc"), self.getUOM(Unit.METRE), \
                    self.getUOM(Unit.SQUARE_SECOND))

        elif (unit == Unit.CUBIC_METRE):
            # cubic metre
            uom = self.createPowerUOM(UnitType.VOLUME, Unit.CUBIC_METRE, MeasurementSystem.unitStr("m3.name"), \
                    MeasurementSystem.unitStr("m3.symbol"), MeasurementSystem.unitStr("m3.desc"), self.getUOM(Unit.METRE), 3)

        elif (unit == Unit.LITRE):
            # litre
            uom = self.createScalarUOM(UnitType.VOLUME, Unit.LITRE, MeasurementSystem.unitStr("litre.name"), \
                    MeasurementSystem.unitStr("litre.symbol"), MeasurementSystem.unitStr("litre.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.CUBIC_METRE))

        elif (unit == Unit.CUBIC_METRE_PER_SEC):
            # flow (volume)
            uom = self.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, Unit.CUBIC_METRE_PER_SEC,
                    MeasurementSystem.unitStr("m3PerSec.name"), MeasurementSystem.unitStr("m3PerSec.symbol"), \
                    MeasurementSystem.unitStr("m3PerSec.desc"), self.getUOM(Unit.CUBIC_METRE), self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_SEC):
            # flow (mass)
            uom = self.createQuotientUOM(UnitType.MASS_FLOW, Unit.KILOGRAM_PER_SEC, MeasurementSystem.unitStr("kgPerSec.name"), \
                    MeasurementSystem.unitStr("kgPerSec.symbol"), MeasurementSystem.unitStr("kgPerSec.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_CU_METRE):
            # kg/m^3
            uom = self.createQuotientUOM(UnitType.DENSITY, Unit.KILOGRAM_PER_CU_METRE, MeasurementSystem.unitStr("kg_m3.name"), \
                    MeasurementSystem.unitStr("kg_m3.symbol"), MeasurementSystem.unitStr("kg_m3.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getUOM(Unit.CUBIC_METRE))

        elif (unit == Unit.PASCAL_SECOND):
            # dynamic viscosity
            uom = self.createProductUOM(UnitType.DYNAMIC_VISCOSITY, Unit.PASCAL_SECOND, MeasurementSystem.unitStr("pascal_sec.name"), \
                    MeasurementSystem.unitStr("pascal_sec.symbol"), MeasurementSystem.unitStr("pascal_sec.desc"), self.getUOM(Unit.PASCAL), \
                    self.getSecond())

        elif (unit == Unit.SQUARE_METRE_PER_SEC):
            # kinematic viscosity
            uom = self.createQuotientUOM(UnitType.KINEMATIC_VISCOSITY, Unit.SQUARE_METRE_PER_SEC, \
                    MeasurementSystem.unitStr("m2PerSec.name"), MeasurementSystem.unitStr("m2PerSec.symbol"), \
                    MeasurementSystem.unitStr("m2PerSec.desc"), self.getUOM(Unit.SQUARE_METRE), self.getSecond())

        elif (unit == Unit.CALORIE):
            # thermodynamic calorie
            uom = self.createScalarUOM(UnitType.ENERGY, Unit.CALORIE, MeasurementSystem.unitStr("calorie.name"), \
                    MeasurementSystem.unitStr("calorie.symbol"), MeasurementSystem.unitStr("calorie.desc"))
            uom.setConversion(4.184, self.getUOM(Unit.JOULE))

        elif (unit == Unit.NEWTON):
            # force F = m·A (newton)
            uom = self.createProductUOM(UnitType.FORCE, Unit.NEWTON, MeasurementSystem.unitStr("newton.name"), \
                    MeasurementSystem.unitStr("newton.symbol"), MeasurementSystem.unitStr("newton.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getUOM(Unit.METRE_PER_SEC_SQUARED))

        elif (unit == Unit.NEWTON_METRE):
            # newton-metre
            uom = self.createProductUOM(UnitType.ENERGY, Unit.NEWTON_METRE, MeasurementSystem.unitStr("n_m.name"), \
                    MeasurementSystem.unitStr("n_m.symbol"), MeasurementSystem.unitStr("n_m.desc"), self.getUOM(Unit.NEWTON), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.JOULE):
            # energy (joule)
            uom = self.createProductUOM(UnitType.ENERGY, Unit.JOULE, MeasurementSystem.unitStr("joule.name"), \
                    MeasurementSystem.unitStr("joule.symbol"), MeasurementSystem.unitStr("joule.desc"), self.getUOM(Unit.NEWTON), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.ELECTRON_VOLT):
            # ev
            e = self.getQuantity(Constant.ELEMENTARY_CHARGE)
            uom = self.createProductUOM(UnitType.ENERGY, Unit.ELECTRON_VOLT, MeasurementSystem.unitStr("ev.name"), \
                    MeasurementSystem.unitStr("ev.symbol"), MeasurementSystem.unitStr("ev.desc"), e.self.getUOM(), self.getUOM(Unit.VOLT))
            uom.setScalingFactor(e.getAmount())


        elif (unit == Unit.WATT_HOUR):
            # watt-hour
            uom = self.createProductUOM(UnitType.ENERGY, Unit.WATT_HOUR, MeasurementSystem.unitStr("wh.name"), \
                    MeasurementSystem.unitStr("wh.symbol"), MeasurementSystem.unitStr("wh.desc"), self.getUOM(Unit.WATT), self.getHour())

        elif (unit == Unit.WATT):
            # power (watt)
            uom = self.createQuotientUOM(UnitType.POWER, Unit.WATT, MeasurementSystem.unitStr("watt.name"), \
                    MeasurementSystem.unitStr("watt.symbol"), MeasurementSystem.unitStr("watt.desc"), self.getUOM(Unit.JOULE), self.getSecond())

        elif (unit == Unit.HERTZ):
            # frequency (hertz)
            uom = self.createQuotientUOM(UnitType.FREQUENCY, Unit.HERTZ, MeasurementSystem.unitStr("hertz.name"), \
                    MeasurementSystem.unitStr("hertz.symbol"), MeasurementSystem.unitStr("hertz.desc"), self.getOne(), self.getSecond())

        elif (unit == Unit.RAD_PER_SEC):
            # angular frequency
            uom = self.createQuotientUOM(UnitType.FREQUENCY, Unit.RAD_PER_SEC, MeasurementSystem.unitStr("radpers.name"), \
                    MeasurementSystem.unitStr("radpers.symbol"), MeasurementSystem.unitStr("radpers.desc"), self.getUOM(Unit.RADIAN),
                    self.getSecond())
            uom.setConversion(1.0 / (2.0 * math.pi), self.getUOM(Unit.HERTZ))

        elif (unit == Unit.PASCAL):
            # pressure
            uom = self.createQuotientUOM(UnitType.PRESSURE, Unit.PASCAL, MeasurementSystem.unitStr("pascal.name"), \
                    MeasurementSystem.unitStr("pascal.symbol"), MeasurementSystem.unitStr("pascal.desc"), self.getUOM(Unit.NEWTON),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.ATMOSPHERE):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, Unit.ATMOSPHERE, MeasurementSystem.unitStr("atm.name"), \
                    MeasurementSystem.unitStr("atm.symbol"), MeasurementSystem.unitStr("atm.desc"))
            uom.setConversion(101325, self.getUOM(Unit.PASCAL))

        elif (unit == Unit.BAR):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, Unit.BAR, MeasurementSystem.unitStr("bar.name"), \
                    MeasurementSystem.unitStr("bar.symbol"), MeasurementSystem.unitStr("bar.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.PASCAL), 1.0E+05)

        elif (unit == Unit.COULOMB):
            # charge (coulomb)
            uom = self.createProductUOM(UnitType.ELECTRIC_CHARGE, Unit.COULOMB, MeasurementSystem.unitStr("coulomb.name"), \
                    MeasurementSystem.unitStr("coulomb.symbol"), MeasurementSystem.unitStr("coulomb.desc"), self.getUOM(Unit.AMPERE), \
                    self.getSecond())

        elif (unit == Unit.VOLT):
            # voltage (volt)
            uom = self.createQuotientUOM(UnitType.ELECTROMOTIVE_FORCE, Unit.VOLT, MeasurementSystem.unitStr("volt.name"), \
                    MeasurementSystem.unitStr("volt.symbol"), MeasurementSystem.unitStr("volt.desc"), self.getUOM(Unit.WATT), \
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.OHM):
            # resistance (ohm)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_RESISTANCE, Unit.OHM, MeasurementSystem.unitStr("ohm.name"), \
                    MeasurementSystem.unitStr("ohm.symbol"), MeasurementSystem.unitStr("ohm.desc"), self.getUOM(Unit.VOLT), self.getUOM(Unit.AMPERE))

        elif (unit == Unit.FARAD):
            # capacitance (farad)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CAPACITANCE, Unit.FARAD, MeasurementSystem.unitStr("farad.name"), \
                    MeasurementSystem.unitStr("farad.symbol"), MeasurementSystem.unitStr("farad.desc"), self.getUOM(Unit.COULOMB), \
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.FARAD_PER_METRE):
            # electric permittivity (farad/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_PERMITTIVITY, Unit.FARAD_PER_METRE, MeasurementSystem.unitStr("fperm.name"), \
                    MeasurementSystem.unitStr("fperm.symbol"), MeasurementSystem.unitStr("fperm.desc"), self.getUOM(Unit.FARAD), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.AMPERE_PER_METRE):
            # electric field strength(ampere/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_FIELD_STRENGTH, Unit.AMPERE_PER_METRE, \
                    MeasurementSystem.unitStr("aperm.name"), MeasurementSystem.unitStr("aperm.symbol"), MeasurementSystem.unitStr("aperm.desc"), \
                    self.getUOM(Unit.AMPERE), self.getUOM(Unit.METRE))

        elif (unit == Unit.WEBER):
            # magnetic flux (weber)
            uom = self.createProductUOM(UnitType.MAGNETIC_FLUX, Unit.WEBER, MeasurementSystem.unitStr("weber.name"), \
                    MeasurementSystem.unitStr("weber.symbol"), MeasurementSystem.unitStr("weber.desc"), self.getUOM(Unit.VOLT), self.getSecond())

        elif (unit == Unit.TESLA):
            # magnetic flux density (tesla)
            uom = self.createQuotientUOM(UnitType.MAGNETIC_FLUX_DENSITY, Unit.TESLA, MeasurementSystem.unitStr("tesla.name"), \
                    MeasurementSystem.unitStr("tesla.symbol"), MeasurementSystem.unitStr("tesla.desc"), self.getUOM(Unit.WEBER), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.HENRY):
            # inductance (henry)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_INDUCTANCE, Unit.HENRY, MeasurementSystem.unitStr("henry.name"), \
                    MeasurementSystem.unitStr("henry.symbol"), MeasurementSystem.unitStr("henry.desc"), self.getUOM(Unit.WEBER), \
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.SIEMENS):
            # electrical conductance (siemens)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CONDUCTANCE, Unit.SIEMENS, MeasurementSystem.unitStr("siemens.name"), \
                    MeasurementSystem.unitStr("siemens.symbol"), MeasurementSystem.unitStr("siemens.desc"), self.getUOM(Unit.AMPERE), \
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.CELSIUS):
            # °C = °K - 273.15
            uom = self.createScalarUOM(UnitType.TEMPERATURE, Unit.CELSIUS, MeasurementSystem.unitStr("celsius.name"), \
                    MeasurementSystem.unitStr("celsius.symbol"), MeasurementSystem.unitStr("celsius.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.KELVIN), 273.15)

        elif (unit == Unit.LUMEN):
            # luminous flux (lumen)
            uom = self.createProductUOM(UnitType.LUMINOUS_FLUX, Unit.LUMEN, MeasurementSystem.unitStr("lumen.name"), \
                    MeasurementSystem.unitStr("lumen.symbol"), MeasurementSystem.unitStr("lumen.desc"), self.getUOM(Unit.CANDELA), \
                    self.getUOM(Unit.STERADIAN))

        elif (unit == Unit.LUX):
            # illuminance (lux)
            uom = self.createQuotientUOM(UnitType.ILLUMINANCE, Unit.LUX, MeasurementSystem.unitStr("lux.name"), \
                    MeasurementSystem.unitStr("lux.symbol"), MeasurementSystem.unitStr("lux.desc"), self.getUOM(Unit.LUMEN), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.BECQUEREL):
            # radioactivity (becquerel). Same definition as Hertz 1/s)
            uom = self.createQuotientUOM(UnitType.RADIOACTIVITY, Unit.BECQUEREL, MeasurementSystem.unitStr("becquerel.name"), \
                    MeasurementSystem.unitStr("becquerel.symbol"), MeasurementSystem.unitStr("becquerel.desc"), self.getOne(), self.self.getSecond())

        elif (unit == Unit.GRAY):
            # gray (Gy)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_ABSORBED, Unit.GRAY, MeasurementSystem.unitStr("gray.name"), \
                    MeasurementSystem.unitStr("gray.symbol"), MeasurementSystem.unitStr("gray.desc"), self.getUOM(Unit.JOULE), \
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERT):
            # sievert (Sv)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_EFFECTIVE, Unit.SIEVERT, MeasurementSystem.unitStr("sievert.name"), \
                    MeasurementSystem.unitStr("sievert.symbol"), MeasurementSystem.unitStr("sievert.desc"), self.getUOM(Unit.JOULE), \
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERTS_PER_HOUR):
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_RATE, Unit.SIEVERTS_PER_HOUR, MeasurementSystem.unitStr("sph.name"), \
                    MeasurementSystem.unitStr("sph.symbol"), MeasurementSystem.unitStr("sph.desc"), self.getUOM(Unit.SIEVERT), self.getHour())

        elif (unit == Unit.KATAL):
            # katal (kat)
            uom = self.createQuotientUOM(UnitType.CATALYTIC_ACTIVITY, Unit.KATAL, MeasurementSystem.unitStr("katal.name"), \
                    MeasurementSystem.unitStr("katal.symbol"), MeasurementSystem.unitStr("katal.desc"), self.getUOM(Unit.MOLE), self.getSecond())

        elif (unit == Unit.UNIT):
            # Unit (U)
            uom = self.createScalarUOM(UnitType.CATALYTIC_ACTIVITY, Unit.UNIT, MeasurementSystem.unitStr("unit.name"), \
                    MeasurementSystem.unitStr("unit.symbol"), MeasurementSystem.unitStr("unit.desc"))
            uom.setConversion(1.0E-06 / 60, self.getUOM(Unit.KATAL))

        elif (unit == Unit.INTERNATIONAL_UNIT):
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, Unit.INTERNATIONAL_UNIT, MeasurementSystem.unitStr("iu.name"), \
                    MeasurementSystem.unitStr("iu.symbol"), MeasurementSystem.unitStr("iu.desc"))

        elif (unit == Unit.ANGSTROM):
            # length
            uom = self.createScalarUOM(UnitType.LENGTH, Unit.ANGSTROM, MeasurementSystem.unitStr("angstrom.name"), \
                    MeasurementSystem.unitStr("angstrom.symbol"), MeasurementSystem.unitStr("angstrom.desc"))
            uom.setConversion(0.1, self.getUOM(Prefix.nano(), self.getUOM(Unit.METRE)))

        elif (unit == Unit.BIT):
            # computer bit
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, Unit.BIT, MeasurementSystem.unitStr("bit.name"), \
                    MeasurementSystem.unitStr("bit.symbol"), MeasurementSystem.unitStr("bit.desc"))

        elif (unit == Unit.BYTE):
            # computer byte
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, Unit.BYTE, MeasurementSystem.unitStr("byte.name"), \
                    MeasurementSystem.unitStr("byte.symbol"), MeasurementSystem.unitStr("byte.desc"))
            uom.setConversion(8, self.getUOM(Unit.BIT))

        elif (unit == Unit.WATTS_PER_SQ_METRE):
            uom = self.createQuotientUOM(UnitType.IRRADIANCE, Unit.WATTS_PER_SQ_METRE, MeasurementSystem.unitStr("wsm.name"), \
                    MeasurementSystem.unitStr("wsm.symbol"), MeasurementSystem.unitStr("wsm.desc"), self.getUOM(Unit.WATT), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.PARSEC):
            uom = self.createScalarUOM(UnitType.LENGTH, Unit.PARSEC, MeasurementSystem.unitStr("parsec.name"), \
                    MeasurementSystem.unitStr("parsec.symbol"), MeasurementSystem.unitStr("parsec.desc")) 
            uom.setConversion(3.08567758149137E+16, self.getUOM(Unit.METRE))

        elif (unit == Unit.ASTRONOMICAL_UNIT):
            uom = self.createScalarUOM(UnitType.LENGTH, Unit.ASTRONOMICAL_UNIT, MeasurementSystem.unitStr("au.name"), \
                    MeasurementSystem.unitStr("au.symbol"), MeasurementSystem.unitStr("au.desc"))
            uom.setConversion(1.49597870700E+11, self.getUOM(Unit.METRE))
        
        return uom
    
    def createCustomaryUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.RANKINE):
            # Rankine (base) 
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, \
                MeasurementSystem.unitStr("rankine.name"), MeasurementSystem.unitStr("rankine.symbol"), MeasurementSystem.unitStr("rankine.desc"))
            
            # create bridge to SI
            uom.setBridgeConversion(5.0/9.0, self.self.getUOM(Unit.KELVIN), 0.0)

        return uom
    
    def createUSUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.US_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.unitStr("us_gallon.name"), MeasurementSystem.unitStr("us_gallon.symbol"), MeasurementSystem.unitStr("us_gallon.desc"))
            uom.setConversion(231.0, self.self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        return uom
        
    def createBRUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.BR_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.unitStr("br_gallon.name"), MeasurementSystem.unitStr("br_gallon.symbol"), MeasurementSystem.unitStr("br_gallon.desc"))
            uom.setConversion(277.4194327916215, self.self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        return uom
    
    def createFinancialUnit(self, unit: Unit) -> UnitOfMeasure:
        uom = None
        
        if (unit == Unit.US_DOLLAR):
            # dollar 
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, \
                MeasurementSystem.unitStr("us_dollar.name"), MeasurementSystem.unitStr("us_dollar.symbol"), MeasurementSystem.unitStr("us_dollar.desc"))
            
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