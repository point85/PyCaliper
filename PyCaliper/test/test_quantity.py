import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.enums import Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.test_utils import TestUtils

class TestQuantity(unittest.TestCase): 
    def testNamedQuantity(self):
        msys = MeasurementSystem.instance()
        
        q = Quantity(10.0, Unit.CELSIUS)
        self.assertTrue(str(q) is not None)

        # faraday
        f = msys.getQuantity(Constant.FARADAY_CONSTANT)
        qe = msys.getQuantity(Constant.ELEMENTARY_CHARGE)
        na = msys.getQuantity(Constant.AVAGADRO_CONSTANT)
        
        s = msys.getUOM(Unit.SECOND)
        w = msys.getUOM(Unit.WATT)
        
        eNA = qe.multiply(na)
        self.assertAlmostEqual(f.amount, eNA.amount, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(f.amount, 96485.332123, None, None, TestUtils.DELTA5)

        # epsilon 0
        fm = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "Farad per metre", "F/m", "Farad per metre",
            msys.getUOM(Unit.FARAD), msys.getUOM(Unit.METRE))
        eps0 = msys.getQuantity(Constant.ELECTRIC_PERMITTIVITY)
        self.assertAlmostEqual(eps0.amount, 8.854187817E-12, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(eps0.convert(fm).amount, 8.854187817E-12, None, None, TestUtils.DELTA6)

        # atomic masses
        u = Quantity(1.66053904020E-24, msys.getUOM(Unit.GRAM))
        me = msys.getQuantity(Constant.ELECTRON_MASS)
        bd = me.divide(u).amount
        self.assertAlmostEqual(bd, 5.48579909016E-04, None, None, TestUtils.DELTA6)

        mp = msys.getQuantity(Constant.PROTON_MASS)
        bd = mp.divide(u).amount
        self.assertAlmostEqual(bd, 1.00727646687991, None, None, TestUtils.DELTA6)
        
        # caesium
        cs = msys.getQuantity(Constant.CAESIUM_FREQUENCY)
        periods = cs.multiply(Quantity(1.0, s))
        self.assertAlmostEqual(periods.amount, 9192631770.0, None, None, TestUtils.DELTA0)
        
        # luminous efficacy
        kcd = msys.getQuantity(Constant.LUMINOUS_EFFICACY)
        lum = kcd.multiply(Quantity(1.0, w))
        self.assertAlmostEqual(lum.amount, 683.0, None, None, TestUtils.DELTA0)

    def testAllUnits(self):
        msys = MeasurementSystem.instance()
        
        for u in Unit:
            uom1 = msys.getUOM(u)
            uom2 = msys.getUOM(u)
            self.assertTrue(uom1 == uom2)

            q1 = Quantity(10.0, uom1)
            q2 = q1.convert(uom2)
            self.assertTrue(q1 == q2)

    def testTime(self):
        msys = MeasurementSystem.instance()

        second = msys.getSecond()
        minute = msys.getMinute()

        oneMin = Quantity(1.0, minute)
        oneSec = Quantity(1.0, second)
        converted = oneMin.convert(second)

        self.assertAlmostEqual(converted.amount, 60.0, None, None, TestUtils.DELTA6)
        self.assertTrue(converted.uom == second)

        sixty = oneMin.divide(oneSec)
        self.assertAlmostEqual(sixty.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(sixty.uom.scalingFactor, 60.0, None, None, TestUtils.DELTA6)

        q1 = sixty.convert(msys.getOne())
        self.assertTrue(q1.uom == msys.getOne())
        self.assertAlmostEqual(q1.amount, 60.0, None, None, TestUtils.DELTA6)

        q1 = q1.multiply(oneSec)
        self.assertTrue(q1.convert(second).uom == second)
        self.assertAlmostEqual(q1.amount, 60.0, None, None, TestUtils.DELTA6)

        q1 = q1.convert(minute)
        self.assertTrue(q1.uom == minute)
        self.assertAlmostEqual(q1.amount, 1.0, None, None, TestUtils.DELTA6)
