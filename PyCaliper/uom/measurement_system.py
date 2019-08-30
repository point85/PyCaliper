import math

from PyCaliper.uom.constant import Constant
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.unit import Unit
#from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.unit_type import UnitType
from builtins import staticmethod

class CacheManager:
    def __init__(self):
        self.symbolRegistry = {}
        self.baseRegistry = {}
        self.unitRegistry = {}
    
    def getUOMBySymbol(self, symbol):
        return self.symbolRegistry[symbol]
        
    def getUOMByUnit(self, unit):
        return self.unitRegistry[unit]
    
    def getBaseUOM(self, baseSymbol):
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
    
    def unregisterUnit(self, uom):
        # remove by enumeration
        if (uom.unitType is not None):
            del self.unitRegistry[uom.unit] 
            
        # remove by symbol and base symbol
        del self.symbolRegistry[uom.symbol]
        del self.baseRegistry[uom.getBaseSymbol()]
        
    def registerUnit(self, uom):
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
    # single instance
    unifiedSystem = None
    
    def __init__(self):
        MeasurementSystem.unifiedSystem = self
        self.unitTypeRegistry = {}
        self.cacheManager = CacheManager()

    @staticmethod
    def instance():
        if (MeasurementSystem.unifiedSystem is None):
            MeasurementSystem()
        return MeasurementSystem.unifiedSystem 
    
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
    
    def getUOM(self, unit):
        uom = self.cacheManager.getUOM(unit)

        if (uom is None):
            uom = self.createUOMForUnit(unit)
        return uom
        
    def getOne(self):
        return self.getUOMByUnit(Unit.ONE)
    
    def createScalarUOM(self, unitType, unit, name, symbol, description):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        self.registerUnit(uom)
        return uom
    
    def createSIUnit(self, unit):
        uom = None
        
        if (unit == Unit.ONE):
            # unity
            uom = self.createScalarUOM(UnitType.UNITY, unit, \
                MeasurementSystem.unitStr("one.name"), MeasurementSystem.unitStr("one.symbol"), MeasurementSystem.unitStr("one.desc"))
        
        elif (unit == Unit.PERCENT):
            uom = self.createScalarUOM(UnitType.UNITY, unit, MeasurementSystem.unitStr("percent.name"), \
                    MeasurementSystem.unitStr("percent.symbol"), MeasurementSystem.unitStr("percent.desc"))
            uom.setConversion(0.01, self.getOne())

        elif (unit == Unit.SECOND):
            # second
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("sec.name"), \
                    MeasurementSystem.unitStr("sec.symbol"), MeasurementSystem.unitStr("sec.desc"))

        elif (unit == Unit.MINUTE):
            # minute
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("min.name"), \
                    MeasurementSystem.unitStr("min.symbol"), MeasurementSystem.unitStr("min.desc"))
            uom.setConversion(60.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.HOUR):
            # hour
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("hr.name"), MeasurementSystem.unitStr("hr.symbol"), \
                    MeasurementSystem.unitStr("hr.desc"))
            uom.setConversion(3600.0, self.getUOM(Unit.SECOND))
        
        elif (unit == Unit.DAY):
            # day
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("day.name"), MeasurementSystem.unitStr("day.symbol"), \
                    MeasurementSystem.unitStr("day.desc"))
            uom.setConversion(86400.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.WEEK):
            # week
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("week.name"), \
                    MeasurementSystem.unitStr("week.symbol"), MeasurementSystem.unitStr("week.desc"))
            uom.setConversion(604800.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.JULIAN_YEAR):
            # Julian year
            uom = self.createScalarUOM(UnitType.TIME, unit, MeasurementSystem.unitStr("jyear.name"), \
                    MeasurementSystem.unitStr("jyear.symbol"), MeasurementSystem.unitStr("jyear.desc"))
            uom.setConversion(3.1557600E+07, self.getUOM(Unit.SECOND))

        elif (unit == Unit.SQUARE_SECOND):
            # square second
            uom = self.createPowerUOM(UnitType.TIME_SQUARED, unit, MeasurementSystem.unitStr("s2.name"), \
                    MeasurementSystem.unitStr("s2.symbol"), MeasurementSystem.unitStr("s2.desc"), self.getUOM(Unit.SECOND), 2)

        elif (unit == Unit.MOLE):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, MeasurementSystem.unitStr("mole.name"), \
                    MeasurementSystem.unitStr("mole.symbol"), MeasurementSystem.unitStr("mole.desc"))

        elif (unit == Unit.EQUIVALENT):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, MeasurementSystem.unitStr("equivalent.name"), \
                    MeasurementSystem.unitStr("equivalent.symbol"), MeasurementSystem.unitStr("equivalent.desc"))

        elif (unit == Unit.DECIBEL):
            # decibel
            uom = self.createScalarUOM(UnitType.INTENSITY, unit, MeasurementSystem.unitStr("db.name"), \
                    MeasurementSystem.unitStr("db.symbol"), MeasurementSystem.unitStr("db.desc"))

        elif (unit == Unit.RADIAN):
            # plane angle radian (rad)
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, MeasurementSystem.unitStr("radian.name"), \
                    MeasurementSystem.unitStr("radian.symbol"), MeasurementSystem.unitStr("radian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.STERADIAN):
            # solid angle steradian (sr)
            uom = self.createScalarUOM(UnitType.SOLID_ANGLE, unit, MeasurementSystem.unitStr("steradian.name"), \
                    MeasurementSystem.unitStr("steradian.symbol"), MeasurementSystem.unitStr("steradian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.DEGREE):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, MeasurementSystem.unitStr("degree.name"), \
                    MeasurementSystem.unitStr("degree.symbol"), MeasurementSystem.unitStr("degree.desc"))
            uom.setConversion(math.pi / 180.0, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.ARC_SECOND):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, MeasurementSystem.unitStr("arcsec.name"), \
                    MeasurementSystem.unitStr("arcsec.symbol"), MeasurementSystem.unitStr("arcsec.desc"))
            uom.setConversion(math.pi / 648000.0, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.METRE):
            # fundamental length
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("m.name"), MeasurementSystem.unitStr("m.symbol"), \
                    MeasurementSystem.unitStr("m.desc"))

        elif (unit == Unit.DIOPTER):
            # per metre
            uom = self.createQuotientUOM(UnitType.RECIPROCAL_LENGTH, unit, MeasurementSystem.unitStr("diopter.name"), \
                    MeasurementSystem.unitStr("diopter.symbol"), MeasurementSystem.unitStr("diopter.desc"), self.getOne(), self.getUOM(Unit.METRE))

        elif (unit == Unit.KILOGRAM):
            # fundamental mass
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("kg.name"), \
                    MeasurementSystem.unitStr("kg.symbol"), MeasurementSystem.unitStr("kg.desc"))

        elif (unit == Unit.TONNE):
            # mass
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("tonne.name"), \
                    MeasurementSystem.unitStr("tonne.symbol"), MeasurementSystem.unitStr("tonne.desc"))
            uom.setConversion(Prefix.kilo().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.KELVIN):
            # fundamental temperature
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, MeasurementSystem.unitStr("kelvin.name"), \
                    MeasurementSystem.unitStr("kelvin.symbol"), MeasurementSystem.unitStr("kelvin.desc"))

        elif (unit == Unit.AMPERE):
            # electric current
            uom = self.createScalarUOM(UnitType.ELECTRIC_CURRENT, unit, MeasurementSystem.unitStr("amp.name"), \
                    MeasurementSystem.unitStr("amp.symbol"), MeasurementSystem.unitStr("amp.desc"))

        elif (unit == Unit.CANDELA):
            # luminosity
            uom = self.createScalarUOM(UnitType.LUMINOSITY, unit, MeasurementSystem.unitStr("cd.name"), \
                    MeasurementSystem.unitStr("cd.symbol"), MeasurementSystem.unitStr("cd.desc"))

        elif (unit == Unit.MOLARITY):
            # molar concentration
            uom = self.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, unit, MeasurementSystem.unitStr("molarity.name"), \
                    MeasurementSystem.unitStr("molarity.symbol"), MeasurementSystem.unitStr("molarity.desc"), self.getUOM(Unit.MOLE), \
                    self.getUOM(Unit.LITRE))

        elif (unit == Unit.GRAM): # gram
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("gram.name"), \
                    MeasurementSystem.unitStr("gram.symbol"), MeasurementSystem.unitStr("gram.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.CARAT):
            # carat
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("carat.name"), \
                    MeasurementSystem.unitStr("carat.symbol"), MeasurementSystem.unitStr("carat.desc"))
            uom.setConversion(0.2, self.getUOM(Unit.GRAM))

        elif (unit == Unit.SQUARE_METRE):
            # square metre
            uom = self.createPowerUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("m2.name"), \
                    MeasurementSystem.unitStr("m2.symbol"), MeasurementSystem.unitStr("m2.desc"), self.getUOM(Unit.METRE), 2)

        elif (unit == Unit.HECTARE):
            # hectare
            uom = self.createScalarUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("hectare.name"), \
                    MeasurementSystem.unitStr("hectare.symbol"), MeasurementSystem.unitStr("hectare.desc"))
            uom.setConversion(10000.0, self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.METRE_PER_SEC):
            # velocity
            uom = self.createQuotientUOM(UnitType.VELOCITY, unit, MeasurementSystem.unitStr("mps.name"), \
                    MeasurementSystem.unitStr("mps.symbol"), MeasurementSystem.unitStr("mps.desc"), self.getUOM(Unit.METRE), self.getSecond())

        elif (unit == Unit.METRE_PER_SEC_SQUARED):
            # acceleration
            uom = self.createQuotientUOM(UnitType.ACCELERATION, unit, MeasurementSystem.unitStr("mps2.name"), \
                    MeasurementSystem.unitStr("mps2.symbol"), MeasurementSystem.unitStr("mps2.desc"), self.getUOM(Unit.METRE), \
                    self.getUOM(Unit.SQUARE_SECOND))

        elif (unit == Unit.CUBIC_METRE):
            # cubic metre
            uom = self.createPowerUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("m3.name"), \
                    MeasurementSystem.unitStr("m3.symbol"), MeasurementSystem.unitStr("m3.desc"), self.getUOM(Unit.METRE), 3)

        elif (unit == Unit.LITRE):
            # litre
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("litre.name"), \
                    MeasurementSystem.unitStr("litre.symbol"), MeasurementSystem.unitStr("litre.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.CUBIC_METRE))

        elif (unit == Unit.CUBIC_METRE_PER_SEC):
            # flow (volume)
            uom = self.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, unit,
                    MeasurementSystem.unitStr("m3PerSec.name"), MeasurementSystem.unitStr("m3PerSec.symbol"), \
                    MeasurementSystem.unitStr("m3PerSec.desc"), self.getUOM(Unit.CUBIC_METRE), self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_SEC):
            # flow (mass)
            uom = self.createQuotientUOM(UnitType.MASS_FLOW, unit, MeasurementSystem.unitStr("kgPerSec.name"), \
                    MeasurementSystem.unitStr("kgPerSec.symbol"), MeasurementSystem.unitStr("kgPerSec.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_CU_METRE):
            # kg/m^3
            uom = self.createQuotientUOM(UnitType.DENSITY, unit, MeasurementSystem.unitStr("kg_m3.name"), \
                    MeasurementSystem.unitStr("kg_m3.symbol"), MeasurementSystem.unitStr("kg_m3.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getUOM(Unit.CUBIC_METRE))

        elif (unit == Unit.PASCAL_SECOND):
            # dynamic viscosity
            uom = self.createProductUOM(UnitType.DYNAMIC_VISCOSITY, unit, MeasurementSystem.unitStr("pascal_sec.name"), \
                    MeasurementSystem.unitStr("pascal_sec.symbol"), MeasurementSystem.unitStr("pascal_sec.desc"), self.getUOM(Unit.PASCAL), \
                    self.getSecond())

        elif (unit == Unit.SQUARE_METRE_PER_SEC):
            # kinematic viscosity
            uom = self.createQuotientUOM(UnitType.KINEMATIC_VISCOSITY, unit, \
                    MeasurementSystem.unitStr("m2PerSec.name"), MeasurementSystem.unitStr("m2PerSec.symbol"), \
                    MeasurementSystem.unitStr("m2PerSec.desc"), self.getUOM(Unit.SQUARE_METRE), self.getSecond())

        elif (unit == Unit.CALORIE):
            # thermodynamic calorie
            uom = self.createScalarUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("calorie.name"), \
                    MeasurementSystem.unitStr("calorie.symbol"), MeasurementSystem.unitStr("calorie.desc"))
            uom.setConversion(4.184, self.getUOM(Unit.JOULE))

        elif (unit == Unit.NEWTON):
            # force F = m·A (newton)
            uom = self.createProductUOM(UnitType.FORCE, unit, MeasurementSystem.unitStr("newton.name"), \
                    MeasurementSystem.unitStr("newton.symbol"), MeasurementSystem.unitStr("newton.desc"), self.getUOM(Unit.KILOGRAM), \
                    self.getUOM(Unit.METRE_PER_SEC_SQUARED))

        elif (unit == Unit.NEWTON_METRE):
            # newton-metre
            uom = self.createProductUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("n_m.name"), \
                    MeasurementSystem.unitStr("n_m.symbol"), MeasurementSystem.unitStr("n_m.desc"), self.getUOM(Unit.NEWTON), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.JOULE):
            # energy (joule)
            uom = self.createProductUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("joule.name"), \
                    MeasurementSystem.unitStr("joule.symbol"), MeasurementSystem.unitStr("joule.desc"), self.getUOM(Unit.NEWTON), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.ELECTRON_VOLT):
            # ev
            e = self.getQuantity(Constant.ELEMENTARY_CHARGE)
            uom = self.createProductUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("ev.name"), \
                    MeasurementSystem.unitStr("ev.symbol"), MeasurementSystem.unitStr("ev.desc"), e.self.getUOM(), self.getUOM(Unit.VOLT))
            uom.setScalingFactor(e.getAmount())

        elif (unit == Unit.WATT_HOUR):
            # watt-hour
            uom = self.createProductUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("wh.name"), \
                    MeasurementSystem.unitStr("wh.symbol"), MeasurementSystem.unitStr("wh.desc"), self.getUOM(Unit.WATT), self.getHour())

        elif (unit == Unit.WATT):
            # power (watt)
            uom = self.createQuotientUOM(UnitType.POWER, unit, MeasurementSystem.unitStr("watt.name"), \
                    MeasurementSystem.unitStr("watt.symbol"), MeasurementSystem.unitStr("watt.desc"), self.getUOM(Unit.JOULE), self.getSecond())

        elif (unit == Unit.HERTZ):
            # frequency (hertz)
            uom = self.createQuotientUOM(UnitType.FREQUENCY, unit, MeasurementSystem.unitStr("hertz.name"), \
                    MeasurementSystem.unitStr("hertz.symbol"), MeasurementSystem.unitStr("hertz.desc"), self.getOne(), self.getSecond())

        elif (unit == Unit.RAD_PER_SEC):
            # angular frequency
            uom = self.createQuotientUOM(UnitType.FREQUENCY, unit, MeasurementSystem.unitStr("radpers.name"), \
                    MeasurementSystem.unitStr("radpers.symbol"), MeasurementSystem.unitStr("radpers.desc"), self.getUOM(Unit.RADIAN),
                    self.getSecond())
            uom.setConversion(1.0 / (2.0 * math.pi), self.getUOM(Unit.HERTZ))

        elif (unit == Unit.PASCAL):
            # pressure
            uom = self.createQuotientUOM(UnitType.PRESSURE, unit, MeasurementSystem.unitStr("pascal.name"), \
                    MeasurementSystem.unitStr("pascal.symbol"), MeasurementSystem.unitStr("pascal.desc"), self.getUOM(Unit.NEWTON),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.ATMOSPHERE):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, MeasurementSystem.unitStr("atm.name"), \
                    MeasurementSystem.unitStr("atm.symbol"), MeasurementSystem.unitStr("atm.desc"))
            uom.setConversion(101325.0, self.getUOM(Unit.PASCAL))

        elif (unit == Unit.BAR):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, MeasurementSystem.unitStr("bar.name"), \
                    MeasurementSystem.unitStr("bar.symbol"), MeasurementSystem.unitStr("bar.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.PASCAL), 1.0E+05)

        elif (unit == Unit.COULOMB):
            # charge (coulomb)
            uom = self.createProductUOM(UnitType.ELECTRIC_CHARGE, unit, MeasurementSystem.unitStr("coulomb.name"), \
                    MeasurementSystem.unitStr("coulomb.symbol"), MeasurementSystem.unitStr("coulomb.desc"), self.getUOM(Unit.AMPERE), \
                    self.getSecond())

        elif (unit == Unit.VOLT):
            # voltage (volt)
            uom = self.createQuotientUOM(UnitType.ELECTROMOTIVE_FORCE, unit, MeasurementSystem.unitStr("volt.name"), \
                    MeasurementSystem.unitStr("volt.symbol"), MeasurementSystem.unitStr("volt.desc"), self.getUOM(Unit.WATT), \
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.OHM):
            # resistance (ohm)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_RESISTANCE, unit, MeasurementSystem.unitStr("ohm.name"), \
                    MeasurementSystem.unitStr("ohm.symbol"), MeasurementSystem.unitStr("ohm.desc"), self.getUOM(Unit.VOLT), self.getUOM(Unit.AMPERE))

        elif (unit == Unit.FARAD):
            # capacitance (farad)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CAPACITANCE, unit, MeasurementSystem.unitStr("farad.name"), \
                    MeasurementSystem.unitStr("farad.symbol"), MeasurementSystem.unitStr("farad.desc"), self.getUOM(Unit.COULOMB), \
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.FARAD_PER_METRE):
            # electric permittivity (farad/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_PERMITTIVITY, unit, MeasurementSystem.unitStr("fperm.name"), \
                    MeasurementSystem.unitStr("fperm.symbol"), MeasurementSystem.unitStr("fperm.desc"), self.getUOM(Unit.FARAD), \
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.AMPERE_PER_METRE):
            # electric field strength(ampere/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_FIELD_STRENGTH, unit, \
                    MeasurementSystem.unitStr("aperm.name"), MeasurementSystem.unitStr("aperm.symbol"), MeasurementSystem.unitStr("aperm.desc"), \
                    self.getUOM(Unit.AMPERE), self.getUOM(Unit.METRE))

        elif (unit == Unit.WEBER):
            # magnetic flux (weber)
            uom = self.createProductUOM(UnitType.MAGNETIC_FLUX, unit, MeasurementSystem.unitStr("weber.name"), \
                    MeasurementSystem.unitStr("weber.symbol"), MeasurementSystem.unitStr("weber.desc"), self.getUOM(Unit.VOLT), self.getSecond())

        elif (unit == Unit.TESLA):
            # magnetic flux density (tesla)
            uom = self.createQuotientUOM(UnitType.MAGNETIC_FLUX_DENSITY, unit, MeasurementSystem.unitStr("tesla.name"), \
                    MeasurementSystem.unitStr("tesla.symbol"), MeasurementSystem.unitStr("tesla.desc"), self.getUOM(Unit.WEBER), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.HENRY):
            # inductance (henry)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_INDUCTANCE, unit, MeasurementSystem.unitStr("henry.name"), \
                    MeasurementSystem.unitStr("henry.symbol"), MeasurementSystem.unitStr("henry.desc"), self.getUOM(Unit.WEBER), \
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.SIEMENS):
            # electrical conductance (siemens)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CONDUCTANCE, unit, MeasurementSystem.unitStr("siemens.name"), \
                    MeasurementSystem.unitStr("siemens.symbol"), MeasurementSystem.unitStr("siemens.desc"), self.getUOM(Unit.AMPERE), \
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.CELSIUS):
            # °C = °K - 273.15
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, MeasurementSystem.unitStr("celsius.name"), \
                    MeasurementSystem.unitStr("celsius.symbol"), MeasurementSystem.unitStr("celsius.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.KELVIN), 273.15)

        elif (unit == Unit.LUMEN):
            # luminous flux (lumen)
            uom = self.createProductUOM(UnitType.LUMINOUS_FLUX, unit, MeasurementSystem.unitStr("lumen.name"), \
                    MeasurementSystem.unitStr("lumen.symbol"), MeasurementSystem.unitStr("lumen.desc"), self.getUOM(Unit.CANDELA), \
                    self.getUOM(Unit.STERADIAN))

        elif (unit == Unit.LUX):
            # illuminance (lux)
            uom = self.createQuotientUOM(UnitType.ILLUMINANCE, unit, MeasurementSystem.unitStr("lux.name"), \
                    MeasurementSystem.unitStr("lux.symbol"), MeasurementSystem.unitStr("lux.desc"), self.getUOM(Unit.LUMEN), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.BECQUEREL):
            # radioactivity (becquerel). Same definition as Hertz 1/s)
            uom = self.createQuotientUOM(UnitType.RADIOACTIVITY, unit, MeasurementSystem.unitStr("becquerel.name"), \
                    MeasurementSystem.unitStr("becquerel.symbol"), MeasurementSystem.unitStr("becquerel.desc"), self.getOne(), self.getSecond())

        elif (unit == Unit.GRAY):
            # gray (Gy)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_ABSORBED, unit, MeasurementSystem.unitStr("gray.name"), \
                    MeasurementSystem.unitStr("gray.symbol"), MeasurementSystem.unitStr("gray.desc"), self.getUOM(Unit.JOULE), \
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERT):
            # sievert (Sv)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_EFFECTIVE, unit, MeasurementSystem.unitStr("sievert.name"), \
                    MeasurementSystem.unitStr("sievert.symbol"), MeasurementSystem.unitStr("sievert.desc"), self.getUOM(Unit.JOULE), \
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERTS_PER_HOUR):
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_RATE, unit, MeasurementSystem.unitStr("sph.name"), \
                    MeasurementSystem.unitStr("sph.symbol"), MeasurementSystem.unitStr("sph.desc"), self.getUOM(Unit.SIEVERT), self.getHour())

        elif (unit == Unit.KATAL):
            # katal (kat)
            uom = self.createQuotientUOM(UnitType.CATALYTIC_ACTIVITY, unit, MeasurementSystem.unitStr("katal.name"), \
                    MeasurementSystem.unitStr("katal.symbol"), MeasurementSystem.unitStr("katal.desc"), self.getUOM(Unit.MOLE), self.getSecond())

        elif (unit == Unit.UNIT):
            # Unit (U)
            uom = self.createScalarUOM(UnitType.CATALYTIC_ACTIVITY, unit, MeasurementSystem.unitStr("unit.name"), \
                    MeasurementSystem.unitStr("unit.symbol"), MeasurementSystem.unitStr("unit.desc"))
            uom.setConversion(1.0E-06 / 60.0, self.getUOM(Unit.KATAL))

        elif (unit == Unit.INTERNATIONAL_UNIT):
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, MeasurementSystem.unitStr("iu.name"), \
                    MeasurementSystem.unitStr("iu.symbol"), MeasurementSystem.unitStr("iu.desc"))

        elif (unit == Unit.ANGSTROM):
            # length
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("angstrom.name"), \
                    MeasurementSystem.unitStr("angstrom.symbol"), MeasurementSystem.unitStr("angstrom.desc"))
            uom.setConversion(0.1, self.getUOM(Prefix.nano(), self.getUOM(Unit.METRE)))

        elif (unit == Unit.BIT):
            # computer bit
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, unit, MeasurementSystem.unitStr("bit.name"), \
                    MeasurementSystem.unitStr("bit.symbol"), MeasurementSystem.unitStr("bit.desc"))

        elif (unit == Unit.BYTE):
            # computer byte
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, unit, MeasurementSystem.unitStr("byte.name"), \
                    MeasurementSystem.unitStr("byte.symbol"), MeasurementSystem.unitStr("byte.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BIT))

        elif (unit == Unit.WATTS_PER_SQ_METRE):
            uom = self.createQuotientUOM(UnitType.IRRADIANCE, unit, MeasurementSystem.unitStr("wsm.name"), \
                    MeasurementSystem.unitStr("wsm.symbol"), MeasurementSystem.unitStr("wsm.desc"), self.getUOM(Unit.WATT), \
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.PARSEC):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("parsec.name"), \
                    MeasurementSystem.unitStr("parsec.symbol"), MeasurementSystem.unitStr("parsec.desc")) 
            uom.setConversion(3.08567758149137E+16, self.getUOM(Unit.METRE))

        elif (unit == Unit.ASTRONOMICAL_UNIT):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("au.name"), \
                    MeasurementSystem.unitStr("au.symbol"), MeasurementSystem.unitStr("au.desc"))
            uom.setConversion(1.49597870700E+11, self.getUOM(Unit.METRE))
        
        return uom
    
    def createCustomaryUnit(self, unit):
        uom = None
        
        if (unit == Unit.RANKINE):
            # Rankine (base) 
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, \
                MeasurementSystem.unitStr("rankine.name"), MeasurementSystem.unitStr("rankine.symbol"), MeasurementSystem.unitStr("rankine.desc"))
            
            # create bridge to SI
            uom.setBridgeConversion(5.0/9.0, self.getUOM(Unit.KELVIN), 0.0)
            
        elif (unit == Unit.FAHRENHEIT):
            # Fahrenheit
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, MeasurementSystem.unitStr("fahrenheit.name"), \
                    MeasurementSystem.unitStr("fahrenheit.symbol"), MeasurementSystem.unitStr("fahrenheit.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.RANKINE), 459.67)
            
        elif (unit == Unit.POUND_MASS):
            # lb mass (base)
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("lbm.name"), \
                    MeasurementSystem.unitStr("lbm.symbol"), MeasurementSystem.unitStr("lbm.desc"))

            # create bridge to SI
            uom.setBridgeConversion(0.45359237, self.getUOM(Unit.KILOGRAM), 0.0)       

        elif (unit == Unit.OUNCE):
            # ounce
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("ounce.name"), \
                    MeasurementSystem.unitStr("ounce.symbol"), MeasurementSystem.unitStr("ounce.desc"))
            uom.setConversion(0.0625, self.getUOM(Unit.POUND_MASS))
            
        elif (unit == Unit.TROY_OUNCE):
            # troy ounce
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("troy_oz.name"), \
                    MeasurementSystem.unitStr("troy_oz.symbol"), MeasurementSystem.unitStr("troy_oz.desc"))
            uom.setConversion(31.1034768, self.getUOM(Unit.GRAM))
            
        elif (unit == Unit.SLUG):
            # slug
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("slug.name"), \
                    MeasurementSystem.unitStr("slug.symbol"), MeasurementSystem.unitStr("slug.desc"))
            g = self.getQuantity(Constant.GRAVITY).convert(self.getUOM(Unit.FEET_PER_SEC_SQUARED))
            uom.setConversion(g.getAmount(), self.getUOM(Unit.POUND_MASS))
            

        elif (unit == Unit.FOOT):
            # foot (foot is base conversion unit)
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("foot.name"), \
                    MeasurementSystem.unitStr("foot.symbol"), MeasurementSystem.unitStr("foot.desc"))

            # bridge to SI
            uom.setBridgeConversion(0.3048, self.getUOM(Unit.METRE), 0)

        elif (unit == Unit.INCH):
            # inch
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("inch.name"), \
                    MeasurementSystem.unitStr("inch.symbol"), MeasurementSystem.unitStr("inch.desc"))
            uom.setConversion(1.0 / 12.0, self.getUOM(Unit.FOOT))
            
        elif (unit == Unit.MIL):
            # inch
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("mil.name"), MeasurementSystem.unitStr("mil.symbol"), \
                    MeasurementSystem.unitStr("mil.desc"))
            uom.setConversion(Prefix.milli().getFactor(), self.getUOM(Unit.INCH))
            
        elif (unit == Unit.POINT):
            # point
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("point.name"), \
                    MeasurementSystem.unitStr("point.symbol"), MeasurementSystem.unitStr("point.desc"))
            uom.setConversion(1.0 / 72.0, self.getUOM(Unit.INCH))
            
        elif (unit == Unit.YARD):
            # yard
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("yard.name"), \
                    MeasurementSystem.unitStr("yard.symbol"), MeasurementSystem.unitStr("yard.desc"))
            uom.setConversion(3.0, self.getUOM(Unit.FOOT))
            
        elif (unit == Unit.MILE):
            # mile
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("mile.name"), \
                    MeasurementSystem.unitStr("mile.symbol"), MeasurementSystem.unitStr("mile.desc"))
            uom.setConversion(5280.0, self.getUOM(Unit.FOOT))
            
        elif (unit == Unit.NAUTICAL_MILE):
            # nautical mile
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("NM.name"), \
                    MeasurementSystem.unitStr("NM.symbol"), MeasurementSystem.unitStr("NM.desc"))
            uom.setConversion(6080.0, self.getUOM(Unit.FOOT))
            
        elif (unit == Unit.FATHOM):
            # fathom
            uom = self.createScalarUOM(UnitType.LENGTH, unit, MeasurementSystem.unitStr("fth.name"),
                    MeasurementSystem.unitStr("fth.symbol"), MeasurementSystem.unitStr("fth.desc"))
            uom.setConversion(6.0, self.getUOM(Unit.FOOT))

            
        elif (unit == Unit.PSI):
            # psi
            uom = self.createQuotientUOM(UnitType.PRESSURE, unit, MeasurementSystem.unitStr("psi.name"), \
                    MeasurementSystem.unitStr("psi.symbol"), MeasurementSystem.unitStr("psi.desc"), self.getUOM(Unit.POUND_FORCE), \
                    self.getUOM(Unit.SQUARE_INCH))
            
        elif (unit == Unit.IN_HG):
            # inches of Mercury
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, MeasurementSystem.unitStr("inhg.name"), \
                    MeasurementSystem.unitStr("inhg.symbol"), MeasurementSystem.unitStr("inhg.desc"))
            uom.setConversion(0.4911531047, self.getUOM(Unit.PSI))     

        elif (unit == Unit.SQUARE_INCH):
            # square inch
            uom = self.createPowerUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("in2.name"), \
                    MeasurementSystem.unitStr("in2.symbol"), MeasurementSystem.unitStr("in2.desc"), self.getUOM(Unit.INCH), 2)
            uom.setConversion(1.0 / 144.0, self.getUOM(Unit.SQUARE_FOOT))
            
        elif (unit == Unit.SQUARE_FOOT):
            # square foot
            uom = self.createPowerUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("ft2.name"), \
                    MeasurementSystem.unitStr("ft2.symbol"), MeasurementSystem.unitStr("ft2.desc"), self.getUOM(Unit.FOOT), 2)
            
        elif (unit == Unit.SQUARE_YARD):
            # square yard
            uom = self.createPowerUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("yd2.name"), \
                    MeasurementSystem.unitStr("yd2.symbol"), MeasurementSystem.unitStr("yd2.desc"), self.getUOM(Unit.YARD), 2)    
        elif (unit == Unit.ACRE):
            # acre
            uom = self.createScalarUOM(UnitType.AREA, unit, MeasurementSystem.unitStr("acre.name"), \
                    MeasurementSystem.unitStr("acre.symbol"), MeasurementSystem.unitStr("acre.desc"))
            uom.setConversion(43560.0, self.getUOM(Unit.SQUARE_FOOT))
            
        elif (unit == Unit.CUBIC_INCH):
            # cubic inch
            uom = self.createPowerUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("in3.name"), \
                    MeasurementSystem.unitStr("in3.symbol"), MeasurementSystem.unitStr("in3.desc"), self.getUOM(Unit.INCH), 3)
            uom.setConversion(1.0 / 1728.0, self.getUOM(Unit.CUBIC_FOOT))
            
        elif (unit == Unit.CUBIC_FOOT):
            # cubic feet
            uom = self.createPowerUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("ft3.name"), \
                    MeasurementSystem.unitStr("ft3.symbol"), MeasurementSystem.unitStr("ft3.desc"), self.getUOM(Unit.FOOT), 3)
            
        elif (unit == Unit.CUBIC_FEET_PER_SEC):
            # flow (volume)
            uom = self.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, unit,
                    MeasurementSystem.unitStr("ft3PerSec.name"), MeasurementSystem.unitStr("ft3PerSec.symbol"), \
                    MeasurementSystem.unitStr("ft3PerSec.desc"), self.getUOM(Unit.CUBIC_FOOT), self.getSecond())
            
        elif (unit == Unit.CORD):
            # cord
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("cord.name"), \
                    MeasurementSystem.unitStr("cord.symbol"), MeasurementSystem.unitStr("cord.desc"))
            uom.setConversion(128.0, self.getUOM(Unit.CUBIC_FOOT))
            
        elif (unit == Unit.CUBIC_YARD):
            # cubic yard
            uom = self.createPowerUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("yd3.name"), \
                    MeasurementSystem.unitStr("yd3.symbol"), MeasurementSystem.unitStr("yd3.desc"), self.getUOM(Unit.YARD), 3)
            
        elif (unit == Unit.FEET_PER_SEC):
            # feet/sec
            uom = self.createQuotientUOM(UnitType.VELOCITY, unit, MeasurementSystem.unitStr("fps.name"), \
                    MeasurementSystem.unitStr("fps.symbol"), MeasurementSystem.unitStr("fps.desc"), self.getUOM(Unit.FOOT), self.getSecond())
            

        elif (unit == Unit.KNOT):
            # knot
            uom = self.createScalarUOM(UnitType.VELOCITY, unit, MeasurementSystem.unitStr("knot.name"), \
                    MeasurementSystem.unitStr("knot.symbol"), MeasurementSystem.unitStr("knot.desc"))
            uom.setConversion(6080.0 / 3600.0, self.getUOM(Unit.FEET_PER_SEC))
            

        elif (unit == Unit.FEET_PER_SEC_SQUARED):
            # acceleration
            uom = self.createQuotientUOM(UnitType.ACCELERATION, unit, MeasurementSystem.unitStr("ftps2.name"), \
                    MeasurementSystem.unitStr("ftps2.symbol"), MeasurementSystem.unitStr("ftps2.desc"), self.getUOM(Unit.FOOT), \
                    self.getUOM(Unit.SQUARE_SECOND))

        elif (unit == Unit.HP):
            # HP (mechanical)
            uom = self.createProductUOM(UnitType.POWER, unit, MeasurementSystem.unitStr("hp.name"), MeasurementSystem.unitStr("hp.symbol"), \
                    MeasurementSystem.unitStr("hp.desc"), self.getUOM(Unit.POUND_FORCE), self.getUOM(Unit.FEET_PER_SEC))
            uom.setScalingFactor(550.0)
            
        elif (unit == Unit.BTU):
            # BTU = 1055.056 Joules (778.169 ft-lbf)
            uom = self.createScalarUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("btu.name"), MeasurementSystem.unitStr("btu.symbol"), \
                    MeasurementSystem.unitStr("btu.desc"))
            uom.setConversion(778.1692622659652, self.getUOM(Unit.FOOT_POUND_FORCE))           

        elif (unit == Unit.FOOT_POUND_FORCE):
            # ft-lbf
            uom = self.createProductUOM(UnitType.ENERGY, unit, MeasurementSystem.unitStr("ft_lbf.name"), \
                    MeasurementSystem.unitStr("ft_lbf.symbol"), MeasurementSystem.unitStr("ft_lbf.desc"), self.getUOM(Unit.FOOT),
                    self.getUOM(Unit.POUND_FORCE))
            
        elif (unit == Unit.POUND_FORCE):
            # force F = m·A (lbf)
            uom = self.createProductUOM(UnitType.FORCE, unit, MeasurementSystem.unitStr("lbf.name"), \
                    MeasurementSystem.unitStr("lbf.symbol"), MeasurementSystem.unitStr("lbf.desc"), self.getUOM(Unit.POUND_MASS), \
                    self.getUOM(Unit.FEET_PER_SEC_SQUARED))

            # factor is acceleration of gravity
            gravity = self.getQuantity(Constant.GRAVITY).convert(self.getUOM(Unit.FEET_PER_SEC_SQUARED))
            uom.setScalingFactor(gravity.getAmount())
            
        elif (unit == Unit.GRAIN):
            # mass
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("grain.name"), \
                    MeasurementSystem.unitStr("grain.symbol"), MeasurementSystem.unitStr("grain.desc"))
            uom.setConversion(1.0 / 7000.0, self.getUOM(Unit.POUND_MASS))
            
        elif (unit == Unit.MILES_PER_HOUR):
            # velocity
            uom = self.createScalarUOM(UnitType.VELOCITY, unit, MeasurementSystem.unitStr("mph.name"), \
                    MeasurementSystem.unitStr("mph.symbol"), MeasurementSystem.unitStr("mph.desc"))
            uom.setConversion(5280.0 / 3600.0, self.getUOM(Unit.FEET_PER_SEC))
            
        elif (unit == Unit.REV_PER_MIN):
            # rpm
            uom = self.createQuotientUOM(UnitType.FREQUENCY, unit, MeasurementSystem.unitStr("rpm.name"), \
                    MeasurementSystem.unitStr("rpm.symbol"), MeasurementSystem.unitStr("rpm.desc"), self.getOne(), self.getMinute())
            
        return uom
    
    def createUSUnit(self, unit):
        uom = None
        
        if (unit == Unit.US_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.unitStr("us_gallon.name"), MeasurementSystem.unitStr("us_gallon.symbol"), MeasurementSystem.unitStr("us_gallon.desc"))
            uom.setConversion(231.0, self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        elif (unit == Unit. US_BARREL):
            # barrel
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_bbl.name"), \
                    MeasurementSystem.unitStr("us_bbl.symbol"), MeasurementSystem.unitStr("us_bbl.desc"))
            uom.setConversion(42.0, self.getUOM(Unit.US_GALLON))
            
        elif (unit == Unit. US_BUSHEL):
            # bushel
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_bu.name"), \
                    MeasurementSystem.unitStr("us_bu.symbol"), MeasurementSystem.unitStr("us_bu.desc"))
            uom.setConversion(2150.42058, self.getUOM(Unit.CUBIC_INCH))
            
        elif (unit == Unit. US_FLUID_OUNCE):
            # fluid ounce
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_fl_oz.name"), \
                    MeasurementSystem.unitStr("us_fl_oz.symbol"), MeasurementSystem.unitStr("us_fl_oz.desc"))
            uom.setConversion(0.0078125, self.getUOM(Unit.US_GALLON))
            
        elif (unit == Unit. US_CUP):
            # cup
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_cup.name"), \
                    MeasurementSystem.unitStr("us_cup.symbol"), MeasurementSystem.unitStr("us_cup.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.US_FLUID_OUNCE))

        elif (unit == Unit. US_PINT):
            # pint
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_pint.name"), \
                    MeasurementSystem.unitStr("us_pint.symbol"), MeasurementSystem.unitStr("us_pint.desc"))
            uom.setConversion(16.0, self.getUOM(Unit.US_FLUID_OUNCE))
            
        elif (unit == Unit. US_QUART):
            # quart
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_quart.name"), \
                    MeasurementSystem.unitStr("us_quart.symbol"), MeasurementSystem.unitStr("us_quart.desc"))
            uom.setConversion(32.0, self.getUOM(Unit.US_FLUID_OUNCE))
            
        elif (unit == Unit. US_TABLESPOON):
            # tablespoon
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_tbsp.name"), \
                    MeasurementSystem.unitStr("us_tbsp.symbol"), MeasurementSystem.unitStr("us_tbsp.desc"))
            uom.setConversion(0.5, self.getUOM(Unit.US_FLUID_OUNCE))
            
        elif (unit == Unit. US_TEASPOON):
            # teaspoon
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("us_tsp.name"), \
                    MeasurementSystem.unitStr("us_tsp.symbol"), MeasurementSystem.unitStr("us_tsp.desc"))
            uom.setConversion(1.0 / 6.0, self.getUOM(Unit.US_FLUID_OUNCE))
            
        elif (unit == Unit. US_TON):
            # ton
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("us_ton.name"), \
                    MeasurementSystem.unitStr("us_ton.symbol"), MeasurementSystem.unitStr("us_ton.desc"))
            uom.setConversion(2000.0, self.getUOM(Unit.POUND_MASS))
            
        return uom
        
    def createBRUnit(self, unit):
        uom = None
        
        if (unit == Unit.BR_GALLON):
            # gallon 
            uom = self.createScalarUOM(UnitType.VOLUME, unit, \
                MeasurementSystem.unitStr("br_gallon.name"), MeasurementSystem.unitStr("br_gallon.symbol"), MeasurementSystem.unitStr("br_gallon.desc"))
            uom.setConversion(277.4194327916215, self.getUOM(Unit.CUBIC_INCH), 0.0)
            
        elif (unit == Unit.BR_BUSHEL):
            # bushel
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_bu.name"), \
                    MeasurementSystem.unitStr("br_bu.symbol"), MeasurementSystem.unitStr("br_bu.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BR_GALLON))
            
        elif (unit == Unit.BR_FLUID_OUNCE):
            # fluid ounce
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_fl_oz.name"), \
                    MeasurementSystem.unitStr("br_fl_oz.symbol"), MeasurementSystem.unitStr("br_fl_oz.desc"))
            uom.setConversion(0.00625, self.getUOM(Unit.BR_GALLON))
            
        elif (unit == Unit.BR_CUP):
            # cup
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_cup.name"), \
                    MeasurementSystem.unitStr("br_cup.symbol"), MeasurementSystem.unitStr("br_cup.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BR_FLUID_OUNCE))
            
        elif (unit == Unit.BR_PINT):
            # pint
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_pint.name"), \
                    MeasurementSystem.unitStr("br_pint.symbol"), MeasurementSystem.unitStr("br_pint.desc"))
            uom.setConversion(20.0, self.getUOM(Unit.BR_FLUID_OUNCE))
            
        elif (unit == Unit.BR_QUART):
            # quart
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_quart.name"), \
                    MeasurementSystem.unitStr("br_quart.symbol"), MeasurementSystem.unitStr("br_quart.desc"))
            uom.setConversion(40.0, self.getUOM(Unit.BR_FLUID_OUNCE))
            
        elif (unit == Unit.BR_TABLESPOON):
            # tablespoon
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_tbsp.name"), \
                    MeasurementSystem.unitStr("br_tbsp.symbol"), MeasurementSystem.unitStr("br_tbsp.desc"))
            uom.setConversion(0.625, self.getUOM(Unit.BR_FLUID_OUNCE))
            
        elif (unit == Unit.BR_TEASPOON):
            # teaspoon
            uom = self.createScalarUOM(UnitType.VOLUME, unit, MeasurementSystem.unitStr("br_tsp.name"), \
                    MeasurementSystem.unitStr("br_tsp.symbol"), MeasurementSystem.unitStr("br_tsp.desc"))
            uom.setConversion(5.0 / 24.0, self.getUOM(Unit.BR_FLUID_OUNCE))
            
        elif (unit == Unit.BR_TON):
            # ton
            uom = self.createScalarUOM(UnitType.MASS, unit, MeasurementSystem.unitStr("br_ton.name"), \
                    MeasurementSystem.unitStr("br_ton.symbol"), MeasurementSystem.unitStr("br_ton.desc"))
            uom.setConversion(2240.0, self.getUOM(Unit.POUND_MASS))
            
        return uom
    
    def createFinancialUnit(self, unit):
        uom = None
        
        if (unit == Unit.US_DOLLAR):
            # dollar 
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, \
                MeasurementSystem.unitStr("us_dollar.name"), MeasurementSystem.unitStr("us_dollar.symbol"), MeasurementSystem.unitStr("us_dollar.desc"))
            
        elif (unit == Unit.EURO):
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, MeasurementSystem.unitStr.getString("euro.name"), \
                    MeasurementSystem.unitStr.getString("euro.symbol"), MeasurementSystem.unitStr.getString("euro.desc"))
            

        elif (unit == Unit.YUAN):
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, MeasurementSystem.unitStr.getString("yuan.name"), \
                    MeasurementSystem.unitStr.getString("yuan.symbol"), MeasurementSystem.unitStr.getString("yuan.desc"))
            
        return uom
    
    def createUOMForUnit(self, unit):
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
    
    def getQuantity(self, constant: Constant):
        named = None

        if (constant == Constant. LIGHT_VELOCITY):
            named = Quantity(299792458.0, self.getUOM(Unit.METRE_PER_SEC))
            named.setName(MeasurementSystem.unitStr("light.name"))
            named.setSymbol(MeasurementSystem.unitStr("light.symbol"))
            named.setDescription(MeasurementSystem.unitStr("light.desc"))
            
        elif (constant == Constant. LIGHT_YEAR):
            year = Quantity(1.0, self.getUOM(Unit.JULIAN_YEAR))
            named = self.getQuantity(Constant.LIGHT_VELOCITY).multiply(year)
            named.setName(MeasurementSystem.unitStr("ly.name"))
            named.setSymbol(MeasurementSystem.unitStr("ly.symbol"))
            named.setDescription(MeasurementSystem.unitStr("ly.desc"))
            
        elif (constant == Constant. GRAVITY):
            named = Quantity(9.80665, self.getUOM(Unit.METRE_PER_SEC_SQUARED))
            named.setName(MeasurementSystem.unitStr("gravity.name"))
            named.setSymbol(MeasurementSystem.unitStr("gravity.symbol"))
            named.setDescription(MeasurementSystem.unitStr("gravity.desc"))
            
        elif (constant == Constant. PLANCK_CONSTANT):
            js = self.createProductUOM(self.getUOM(Unit.JOULE), self.getSecond())
            named = Quantity(6.62607015E-34, js)
            named.setName(MeasurementSystem.unitStr("planck.name"))
            named.setSymbol(MeasurementSystem.unitStr("planck.symbol"))
            named.setDescription(MeasurementSystem.unitStr("planck.desc"))
            
        elif (constant == Constant. BOLTZMANN_CONSTANT):
            jk = self.createQuotientUOM(self.getUOM(Unit.JOULE), self.getUOM(Unit.KELVIN))
            named = Quantity(1.380649E-23, jk)
            named.setName(MeasurementSystem.unitStr("boltzmann.name"))
            named.setSymbol(MeasurementSystem.unitStr("boltzmann.symbol"))
            named.setDescription(MeasurementSystem.unitStr("boltzmann.desc"))    

        elif (constant == Constant. AVAGADRO_CONSTANT):
            # NA
            named = Quantity(6.02214076E+23, self.getOne())
            named.setName(MeasurementSystem.unitStr("avo.name"))
            named.setSymbol(MeasurementSystem.unitStr("avo.symbol"))
            named.setDescription(MeasurementSystem.unitStr("avo.desc"))
            
        elif (constant == Constant. GAS_CONSTANT):
            # R
            named = self.getQuantity(Constant.BOLTZMANN_CONSTANT).multiply(self.getQuantity(Constant.AVAGADRO_CONSTANT))
            named.setName(MeasurementSystem.unitStr("gas.name"))
            named.setSymbol(MeasurementSystem.unitStr("gas.symbol"))
            named.setDescription(MeasurementSystem.unitStr("gas.desc"))
            
        elif (constant == Constant. ELEMENTARY_CHARGE):
            # e
            named = Quantity(1.602176634E-19, self.getUOM(Unit.COULOMB))
            named.setName(MeasurementSystem.unitStr("e.name"))
            named.setSymbol(MeasurementSystem.unitStr("e.symbol"))
            named.setDescription(MeasurementSystem.unitStr("e.desc"))
            
        elif (constant == Constant. FARADAY_CONSTANT):
            # F = e.NA
            qe = self.getQuantity(Constant.ELEMENTARY_CHARGE)
            named = qe.multiply(self.getQuantity(Constant.AVAGADRO_CONSTANT))
            named.setName(MeasurementSystem.unitStr("faraday.name"))
            named.setSymbol(MeasurementSystem.unitStr("faraday.symbol"))
            named.setDescription(MeasurementSystem.unitStr("faraday.desc"))
            
        elif (constant == Constant. ELECTRIC_PERMITTIVITY):
            # epsilon0 = 1/(mu0*c^2)
            vc = self.getQuantity(Constant.LIGHT_VELOCITY)
            named = self.getQuantity(Constant.MAGNETIC_PERMEABILITY).multiply(vc).multiply(vc).invert()
            named.setName(MeasurementSystem.unitStr("eps0.name"))
            named.setSymbol(MeasurementSystem.unitStr("eps0.symbol"))
            named.setDescription(MeasurementSystem.unitStr("eps0.desc"))
            
        elif (constant == Constant. MAGNETIC_PERMEABILITY):
            # mu0
            hm = self.createQuotientUOM(self.getUOM(Unit.HENRY), self.getUOM(Unit.METRE))
            fourPi = 4.0 * math.pi * 1.0E-07
            named = Quantity(fourPi, hm)
            named.setName(MeasurementSystem.unitStr("mu0.name"))
            named.setSymbol(MeasurementSystem.unitStr("mu0.symbol"))
            named.setDescription(MeasurementSystem.unitStr("mu0.desc"))
            
        elif (constant == Constant. ELECTRON_MASS):
            # me
            named = Quantity(9.1093835611E-28, self.getUOM(Unit.GRAM))
            named.setName(MeasurementSystem.unitStr("me.name"))
            named.setSymbol(MeasurementSystem.unitStr("me.symbol"))
            named.setDescription(MeasurementSystem.unitStr("me.desc"))
            
        elif (constant == Constant. PROTON_MASS):
            # mp
            named = Quantity(1.67262189821E-24, self.getUOM(Unit.GRAM))
            named.setName(MeasurementSystem.unitStr("mp.name"))
            named.setSymbol(MeasurementSystem.unitStr("mp.symbol"))
            named.setDescription(MeasurementSystem.unitStr("mp.desc"))
            
        elif (constant == Constant. STEFAN_BOLTZMANN):
            k4 = self.createPowerUOM(self.getUOM(Unit.KELVIN), 4)
            sb = self.createQuotientUOM(self.getUOM(Unit.WATTS_PER_SQ_METRE), k4)
            named = Quantity(5.67036713E-08, sb)
            named.setName(MeasurementSystem.unitStr("sb.name"))
            named.setSymbol(MeasurementSystem.unitStr("sb.symbol"))
            named.setDescription(MeasurementSystem.unitStr("sb.desc"))
            
        elif (constant == Constant. HUBBLE_CONSTANT):
            kps = self.getUOM(Prefix.kilo(), self.getUOM(Unit.METRE_PER_SEC))
            mpc = self.getUOM(Prefix.mega(), self.getUOM(Unit.PARSEC))
            hubble = self.createQuotientUOM(kps, mpc)
            named = Quantity(71.9, hubble)
            named.setName(MeasurementSystem.unitStr("hubble.name"))
            named.setSymbol(MeasurementSystem.unitStr("hubble.symbol"))
            named.setDescription(MeasurementSystem.unitStr("hubble.desc"))
                 
        elif (constant == Constant. CAESIUM_FREQUENCY):
            named = Quantity(9192631770.0, self.getUOM(Unit.HERTZ))
            named.setName(MeasurementSystem.unitStr("caesium.name"))
            named.setSymbol(MeasurementSystem.unitStr("caesium.symbol"))
            named.setDescription(MeasurementSystem.unitStr("caesium.desc"))
                      
        elif (constant == Constant. LUMINOUS_EFFICACY):
            kcd = self.createQuotientUOM(self.getUOM(Unit.LUMEN), self.getUOM(Unit.WATT))
            named = Quantity(683.0, kcd)
            named.setName(MeasurementSystem.unitStr("kcd.name"))
            named.setSymbol(MeasurementSystem.unitStr("kcd.symbol"))
            named.setDescription(MeasurementSystem.unitStr("kcd.desc"))

        return named
    
    def createPowerUOM(self, unitType, unit, name, symbol, description, base, exponent):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setPowerUnit(base, exponent)
        self.registerUnit(uom)
        return uom
    
    def createUnclassifiedPowerUOM(self, base, exponent): 
        from PyCaliper.uom.unit_of_measure import UnitOfMeasure 
        if (base is None):          
            msg = MeasurementSystem.messageStr("base.cannot.be.null")
            raise Exception(msg)
    
        # create symbol
        symbol = UnitOfMeasure.generatePowerSymbol(base, exponent)
        return self.createPowerUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, base, exponent)
    
    def createProductUOM(self, unitType, unit, name, symbol, description, multiplier, multiplicand):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setProductUnits(multiplier, multiplicand)
        self.registerUnit(uom)
        return uom
    
    def createUnclassifiedProductUOM(self, multiplier, multiplicand):
        from PyCaliper.uom.unit_of_measure import UnitOfMeasure
        if (multiplier is None):          
            msg = MeasurementSystem.messageStr("multiplier.cannot.be.null")
            raise Exception(msg)
        
        if (multiplicand is None):          
            msg = MeasurementSystem.messageStr("multiplicand.cannot.be.null")
            raise Exception(msg)
        
        symbol = UnitOfMeasure.generateProductSymbol(multiplier, multiplicand)
        return self.createProductUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, multiplier, multiplicand)
    
    def createUnclassifiedQuotientUOM(self, dividend, divisor):
        from PyCaliper.uom.unit_of_measure import UnitOfMeasure
        if (dividend is None):
            msg = MeasurementSystem.messageStr("dividend.cannot.be.null")
            raise Exception(msg)
        
        if (divisor is None):
            msg = MeasurementSystem.messageStr("divisor.cannot.be.null")
            raise Exception(msg)
        
        symbol = UnitOfMeasure.generateQuotientSymbol(dividend, divisor)
        return self.createQuotientUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, dividend, divisor)
    
    def createQuotientUOM(self, unitType, unit, name, symbol, description, dividend, divisor):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setQuotientUnits(dividend, divisor)
        self.registerUnit(uom)
        return uom

    def createUOM(self, unitType, unit, name, symbol, description):
        from PyCaliper.uom.unit_of_measure import UnitOfMeasure
        if (symbol is None or len(symbol) == 0):
            msg = MeasurementSystem.messageStr("symbol.cannot.be.null")
            raise Exception(msg)
        
        if (unitType is None):
            msg = MeasurementSystem.messageStr("unit.type.cannot.be.null")
            raise Exception(msg)
        
        uom = self.cacheManager.self.getUOM(symbol)
        
        if (uom is None):
            # create a new one
            uom = UnitOfMeasure(unitType, name, symbol, description)
            uom.setAbscissaUnit(uom)
            uom.setEnumeration(unit)
            
        return uom
    
    def getSecond(self):
        return self.getUOMByUnit(Unit.SECOND)
    
    def getMinute(self):
        return self.getUOMByUnit(Unit.MINUTE)
    
    def getHour(self):
        return self.getUOMByUnit(Unit.HOUR)
    
    def getDay(self):
        return self.getUOMByUnit(Unit.DAY)
    
    def getRegisteredUnits(self):
        units = self.cacheManager.getCachedUnits()
        return units.sort()
    
    def getUnitsOfMeasure(self, unitType):
        units = []
        
        if (unitType == UnitType.LENGTH):
            # SI
            units.append(self.getUOM(Unit.METRE))
            units.append(self.getUOM(Unit.ANGSTROM))
            units.append(self.getUOM(Unit.PARSEC))
            units.append(self.getUOM(Unit.ASTRONOMICAL_UNIT))

            # customary
            units.append(self.getUOM(Unit.FOOT))
            units.append(self.getUOM(Unit.INCH))
            units.append(self.getUOM(Unit.MIL))
            units.append(self.getUOM(Unit.POINT))
            units.append(self.getUOM(Unit.YARD))
            units.append(self.getUOM(Unit.MILE))
            units.append(self.getUOM(Unit.NAUTICAL_MILE))
            units.append(self.getUOM(Unit.FATHOM))
                
        elif (unitType == UnitType.MASS):
            units.append(self.getUOM(Unit.KILOGRAM))
            units.append(self.getUOM(Unit.TONNE))
            units.append(self.getUOM(Unit.CARAT))

            # customary
            units.append(self.getUOM(Unit.POUND_MASS))
            units.append(self.getUOM(Unit.OUNCE))
            units.append(self.getUOM(Unit.TROY_OUNCE))
            units.append(self.getUOM(Unit.SLUG))
            units.append(self.getUOM(Unit.GRAIN))

            # US
            units.append(self.getUOM(Unit.US_TON))

            # British
            units.append(self.getUOM(Unit.BR_TON))
            
        elif (unitType == UnitType.TIME):
            units.append(self.getUOM(Unit.SECOND))
            units.append(self.getUOM(Unit.MINUTE))
            units.append(self.getUOM(Unit.HOUR))
            units.append(self.getUOM(Unit.DAY))
            units.append(self.getUOM(Unit.WEEK))
            units.append(self.getUOM(Unit.JULIAN_YEAR))    
            
        elif (unitType == UnitType.ACCELERATION):
            units.append(self.getUOM(Unit.METRE_PER_SEC_SQUARED))
            units.append(self.getUOM(Unit.FEET_PER_SEC_SQUARED))
            
        elif (unitType == UnitType.AREA):
            # customary
            units.append(self.getUOM(Unit.SQUARE_INCH))
            units.append(self.getUOM(Unit.SQUARE_FOOT))
            units.append(self.getUOM(Unit.SQUARE_YARD))
            units.append(self.getUOM(Unit.ACRE))

            # SI
            units.append(self.getUOM(Unit.SQUARE_METRE))
            units.append(self.getUOM(Unit.HECTARE))            

        elif (unitType == UnitType.CATALYTIC_ACTIVITY):
            units.append(self.getUOM(Unit.KATAL))
            units.append(self.getUOM(Unit.UNIT))

        elif (unitType == UnitType.COMPUTER_SCIENCE):
            units.append(self.getUOM(Unit.BIT))
            units.append(self.getUOM(Unit.BYTE))

        elif (unitType == UnitType.DENSITY):
            units.append(self.getUOM(Unit.KILOGRAM_PER_CU_METRE))

        elif (unitType == UnitType.DYNAMIC_VISCOSITY):
            units.append(self.getUOM(Unit.PASCAL_SECOND))

        elif (unitType == UnitType.ELECTRIC_CAPACITANCE):
            units.append(self.getUOM(Unit.FARAD))

        elif (unitType == UnitType.ELECTRIC_CHARGE):
            units.append(self.getUOM(Unit.COULOMB))

        elif (unitType == UnitType.ELECTRIC_CONDUCTANCE):
            units.append(self.getUOM(Unit.SIEMENS))

        elif (unitType == UnitType.ELECTRIC_CURRENT):
            units.append(self.getUOM(Unit.AMPERE))

        elif (unitType == UnitType.ELECTRIC_FIELD_STRENGTH):
            units.append(self.getUOM(Unit.AMPERE_PER_METRE))

        elif (unitType == UnitType.ELECTRIC_INDUCTANCE):
            units.append(self.getUOM(Unit.HENRY))

        elif (unitType == UnitType.ELECTRIC_PERMITTIVITY):
            units.append(self.getUOM(Unit.FARAD_PER_METRE))

        elif (unitType == UnitType.ELECTRIC_RESISTANCE):
            units.append(self.getUOM(Unit.OHM))

        elif (unitType == UnitType.ELECTROMOTIVE_FORCE):
            units.append(self.getUOM(Unit.VOLT))

        elif (unitType == UnitType.ENERGY):
            # customary
            units.append(self.getUOM(Unit.BTU))
            units.append(self.getUOM(Unit.FOOT_POUND_FORCE))

            # SI
            units.append(self.getUOM(Unit.CALORIE))
            units.append(self.getUOM(Unit.NEWTON_METRE))
            units.append(self.getUOM(Unit.JOULE))
            units.append(self.getUOM(Unit.WATT_HOUR))
            units.append(self.getUOM(Unit.ELECTRON_VOLT))


        elif (unitType == UnitType.CURRENCY):
            units.append(self.getUOM(Unit.US_DOLLAR))
            units.append(self.getUOM(Unit.EURO))
            units.append(self.getUOM(Unit.YUAN))

        elif (unitType == UnitType.FORCE):
            # customary
            units.append(self.getUOM(Unit.POUND_FORCE))

            # SI
            units.append(self.getUOM(Unit.NEWTON))

        elif (unitType == UnitType.FREQUENCY):
            units.append(self.getUOM(Unit.REV_PER_MIN))
            units.append(self.getUOM(Unit.HERTZ))
            units.append(self.getUOM(Unit.RAD_PER_SEC))

        elif (unitType == UnitType.ILLUMINANCE):
            units.append(self.getUOM(Unit.LUX))

        elif (unitType == UnitType.INTENSITY):
            units.append(self.getUOM(Unit.DECIBEL))

        elif (unitType == UnitType.IRRADIANCE):
            units.append(self.getUOM(Unit.WATTS_PER_SQ_METRE))

        elif (unitType == UnitType.KINEMATIC_VISCOSITY):
            units.append(self.getUOM(Unit.SQUARE_METRE_PER_SEC))

        elif (unitType == UnitType.LUMINOSITY):
            units.append(self.getUOM(Unit.CANDELA))

        elif (unitType == UnitType.LUMINOUS_FLUX):
            units.append(self.getUOM(Unit.LUMEN))

        elif (unitType == UnitType.MAGNETIC_FLUX):
            units.append(self.getUOM(Unit.WEBER))

        elif (unitType == UnitType.MAGNETIC_FLUX_DENSITY):
            units.append(self.getUOM(Unit.TESLA))

        elif (unitType == UnitType.MASS_FLOW):
            units.append(self.getUOM(Unit.KILOGRAM_PER_SEC))

        elif (unitType == UnitType.MOLAR_CONCENTRATION):
            units.append(self.getUOM(Unit.MOLARITY))

        elif (unitType == UnitType.PLANE_ANGLE):
            units.append(self.getUOM(Unit.DEGREE))
            units.append(self.getUOM(Unit.RADIAN))
            units.append(self.getUOM(Unit.ARC_SECOND))

        elif (unitType == UnitType.POWER):
            units.append(self.getUOM(Unit.HP))
            units.append(self.getUOM(Unit.WATT))

        elif (unitType == UnitType.PRESSURE):
            # customary
            units.append(self.getUOM(Unit.PSI))
            units.append(self.getUOM(Unit.IN_HG))

            # SI
            units.append(self.getUOM(Unit.PASCAL))
            units.append(self.getUOM(Unit.ATMOSPHERE))
            units.append(self.getUOM(Unit.BAR))

        elif (unitType == UnitType.RADIATION_DOSE_ABSORBED):
            units.append(self.getUOM(Unit.GRAY))

        elif (unitType == UnitType.RADIATION_DOSE_EFFECTIVE):
            units.append(self.getUOM(Unit.SIEVERT))

        elif (unitType == UnitType.RADIATION_DOSE_RATE):
            units.append(self.getUOM(Unit.SIEVERTS_PER_HOUR))

        elif (unitType == UnitType.RADIOACTIVITY):
            units.append(self.getUOM(Unit.BECQUEREL))

        elif (unitType == UnitType.RECIPROCAL_LENGTH):
            units.append(self.getUOM(Unit.DIOPTER))

        elif (unitType == UnitType.SOLID_ANGLE):
            units.append(self.getUOM(Unit.STERADIAN))

        elif (unitType == UnitType.SUBSTANCE_AMOUNT):
            units.append(self.getUOM(Unit.MOLE))
            units.append(self.getUOM(Unit.EQUIVALENT))
            units.append(self.getUOM(Unit.INTERNATIONAL_UNIT))

        elif (unitType == UnitType.TEMPERATURE):
            # customary
            units.append(self.getUOM(Unit.RANKINE))
            units.append(self.getUOM(Unit.FAHRENHEIT))

            # SI
            units.append(self.getUOM(Unit.KELVIN))
            units.append(self.getUOM(Unit.CELSIUS))

        elif (unitType == UnitType.TIME_SQUARED):
            units.append(self.getUOM(Unit.SQUARE_SECOND))

        elif (unitType == UnitType.UNITY):
            units.append(self.getUOM(Unit.ONE))
            units.append(self.getUOM(Unit.PERCENT))

        elif (unitType == UnitType.VELOCITY):
            # customary
            units.append(self.getUOM(Unit.FEET_PER_SEC))
            units.append(self.getUOM(Unit.MILES_PER_HOUR))
            units.append(self.getUOM(Unit.KNOT))

            # SI
            units.append(self.getUOM(Unit.METRE_PER_SEC))

        elif (unitType == UnitType.VOLUME):
            # British
            units.append(self.getUOM(Unit.BR_BUSHEL))
            units.append(self.getUOM(Unit.BR_CUP))
            units.append(self.getUOM(Unit.BR_FLUID_OUNCE))
            units.append(self.getUOM(Unit.BR_GALLON))
            units.append(self.getUOM(Unit.BR_PINT))
            units.append(self.getUOM(Unit.BR_QUART))
            units.append(self.getUOM(Unit.BR_TABLESPOON))
            units.append(self.getUOM(Unit.BR_TEASPOON))

            # customary
            units.append(self.getUOM(Unit.CUBIC_FOOT))
            units.append(self.getUOM(Unit.CUBIC_YARD))
            units.append(self.getUOM(Unit.CUBIC_INCH))
            units.append(self.getUOM(Unit.CORD))

            # SI
            units.append(self.getUOM(Unit.CUBIC_METRE))
            units.append(self.getUOM(Unit.LITRE))

            # US
            units.append(self.getUOM(Unit.US_BARREL))
            units.append(self.getUOM(Unit.US_BUSHEL))
            units.append(self.getUOM(Unit.US_CUP))
            units.append(self.getUOM(Unit.US_FLUID_OUNCE))
            units.append(self.getUOM(Unit.US_GALLON))
            units.append(self.getUOM(Unit.US_PINT))
            units.append(self.getUOM(Unit.US_QUART))
            units.append(self.getUOM(Unit.US_TABLESPOON))
            units.append(self.getUOM(Unit.US_TEASPOON))

        elif (unitType == UnitType.VOLUMETRIC_FLOW):
            units.append(self.getUOM(Unit.CUBIC_METRE_PER_SEC))
            units.append(self.getUOM(Unit.CUBIC_FEET_PER_SEC))
            
    def getUOMBySymbol(self, symbol):
        return self.cacheManager.getUOMBySymbol(symbol)
            
    def getUOMForUnit(self, prefix: Prefix, unit):
        return self.getUOMWithPrefix(prefix, MeasurementSystem.instance().getUOM(unit))
    
    def getUOMWithPrefix(self, prefix: Prefix, targetUOM):
        symbol = prefix.symbol+ targetUOM.symbol
        scaled = self.getUOMBySymbol(symbol)

        # if not found, create it
        if (scaled is None):
            # generate a name and description
            name = prefix.name + targetUOM.name
            description = str(prefix.factor) + " " + str(targetUOM.name)

            # scaling factor
            scalingFactor = targetUOM.scalingFactor * prefix.factor

            # create the unit of measure and set conversion
            scaled = self.createScalarUOM(targetUOM.unitType, None, name, symbol, description)
            scaled.setConversion(scalingFactor, targetUOM.abscissaUnit)

        return scaled
    
    def quantityFromPrefixedUnit(self, amount, prefix, unit):
        uom = MeasurementSystem.instance().getUOM(prefix, unit)
        return Quantity(amount, uom)
    
    def quantityFromUnit(self, amount, unit): 
        uom = MeasurementSystem.instance().getUOM(unit)
        return Quantity(amount, uom)
        
    def quantityFromStringUnit(self, strAmount, unit):
        amount = Quantity.createAmountFromString(strAmount)
        uom = MeasurementSystem.instance().getUOM(unit)
        return Quantity(amount, uom)
    
    def convertQuantityToUnit(self, quantity, unit):
        return quantity.convert(MeasurementSystem.instance().getUOM(unit))
    
    def convertQuantityToPrefixUnit(self, quantity, prefix, unit):
        return quantity.convert(MeasurementSystem.instance().getUOM(prefix, unit))
    
    def quantityToPower(self, quantity, exponent):
        amount = math.pow(self.quantity, exponent)
        uom = MeasurementSystem.instance().createPowerUOM(quantity.uom, exponent)
        return Quantity(amount, uom) 
