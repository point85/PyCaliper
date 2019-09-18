import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.prefix import Prefix
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

    def testTemperature(self):
        msys = MeasurementSystem.instance()

        K = msys.getUOM(Unit.KELVIN)
        C = msys.getUOM(Unit.CELSIUS)
        R = msys.getUOM(Unit.RANKINE)
        F = msys.getUOM(Unit.FAHRENHEIT)

        q1 = Quantity(212.0, F)
        q2 = q1.convert(C)
        self.assertAlmostEqual(q2.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(F).amount, 212.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(32.0, F)
        q2 = q1.convert(C)
        self.assertAlmostEqual(q2.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(F).amount, 32.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(0.0, F)
        q2 = q1.convert(C)
        self.assertAlmostEqual(q2.amount, -17.7777777777778, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(F).amount, 0.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(459.67, R)
        q2 = q1.convert(F)
        self.assertAlmostEqual(q2.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(R).amount, 459.67, None, None, TestUtils.DELTA6)

        q2 = q1.convert(K)
        self.assertAlmostEqual(q2.amount, 255.3722222222222, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(R).amount, 459.67, None, None, TestUtils.DELTA6)

        q2 = q1.convert(C)
        self.assertAlmostEqual(q2.amount, -17.7777777777778, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(R).amount, 459.67, None, None, TestUtils.DELTA6)

        q1 = Quantity(273.15, K)
        q2 = q1.convert(C)
        self.assertAlmostEqual(q2.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(K).amount, 273.15, None, None, TestUtils.DELTA6)

        q1 = Quantity(0.0, K)
        q2 = q1.convert(R)
        self.assertAlmostEqual(q2.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(K).amount, 0.0, None, None, TestUtils.DELTA6)
        
    def testLength(self):
        msys = MeasurementSystem.instance()
        
        m = msys.getUOM(Unit.METRE)
        cm = msys.createPrefixedUOM(Prefix.centi(), m)
        m2 = msys.getUOM(Unit.SQUARE_METRE)

        cmsym = "cm" + "0x00B2"
        cm2 = msys.getUOM(cmsym)

        if (cm2 is None):
            cm2 = msys.createPowerUOM(UnitType.AREA, None, "square centimetres", cmsym, "centimetres squared", cm, 2)

        ft = msys.getUOM(Unit.FOOT)
        yd = msys.getUOM(Unit.YARD)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)
        in2 = msys.getUOM(Unit.SQUARE_INCH)

        q1 = Quantity(1.0, ft2)
        q2 = q1.convert(in2)
        self.assertAlmostEqual(q2.amount, 144.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(ft2).amount, 1.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(1.0, msys.getUOM(Unit.SQUARE_METRE))
        q2 = q1.convert(ft2)
        self.assertAlmostEqual(q2.amount, 10.76391041670972, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(m2).amount, 1.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(3, ft)
        q2 = q1.convert(yd)
        self.assertAlmostEqual(q2.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(ft).amount, 3.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(1.0, ft)
        q2 = q1.convert(m)
        self.assertAlmostEqual(q2.amount, 0.3048, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(ft).amount, 1.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(100, cm)
        q2 = q1.convert(m)
        self.assertAlmostEqual(q2.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.convert(cm).amount, 100.0, None, None, TestUtils.DELTA6)

        # add
        q1 = Quantity(50.0, cm)
        q2 = Quantity(50.0, cm)
        q3 = q1.add(q2)
        self.assertAlmostEqual(q3.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.convert(m).amount, 1.0, None, None, TestUtils.DELTA6)

        q4 = q2.add(q1)
        self.assertAlmostEqual(q4.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q4.convert(m).amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3 == q4)

        # subtract
        q3 = q1.subtract(q2)
        self.assertAlmostEqual(q3.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.convert(m).amount, 0.0, None, None, TestUtils.DELTA6)

        q4 = q2.subtract(q1)
        self.assertAlmostEqual(q4.amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q4.convert(m).amount, 0.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3 == q4)

        # multiply
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 2500.0, None, None, TestUtils.DELTA6)

        q4 = q3.convert(cm2)
        self.assertAlmostEqual(q4.amount, 2500.0, None, None, TestUtils.DELTA6)

        q4 = q3.convert(m2)
        self.assertAlmostEqual(q4.amount, 0.25, None, None, TestUtils.DELTA6)

        # divide
        q4 = q3.divide(q1)
        self.assertTrue(q4 == q2)

