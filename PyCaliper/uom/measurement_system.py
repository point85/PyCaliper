import math
from builtins import staticmethod
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Constant
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.localizer import Localizer


class MeasurementSystem:    
    # single instance
    __unifiedSystem = None
    
    def __init__(self):
        MeasurementSystem.__unifiedSystem = self
        #TODO self.primeUomCache()

    @staticmethod
    def instance():
        if (MeasurementSystem.__unifiedSystem is None):
            MeasurementSystem()
        return MeasurementSystem.__unifiedSystem 
    
    def primeUomCache(self):
        self.getUOM(Unit.ONE)
        self.getUOM(Unit.SECOND)
        self.getUOM(Unit.METRE)
        
    def getUOM(self, unit):
        uom = CacheManager.instance().getUOMByUnit(unit)

        if (uom is None):
            uom = self.createUOMForUnit(unit)
            
        return uom
        
    def getOne(self):
        return self.getUOM(Unit.ONE)
    
    def createScalarUOM(self, unitType, unit, name, symbol, description):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        CacheManager.instance().registerUnit(uom)
        return uom
    
    def createBaseSIUnit(self, unit):
        uom = None
        
        if (unit == Unit.ONE):
            # unity
            uom = self.createScalarUOM(UnitType.UNITY, unit,
                    Localizer.instance().langStr("one.name"), Localizer.instance().langStr("one.symbol"), 
                    Localizer.instance().langStr("one.desc"))
        
        elif (unit == Unit.SECOND):
            # second
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("sec.name"),
                    Localizer.instance().langStr("sec.symbol"), Localizer.instance().langStr("sec.desc"))

        elif (unit == Unit.MINUTE):
            # minute
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("min.name"),
                    Localizer.instance().langStr("min.symbol"), Localizer.instance().langStr("min.desc"))
            uom.setConversion(60.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.HOUR):
            # hour
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("hr.name"), Localizer.instance().langStr("hr.symbol"),
                    Localizer.instance().langStr("hr.desc"))
            uom.setConversion(3600.0, self.getUOM(Unit.SECOND))
        
        elif (unit == Unit.DAY):
            # day
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("day.name"), Localizer.instance().langStr("day.symbol"),
                    Localizer.instance().langStr("day.desc"))
            uom.setConversion(86400.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.WEEK):
            # week
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("week.name"),
                    Localizer.instance().langStr("week.symbol"), Localizer.instance().langStr("week.desc"))
            uom.setConversion(604800.0, self.getUOM(Unit.SECOND))

        elif (unit == Unit.JULIAN_YEAR):
            # Julian year
            uom = self.createScalarUOM(UnitType.TIME, unit, Localizer.instance().langStr("jyear.name"),
                    Localizer.instance().langStr("jyear.symbol"), Localizer.instance().langStr("jyear.desc"))
            uom.setConversion(3.1557600E+07, self.getUOM(Unit.SECOND))
        
        elif (unit == Unit.METRE):
            # fundamental length
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("m.name"), Localizer.instance().langStr("m.symbol"),
                    Localizer.instance().langStr("m.desc"))

        elif (unit == Unit.SQUARE_METRE):
            # square metre
            uom = self.createPowerUOM(UnitType.AREA, unit, Localizer.instance().langStr("m2.name"),
                    Localizer.instance().langStr("m2.symbol"), Localizer.instance().langStr("m2.desc"), self.getUOM(Unit.METRE), 2)
            
        elif (unit == Unit.CUBIC_METRE):
            # cubic metre
            uom = self.createPowerUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("m3.name"),
                    Localizer.instance().langStr("m3.symbol"), Localizer.instance().langStr("m3.desc"), self.getUOM(Unit.METRE), 3)            
                    
        elif (unit == Unit.KILOGRAM):
            # fundamental mass
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("kg.name"),
                    Localizer.instance().langStr("kg.symbol"), Localizer.instance().langStr("kg.desc"))    
                
        elif (unit == Unit.GRAM):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("gram.name"),
                    Localizer.instance().langStr("gram.symbol"), Localizer.instance().langStr("gram.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.LITRE):
            # litre
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("litre.name"),
                    Localizer.instance().langStr("litre.symbol"), Localizer.instance().langStr("litre.desc"))
            uom.setConversion(Prefix.milli().factor, self.getUOM(Unit.CUBIC_METRE))        
        
        elif (unit == Unit.KELVIN):
            # fundamental temperature
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, Localizer.instance().langStr("kelvin.name"),
                    Localizer.instance().langStr("kelvin.symbol"), Localizer.instance().langStr("kelvin.desc"))

        elif (unit == Unit.CELSIUS):
            # °C = °K - 273.15
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, Localizer.instance().langStr("celsius.name"),
                    Localizer.instance().langStr("celsius.symbol"), Localizer.instance().langStr("celsius.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.KELVIN), 273.15)
            
        elif (unit == Unit.AMPERE):
            # electric current
            uom = self.createScalarUOM(UnitType.ELECTRIC_CURRENT, unit, Localizer.instance().langStr("amp.name"),
                    Localizer.instance().langStr("amp.symbol"), Localizer.instance().langStr("amp.desc"))
        return uom
    
    def createSIUnit(self, unit):
        uom = None
        
        if (unit == Unit.PERCENT):
            uom = self.createScalarUOM(UnitType.UNITY, unit, Localizer.instance().langStr("percent.name"),
                    Localizer.instance().langStr("percent.symbol"), Localizer.instance().langStr("percent.desc"))
            uom.setConversion(0.01, self.getOne())

        elif (unit == Unit.SQUARE_SECOND):
            # square second
            uom = self.createPowerUOM(UnitType.TIME_SQUARED, unit, Localizer.instance().langStr("s2.name"),
                    Localizer.instance().langStr("s2.symbol"), Localizer.instance().langStr("s2.desc"), self.getUOM(Unit.SECOND), 2)

        elif (unit == Unit.MOLE):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, Localizer.instance().langStr("mole.name"),
                    Localizer.instance().langStr("mole.symbol"), Localizer.instance().langStr("mole.desc"))

        elif (unit == Unit.EQUIVALENT):
            # substance amount
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, Localizer.instance().langStr("equivalent.name"),
                    Localizer.instance().langStr("equivalent.symbol"), Localizer.instance().langStr("equivalent.desc"))

        elif (unit == Unit.DECIBEL):
            # decibel
            uom = self.createScalarUOM(UnitType.INTENSITY, unit, Localizer.instance().langStr("db.name"),
                    Localizer.instance().langStr("db.symbol"), Localizer.instance().langStr("db.desc"))

        elif (unit == Unit.RADIAN):
            # plane angle radian (rad)
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, Localizer.instance().langStr("radian.name"),
                    Localizer.instance().langStr("radian.symbol"), Localizer.instance().langStr("radian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.STERADIAN):
            # solid angle steradian (sr)
            uom = self.createScalarUOM(UnitType.SOLID_ANGLE, unit, Localizer.instance().langStr("steradian.name"),
                    Localizer.instance().langStr("steradian.symbol"), Localizer.instance().langStr("steradian.desc"))
            uom.setConversion(self.getOne())

        elif (unit == Unit.DEGREE):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, Localizer.instance().langStr("degree.name"),
                    Localizer.instance().langStr("degree.symbol"), Localizer.instance().langStr("degree.desc"))
            uom.setConversion(math.pi / 180.0, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.ARC_SECOND):
            # degree of arc
            uom = self.createScalarUOM(UnitType.PLANE_ANGLE, unit, Localizer.instance().langStr("arcsec.name"),
                    Localizer.instance().langStr("arcsec.symbol"), Localizer.instance().langStr("arcsec.desc"))
            uom.setConversion(math.pi / 648000.0, self.getUOM(Unit.RADIAN))

        elif (unit == Unit.DIOPTER):
            # per metre
            uom = self.createQuotientUOM(UnitType.RECIPROCAL_LENGTH, unit, Localizer.instance().langStr("diopter.name"),
                    Localizer.instance().langStr("diopter.symbol"), Localizer.instance().langStr("diopter.desc"), self.getOne(), self.getUOM(Unit.METRE))

        elif (unit == Unit.TONNE):
            # mass
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("tonne.name"),
                    Localizer.instance().langStr("tonne.symbol"), Localizer.instance().langStr("tonne.desc"))
            uom.setConversion(Prefix.kilo().factor, self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.CANDELA):
            # luminosity
            uom = self.createScalarUOM(UnitType.LUMINOSITY, unit, Localizer.instance().langStr("cd.name"),
                    Localizer.instance().langStr("cd.symbol"), Localizer.instance().langStr("cd.desc"))

        elif (unit == Unit.MOLARITY):
            # molar concentration
            uom = self.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, unit, Localizer.instance().langStr("molarity.name"),
                    Localizer.instance().langStr("molarity.symbol"), Localizer.instance().langStr("molarity.desc"), self.getUOM(Unit.MOLE),
                    self.getUOM(Unit.LITRE))

        elif (unit == Unit.CARAT):
            # carat
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("carat.name"),
                    Localizer.instance().langStr("carat.symbol"), Localizer.instance().langStr("carat.desc"))
            uom.setConversion(0.2, self.getUOM(Unit.GRAM))

        elif (unit == Unit.HECTARE):
            # hectare
            uom = self.createScalarUOM(UnitType.AREA, unit, Localizer.instance().langStr("hectare.name"),
                    Localizer.instance().langStr("hectare.symbol"), Localizer.instance().langStr("hectare.desc"))
            uom.setConversion(10000.0, self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.METRE_PER_SEC):
            # velocity
            uom = self.createQuotientUOM(UnitType.VELOCITY, unit, Localizer.instance().langStr("mps.name"),
                    Localizer.instance().langStr("mps.symbol"), Localizer.instance().langStr("mps.desc"), self.getUOM(Unit.METRE), self.getSecond())

        elif (unit == Unit.METRE_PER_SEC_SQUARED):
            # acceleration
            uom = self.createQuotientUOM(UnitType.ACCELERATION, unit, Localizer.instance().langStr("mps2.name"),
                    Localizer.instance().langStr("mps2.symbol"), Localizer.instance().langStr("mps2.desc"), self.getUOM(Unit.METRE),
                    self.getUOM(Unit.SQUARE_SECOND))

        elif (unit == Unit.CUBIC_METRE_PER_SEC):
            # flow (volume)
            uom = self.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, unit,
                    Localizer.instance().langStr("m3PerSec.name"), Localizer.instance().langStr("m3PerSec.symbol"),
                    Localizer.instance().langStr("m3PerSec.desc"), self.getUOM(Unit.CUBIC_METRE), self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_SEC):
            # flow (mass)
            uom = self.createQuotientUOM(UnitType.MASS_FLOW, unit, Localizer.instance().langStr("kgPerSec.name"),
                    Localizer.instance().langStr("kgPerSec.symbol"), Localizer.instance().langStr("kgPerSec.desc"), self.getUOM(Unit.KILOGRAM),
                    self.getSecond())

        elif (unit == Unit.KILOGRAM_PER_CU_METRE):
            # kg/m^3
            uom = self.createQuotientUOM(UnitType.DENSITY, unit, Localizer.instance().langStr("kg_m3.name"),
                    Localizer.instance().langStr("kg_m3.symbol"), Localizer.instance().langStr("kg_m3.desc"), self.getUOM(Unit.KILOGRAM),
                    self.getUOM(Unit.CUBIC_METRE))

        elif (unit == Unit.PASCAL_SECOND):
            # dynamic viscosity
            uom = self.createProductUOM(UnitType.DYNAMIC_VISCOSITY, unit, Localizer.instance().langStr("pascal_sec.name"),
                    Localizer.instance().langStr("pascal_sec.symbol"), Localizer.instance().langStr("pascal_sec.desc"), self.getUOM(Unit.PASCAL),
                    self.getSecond())

        elif (unit == Unit.SQUARE_METRE_PER_SEC):
            # kinematic viscosity
            uom = self.createQuotientUOM(UnitType.KINEMATIC_VISCOSITY, unit,
                    Localizer.instance().langStr("m2PerSec.name"), Localizer.instance().langStr("m2PerSec.symbol"),
                    Localizer.instance().langStr("m2PerSec.desc"), self.getUOM(Unit.SQUARE_METRE), self.getSecond())

        elif (unit == Unit.CALORIE):
            # thermodynamic calorie
            uom = self.createScalarUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("calorie.name"),
                    Localizer.instance().langStr("calorie.symbol"), Localizer.instance().langStr("calorie.desc"))
            uom.setConversion(4.184, self.getUOM(Unit.JOULE))

        elif (unit == Unit.NEWTON):
            # force F = m·A (newton)
            uom = self.createProductUOM(UnitType.FORCE, unit, Localizer.instance().langStr("newton.name"),
                    Localizer.instance().langStr("newton.symbol"), Localizer.instance().langStr("newton.desc"), self.getUOM(Unit.KILOGRAM),
                    self.getUOM(Unit.METRE_PER_SEC_SQUARED))

        elif (unit == Unit.NEWTON_METRE):
            # newton-metre
            uom = self.createProductUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("n_m.name"),
                    Localizer.instance().langStr("n_m.symbol"), Localizer.instance().langStr("n_m.desc"), self.getUOM(Unit.NEWTON),
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.JOULE):
            # energy (joule)
            uom = self.createProductUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("joule.name"),
                    Localizer.instance().langStr("joule.symbol"), Localizer.instance().langStr("joule.desc"), self.getUOM(Unit.NEWTON),
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.ELECTRON_VOLT):
            # ev
            e = self.getQuantity(Constant.ELEMENTARY_CHARGE)
            uom = self.createProductUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("ev.name"),
                    Localizer.instance().langStr("ev.symbol"), Localizer.instance().langStr("ev.desc"), e.self.getUOM(), self.getUOM(Unit.VOLT))
            uom.setScalingFactor(e.getAmount())

        elif (unit == Unit.WATT_HOUR):
            # watt-hour
            uom = self.createProductUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("wh.name"),
                    Localizer.instance().langStr("wh.symbol"), Localizer.instance().langStr("wh.desc"), self.getUOM(Unit.WATT), self.getHour())

        elif (unit == Unit.WATT):
            # power (watt)
            uom = self.createQuotientUOM(UnitType.POWER, unit, Localizer.instance().langStr("watt.name"),
                    Localizer.instance().langStr("watt.symbol"), Localizer.instance().langStr("watt.desc"), self.getUOM(Unit.JOULE), self.getSecond())

        elif (unit == Unit.HERTZ):
            # frequency (hertz)
            uom = self.createQuotientUOM(UnitType.FREQUENCY, unit, Localizer.instance().langStr("hertz.name"),
                    Localizer.instance().langStr("hertz.symbol"), Localizer.instance().langStr("hertz.desc"), self.getOne(), self.getSecond())

        elif (unit == Unit.RAD_PER_SEC):
            # angular frequency
            uom = self.createQuotientUOM(UnitType.FREQUENCY, unit, Localizer.instance().langStr("radpers.name"),
                    Localizer.instance().langStr("radpers.symbol"), Localizer.instance().langStr("radpers.desc"), self.getUOM(Unit.RADIAN),
                    self.getSecond())
            uom.setConversion(1.0 / (2.0 * math.pi), self.getUOM(Unit.HERTZ))

        elif (unit == Unit.PASCAL):
            # pressure
            uom = self.createQuotientUOM(UnitType.PRESSURE, unit, Localizer.instance().langStr("pascal.name"),
                    Localizer.instance().langStr("pascal.symbol"), Localizer.instance().langStr("pascal.desc"), self.getUOM(Unit.NEWTON),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.ATMOSPHERE):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, Localizer.instance().langStr("atm.name"),
                    Localizer.instance().langStr("atm.symbol"), Localizer.instance().langStr("atm.desc"))
            uom.setConversion(101325.0, self.getUOM(Unit.PASCAL))

        elif (unit == Unit.BAR):
            # pressure
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, Localizer.instance().langStr("bar.name"),
                    Localizer.instance().langStr("bar.symbol"), Localizer.instance().langStr("bar.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.PASCAL), 1.0E+05)

        elif (unit == Unit.COULOMB):
            # charge (coulomb)
            uom = self.createProductUOM(UnitType.ELECTRIC_CHARGE, unit, Localizer.instance().langStr("coulomb.name"),
                    Localizer.instance().langStr("coulomb.symbol"), Localizer.instance().langStr("coulomb.desc"), self.getUOM(Unit.AMPERE),
                    self.getSecond())

        elif (unit == Unit.VOLT):
            # voltage (volt)
            uom = self.createQuotientUOM(UnitType.ELECTROMOTIVE_FORCE, unit, Localizer.instance().langStr("volt.name"),
                    Localizer.instance().langStr("volt.symbol"), Localizer.instance().langStr("volt.desc"), self.getUOM(Unit.WATT),
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.OHM):
            # resistance (ohm)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_RESISTANCE, unit, Localizer.instance().langStr("ohm.name"),
                    Localizer.instance().langStr("ohm.symbol"), Localizer.instance().langStr("ohm.desc"), self.getUOM(Unit.VOLT), self.getUOM(Unit.AMPERE))

        elif (unit == Unit.FARAD):
            # capacitance (farad)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CAPACITANCE, unit, Localizer.instance().langStr("farad.name"),
                    Localizer.instance().langStr("farad.symbol"), Localizer.instance().langStr("farad.desc"), self.getUOM(Unit.COULOMB),
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.FARAD_PER_METRE):
            # electric permittivity (farad/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_PERMITTIVITY, unit, Localizer.instance().langStr("fperm.name"),
                    Localizer.instance().langStr("fperm.symbol"), Localizer.instance().langStr("fperm.desc"), self.getUOM(Unit.FARAD),
                    self.getUOM(Unit.METRE))

        elif (unit == Unit.AMPERE_PER_METRE):
            # electric field strength(ampere/metre)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_FIELD_STRENGTH, unit,
                    Localizer.instance().langStr("aperm.name"), Localizer.instance().langStr("aperm.symbol"), Localizer.instance().langStr("aperm.desc"),
                    self.getUOM(Unit.AMPERE), self.getUOM(Unit.METRE))

        elif (unit == Unit.WEBER):
            # magnetic flux (weber)
            uom = self.createProductUOM(UnitType.MAGNETIC_FLUX, unit, Localizer.instance().langStr("weber.name"),
                    Localizer.instance().langStr("weber.symbol"), Localizer.instance().langStr("weber.desc"), self.getUOM(Unit.VOLT), self.getSecond())

        elif (unit == Unit.TESLA):
            # magnetic flux density (tesla)
            uom = self.createQuotientUOM(UnitType.MAGNETIC_FLUX_DENSITY, unit, Localizer.instance().langStr("tesla.name"),
                    Localizer.instance().langStr("tesla.symbol"), Localizer.instance().langStr("tesla.desc"), self.getUOM(Unit.WEBER),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.HENRY):
            # inductance (henry)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_INDUCTANCE, unit, Localizer.instance().langStr("henry.name"),
                    Localizer.instance().langStr("henry.symbol"), Localizer.instance().langStr("henry.desc"), self.getUOM(Unit.WEBER),
                    self.getUOM(Unit.AMPERE))

        elif (unit == Unit.SIEMENS):
            # electrical conductance (siemens)
            uom = self.createQuotientUOM(UnitType.ELECTRIC_CONDUCTANCE, unit, Localizer.instance().langStr("siemens.name"),
                    Localizer.instance().langStr("siemens.symbol"), Localizer.instance().langStr("siemens.desc"), self.getUOM(Unit.AMPERE),
                    self.getUOM(Unit.VOLT))

        elif (unit == Unit.LUMEN):
            # luminous flux (lumen)
            uom = self.createProductUOM(UnitType.LUMINOUS_FLUX, unit, Localizer.instance().langStr("lumen.name"),
                    Localizer.instance().langStr("lumen.symbol"), Localizer.instance().langStr("lumen.desc"), self.getUOM(Unit.CANDELA),
                    self.getUOM(Unit.STERADIAN))

        elif (unit == Unit.LUX):
            # illuminance (lux)
            uom = self.createQuotientUOM(UnitType.ILLUMINANCE, unit, Localizer.instance().langStr("lux.name"),
                    Localizer.instance().langStr("lux.symbol"), Localizer.instance().langStr("lux.desc"), self.getUOM(Unit.LUMEN),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.BECQUEREL):
            # radioactivity (becquerel). Same definition as Hertz 1/s)
            uom = self.createQuotientUOM(UnitType.RADIOACTIVITY, unit, Localizer.instance().langStr("becquerel.name"),
                    Localizer.instance().langStr("becquerel.symbol"), Localizer.instance().langStr("becquerel.desc"), self.getOne(), self.getSecond())

        elif (unit == Unit.GRAY):
            # gray (Gy)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_ABSORBED, unit, Localizer.instance().langStr("gray.name"),
                    Localizer.instance().langStr("gray.symbol"), Localizer.instance().langStr("gray.desc"), self.getUOM(Unit.JOULE),
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERT):
            # sievert (Sv)
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_EFFECTIVE, unit, Localizer.instance().langStr("sievert.name"),
                    Localizer.instance().langStr("sievert.symbol"), Localizer.instance().langStr("sievert.desc"), self.getUOM(Unit.JOULE),
                    self.getUOM(Unit.KILOGRAM))

        elif (unit == Unit.SIEVERTS_PER_HOUR):
            uom = self.createQuotientUOM(UnitType.RADIATION_DOSE_RATE, unit, Localizer.instance().langStr("sph.name"),
                    Localizer.instance().langStr("sph.symbol"), Localizer.instance().langStr("sph.desc"), self.getUOM(Unit.SIEVERT), self.getHour())

        elif (unit == Unit.KATAL):
            # katal (kat)
            uom = self.createQuotientUOM(UnitType.CATALYTIC_ACTIVITY, unit, Localizer.instance().langStr("katal.name"),
                    Localizer.instance().langStr("katal.symbol"), Localizer.instance().langStr("katal.desc"), self.getUOM(Unit.MOLE), self.getSecond())

        elif (unit == Unit.UNIT):
            # Unit (U)
            uom = self.createScalarUOM(UnitType.CATALYTIC_ACTIVITY, unit, Localizer.instance().langStr("unit.name"),
                    Localizer.instance().langStr("unit.symbol"), Localizer.instance().langStr("unit.desc"))
            uom.setConversion(1.0E-06 / 60.0, self.getUOM(Unit.KATAL))

        elif (unit == Unit.INTERNATIONAL_UNIT):
            uom = self.createScalarUOM(UnitType.SUBSTANCE_AMOUNT, unit, Localizer.instance().langStr("iu.name"),
                    Localizer.instance().langStr("iu.symbol"), Localizer.instance().langStr("iu.desc"))

        elif (unit == Unit.ANGSTROM):
            # length
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("angstrom.name"),
                    Localizer.instance().langStr("angstrom.symbol"), Localizer.instance().langStr("angstrom.desc"))
            uom.setConversion(0.1, self.getUOM(Prefix.nano(), self.getUOM(Unit.METRE)))

        elif (unit == Unit.BIT):
            # computer bit
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, unit, Localizer.instance().langStr("bit.name"),
                    Localizer.instance().langStr("bit.symbol"), Localizer.instance().langStr("bit.desc"))

        elif (unit == Unit.BYTE):
            # computer byte
            uom = self.createScalarUOM(UnitType.COMPUTER_SCIENCE, unit, Localizer.instance().langStr("byte.name"),
                    Localizer.instance().langStr("byte.symbol"), Localizer.instance().langStr("byte.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BIT))

        elif (unit == Unit.WATTS_PER_SQ_METRE):
            uom = self.createQuotientUOM(UnitType.IRRADIANCE, unit, Localizer.instance().langStr("wsm.name"),
                    Localizer.instance().langStr("wsm.symbol"), Localizer.instance().langStr("wsm.desc"), self.getUOM(Unit.WATT),
                    self.getUOM(Unit.SQUARE_METRE))

        elif (unit == Unit.PARSEC):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("parsec.name"),
                    Localizer.instance().langStr("parsec.symbol"), Localizer.instance().langStr("parsec.desc")) 
            uom.setConversion(3.08567758149137E+16, self.getUOM(Unit.METRE))

        elif (unit == Unit.ASTRONOMICAL_UNIT):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("au.name"),
                    Localizer.instance().langStr("au.symbol"), Localizer.instance().langStr("au.desc"))
            uom.setConversion(1.49597870700E+11, self.getUOM(Unit.METRE))
        
        return uom

    def createCustomaryUnit(self, unit):
        uom = None
        
        if (unit == Unit.RANKINE): 
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit,
                Localizer.instance().langStr("rankine.name"), Localizer.instance().langStr("rankine.symbol"), Localizer.instance().langStr("rankine.desc"))
                
            # create bridge to SI
            uom.setBridgeConversion(5.0 / 9.0, self.getUOM(Unit.KELVIN), 0.0)
                
        elif (unit == Unit.FAHRENHEIT):
            uom = self.createScalarUOM(UnitType.TEMPERATURE, unit, Localizer.instance().langStr("fahrenheit.name"),
                Localizer.instance().langStr("fahrenheit.symbol"), Localizer.instance().langStr("fahrenheit.desc"))
            uom.setConversion(1.0, self.getUOM(Unit.RANKINE), 459.67)
                
        elif (unit == Unit.POUND_MASS):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("lbm.name"),
                Localizer.instance().langStr("lbm.symbol"), Localizer.instance().langStr("lbm.desc"))
    
            # create bridge to SI
            uom.setBridgeConversion(0.45359237, self.getUOM(Unit.KILOGRAM), 0.0)  
        
        elif (unit == Unit.OUNCE):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("ounce.name"),
                Localizer.instance().langStr("ounce.symbol"), Localizer.instance().langStr("ounce.desc"))
            uom.setConversion(0.0625, self.getUOM(Unit.POUND_MASS))
                
        elif (unit == Unit.TROY_OUNCE):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("troy_oz.name"),
                Localizer.instance().langStr("troy_oz.symbol"), Localizer.instance().langStr("troy_oz.desc"))
            uom.setConversion(31.1034768, self.getUOM(Unit.GRAM))
            
        elif (unit == Unit.SLUG):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("slug.name"),
                Localizer.instance().langStr("slug.symbol"), Localizer.instance().langStr("slug.desc"))
            g = self.getQuantity(Constant.GRAVITY).convert(self.getUOM(Unit.FEET_PER_SEC_SQUARED))
            uom.setConversion(g.getAmount(), self.getUOM(Unit.POUND_MASS))
                
        elif (unit == Unit.FOOT):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("foot.name"),
                Localizer.instance().langStr("foot.symbol"), Localizer.instance().langStr("foot.desc"))
    
            # bridge to SI
            uom.setBridgeConversion(0.3048, self.getUOM(Unit.METRE), 0.0)
    
        elif (unit == Unit.INCH):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("inch.name"),
                Localizer.instance().langStr("inch.symbol"), Localizer.instance().langStr("inch.desc"))
            uom.setConversion(1.0 / 12.0, self.getUOM(Unit.FOOT))
                
        elif (unit == Unit.MIL):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("mil.name"), Localizer.instance().langStr("mil.symbol"),
                Localizer.instance().langStr("mil.desc"))
            uom.setConversion(Prefix.milli().getFactor(), self.getUOM(Unit.INCH))
                
        elif (unit == Unit.POINT):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("point.name"),
                Localizer.instance().langStr("point.symbol"), Localizer.instance().langStr("point.desc"))
            uom.setConversion(1.0 / 72.0, self.getUOM(Unit.INCH))
            
        elif (unit == Unit.YARD):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("yard.name"),
                Localizer.instance().langStr("yard.symbol"), Localizer.instance().langStr("yard.desc"))
            uom.setConversion(3.0, self.getUOM(Unit.FOOT))
                
        elif (unit == Unit.MILE):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("mile.name"),
                Localizer.instance().langStr("mile.symbol"), Localizer.instance().langStr("mile.desc"))
            uom.setConversion(5280.0, self.getUOM(Unit.FOOT))
                
        elif (unit == Unit.NAUTICAL_MILE):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("NM.name"),
                Localizer.instance().langStr("NM.symbol"), Localizer.instance().langStr("NM.desc"))
            uom.setConversion(6080.0, self.getUOM(Unit.FOOT))
                
        elif (unit == Unit.FATHOM):
            uom = self.createScalarUOM(UnitType.LENGTH, unit, Localizer.instance().langStr("fth.name"),
                Localizer.instance().langStr("fth.symbol"), Localizer.instance().langStr("fth.desc"))
            uom.setConversion(6.0, self.getUOM(Unit.FOOT))
    
        elif (unit == Unit.PSI):
            uom = self.createQuotientUOM(UnitType.PRESSURE, unit, Localizer.instance().langStr("psi.name"),
                Localizer.instance().langStr("psi.symbol"), Localizer.instance().langStr("psi.desc"), self.getUOM(Unit.POUND_FORCE),
                self.getUOM(Unit.SQUARE_INCH))
            
        elif (unit == Unit.IN_HG):
            uom = self.createScalarUOM(UnitType.PRESSURE, unit, Localizer.instance().langStr("inhg.name"),
                Localizer.instance().langStr("inhg.symbol"), Localizer.instance().langStr("inhg.desc"))
            uom.setConversion(0.4911531047, self.getUOM(Unit.PSI)) 
    
        elif (unit == Unit.SQUARE_INCH):
            uom = self.createPowerUOM(UnitType.AREA, unit, Localizer.instance().langStr("in2.name"),
                Localizer.instance().langStr("in2.symbol"), Localizer.instance().langStr("in2.desc"), self.getUOM(Unit.INCH), 2)
            uom.setConversion(1.0 / 144.0, self.getUOM(Unit.SQUARE_FOOT))
                
        elif (unit == Unit.SQUARE_FOOT):
            uom = self.createPowerUOM(UnitType.AREA, unit, Localizer.instance().langStr("ft2.name"),
                Localizer.instance().langStr("ft2.symbol"), Localizer.instance().langStr("ft2.desc"), self.getUOM(Unit.FOOT), 2)
                
        elif (unit == Unit.SQUARE_YARD):
            uom = self.createPowerUOM(UnitType.AREA, unit, Localizer.instance().langStr("yd2.name"),
                Localizer.instance().langStr("yd2.symbol"), Localizer.instance().langStr("yd2.desc"), self.getUOM(Unit.YARD), 2)    
                
        elif (unit == Unit.SQUARE_FOOT):
            uom = self.createScalarUOM(UnitType.AREA, unit, Localizer.instance().langStr("acre.name"),
                Localizer.instance().langStr("acre.symbol"), Localizer.instance().langStr("acre.desc"))
            uom.setConversion(43560.0, self.getUOM(Unit.SQUARE_FOOT))
                
        elif (unit == Unit.CUBIC_INCH):
            uom = self.createPowerUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("in3.name"),
                Localizer.instance().langStr("in3.symbol"), Localizer.instance().langStr("in3.desc"), self.getUOM(Unit.INCH), 3)
            uom.setConversion(1.0 / 1728.0, self.getUOM(Unit.CUBIC_FOOT))
            
        elif (unit == Unit.CUBIC_FOOT):
            uom = self.createPowerUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("ft3.name"),
                Localizer.instance().langStr("ft3.symbol"), Localizer.instance().langStr("ft3.desc"), self.getUOM(Unit.FOOT), 3)
                
        elif (unit == Unit.CUBIC_FEET_PER_SEC):
            uom = self.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, unit,
                Localizer.instance().langStr("ft3PerSec.name"), Localizer.instance().langStr("ft3PerSec.symbol"),
                Localizer.instance().langStr("ft3PerSec.desc"), self.getUOM(Unit.CUBIC_FOOT), self.getSecond())
            
        elif (unit == Unit.CORD):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("cord.name"),
                Localizer.instance().langStr("cord.symbol"), Localizer.instance().langStr("cord.desc"))
            uom.setConversion(128.0, self.getUOM(Unit.CUBIC_FOOT))
                
        elif (unit == Unit.CUBIC_YARD):
            uom = self.createPowerUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("yd3.name"),
                Localizer.instance().langStr("yd3.symbol"), Localizer.instance().langStr("yd3.desc"), self.getUOM(Unit.YARD), 3)
                
        elif (unit == Unit.FEET_PER_SEC):
            uom = self.createQuotientUOM(UnitType.VELOCITY, unit, Localizer.instance().langStr("fps.name"),
                Localizer.instance().langStr("fps.symbol"), Localizer.instance().langStr("fps.desc"), self.getUOM(Unit.FOOT), self.getSecond())
                
        elif (unit == Unit.KNOT):
            uom = self.createScalarUOM(UnitType.VELOCITY, unit, Localizer.instance().langStr("knot.name"),
                Localizer.instance().langStr("knot.symbol"), Localizer.instance().langStr("knot.desc"))
            uom.setConversion(6080.0 / 3600.0, self.getUOM(Unit.FEET_PER_SEC))
                
        elif (unit == Unit.FEET_PER_SEC_SQUARED):
            uom = self.createQuotientUOM(UnitType.ACCELERATION, Unit.FEET_PER_SEC_SQUARED, Localizer.instance().langStr("ftps2.name"),
                    Localizer.instance().langStr("ftps2.symbol"), Localizer.instance().langStr("ftps2.desc"), self.getUOM(Unit.FOOT),
                    self.getUOM(Unit.SQUARE_SECOND))
    
        elif (unit == Unit.HP):
            uom = self.createProductUOM(UnitType.POWER, unit, Localizer.instance().langStr("hp.name"), Localizer.instance().langStr("hp.symbol"),
                Localizer.instance().langStr("hp.desc"), self.getUOM(Unit.POUND_FORCE), self.getUOM(Unit.FEET_PER_SEC))
            uom.setScalingFactor(550.0)
            
        elif (unit == Unit.BTU):
            uom = self.createScalarUOM(UnitType.ENERGY, Unit.BTU, Localizer.instance().langStr("btu.name"), Localizer.instance().langStr("btu.symbol"),
                Localizer.instance().langStr("btu.desc"))
            uom.setConversion(778.1692622659652, self.getUOM(Unit.FOOT_POUND_FORCE))          
    
        elif (unit == Unit.FOOT_POUND_FORCE):
            uom = self.createProductUOM(UnitType.ENERGY, unit, Localizer.instance().langStr("ft_lbf.name"),
                Localizer.instance().langStr("ft_lbf.symbol"), Localizer.instance().langStr("ft_lbf.desc"), self.getUOM(Unit.FOOT),
                self.getUOM(Unit.POUND_FORCE))
            
        elif (unit == Unit.POUND_FORCE):
            uom = self.createProductUOM(UnitType.FORCE, unit, Localizer.instance().langStr("lbf.name"),
                Localizer.instance().langStr("lbf.symbol"), Localizer.instance().langStr("lbf.desc"), self.getUOM(Unit.POUND_MASS),
                self.getUOM(Unit.FEET_PER_SEC_SQUARED))
    
            # factor is acceleration of gravity
            gravity = self.getQuantity(Constant.GRAVITY).convert(self.getUOM(Unit.FEET_PER_SEC_SQUARED))
            uom.setScalingFactor(gravity.getAmount())
                
        elif (unit == Unit.GRAIN):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("grain.name"),
                Localizer.instance().langStr("grain.symbol"), Localizer.instance().langStr("grain.desc"))
            uom.setConversion(1.0 / 7000.0, self.getUOM(Unit.POUND_MASS))
                
        elif (unit == Unit.MILES_PER_HOUR):
            uom = self.createScalarUOM(UnitType.VELOCITY, unit, Localizer.instance().langStr("mph.name"),
                    Localizer.instance().langStr("mph.symbol"), Localizer.instance().langStr("mph.desc"))
            uom.setConversion(5280.0 / 3600.0, self.getUOM(Unit.FEET_PER_SEC))
                
        elif (unit == Unit.REV_PER_MIN):
            return self.createQuotientUOM(UnitType.FREQUENCY, unit, Localizer.instance().langStr("rpm.name"),
                Localizer.instance().langStr("rpm.symbol"), Localizer.instance().langStr("rpm.desc"), self.getOne(), self.getMinute())       
            
        return uom   

    def createUSUnit(self, unit):
        uom = None
        
        if (unit == Unit.US_GALLON):
            uom = self.createScalarUOM(UnitType.VOLUME, unit,
                Localizer.instance().langStr("us_gallon.name"), Localizer.instance().langStr("us_gallon.symbol"), Localizer.instance().langStr("us_gallon.desc"))
            uom.setConversion(231.0, self.getUOM(Unit.CUBIC_INCH), 0.0)
        
        elif (unit == Unit.US_BARREL):        
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_bbl.name"),
                    Localizer.instance().langStr("us_bbl.symbol"), Localizer.instance().langStr("us_bbl.desc"))
            uom.setConversion(42.0, self.getUOM(Unit.US_GALLON))
        
        elif (unit == Unit.US_BUSHEL):        
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_bu.name"),
                    Localizer.instance().langStr("us_bu.symbol"), Localizer.instance().langStr("us_bu.desc"))
            uom.setConversion(2150.42058, self.getUOM(Unit.CUBIC_INCH))   
    
        elif (unit == Unit.US_FLUID_OUNCE):        
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_fl_oz.name"),
                    Localizer.instance().langStr("us_fl_oz.symbol"), Localizer.instance().langStr("us_fl_oz.desc"))
            uom.setConversion(0.0078125, self.getUOM(Unit.US_GALLON))
           
        elif (unit == Unit.US_CUP):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_cup.name"),
                    Localizer.instance().langStr("us_cup.symbol"), Localizer.instance().langStr("us_cup.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.US_FLUID_OUNCE))
    
        elif (unit == Unit.US_PINT):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_pint.name"),
                    Localizer.instance().langStr("us_pint.symbol"), Localizer.instance().langStr("us_pint.desc"))
            uom.setConversion(16.0, self.getUOM(Unit.US_FLUID_OUNCE))
    
        elif (unit == Unit.US_QUART):        
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_quart.name"),
                    Localizer.instance().langStr("us_quart.symbol"), Localizer.instance().langStr("us_quart.desc"))
            uom.setConversion(32.0, self.getUOM(Unit.US_FLUID_OUNCE))
        
        elif (unit == Unit.US_TABLESPOON):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("us_tbsp.name"),
                    Localizer.instance().langStr("us_tbsp.symbol"), Localizer.instance().langStr("us_tbsp.desc"))
            uom.setConversion(0.5, self.getUOM(Unit.US_FLUID_OUNCE))
        
        elif (unit == Unit.US_TEASPOON):        
            uom = self.createScalarUOM(UnitType.VOLUME, Unit.US_TEASPOON, Localizer.instance().langStr("us_tsp.name"),
                    Localizer.instance().langStr("us_tsp.symbol"), Localizer.instance().langStr("us_tsp.desc"))
            uom.setConversion(1.0 / 6.0, self.getUOM(Unit.US_FLUID_OUNCE))       
        
        elif (unit == Unit.US_TON):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("us_ton.name"),
                Localizer.instance().langStr("us_ton.symbol"), Localizer.instance().langStr("us_ton.desc"))
            uom.setConversion(2000.0, self.getUOM(Unit.POUND_MASS)) 
               
        return uom
    
    def createBRUnit(self, unit):
        uom = None
        
        if (unit == Unit.BR_GALLON):
            uom = self.createScalarUOM(UnitType.VOLUME, unit,
                    Localizer.instance().langStr("br_gallon.name"), Localizer.instance().langStr("br_gallon.symbol"), Localizer.instance().langStr("br_gallon.desc"))
            uom.setConversion(277.4194327916215, self.getUOM(Unit.CUBIC_INCH), 0.0) 
    
        elif (unit == Unit.BR_BUSHEL):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_bu.name"),
                Localizer.instance().langStr("br_bu.symbol"), Localizer.instance().langStr("br_bu.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BR_GALLON))
        
        elif (unit == Unit.BR_FLUID_OUNCE):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_fl_oz.name"),
                Localizer.instance().langStr("br_fl_oz.symbol"), Localizer.instance().langStr("br_fl_oz.desc"))
            uom.setConversion(0.00625, self.getUOM(Unit.BR_GALLON))
        
        elif (unit == Unit.BR_CUP):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_cup.name"),
                Localizer.instance().langStr("br_cup.symbol"), Localizer.instance().langStr("br_cup.desc"))
            uom.setConversion(8.0, self.getUOM(Unit.BR_FLUID_OUNCE))
        
        elif (unit == Unit.BR_PINT):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_pint.name"),
                Localizer.instance().langStr("br_pint.symbol"), Localizer.instance().langStr("br_pint.desc"))
            uom.setConversion(20.0, self.getUOM(Unit.BR_FLUID_OUNCE))
    
        elif (unit == Unit.BR_QUART):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_quart.name"),
                Localizer.instance().langStr("br_quart.symbol"), Localizer.instance().langStr("br_quart.desc"))
            uom.setConversion(40.0, self.getUOM(Unit.BR_FLUID_OUNCE))
        
        elif (unit == Unit.BR_TABLESPOON):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_tbsp.name"),
               Localizer.instance().langStr("br_tbsp.symbol"), Localizer.instance().langStr("br_tbsp.desc"))
            uom.setConversion(0.625, self.getUOM(Unit.BR_FLUID_OUNCE))  

        elif (unit == Unit.BR_TEASPOON):
            uom = self.createScalarUOM(UnitType.VOLUME, unit, Localizer.instance().langStr("br_tsp.name"),
                Localizer.instance().langStr("br_tsp.symbol"), Localizer.instance().langStr("br_tsp.desc"))
            uom.setConversion(5.0 / 24.0, self.getUOM(Unit.BR_FLUID_OUNCE))
        
        elif (unit == Unit.BR_TON):
            uom = self.createScalarUOM(UnitType.MASS, unit, Localizer.instance().langStr("br_ton.name"),
                Localizer.instance().langStr("br_ton.symbol"), Localizer.instance().langStr("br_ton.desc"))
            uom.setConversion(2240.0, self.getUOM(Unit.POUND_MASS))    
                
        return uom     
    
    def createFinancialUnit(self, unit):
        uom = None 
        
        if (unit == Unit.US_DOLLAR):
            uom = self.createScalarUOM(UnitType.CURRENCY, unit,
            Localizer.instance().langStr("us_dollar.name"), Localizer.instance().langStr("us_dollar.symbol"), Localizer.instance().langStr("us_dollar.desc"))
        
        elif (unit == Unit.EURO):
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, Localizer.instance().langStr("euro.name"),
            Localizer.instance().langStr("euro.symbol"), Localizer.instance().langStr("euro.desc"))
        
        elif (unit == Unit.YUAN):
            uom = self.createScalarUOM(UnitType.CURRENCY, unit, Localizer.instance().langStr("yuan.name"),
            Localizer.instance().langStr("yuan.symbol"), Localizer.instance().langStr("yuan.desc"))
    
        return uom
    
    def createUOMForUnit(self, unit):
        # SI
        uom = self.createBaseSIUnit(unit)

        if (uom is not None):
            return uom
                
        # SI other
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

        # currency
        uom = self.createFinancialUnit(unit)

        return uom
    
    def getQuantity(self, constant: Constant):
        named = None

        if (constant == Constant.LIGHT_VELOCITY):
            named = Quantity(299792458.0, self.getUOM(Unit.METRE_PER_SEC))
            named.name = Localizer.instance().langStr("light.name")
            named.symbol = Localizer.instance().langStr("light.symbol")
            named.description = Localizer.instance().langStr("light.desc")
            
        elif (constant == Constant.LIGHT_YEAR):
            year = Quantity(1.0, self.getUOM(Unit.JULIAN_YEAR))
            named = self.getQuantity(Constant.LIGHT_VELOCITY).multiply(year)
            named.name = Localizer.instance().langStr("ly.name")
            named.symbol = Localizer.instance().langStr("ly.symbol")
            named.description = Localizer.instance().langStr("ly.desc")
            
        elif (constant == Constant.GRAVITY):
            named = Quantity(9.80665, self.getUOM(Unit.METRE_PER_SEC_SQUARED))
            named.name = Localizer.instance().langStr("gravity.name")
            named.symbol = Localizer.instance().langStr("gravity.symbol")
            named.description = Localizer.instance().langStr("gravity.desc")
            
        elif (constant == Constant.PLANCK_CONSTANT):
            js = self.createProductUOM(self.getUOM(Unit.JOULE), self.getSecond())
            named = Quantity(6.62607015E-34, js)
            named.name = Localizer.instance().langStr("planck.name")
            named.symbol = Localizer.instance().langStr("planck.symbol")
            named.description = Localizer.instance().langStr("planck.desc")
            
        elif (constant == Constant.BOLTZMANN_CONSTANT):
            jk = self.createQuotientUOM(self.getUOM(Unit.JOULE), self.getUOM(Unit.KELVIN))
            named = Quantity(1.380649E-23, jk)
            named.name = Localizer.instance().langStr("boltzmann.name")
            named.symbol = Localizer.instance().langStr("boltzmann.symbol")
            named.description = Localizer.instance().langStr("boltzmann.desc")    

        elif (constant == Constant.AVAGADRO_CONSTANT):
            # NA
            named = Quantity(6.02214076E+23, self.getOne())
            named.name = Localizer.instance().langStr("avo.name")
            named.symbol = Localizer.instance().langStr("avo.symbol")
            named.description = Localizer.instance().langStr("avo.desc")
            
        elif (constant == Constant.GAS_CONSTANT):
            # R
            named = self.getQuantity(Constant.BOLTZMANN_CONSTANT).multiply(self.getQuantity(Constant.AVAGADRO_CONSTANT))
            named.name = Localizer.instance().langStr("gas.name")
            named.symbol = Localizer.instance().langStr("gas.symbol")
            named.description = Localizer.instance().langStr("gas.desc")
            
        elif (constant == Constant.ELEMENTARY_CHARGE):
            # e
            named = Quantity(1.602176634E-19, self.getUOM(Unit.COULOMB))
            named.name = Localizer.instance().langStr("e.name")
            named.symbol = Localizer.instance().langStr("e.symbol")
            named.description = Localizer.instance().langStr("e.desc")
            
        elif (constant == Constant.FARADAY_CONSTANT):
            # F = e.NA
            qe = self.getQuantity(Constant.ELEMENTARY_CHARGE)
            named = qe.multiply(self.getQuantity(Constant.AVAGADRO_CONSTANT))
            named.name = Localizer.instance().langStr("faraday.name")
            named.symbol = Localizer.instance().langStr("faraday.symbol")
            named.description = Localizer.instance().langStr("faraday.desc")
            
        elif (constant == Constant.ELECTRIC_PERMITTIVITY):
            # epsilon0 = 1/(mu0*c^2)
            vc = self.getQuantity(Constant.LIGHT_VELOCITY)
            named = self.getQuantity(Constant.MAGNETIC_PERMEABILITY).multiply(vc).multiply(vc).invert()
            named.name = Localizer.instance().langStr("eps0.name")
            named.symbol = Localizer.instance().langStr("eps0.symbol")
            named.description = Localizer.instance().langStr("eps0.desc")
            
        elif (constant == Constant.MAGNETIC_PERMEABILITY):
            # mu0
            hm = self.createQuotientUOM(self.getUOM(Unit.HENRY), self.getUOM(Unit.METRE))
            fourPi = 4.0 * math.pi * 1.0E-07
            named = Quantity(fourPi, hm)
            named.name = Localizer.instance().langStr("mu0.name")
            named.symbol = Localizer.instance().langStr("mu0.symbol")
            named.description = Localizer.instance().langStr("mu0.desc")
            
        elif (constant == Constant.ELECTRON_MASS):
            # me
            named = Quantity(9.1093835611E-28, self.getUOM(Unit.GRAM))
            named.name = Localizer.instance().langStr("me.name")
            named.symbol = Localizer.instance().langStr("me.symbol")
            named.description = Localizer.instance().langStr("me.desc")
            
        elif (constant == Constant.PROTON_MASS):
            # mp
            named = Quantity(1.67262189821E-24, self.getUOM(Unit.GRAM))
            named.name = Localizer.instance().langStr("mp.name")
            named.symbol = Localizer.instance().langStr("mp.symbol")
            named.description = Localizer.instance().langStr("mp.desc")
            
        elif (constant == Constant.STEFAN_BOLTZMANN):
            k4 = self.createPowerUOM(self.getUOM(Unit.KELVIN), 4)
            sb = self.createQuotientUOM(self.getUOM(Unit.WATTS_PER_SQ_METRE), k4)
            named = Quantity(5.67036713E-08, sb)
            named.name = Localizer.instance().langStr("sb.name")
            named.symbol = Localizer.instance().langStr("sb.symbol")
            named.description = Localizer.instance().langStr("sb.desc")
            
        elif (constant == Constant.HUBBLE_CONSTANT):
            kps = self.getUOM(Prefix.kilo(), self.getUOM(Unit.METRE_PER_SEC))
            mpc = self.getUOM(Prefix.mega(), self.getUOM(Unit.PARSEC))
            hubble = self.createQuotientUOM(kps, mpc)
            named = Quantity(71.9, hubble)
            named.name = Localizer.instance().langStr("hubble.name")
            named.symbol = Localizer.instance().langStr("hubble.symbol")
            named.description = Localizer.instance().langStr("hubble.desc")
                 
        elif (constant == Constant.CAESIUM_FREQUENCY):
            named = Quantity(9192631770.0, self.getUOM(Unit.HERTZ))
            named.name = Localizer.instance().langStr("caesium.name")
            named.symbol = Localizer.instance().langStr("caesium.symbol")
            named.description = Localizer.instance().langStr("caesium.desc")
                      
        elif (constant == Constant.LUMINOUS_EFFICACY):
            kcd = self.createQuotientUOM(self.getUOM(Unit.LUMEN), self.getUOM(Unit.WATT))
            named = Quantity(683.0, kcd)
            named.name = Localizer.instance().langStr("kcd.name")
            named.symbol = Localizer.instance().langStr("kcd.symbol")
            named.description = Localizer.instance().langStr("kcd.desc")

        return named
    
    def createPowerUOM(self, unitType, unit, name, symbol, description, base, exponent):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setPowerUnit(base, exponent)
        CacheManager.instance().registerUnit(uom)
        return uom
    
    def createUnclassifiedPowerUOM(self, base, exponent): 
        if (base is None):          
            msg = Localizer.instance().messageStr("base.cannot.be.null")
            raise Exception(msg)
    
        # create symbol
        symbol = UnitOfMeasure.generatePowerSymbol(base, exponent)
        return self.createPowerUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, base, exponent)
    
    def createProductUOM(self, unitType, unit, name, symbol, description, multiplier, multiplicand):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setProductUnits(multiplier, multiplicand)
        CacheManager.instance().registerUnit(uom)
        return uom
    
    def createUnclassifiedProductUOM(self, multiplier, multiplicand):
        if (multiplier is None):          
            msg = Localizer.instance().messageStr("multiplier.cannot.be.null")
            raise Exception(msg)
        
        if (multiplicand is None):          
            msg = Localizer.instance().messageStr("multiplicand.cannot.be.null")
            raise Exception(msg)
        
        symbol = UnitOfMeasure.generateProductSymbol(multiplier, multiplicand)
        return self.createProductUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, multiplier, multiplicand)
    
    def createUnclassifiedQuotientUOM(self, dividend, divisor):
        if (dividend is None):
            msg = Localizer.instance().messageStr("dividend.cannot.be.null")
            raise Exception(msg)
        
        if (divisor is None):
            msg = Localizer.instance().messageStr("divisor.cannot.be.null")
            raise Exception(msg)
        
        symbol = UnitOfMeasure.generateQuotientSymbol(dividend, divisor)
        return self.createQuotientUOM(UnitType.UNCLASSIFIED, None, None, symbol, None, dividend, divisor)
    
    def createQuotientUOM(self, unitType, unit, name, symbol, description, dividend, divisor):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        uom.setQuotientUnits(dividend, divisor)
        CacheManager.instance().registerUnit(uom)
        return uom

    def createUOM(self, unitType, unit, name, symbol, description):
        if (symbol is None or len(symbol) == 0):
            msg = Localizer.instance().messageStr("symbol.cannot.be.null")
            raise Exception(msg)
        
        if (unitType is None):
            msg = Localizer.instance().messageStr("unit.type.cannot.be.null")
            raise Exception(msg)
        
        uom = CacheManager.instance().getUOMBySymbol(symbol)
        
        if (uom is None):
            # create a new one
            uom = UnitOfMeasure(unitType, name, symbol, description)
            
            uom.abscissaUnit = uom
            uom.unit = unit
            
        return uom
    
    def getSecond(self):
        return self.getUOM(Unit.SECOND)
    
    def getMinute(self):
        return self.getUOM(Unit.MINUTE)
    
    def getHour(self):
        return self.getUOM(Unit.HOUR)
    
    def getRegisteredUnits(self):
        units = CacheManager.instance().getCachedUnits()
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
        return CacheManager.instance().getUOMBySymbol(symbol)
            
    def getUOMForUnit(self, prefix, unit):
        return self.getUOMWithPrefix(prefix, MeasurementSystem.instance().getUOM(unit))
    
    def getUOMWithPrefix(self, prefix, targetUOM):
        symbol = prefix.symbol + targetUOM.symbol
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
