import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.prefix import Prefix
from PyCaliper.test.test_utils import TestUtils
    
class TestBridgesCase(unittest.TestCase):   
    def testBridges(self):   
        msys = MeasurementSystem.instance()   
        # SI
        kg = msys.getUOM(Unit.KILOGRAM)
        m = msys.getUOM(Unit.METRE)
        km = msys.createPrefixedUOM(Prefix.kilo(), m)
        litre = msys.getUOM(Unit.LITRE)
        N = msys.getUOM(Unit.NEWTON)
        m3 = msys.getUOM(Unit.CUBIC_METRE)
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        Nm = msys.getUOM(Unit.NEWTON_METRE)
        pa = msys.getUOM(Unit.PASCAL)
        kPa = msys.createPrefixedUOM(Prefix.kilo(), pa)
        celsius = msys.getUOM(Unit.CELSIUS)
    
        # US
        lbm = msys.getUOM(Unit.POUND_MASS)
        lbf = msys.getUOM(Unit.POUND_FORCE)
        mi = msys.getUOM(Unit.MILE)
        ft = msys.getUOM(Unit.FOOT)
        gal = msys.getUOM(Unit.US_GALLON)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)
        ft3 = msys.getUOM(Unit.CUBIC_FOOT)
        acre = msys.getUOM(Unit.ACRE)
        ftlbf = msys.getUOM(Unit.FOOT_POUND_FORCE)
        psi = msys.getUOM(Unit.PSI)
        fahrenheit = msys.getUOM(Unit.FAHRENHEIT)
                
        self.assertEqual(ft.bridgeOffset, 0.0)
        
        q1 = Quantity(10.0, ft)
        q2 = q1.convert(m)
        self.assertAlmostEqual(q2.amount, 3.048, None, None, TestUtils.DELTA6)
        
        q3 = q2.convert(q1.uom)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        
        q1 = Quantity(10.0, kg)
        q2 = q1.convert(lbm)
        self.assertAlmostEqual(q2.amount, 22.0462262185, None, None, TestUtils.DELTA6)
        q3 = q2.convert(q1.uom)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        
        q1 = Quantity(212.0, fahrenheit)
        q2 = q1.convert(celsius)
        self.assertAlmostEqual(q2.amount, 100, None, None, TestUtils.DELTA6)
        q3 = q2.convert(q1.uom)
        self.assertAlmostEqual(q3.amount, 212, None, None, TestUtils.DELTA6)
        
        mm = msys.createProductUOM(UnitType.AREA, None, "name", "mxm", "", m, m)
        
        q1 = Quantity(10.0, mm)
        q2 = q1.convert(ft2)
        self.assertAlmostEqual(q2.amount, 107.639104167, None, None, TestUtils.DELTA6)
        q2 = q2.convert(m2)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        
        mhr = msys.getUOM("m/hr")
        
        if (mhr is None):
            mhr = msys.createScalarUOM(UnitType.VELOCITY, None, "m/hr", "m/hr", "")
            mhr.setConversion(1.0 / 3600.0, msys.getUOM(Unit.METRE_PER_SEC))
        
        q1 = Quantity(10.0, psi)
        q2 = q1.convert(kPa)
        self.assertAlmostEqual(q2.amount, 68.94757280343134, None, None, TestUtils.DELTA6)
        
        q2 = q2.convert(psi)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, mhr)
        q2 = q1.convert(msys.getUOM(Unit.FEET_PER_SEC))
        self.assertAlmostEqual(q2.amount, 0.009113444152814231, None, None, TestUtils.DELTA6)
        q2 = q2.convert(mhr)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, gal)
        q2 = q1.convert(litre)
        self.assertAlmostEqual(q2.amount, 37.8541178, None, None, TestUtils.DELTA6)
        q2 = q2.convert(gal)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, m3)
        q2 = q1.convert(ft3)
        self.assertAlmostEqual(q2.amount, 353.1466672398284, None, None, TestUtils.DELTA6)
        q2 = q2.convert(m3)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, N)
        q2 = q1.convert(lbf)
        self.assertAlmostEqual(q2.amount, 2.24809, None, None, TestUtils.DELTA6)
        q2 = q2.convert(N)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, ftlbf)
        q2 = q1.convert(Nm)
        self.assertAlmostEqual(q2.amount, 13.558179483314004, None, None, TestUtils.DELTA6)
        q2 = q2.convert(ftlbf)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, lbm)
        q2 = q1.convert(kg)
        self.assertAlmostEqual(q2.amount, 4.5359237, None, None, TestUtils.DELTA6)
        q2 = q2.convert(lbm)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, km)
        q2 = q1.convert(mi)
        self.assertAlmostEqual(q2.amount, 6.21371192237, None, None, TestUtils.DELTA6)
        q2 = q2.convert(km)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        # length
        q1 = Quantity(10.0, msys.getUOM(Unit.METRE))
        q2 = q1.convert(msys.getUOM(Unit.INCH))
        self.assertAlmostEqual(q2.amount, 393.7007874015748, None, None, TestUtils.DELTA6)
        q2 = q2.convert(msys.getUOM(Unit.METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q2 = q1.convert(msys.getUOM(Unit.FOOT))
        self.assertAlmostEqual(q2.amount, 32.80839895013123, None, None, TestUtils.DELTA6)
        q2 = q2.convert(msys.getUOM(Unit.METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        # area
        q1 = Quantity(10.0, msys.getUOM(Unit.SQUARE_METRE))
        q2 = q1.convert(msys.getUOM(Unit.SQUARE_INCH))
        self.assertAlmostEqual(q2.amount, 15500.031000062, None, None, TestUtils.DELTA6)
        q2 = q2.convert(msys.getUOM(Unit.SQUARE_METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q2 = q1.convert(msys.getUOM(Unit.SQUARE_FOOT))
        self.assertAlmostEqual(q2.amount, 107.6391041670972, None, None, TestUtils.DELTA6)
        q2 = q2.convert(msys.getUOM(Unit.SQUARE_METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        # volume
        q1 = Quantity(10.0, msys.getUOM(Unit.LITRE))
        q2 = q1.convert(msys.getUOM(Unit.US_GALLON))
        self.assertAlmostEqual(q2.amount, 2.641720523581484, None, None, TestUtils.DELTA6)
        q2 = q2.convert(msys.getUOM(Unit.LITRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(4.0468564224, m)
        q2 = Quantity(1000.0, m)
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 4046.8564224, None, None, TestUtils.DELTA6)

        uom = q3.uom
        base = uom.getPowerBase()
        sf = uom.scalingFactor

        self.assertTrue(uom.abscissaUnit == m2)
        self.assertTrue(base == m)
        self.assertAlmostEqual(sf, 1.0, None, None, TestUtils.DELTA6)

        q4 = q3.convert(acre)
        self.assertAlmostEqual(q4.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == acre)

        usSec = msys.getSecond()

        v1 = msys.getUOMBySymbol("m/hr")

        v2 = msys.getUOM(Unit.METRE_PER_SEC)
        v3 = msys.createQuotientUOM(UnitType.VELOCITY, None, "", "ft/usec", "", ft, usSec)

        d1 = msys.getUOM(Unit.KILOGRAM_PER_CU_METRE)
        d2 = msys.createQuotientUOM(UnitType.DENSITY, None, "density", "lbm/gal", "", lbm, gal)

        q1 = Quantity(10.0, v1)
        q2 = q1.convert(v3)

        q1 = Quantity(10.0, v1)
        q2 = q1.convert(v2)

        q1 = Quantity(10.0, d1)
        q2 = q1.convert(d2)
        
    def testBridgeUnits(self):
        msys = MeasurementSystem.instance()
        
        bridge1 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "Bridge1", "B1", "description")
        bridge2 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "Bridge2", "B2", "description")

        bridge1.setBridgeConversion(1.0, bridge2, 0.0)
        self.assertTrue(bridge1.bridgeScalingFactor == 1.0)
        self.assertTrue(bridge1.bridgeAbscissaUnit  == bridge2)
        self.assertTrue(bridge1.bridgeOffset == 0.0)

        try:
            bridge1.setConversion(10.0, bridge1, 0.0)
            self.fail("Invalid conversion")
        except:
            pass

        try:
            bridge1.setConversion(1.0, bridge1, 10.0)
            self.fail("Invalid conversion")
        except:
            pass
