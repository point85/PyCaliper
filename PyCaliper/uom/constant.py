from enum import Enum, auto

class Constant(Enum):
    """
    This enumeration contains the values for fundamental constants commonly used
         in science, technology, engineering and math.
    """
    
    LIGHT_VELOCITY = auto()
    LIGHT_YEAR = auto() 
    GRAVITY = auto() 
    PLANCK_CONSTANT = auto() 
    BOLTZMANN_CONSTANT = auto() 
    AVAGADRO_CONSTANT = auto() 
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