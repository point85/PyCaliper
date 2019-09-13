import unittest
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.enums import Unit

class TestBridges(unittest.TestCase):
    """
    def __init__(self):
        super().__init__()
    """    
    def testBridges(self):
        # SI
        kg = MeasurementSystem.instance().getUOM(Unit.KILOGRAM)
        m = MeasurementSystem.instance().getUOM(Unit.METRE)
        km = MeasurementSystem.instance().getUOM(Prefix.kilo(), m)
        litre = MeasurementSystem.instance().getUOM(Unit.LITRE)
        N = MeasurementSystem.instance().getUOM(Unit.NEWTON)
        m3 = MeasurementSystem.instance().getUOM(Unit.CUBIC_METRE)
        m2 = MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE)
        Nm = MeasurementSystem.instance().getUOM(Unit.NEWTON_METRE)
        pa = MeasurementSystem.instance().getUOM(Unit.PASCAL)
        kPa = MeasurementSystem.instance().getUOM(Prefix.kilo(), pa)
        celsius = MeasurementSystem.instance().getUOM(Unit.CELSIUS)
    
        # US
        lbm = MeasurementSystem.instance().getUOM(Unit.POUND_MASS)
        lbf = MeasurementSystem.instance().getUOM(Unit.POUND_FORCE)
        mi = MeasurementSystem.instance().getUOM(Unit.MILE)
        ft = MeasurementSystem.instance().getUOM(Unit.FOOT)
        gal = MeasurementSystem.instance().getUOM(Unit.US_GALLON)
        ft2 = MeasurementSystem.instance().getUOM(Unit.SQUARE_FOOT)
        ft3 = MeasurementSystem.instance().getUOM(Unit.CUBIC_FOOT)
        acre = MeasurementSystem.instance().getUOM(Unit.ACRE)
        ftlbf = MeasurementSystem.instance().getUOM(Unit.FOOT_POUND_FORCE)
        psi = MeasurementSystem.instance().getUOM(Unit.PSI)
        fahrenheit = MeasurementSystem.instance().getUOM(Unit.FAHRENHEIT)
                
        self.assertEqual(ft.getBridgeOffset(), 0.0)
        
        q1 = Quantity(10.0, ft)
        q2 = q1.convert(m)
        self.assertAlmostEqual(q2.getAmount(), 3.048, None, None, self.DELTA6)
        
        """
        q3 = q2.convert(q1.getUOM())
        assert BaseTest.isCloseTo(q3.getAmount(), 10.0, self.DELTA6)
        
        q1 = Quantity(10.0, kg)
        q2 = q1.convert(lbm)
        assert BaseTest.isCloseTo(q2.getAmount(), 22.0462, self.DELTA4)
        q3 = q2.convert(q1.getUOM())
        assert BaseTest.isCloseTo(q3.getAmount(), 10.0, self.DELTA6)
        
        q1 = Quantity(212.0, fahrenheit)
        q2 = q1.convert(celsius)
        assert BaseTest.isCloseTo(q2.getAmount(), 100, self.DELTA6)
        q3 = q2.convert(q1.getUOM())
        assert BaseTest.isCloseTo(q3.getAmount(), 212, self.DELTA6)
        
        mm = MeasurementSystem.instance().createProductUOM(UnitType.AREA, "name", "mxm", "", m, m)
        
        q1 = Quantity(10.0, mm)
        q2 = q1.convert(ft2)
        assert BaseTest.isCloseTo(q2.getAmount(), 107.639104167, self.DELTA6)
        q2 = q2.convert(m2)
        assert BaseTest.isCloseTo(q2.getAmount(), 10.0, self.DELTA6)
        
        mhr = MeasurementSystem.instance().getUOM("m/hr")
        
        if (mhr is None):
            mhr = MeasurementSystem.instance().createScalarUOM(UnitType.VELOCITY, "m/hr", "m/hr", "")
            mhr.setConversion(1.0 / 3600.0, MeasurementSystem.instance().getUOM(Unit.METRE_PER_SEC))
        
        q1 = Quantity(10.0, psi)
        q2 = q1.convert(kPa)
        assert BaseTest.isCloseTo(q2.getAmount(), 68.94757280343134, self.DELTA6)
        """

"""
if __name__ == '__main__':
    unittest.main()
"""