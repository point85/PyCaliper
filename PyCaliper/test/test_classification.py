import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.cache_manager import CacheManager

class TestClassification(unittest.TestCase):    
    def testClassifications(self):
        msys = MeasurementSystem.instance()
        
        one = msys.getOne()
        s = msys.getSecond()
        m = msys.getUOM(Unit.METRE)
        kg = msys.getUOM(Unit.KILOGRAM)
        degC = msys.getUOM(Unit.CELSIUS)
        amp = msys.getUOM(Unit.AMPERE)
        mol = msys.getUOM(Unit.MOLE)
        cd = msys.getUOM(Unit.CANDELA)
        ft = msys.getUOM(Unit.FOOT)
        
        # base types
        self.assertTrue(one.classify().unitType == UnitType.UNITY)
        self.assertTrue(s.classify().unitType == UnitType.TIME)
        self.assertTrue(m.classify().unitType == UnitType.LENGTH)
        self.assertTrue(kg.classify().unitType == UnitType.MASS)
        self.assertTrue(degC.classify().unitType == UnitType.TEMPERATURE)
        self.assertTrue(amp.classify().unitType == UnitType.ELECTRIC_CURRENT)
        self.assertTrue(mol.classify().unitType == UnitType.SUBSTANCE_AMOUNT)
        self.assertTrue(cd.classify().unitType == UnitType.LUMINOSITY)
        self.assertTrue(msys.getUOM(Unit.US_DOLLAR).classify().unitType == UnitType.CURRENCY)
        self.assertTrue(msys.getUOM(Unit.BIT).classify().unitType == UnitType.COMPUTER_SCIENCE)
        
        # powers
        ft2 = msys.createUnclassifiedPowerUOM(ft, 2)
        m2 = msys.createUnclassifiedPowerUOM(m, 2)
        m3 = msys.createUnclassifiedPowerUOM(m, 3)
        mm2 = msys.createUnclassifiedPowerUOM(m, -2)
        mm3 = msys.createUnclassifiedPowerUOM(m, -3)        
        s2 = msys.createUnclassifiedPowerUOM(s, 2)
        s3 = msys.createUnclassifiedPowerUOM(s, 3)
        s4 = msys.createUnclassifiedPowerUOM(s, 4)
        sm1 = msys.createUnclassifiedPowerUOM(s, -1)
        sm3 = msys.createUnclassifiedPowerUOM(s, -3)
        amp2 = msys.createUnclassifiedPowerUOM(amp, 2)
        ampm2 = msys.createUnclassifiedPowerUOM(amp, -2)
        kgm1 = msys.createUnclassifiedPowerUOM(kg, -1)
        
        # area
        self.assertTrue(ft2.classify().unitType == UnitType.AREA)
        
        # volume
        self.assertTrue(m.multiply(m).multiply(m).classify().unitType == UnitType.VOLUME)
        
        # density
        self.assertTrue(kg.divide(m3).classify().unitType == UnitType.DENSITY)
        
        # speed
        self.assertTrue(m.divide(s).classify().unitType == UnitType.VELOCITY)
        
        # volumetric flow
        self.assertTrue(m3.divide(s).classify().unitType == UnitType.VOLUMETRIC_FLOW)
        
        # mass flow
        self.assertTrue(kg.divide(s).classify().unitType == UnitType.MASS_FLOW)
        
        # frequency
        self.assertTrue(one.divide(s).classify().unitType == UnitType.FREQUENCY)
        
        # acceleration
        self.assertTrue(m.divide(s2).classify().unitType == UnitType.ACCELERATION)
        
        # force
        self.assertTrue(m.multiply(kg).divide(s2).classify().unitType == UnitType.FORCE)
        
        # pressure
        self.assertTrue(kg.divide(m).divide(s2).classify().unitType == UnitType.PRESSURE)
        
        # energy
        self.assertTrue(kg.multiply(m).multiply(m).divide(s2).classify().unitType == UnitType.ENERGY)
        
        # power
        self.assertTrue(kg.multiply(m).multiply(m).divide(s3).classify().unitType == UnitType.POWER)
        
        # electric charge
        self.assertTrue(s.multiply(amp).classify().unitType == UnitType.ELECTRIC_CHARGE)
        
        # electromotive force
        self.assertTrue(kg.multiply(m2.divide(amp).divide(s3)).classify().unitType == UnitType.ELECTROMOTIVE_FORCE)
        
        # electric resistance
        self.assertTrue(kg.multiply(mm3.multiply(amp2.multiply(s4))).classify().unitType == UnitType.ELECTRIC_RESISTANCE)
        
        # electric capacitance
        self.assertTrue(sm3.multiply(ampm2.multiply(m2.divide(kg))).classify().unitType == UnitType.ELECTRIC_CAPACITANCE)
        
        # electric permittivity                
        self.assertTrue(s4.multiply(amp2.multiply(mm3.divide(kg))).classify().unitType == UnitType.ELECTRIC_PERMITTIVITY)
        
        # electric field strength
        self.assertTrue(amp.divide(m).classify().unitType == UnitType.ELECTRIC_FIELD_STRENGTH)
        
        # magnetic flux
        self.assertTrue(kg.divide(amp).divide(s2.multiply(m2)).classify().unitType == UnitType.MAGNETIC_FLUX)    
        
        # magnetic flux density
        self.assertTrue(kg.divide(amp).divide(s2).classify().unitType == UnitType.MAGNETIC_FLUX_DENSITY)
    
        # inductance
        self.assertTrue(kg.multiply(ampm2).divide(s2).multiply(m2).classify().unitType == UnitType.ELECTRIC_INDUCTANCE)
        
        # conductance
        self.assertTrue(kgm1.multiply(amp2).multiply(s3).multiply(mm2).classify().unitType == UnitType.ELECTRIC_CONDUCTANCE)
        
        # luminous flux
        ut = cd.multiply(one).classify().unitType
        self.assertTrue(ut == UnitType.LUMINOUS_FLUX or ut == UnitType.LUMINOSITY)
        
        # illuminance
        self.assertTrue(cd.divide(m2).classify().unitType == UnitType.ILLUMINANCE)
        
        # radiation dose absorbed and effective
        ut = m2.divide(s2).classify().unitType
        self.assertTrue(ut == UnitType.RADIATION_DOSE_ABSORBED or ut == UnitType.RADIATION_DOSE_EFFECTIVE)
        
        # radiation dose rate
        self.assertTrue(m2.divide(s3).classify().unitType == UnitType.RADIATION_DOSE_RATE)
        
        # radioactivity
        ut = sm1.classify().unitType
        self.assertTrue(ut == UnitType.RADIOACTIVITY or ut == UnitType.FREQUENCY)
        
        # catalytic activity
        self.assertTrue(mol.divide(s).classify().unitType == UnitType.CATALYTIC_ACTIVITY)
        
        # dynamic viscosity
        self.assertTrue(kg.divide(s).multiply(m).classify().unitType == UnitType.DYNAMIC_VISCOSITY)
        
        # kinematic viscosity
        self.assertTrue(m2.divide(s).classify().unitType == UnitType.KINEMATIC_VISCOSITY)
        
        # reciprocal length
        self.assertTrue(one.divide(m).classify().unitType == UnitType.RECIPROCAL_LENGTH)
        
        # plane angle
        typeMap = CacheManager.instance().getTypeMap(UnitType.PLANE_ANGLE)
        self.assertTrue(len(typeMap) == 0)
        
        baseMap = msys.getUOM(Unit.RADIAN).getBaseUnitsOfMeasure()
        self.assertTrue(len(baseMap) == 0)
        
        # solid angle
        typeMap = CacheManager.instance().getTypeMap(UnitType.SOLID_ANGLE)
        self.assertTrue(len(typeMap) == 0)
        baseMap = msys.getUOM(Unit.STERADIAN).getBaseUnitsOfMeasure()
        self.assertTrue(len(baseMap) == 0)
        
        # time squared
        self.assertTrue(s2.classify().unitType == UnitType.TIME_SQUARED)
        
        # molar concentration
        self.assertTrue(mol.divide(m3).classify().unitType == UnitType.MOLAR_CONCENTRATION)
        
        # irradiance
        self.assertTrue(kg.divide(s3).classify().unitType == UnitType.IRRADIANCE)

        