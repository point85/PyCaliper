import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.prefix import Prefix
from PyCaliper.test.base import TestUtils
    
class TestImports(unittest.TestCase):   
    def testBridges(self):        
        # SI
        kg = MeasurementSystem.instance().getUOM(Unit.KILOGRAM)
        m = MeasurementSystem.instance().getUOM(Unit.METRE)
        km = MeasurementSystem.instance().createPrefixedUOM(Prefix.kilo(), m)
        litre = MeasurementSystem.instance().getUOM(Unit.LITRE)
        N = MeasurementSystem.instance().getUOM(Unit.NEWTON)
        m3 = MeasurementSystem.instance().getUOM(Unit.CUBIC_METRE)
        m2 = MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE)
        Nm = MeasurementSystem.instance().getUOM(Unit.NEWTON_METRE)
        pa = MeasurementSystem.instance().getUOM(Unit.PASCAL)
        kPa = MeasurementSystem.instance().createPrefixedUOM(Prefix.kilo(), pa)
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
        
        mm = MeasurementSystem.instance().createProductUOM(UnitType.AREA, None, "name", "mxm", "", m, m)
        
        q1 = Quantity(10.0, mm)
        q2 = q1.convert(ft2)
        self.assertAlmostEqual(q2.amount, 107.639104167, None, None, TestUtils.DELTA6)
        q2 = q2.convert(m2)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        
        mhr = MeasurementSystem.instance().getUOM("m/hr")
        
        if (mhr is None):
            mhr = MeasurementSystem.instance().createScalarUOM(UnitType.VELOCITY, None, "m/hr", "m/hr", "")
            mhr.setConversion(1.0 / 3600.0, MeasurementSystem.instance().getUOM(Unit.METRE_PER_SEC))
        
        q1 = Quantity(10.0, psi)
        q2 = q1.convert(kPa)
        self.assertAlmostEqual(q2.amount, 68.94757280343134, None, None, TestUtils.DELTA6)
        
        q2 = q2.convert(psi)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, mhr)
        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.FEET_PER_SEC))
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
        q1 = Quantity(10.0, MeasurementSystem.instance().getUOM(Unit.METRE))
        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.INCH))
        self.assertAlmostEqual(q2.amount, 393.7007874015748, None, None, TestUtils.DELTA6)
        q2 = q2.convert(MeasurementSystem.instance().getUOM(Unit.METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.FOOT))
        self.assertAlmostEqual(q2.amount, 32.80839895013123, None, None, TestUtils.DELTA6)
        q2 = q2.convert(MeasurementSystem.instance().getUOM(Unit.METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        # area
        q1 = Quantity(10.0, MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE))
        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.SQUARE_INCH))
        self.assertAlmostEqual(q2.amount, 15500.031000062, None, None, TestUtils.DELTA6)
        q2 = q2.convert(MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.SQUARE_FOOT))
        self.assertAlmostEqual(q2.amount, 107.6391041670972, None, None, TestUtils.DELTA6)
        q2 = q2.convert(MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE))
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        # volume
        q1 = Quantity(10.0, MeasurementSystem.instance().getUOM(Unit.LITRE))
        q2 = q1.convert(MeasurementSystem.instance().getUOM(Unit.US_GALLON))
        self.assertAlmostEqual(q2.amount, 2.641720523581484, None, None, TestUtils.DELTA6)
        q2 = q2.convert(MeasurementSystem.instance().getUOM(Unit.LITRE))
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

        usSec = MeasurementSystem.instance().getSecond()

        v1 = MeasurementSystem.instance().getUOMBySymbol("m/hr")

        v2 = MeasurementSystem.instance().getUOM(Unit.METRE_PER_SEC)
        v3 = MeasurementSystem.instance().createQuotientUOM(UnitType.VELOCITY, None, "", "ft/usec", "", ft, usSec)

        d1 = MeasurementSystem.instance().getUOM(Unit.KILOGRAM_PER_CU_METRE)
        d2 = MeasurementSystem.instance().createQuotientUOM(UnitType.DENSITY, None, "density", "lbm/gal", "", lbm, gal)

        q1 = Quantity(10.0, v1)
        q2 = q1.convert(v3)

        q1 = Quantity(10.0, v1)
        q2 = q1.convert(v2)

        q1 = Quantity(10.0, d1)
        q2 = q1.convert(d2)
