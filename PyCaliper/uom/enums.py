from enum import Enum, auto

##
# An enumeration of the basic types of units of measure
#
class MeasurementType(Enum):
    SCALAR = auto() 
    PRODUCT = auto() 
    QUOTIENT = auto() 
    POWER = auto()
    
##
# This enumeration contains the values for fundamental constants commonly used in science, technology, engineering and math.
#   
class Constant(Enum):
    LIGHT_VELOCITY = auto()
    LIGHT_YEAR = auto() 
    GRAVITY = auto() 
    PLANCK_CONSTANT = auto() 
    BOLTZMANN_CONSTANT = auto() 
    AVOGADRO_CONSTANT = auto() 
    GAS_CONSTANT = auto() 
    ELEMENTARY_CHARGE = auto() 
    ELECTRIC_PERMITTIVITY = auto() 
    MAGNETIC_PERMEABILITY = auto() 
    FARADAY_CONSTANT = auto() 
    ELECTRON_MASS = auto() 
    PROTON_MASS = auto() 
    STEFAN_BOLTZMANN = auto() 
    HUBBLE_CONSTANT = auto() 
    CAESIUM_FREQUENCY = auto() 
    LUMINOUS_EFFICACY = auto() 
    
    def __str__(self):
        return self.name + ", " + str(self.value)

##
# An enumeration of the types of units of measure
#
class UnitType(Enum):
    # dimension-less "1"
    UNITY = auto()

    # fundamental
    LENGTH = auto() 
    MASS = auto() 
    TIME = auto() 
    ELECTRIC_CURRENT = auto() 
    TEMPERATURE = auto() 
    SUBSTANCE_AMOUNT = auto() 
    LUMINOSITY = auto()

    # other physical
    AREA = auto() 
    VOLUME = auto() 
    DENSITY = auto() 
    VELOCITY = auto() 
    VOLUMETRIC_FLOW = auto() 
    MASS_FLOW = auto() 
    FREQUENCY = auto() 
    ACCELERATION = auto() 
    FORCE = auto() 
    PRESSURE = auto() 
    ENERGY = auto() 
    POWER = auto() 
    ELECTRIC_CHARGE = auto()
    ELECTROMOTIVE_FORCE = auto() 
    ELECTRIC_RESISTANCE = auto() 
    ELECTRIC_CAPACITANCE = auto() 
    ELECTRIC_PERMITTIVITY = auto() 
    ELECTRIC_FIELD_STRENGTH = auto()
    MAGNETIC_FLUX = auto() 
    MAGNETIC_FLUX_DENSITY = auto() 
    ELECTRIC_INDUCTANCE = auto() 
    ELECTRIC_CONDUCTANCE = auto()
    LUMINOUS_FLUX = auto() 
    ILLUMINANCE = auto() 
    RADIATION_DOSE_ABSORBED = auto() 
    RADIATION_DOSE_EFFECTIVE = auto() 
    RADIATION_DOSE_RATE = auto() 
    RADIOACTIVITY = auto() 
    CATALYTIC_ACTIVITY = auto() 
    DYNAMIC_VISCOSITY = auto()
    KINEMATIC_VISCOSITY = auto() 
    RECIPROCAL_LENGTH = auto() 
    PLANE_ANGLE = auto() 
    SOLID_ANGLE = auto() 
    INTENSITY = auto() 
    COMPUTER_SCIENCE = auto() 
    TIME_SQUARED = auto() 
    MOLAR_CONCENTRATION = auto() 
    IRRADIANCE = auto()

    # currency
    CURRENCY = auto()

    # unclassified.  Reserved for use when creating custom units of measure.
    UNCLASSIFIED = auto()

