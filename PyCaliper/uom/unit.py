from enum import Enum, auto


class Unit(Enum):
    """
    Unit is an enumeration of common units of measure in the International
    Customary = auto() SI = auto() US and British Imperial systems.
    """
    
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
