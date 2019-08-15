from enum import Enum, auto

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