##
# Unit is an enumeration of common units of measure in the International,
# Customary, SI, US and British Imperial systems.
#
class Unit(Enum):
    # dimension-less "1" or unity
    ONE = auto() 
    PERCENT = auto()
    # time
    SECOND = auto() 
    MINUTE = auto() 
    HOUR = auto() 
    DAY = auto() 
    WEEK = auto() 
    JULIAN_YEAR = auto() 
    SQUARE_SECOND = auto()
    # substance amount
    MOLE = auto() 
    EQUIVALENT = auto() 
    INTERNATIONAL_UNIT = auto()
    # angle
    RADIAN = auto() 
    STERADIAN = auto()
    # degree of arc
    DEGREE = auto() 
    ARC_SECOND = auto()
    # ratio
    DECIBEL = auto()
    # SI units follow
    # length
    METRE = auto() 
    ANGSTROM = auto() 
    DIOPTER = auto() 
    PARSEC = auto() 
    ASTRONOMICAL_UNIT = auto()
    # area
    SQUARE_METRE = auto() 
    HECTARE = auto()
    # temperature
    KELVIN = auto() 
    CELSIUS = auto()
    # mass
    GRAM = auto() 
    KILOGRAM = auto() 
    CARAT = auto() 
    TONNE = auto()
    # volume
    CUBIC_METRE = auto() 
    LITRE = auto()
    # volumetric flow
    CUBIC_METRE_PER_SEC = auto() 
    CUBIC_FEET_PER_SEC = auto()
    # mass flow
    KILOGRAM_PER_SEC = auto()
    # viscosity
    PASCAL_SECOND = auto() 
    SQUARE_METRE_PER_SEC = auto()
    # velocity
    METRE_PER_SEC = auto()
    # acceleration
    METRE_PER_SEC_SQUARED = auto()
    # energy
    JOULE = auto() 
    ELECTRON_VOLT = auto() 
    CALORIE = auto() 
    WATT_HOUR = auto()
    # force
    NEWTON = auto()
    # power
    WATT = auto() 
    WATTS_PER_SQ_METRE = auto()
    # frequency
    HERTZ = auto() 
    RAD_PER_SEC = auto()
    # pressure
    PASCAL = auto() 
    BAR = auto() 
    ATMOSPHERE = auto()
    # electrical
    AMPERE = auto() 
    AMPERE_PER_METRE = auto() 
    COULOMB = auto() 
    VOLT = auto() 
    OHM = auto() 
    FARAD = auto() 
    FARAD_PER_METRE = auto() 
    WEBER = auto() 
    TESLA = auto() 
    HENRY = auto() 
    SIEMENS = auto()
    # molar concentration
    MOLARITY = auto()
    # luminosity
    CANDELA = auto() 
    LUMEN = auto() 
    LUX = auto()
    # radioactivity
    BECQUEREL = auto() 
    GRAY = auto() 
    SIEVERT = auto() 
    SIEVERTS_PER_HOUR = auto()
    # catalytic activity
    KATAL = auto() 
    UNIT = auto()
    # density
    KILOGRAM_PER_CU_METRE = auto()
    # torque (moment of force and energy)
    NEWTON_METRE = auto()
    # IT
    BIT = auto() 
    BYTE = auto()
    # Customary Units follow
    # length
    INCH = auto() 
    FOOT = auto() 
    YARD = auto() 
    MILE = auto() 
    NAUTICAL_MILE = auto() 
    FATHOM = auto() 
    MIL = auto() 
    POINT = auto()
    # temperature
    FAHRENHEIT = auto() 
    RANKINE = auto()
    # mass
    POUND_MASS = auto() 
    OUNCE = auto() 
    SLUG = auto() 
    GRAIN = auto() 
    TROY_OUNCE = auto()
    # force
    POUND_FORCE = auto()
    # torque (moment of force)
    FOOT_POUND_FORCE = auto()
    # area
    SQUARE_INCH = auto() 
    SQUARE_FOOT = auto() 
    SQUARE_YARD = auto() 
    ACRE = auto()
    # volume
    CUBIC_INCH = auto() 
    CUBIC_FOOT = auto() 
    CUBIC_YARD = auto() 
    CORD = auto()
    # velocity
    FEET_PER_SEC = auto() 
    KNOT = auto() 
    MILES_PER_HOUR = auto()
    # frequency
    REV_PER_MIN = auto()
    # acceleration
    FEET_PER_SEC_SQUARED = auto()
    # power
    HP = auto()
    # energy
    BTU = auto()
    # pressure
    PSI = auto() 
    IN_HG = auto()
    # US Units follow
    # volume
    US_TEASPOON = auto() 
    US_TABLESPOON = auto() 
    US_FLUID_OUNCE = auto() 
    US_CUP = auto() 
    US_PINT = auto() 
    US_QUART = auto() 
    US_GALLON = auto() 
    US_BARREL = auto() 
    US_BUSHEL = auto()
    # mass
    US_TON = auto()
    # British units follow
    # volume
    BR_TEASPOON = auto() 
    BR_TABLESPOON = auto() 
    BR_FLUID_OUNCE = auto() 
    BR_CUP = auto() 
    BR_PINT = auto() 
    BR_QUART = auto() 
    BR_GALLON = auto() 
    BR_BUSHEL = auto()
    # mass
    BR_TON = auto()
    # currency
    US_DOLLAR = auto() 
    EURO = auto() 
    YUAN = auto()
