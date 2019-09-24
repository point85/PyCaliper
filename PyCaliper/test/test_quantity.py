import unittest
import math

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

    def testUSQuantity(self):
        msys = MeasurementSystem.instance()
        
        gal = msys.getUOM(Unit.US_GALLON)
        in3 = msys.getUOM(Unit.CUBIC_INCH)
        floz = msys.getUOM(Unit.US_FLUID_OUNCE)
        qt = msys.getUOM(Unit.US_QUART)

        q1 = Quantity(10.0, gal)
        q2 = q1.convert(in3)
        self.assertAlmostEqual(q2.amount, 2310.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == in3)

        q1 = Quantity(128.0, floz)
        q2 = q1.convert(qt)
        self.assertAlmostEqual(q2.amount, 4.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == qt)

        ft = msys.getUOM(Unit.FOOT)
        inch = msys.getUOM(Unit.INCH)
        mi = msys.getUOM(Unit.MILE)

        q1 = Quantity(10.0, ft)
        q2 = q1.convert(inch)

        q1 = Quantity(1.0, mi)

        # British cup to US gallon
        q1 = Quantity(10.0, msys.getUOM(Unit.BR_CUP))
        q2 = q1.convert(msys.getUOM(Unit.US_GALLON))
        self.assertAlmostEqual(q2.amount, 0.6, None, None, TestUtils.DELTA3)

        # US ton to British ton
        q1 = Quantity(10.0, msys.getUOM(Unit.US_TON))
        q2 = q1.convert(msys.getUOM(Unit.BR_TON))
        self.assertAlmostEqual(q2.amount, 8.928571428, None, None, TestUtils.DELTA6)

        # troy ounce to ounce
        q1 = Quantity(10.0, msys.getUOM(Unit.TROY_OUNCE))
        q2 = q1.convert(msys.getUOM(Unit.OUNCE))
        self.assertAlmostEqual(q2.amount, 10.971, None, None, TestUtils.DELTA3)

        # deci-litre to quart
        dl = msys.createPrefixedUOM(Prefix.deci(), msys.getUOM(Unit.LITRE))
        q1 = Quantity(10.0, dl)
        q2 = q1.convert(msys.getUOM(Unit.US_QUART))
        self.assertAlmostEqual(q2.amount, 1.0566882, None, None, TestUtils.DELTA6)
        
    def testSIQuantity(self):
        msys = MeasurementSystem.instance()

        litre = msys.getUOM(Unit.LITRE)
        m3 = msys.getUOM(Unit.CUBIC_METRE)
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        m = msys.getUOM(Unit.METRE)
        cm = msys.createPrefixedUOM(Prefix.centi(), m)
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        secPerM = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, None, "s/m", None, msys.getSecond(), m)
        oneOverM = msys.getUOM(Unit.DIOPTER)
        fperm = msys.getUOM(Unit.FARAD_PER_METRE)

        oneOverCm = msys.createScalarUOM(UnitType.RECIPROCAL_LENGTH, None, None, "1/cm", None)
        oneOverCm.setConversion(100.0, oneOverM)

        q1 = Quantity(10.0, litre)
        q2 = q1.convert(m3)
        self.assertAlmostEqual(q2.amount, 0.01, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == m3)

        q2 = q1.convert(litre)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == litre)

        # add
        q1 = Quantity(2.0, m)
        q2 = Quantity(2.0, cm)
        q3 = q1.add(q2)

        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.abscissaUnit == m)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.amount, 2.02, None, None, TestUtils.DELTA6)

        q4 = q3.convert(cm)
        self.assertAlmostEqual(q4.amount, 202, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == cm)

        # subtract
        q3 = q3.subtract(q1)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.abscissaUnit == m)
        self.assertAlmostEqual(q3.amount, 0.02, None, None, TestUtils.DELTA6)

        q4 = q3.convert(cm)
        self.assertAlmostEqual(q4.amount, 2.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == cm)

        # multiply
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 4.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.scalingFactor, 0.01, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.getBaseSymbol() == m2.getBaseSymbol())

        q4 = q3.divide(q3)
        self.assertAlmostEqual(q4.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == msys.getOne())

        q4 = q3.divide(q1)
        self.assertTrue(q4 == q2)

        q4 = q3.convert(m2)
        self.assertAlmostEqual(q4.amount, 0.04, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == m2)

        # divide
        q3 = q3.divide(q2)
        self.assertAlmostEqual(q3.amount, 2.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == m)
        self.assertTrue(q3 == q1)

        q3 = q3.convert(m)
        self.assertAlmostEqual(q3.amount, 2.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(0.0, litre)

        try:
            q2 = q1.divide(q1)
            self.fail("divide by zero)")
        except:
            pass

        q1 = q3.convert(cm).divideByAmount(10.0)
        self.assertAlmostEqual(q1.amount, 20.0, None, None, TestUtils.DELTA6)

        # invert
        q1 = Quantity(10.0, mps)
        q2 = q1.invert()
        self.assertAlmostEqual(q2.amount, 0.1, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == secPerM)

        q2 = q2.invert()
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == mps)

        q1 = Quantity(10.0, cm)
        q2 = q1.invert()
        self.assertAlmostEqual(q2.amount, 0.1, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == oneOverCm)

        q2 = q2.convert(m.invert())
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom == oneOverM)

        self.assertTrue(str(q2) != None)

        # Newton-metres divided by metres
        q1 = Quantity(10.0, msys.getUOM(Unit.NEWTON_METRE))
        q2 = Quantity(1.0, msys.getUOM(Unit.METRE))
        q3 = q1.divide(q2)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == msys.getUOM(Unit.NEWTON))

        # length multiplied by force
        q1 = Quantity(10.0, msys.getUOM(Unit.NEWTON))
        q2 = Quantity(1.0, msys.getUOM(Unit.METRE))
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        nm2 = msys.getUOM(Unit.NEWTON_METRE)
        self.assertTrue(q3.uom.getBaseSymbol() == nm2.getBaseSymbol())
        q4 = q3.convert(msys.getUOM(Unit.JOULE))
        self.assertTrue(q4.uom == msys.getUOM(Unit.JOULE))

        # farads
        q1 = Quantity(10.0, fperm)
        q2 = Quantity(1.0, m)
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == msys.getUOM(Unit.FARAD))

        # amps
        q1 = Quantity(10.0, msys.getUOM(Unit.AMPERE_PER_METRE))
        q2 = Quantity(1.0, m)
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == msys.getUOM(Unit.AMPERE))

        # Boltzmann and Avogadro
        boltzmann = msys.getQuantity(Constant.BOLTZMANN_CONSTANT)
        avogadro = msys.getQuantity(Constant.AVAGADRO_CONSTANT)
        gas = msys.getQuantity(Constant.GAS_CONSTANT)
        qR = boltzmann.multiply(avogadro)
        self.assertAlmostEqual(qR.uom.scalingFactor, gas.uom.scalingFactor, None, None, TestUtils.DELTA6)

        # Sieverts
        q1 = Quantity(20.0, msys.createPrefixedUOM(Prefix.milli(), msys.getUOM(Unit.SIEVERTS_PER_HOUR)))
        q2 = Quantity(24.0, msys.getHour())
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 480.0, None, None, TestUtils.DELTA6)
        
        # If the concentration of a sulfuric acid solution is c(H2SO4) = 1 mol/L and the equivalence factor is 0.5, what is the normality?
        mol = msys.getUOM(Unit.MOLE)
        molPerL = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "moler conc", "mol/L",
                "mole per litre", mol, litre)
        
        feq = Quantity(0.5, molPerL)
        
        N = Quantity(1.0, molPerL).divide(feq)
        self.assertAlmostEqual(N.amount, 2.0, None, None, TestUtils.DELTA6)
        
    def testPowers(self):
        msys = MeasurementSystem.instance()
        
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        p2 = msys.createPowerUOM(UnitType.AREA, None, "m2^1", "m2^1", "square metres raised to power 1", m2, 1)
        p4 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m2^2", "m2^2", "square metres raised to power 2",
            m2, 2)

        q1 = Quantity(10.0, m2)
        q3 = Quantity(10.0, p4)

        q4 = q3.divide(q1)
        self.assertAlmostEqual(q4.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom.getBaseUOM() == m2)

        q2 = q1.convert(p2)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom.getBaseUOM() == m2)

        # power method
        ft = msys.getUOM(Unit.FOOT)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)
        q1 = Quantity(10.0, ft)

        q3 = msys.quantityToPower(q1, 2)
        self.assertAlmostEqual(q3.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.getBaseSymbol() == ft2.getBaseSymbol())

        q4 = q3.convert(msys.getUOM(Unit.SQUARE_METRE))
        self.assertAlmostEqual(q4.amount, 9.290304, None, None, TestUtils.DELTA6)

        q3 = msys.quantityToPower(q1, 1)
        self.assertTrue(q3.amount == q1.amount)
        self.assertTrue(q3.uom.getBaseSymbol() == q1.uom.getBaseSymbol())

        q3 = msys.quantityToPower(q1, 0)
        self.assertTrue(q3.amount == 1.0)
        self.assertTrue(q3.uom.getBaseSymbol() == msys.getOne().getBaseSymbol())

        q3 = msys.quantityToPower(q1, -1)
        self.assertTrue(q3.amount == 0.1)
        self.assertTrue(q3.uom == ft.invert())

        q3 = msys.quantityToPower(q1, -2)
        self.assertTrue(q3.amount == 0.01)
        self.assertTrue(q3.uom == ft2.invert())
        
    def testSIUnits(self):
        msys = MeasurementSystem.instance()

        newton = msys.getUOM(Unit.NEWTON)
        metre = msys.getUOM(Unit.METRE)
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        cm = msys.createPrefixedUOM(Prefix.centi(), metre)
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        joule = msys.getUOM(Unit.JOULE)
        m3 = msys.getUOM(Unit.CUBIC_METRE)
        farad = msys.getUOM(Unit.FARAD)
        nm = msys.getUOM(Unit.NEWTON_METRE)
        coulomb = msys.getUOM(Unit.COULOMB)
        volt = msys.getUOM(Unit.VOLT)
        watt = msys.getUOM(Unit.WATT)
        cm2 = msys.createProductUOM(UnitType.AREA, None, "square centimetres", "cm" + "0x00B2", "", cm, cm)
        cv = msys.createProductUOM(UnitType.ENERGY, None, "CxV", "CxV", "Coulomb times Volt", coulomb, volt)
        ws = msys.createProductUOM(UnitType.ENERGY, None, "Wxs", "Wxs", "Watt times second", watt,
            msys.getSecond())
        ft3 = msys.getUOM(Unit.CUBIC_FOOT)
        hz = msys.getUOM(Unit.HERTZ)

        self.assertTrue(nm.getBaseSymbol() == joule.getBaseSymbol())
        self.assertTrue(cv.getBaseSymbol() == joule.getBaseSymbol())
        self.assertTrue(ws.getBaseSymbol() == joule.getBaseSymbol())

        q1 = Quantity(10.0, newton)
        q2 = Quantity(10.0, metre)
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.getBaseSymbol() == nm.getBaseSymbol())
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)

        q3 = q3.convert(joule)
        self.assertAlmostEqual(q3.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == joule)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)

        q3 = q3.convert(nm)
        self.assertAlmostEqual(q3.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == nm)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(100.0, cm)
        q2 = q1.convert(metre)
        self.assertAlmostEqual(q2.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q2.uom.unit == Unit.METRE)
        self.assertAlmostEqual(q2.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)

        q2 = q2.convert(cm)
        self.assertAlmostEqual(q2.amount, 100.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q2.uom.scalingFactor, 0.01, None, None, TestUtils.DELTA6)

        q2 = q1
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 10000, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.scalingFactor, 0.0001, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)

        q4 = q3.convert(m2)
        self.assertTrue(q4.uom == m2)
        self.assertAlmostEqual(q4.amount, 1.0, None, None, TestUtils.DELTA6)

        q3 = q3.convert(m2)
        self.assertAlmostEqual(q3.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == m2)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)

        q3 = q3.convert(cm2)
        self.assertAlmostEqual(q3.amount, 10000, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom == cm2)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)

        # power
        onem3 = Quantity(1.0, m3)
        cm3sym = "cm" + "0x00B3"
        cm3 = msys.createPowerUOM(UnitType.VOLUME, None, cm3sym, cm3sym, None, cm, 3)
        megcm3 = Quantity(1E+06, cm3)

        qft3 = onem3.convert(ft3)
        self.assertAlmostEqual(qft3.amount, 35.31466672148859, None, None, TestUtils.DELTA6)

        qtym3 = qft3.convert(m3)
        self.assertAlmostEqual(qtym3.amount, 1.0, None, None, TestUtils.DELTA6)

        qm3 = megcm3.convert(m3)
        self.assertAlmostEqual(qm3.amount, 1.0, None, None, TestUtils.DELTA6)
        qm3 = qm3.convert(cm3)
        self.assertAlmostEqual(qm3.amount, 1E+06, None, None, TestUtils.DELTA6)

        qcm3 = onem3.convert(cm3)
        self.assertAlmostEqual(qcm3.amount, 1E+06, None, None, TestUtils.DELTA6)

        # inversions
        u = metre.invert()
        sym = u.abscissaUnit.symbol
        self.assertTrue(sym == msys.getUOM(Unit.DIOPTER).symbol)

        u = mps.invert()
        self.assertTrue(u.symbol == "s/m")

        uom = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "1/F", "1/F", "one over farad", msys.getOne(),
            farad)
        self.assertTrue(uom.symbol == "1/F")

        # hz to radians per sec
        q1 = Quantity(10.0, msys.getUOM(Unit.HERTZ))
        q2 = q1.convert(msys.getUOM(Unit.RAD_PER_SEC))
        self.assertAlmostEqual(q2.amount, 20.0 * math.pi, None, None, TestUtils.DELTA6)

        q3 = q2.convert(msys.getUOM(Unit.HERTZ))
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)

        # rpm to radians per second
        q1 = Quantity(10.0, msys.getUOM(Unit.REV_PER_MIN))
        q2 = q1.convert(msys.getUOM(Unit.RAD_PER_SEC))
        self.assertAlmostEqual(q2.amount, 1.04719755119, None, None, TestUtils.DELTA6)

        q3 = q2.convert(msys.getUOM(Unit.REV_PER_MIN))
        self.assertAlmostEqual(q3.amount, 10.0, None, None, TestUtils.DELTA6)

        q1 = Quantity(10.0, hz)
        q2 = Quantity(1.0, msys.getMinute())
        q3 = q1.multiply(q2).convert(msys.getOne())
        self.assertAlmostEqual(q3.amount, 600, None, None, TestUtils.DELTA6)

        q1 = Quantity(1.0, msys.getUOM(Unit.ELECTRON_VOLT))
        q2 = q1.convert(msys.getUOM(Unit.JOULE))
        self.assertAlmostEqual(q2.amount, 1.60217656535E-19, None, None, TestUtils.DELTA6)
        
    def testEquations(self):
        msys = MeasurementSystem.instance()

        # body mass index
        height = Quantity(2.0, msys.getUOM(Unit.METRE))
        mass = Quantity(100.0, msys.getUOM(Unit.KILOGRAM))
        bmi = mass.divide(height.multiply(height))
        self.assertAlmostEqual(bmi.amount, 25.0, None, None, TestUtils.DELTA6)

        # E = mc^2
        c = msys.getQuantity(Constant.LIGHT_VELOCITY)
        m = Quantity(1.0, msys.getUOM(Unit.KILOGRAM))
        e = m.multiply(c).multiply(c)
        self.assertAlmostEqual(e.amount, 8.987551787368176E+16, None, None, TestUtils.DELTA6)
        
        # Ideal Gas Law, PV = nRT
        # A cylinder of argon gas contains 50.0 L of Ar at 18.4 atm and 127 C.
        # How many moles of argon are in the cylinder?
        p = Quantity(18.4, msys.getUOM(Unit.ATMOSPHERE)).convert(msys.getUOM(Unit.PASCAL))
        v = Quantity(50.0, msys.getUOM(Unit.LITRE)).convert(msys.getUOM(Unit.CUBIC_METRE))
        t = Quantity(127.0, msys.getUOM(Unit.CELSIUS)).convert(msys.getUOM(Unit.KELVIN))
        n = p.multiply(v).divide(msys.getQuantity(Constant.GAS_CONSTANT).multiply(t))
        self.assertAlmostEqual(n.amount, 28.018664, None, None, TestUtils.DELTA6)
           
        # energy of red light photon = Planck's constant times the frequency
        frequency = Quantity(400.0, msys.createPrefixedUOM(Prefix.tera(), msys.getUOM(Unit.HERTZ)))
        ev = msys.getQuantity(Constant.PLANCK_CONSTANT).multiply(frequency).convert(msys.getUOM(Unit.ELECTRON_VOLT))
        self.assertAlmostEqual(ev.amount, 1.65, None, None, TestUtils.DELTA2)
        
        # wavelength of red light in nanometres
        nm = msys.createPrefixedUOM(Prefix.nano(), msys.getUOM(Unit.METRE))
        wavelength = msys.getQuantity(Constant.LIGHT_VELOCITY).divide(frequency).convert(nm)
        self.assertAlmostEqual(wavelength.amount, 749.48, None, None, TestUtils.DELTA2)

        # Newton's second law of motion (F = ma). Weight of 1 kg in lbf
        mkg = Quantity(1.0, msys.getUOM(Unit.KILOGRAM))
        f = mkg.multiply(msys.getQuantity(Constant.GRAVITY)).convert(msys.getUOM(Unit.POUND_FORCE))
        self.assertAlmostEqual(f.amount, 2.20462, None, None, TestUtils.DELTA5)

        # units per volume of solution, C = A x (m/V)
        # create the "A" unit of measure
        activityUnit = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "activity", "act",
            "activity of material", msys.getUOM(Unit.UNIT), msys.createPrefixedUOM(Prefix.milli(), msys.getUOM(Unit.GRAM)))
        
        # calculate concentration
        activity = Quantity(1.0, activityUnit)
        litre = msys.getUOM(Unit.LITRE)
        ml = msys.createPrefixedUOM(Prefix.milli(), litre)
        g = msys.getUOM(Unit.GRAM)
        mg = msys.createPrefixedUOM(Prefix.milli(), g)
        grams = Quantity(1.0, g).convert(mg)
        volume = Quantity(1.0, ml)
        concentration = activity.multiply(grams.divide(volume))
        self.assertAlmostEqual(concentration.amount, 1000.0, None, None, TestUtils.DELTA6)

        katal = msys.getUOM(Unit.KATAL)
        katals = concentration.multiply(Quantity(1.0, litre)).convert(katal)
        self.assertAlmostEqual(katals.amount, 0.01666667, None, None, TestUtils.DELTA6)
        
        # The Stefan–Boltzmann law states that the power emitted per unit area
        # of the surface of a black body is directly proportional to the 4.0th
        # power of its absolute temperature: sigma * T^4

        # calculate at 1000 Kelvin
        temp = Quantity(1000.0, msys.getUOM(Unit.KELVIN))
        t4 = msys.quantityToPower(temp, 4)
        intensity = msys.getQuantity(Constant.STEFAN_BOLTZMANN).multiply(t4)
        self.assertAlmostEqual(intensity.amount, 56703.67, None, None, TestUtils.DELTA2)
        
        # Hubble's law, v = H0 x D. Let D = 10 Mpc
        d = Quantity(10.0, msys.createPrefixedUOM(Prefix.mega(), msys.getUOM(Unit.PARSEC)))
        h0 = msys.getQuantity(Constant.HUBBLE_CONSTANT)
        velocity = h0.multiply(d)
        self.assertAlmostEqual(velocity.amount, 719, None, None, TestUtils.DELTA3)
        
        # Ideal Gas Law, PV = nRT
        # A cylinder of argon gas contains 50.0 L of Ar at 18.4 atm and 127 C.
        # How many moles of argon are in the cylinder?
        p = Quantity(18.4, msys.getUOM(Unit.ATMOSPHERE)).convert(msys.getUOM(Unit.PASCAL))
        v = Quantity(50.0, msys.getUOM(Unit.LITRE)).convert(msys.getUOM(Unit.CUBIC_METRE))
        t = Quantity(127.0, msys.getUOM(Unit.CELSIUS)).convert(msys.getUOM(Unit.KELVIN))
        n = p.multiply(v).divide(msys.getQuantity(Constant.GAS_CONSTANT).multiply(t))
        self.assertAlmostEqual(n.amount, 28.018664, None, None, TestUtils.DELTA6)
        
        # Arrhenius equation
        # A device has an activation energy of 0.5 and a characteristic life of
        # 2,750 hours at an accelerated temperature of 150 degrees Celsius.
        # Calculate the characteristic life at an expected use temperature of
        # 85 degrees Celsius.

        # Convert the Boltzman constant from J/K to eV/K for the Arrhenius
        # equation
        C = msys.getUOM(Unit.CELSIUS)
        Ta = Quantity(150.0, C)
        # expected use temperature
        Tu = Quantity(85.0, C)
        
        j = Quantity(1.0, msys.getUOM(Unit.JOULE))
        eV = j.convert(msys.getUOM(Unit.ELECTRON_VOLT))
        
        # Boltzmann constant
        bc = msys.getQuantity(Constant.BOLTZMANN_CONSTANT)
        Kb = bc.multiplyByAmount(eV.amount)

        # calculate the acceleration factor
        K = msys.getUOM(Unit.KELVIN)
        factor1 = Tu.convert(K).invert().subtract(Ta.convert(K).invert())
        factor2 = Kb.invert().multiplyByAmount(0.5)
        factor3 = factor1.multiply(factor2)
        AF = math.exp(factor3.amount)
        # calculate longer life at expected use temperature
        life85 = Quantity(2750.0, msys.getHour())
        life150 = life85.multiplyByAmount(AF)
        self.assertAlmostEqual(life150.amount, 33121.4, None, None, TestUtils.DELTA1)

        # energy of red light photon = Planck's constant times the frequency
        hz = msys.getUOM(Unit.HERTZ)
        thz = msys.createPrefixedUOM(Prefix.tera(), hz)
        frequency = Quantity(400.0, thz)
        qp = msys.getQuantity(Constant.PLANCK_CONSTANT)
        evolt = msys.getUOM(Unit.ELECTRON_VOLT)
        qpf = qp.multiply(frequency)
        ev = qpf.convert(evolt)
        self.assertAlmostEqual(ev.amount, 1.65, None, None, TestUtils.DELTA2)

    def testPackaging(self):
        msys = MeasurementSystem.instance()
            
        one16ozCan = msys.createScalarUOM(UnitType.VOLUME, None, "16 oz can", "16ozCan", "16 oz can")
        one16ozCan.setConversion(16.0, msys.getUOM(Unit.US_FLUID_OUNCE))

        q400 = Quantity(400.0, one16ozCan)
        q50 = q400.convert(msys.getUOM(Unit.US_GALLON))
        self.assertAlmostEqual(q50.amount, 50.0, None, None, TestUtils.DELTA6)
        
        # 1 12 oz can = 12 fl.oz.
        one12ozCan = msys.createScalarUOM(UnitType.VOLUME, None, "12 oz can", "12ozCan", "12 oz can")
        one12ozCan.setConversion(12.0, msys.getUOM(Unit.US_FLUID_OUNCE))

        q48 = Quantity(48.0, one12ozCan)
        q36 = q48.convert(one16ozCan)
        self.assertAlmostEqual(q36.amount, 36.0, None, None, TestUtils.DELTA6)

        # 6 12 oz cans = 1 6-pack of 12 oz cans
        sixPackCan = msys.createScalarUOM(UnitType.VOLUME, None, "6-pack", "6PCan", "6-pack of 12 oz cans")
        sixPackCan.setConversion(6.0, one12ozCan)

        fourPackCase = msys.createScalarUOM(UnitType.VOLUME, None, "4 pack case", "4PCase", "case of 4 6-packs")
        fourPackCase.setConversion(4.0, sixPackCan)

        bd = fourPackCase.getConversionFactor(one12ozCan)
        self.assertAlmostEqual(bd, 24.0, None, None, TestUtils.DELTA6)

        bd = one12ozCan.getConversionFactor(fourPackCase)

        bd = fourPackCase.getConversionFactor(sixPackCan)
        bd = sixPackCan.getConversionFactor(fourPackCase)

        bd = sixPackCan.getConversionFactor(one12ozCan)
        bd = one12ozCan.getConversionFactor(sixPackCan)

        tenCases = Quantity(10.0, fourPackCase)

        q1 = tenCases.convert(one12ozCan)
        self.assertAlmostEqual(q1.amount, 240.0, None, None, TestUtils.DELTA6)

        q2 = q1.convert(fourPackCase)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestUtils.DELTA6)

        fortyPacks = Quantity(40.0, sixPackCan)
        q2 = fortyPacks.convert(one12ozCan)
        self.assertAlmostEqual(q2.amount, 240.0, None, None, TestUtils.DELTA6)

        oneCan = Quantity(1.0, one12ozCan)
        q2 = oneCan.convert(sixPackCan)
        self.assertAlmostEqual(q2.amount, 0.1666666666666667, None, None, TestUtils.DELTA6)

        # A beer bottling line is rated at 2000 12 ounce cans/hour (US) at the
        # filler. The case packer packs 4.0 6-packs of cans into a case.
        # Assuming no losses, what should be the rating of the case packer in
        # cases per hour? And, what is the draw-down rate on the holding tank
        # in gallons/minute?
        canph = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "Cans/hr", "cph", "cans per hour", one12ozCan, msys.getHour())
        caseph = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "Case/hr", "caph", "cases per hour", fourPackCase, msys.getHour())
        gpm = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "gpm", "gpm", "gal per minute", msys.getUOM(Unit.US_GALLON), msys.getMinute())
        filler = Quantity(2000.0, canph)

        # draw-down
        draw = filler.convert(gpm)
        self.assertAlmostEqual(draw.amount, 3.125, None, None, TestUtils.DELTA6)

        # case production
        packer = filler.convert(caseph)
        self.assertAlmostEqual(packer.amount, 83.333333, None, None, TestUtils.DELTA6)

    def testGenericQuantity(self):
        msys = MeasurementSystem.instance()
        
        a = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "a", "aUOM", "A")

        b = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "b", "b", "B")
        b.setConversion(10.0, a)

        self.assertTrue(Quantity.createAmountFromString("4.0") == 4.0)

        # add
        q1 = Quantity(4.0, a)

        self.assertFalse(q1 is None)

        q2 = Quantity(4.0, b)
        q3 = q1.add(q2)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        
        self.assertTrue(q3.uom.abscissaUnit == a)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.amount, 44.0, None, None, TestUtils.DELTA6)

        # subtract
        q3 = q1.subtract(q2)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q3.uom.abscissaUnit == a)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.amount, -36.0, None, None, TestUtils.DELTA6)

        # multiply
        q3 = q1.multiply(q2)
        self.assertAlmostEqual(q3.amount, 16.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.scalingFactor, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.offset, 0.0, None, None, TestUtils.DELTA6)

        a2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "a*2", "a*2", "A squared", a, 2)
        q4 = q3.convert(a2)
        self.assertAlmostEqual(q4.amount, 160.0, None, None, TestUtils.DELTA6)
        self.assertTrue(q4.uom == a2)

        q4 = q3.divide(q2)
        self.assertTrue(q4 == q1)
        self.assertAlmostEqual(q4.amount, 4.0, None, None, TestUtils.DELTA6)

        # divide
        q3 = q1.divide(q2)
        self.assertAlmostEqual(q3.amount, 1.0, None, None, TestUtils.DELTA6)
        self.assertAlmostEqual(q3.uom.scalingFactor, 0.1, None, None, TestUtils.DELTA6)

        q4 = q3.multiply(q2)
        self.assertTrue(q4 == q1)

    def testExceptions(self):
        msys = MeasurementSystem.instance()
        
        floz = msys.getUOM(Unit.BR_FLUID_OUNCE)

        q1 = Quantity(10.0, msys.getDay())
        q2 = Quantity(10.0, msys.getUOM(Unit.BR_FLUID_OUNCE))

        try:
            Quantity.createAmountFromString(None)
            self.fail("create")
        except:
            pass

        try:
            q1.convert(floz)
            self.fail("convert")
        except:
            pass

        try:
            q1.add(q2)
            self.fail("add")
        except:
            pass

        try:
            q1.subtract(q2)
            self.fail("subtract")
        except:
            pass

        # OK
        q1.multiply(q2)

        # OK
        q1.divide(q2)

    def testEquality(self):
        msys = MeasurementSystem.instance()

        newton = msys.getUOM(Unit.NEWTON)
        metre = msys.getUOM(Unit.METRE)
        nm = msys.getUOM(Unit.NEWTON_METRE)
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        J = msys.getUOM(Unit.JOULE)

        q1 = Quantity(10.0, newton)
        q2 = Quantity(10.0, metre)
        q3 = Quantity(10.0, nm)
        q5 = Quantity(100.0, nm)

        # unity
        q4 = q5.divide(q3)
        self.assertTrue(q4.uom.getBaseSymbol() == msys.getOne().symbol)
        self.assertTrue(q4.amount == 10.0)

        # Newton-metre (Joules)
        q4 = q1.multiply(q2)
        self.assertTrue(q5.uom.getBaseSymbol() == q4.uom.getBaseSymbol())
        q6 = q5.convert(J)
        self.assertTrue(q6.amount == q4.amount)

        # Newton
        q5 = q4.divide(q2)
        self.assertTrue(q5.uom.getBaseSymbol() == q1.uom.getBaseSymbol())
        self.assertTrue(q5 == q1)

        # metre
        q5 = q4.divide(q1)
        self.assertTrue(q5.uom.getBaseSymbol() == q2.uom.getBaseSymbol())
        self.assertTrue(q5 == q2)

        # square metre
        q4 = q2.multiply(q2)
        q5 = Quantity(100.0, m2)
        self.assertTrue(q5 == q4)

        # metre
        q4 = q5.divide(q2)
        self.assertTrue(q4.uom.getBaseSymbol() == q2.uom.getBaseSymbol())
        self.assertTrue(q4 == q2)

    