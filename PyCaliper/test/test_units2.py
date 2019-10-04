import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.cache_manager import CacheManager

class TestUnits2(unittest.TestCase):
    def testConversions1(self):
        msys = MeasurementSystem.instance()
        
        m = msys.getUOM(Unit.METRE)
        cm = msys.createPrefixedUOM(Prefix.centi(), m)
        N = msys.getUOM(Unit.NEWTON)
        Nm = msys.getUOM(Unit.NEWTON_METRE)
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        sqm = msys.getUOM(Unit.SQUARE_METRE)
        mm = msys.createProductUOM(UnitType.AREA, None, "mxm", "mTimesm", "", m, m)
        mcm = msys.createProductUOM(UnitType.AREA, None, "mxcm", "mxcm", "", m, cm)
        s2 = msys.getUOM(Unit.SQUARE_SECOND)
        
        minOverSec = msys.createQuotientUOM(UnitType.TIME, None, "minsec", "min/sec", "", msys.getMinute(),
                msys.getSecond())

        minOverSecTimesSec = msys.createProductUOM(UnitType.TIME, None, "minOverSecTimesSec",
                "minOverSecTimesSec", "minOverSecTimesSec", minOverSec, msys.getSecond())

        inch = msys.getUOM(Unit.INCH)
        ft = msys.getUOM(Unit.FOOT)
        lbf = msys.getUOM(Unit.POUND_FORCE)
        fph = msys.createQuotientUOM(UnitType.VELOCITY, None, "fph", "ft/hr", "feet per hour", ft, msys.getHour())
        ftlb = msys.getUOM(Unit.FOOT_POUND_FORCE)
        sqft = msys.getUOM(Unit.SQUARE_FOOT)

        oneDivSec = msys.getOne().divide(msys.getSecond())
        inverted = oneDivSec.invert()
        self.assertTrue(inverted == msys.getSecond())

        perSec = msys.createPowerUOM(UnitType.TIME, None, "per second", "perSec", "desc", msys.getSecond(), -1)
        mult = perSec.multiply(msys.getUOM(Unit.SECOND))
        self.assertTrue(mult.getBaseSymbol() == msys.getUOM(Unit.ONE).symbol)

        u = msys.getSecond().invert()
        self.assertTrue(u.scalingFactor == oneDivSec.scalingFactor)

        inverted = u.invert()
        self.assertTrue(inverted == msys.getSecond())

        oneOverSec = CacheManager.instance().getBaseUOM("1/s")
        self.assertTrue(oneOverSec.getBaseSymbol() == oneDivSec.getBaseSymbol())

        inverted = oneOverSec.invert()
        self.assertTrue(inverted.getBaseSymbol() == msys.getSecond().getBaseSymbol())

        minTimesSec = msys.createProductUOM(UnitType.TIME_SQUARED, None, "minsec", "minxsec",
                "minute times a second", msys.getMinute(), msys.getSecond())

        sqMin = msys.getUOM("min^2")
        if (sqMin is None):
            sqMin = msys.createPowerUOM(UnitType.TIME_SQUARED, None, "square minute", "min^2", None, 
                msys.getUOM(Unit.MINUTE), 2)

        perMin = msys.createPowerUOM(UnitType.TIME, None, "per minute", "perMin", None, msys.getMinute(), -1)

        perMin2 = msys.createPowerUOM(UnitType.TIME, None, "per minute squared", "perMin^2", None,
            msys.getMinute(), -2)

        u = perMin2.invert()
        self.assertTrue(u.getBaseSymbol() == sqMin.getBaseSymbol())

        u = perMin.invert()
        bd = u.getConversionFactor(msys.getMinute())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = u.getConversionFactor(msys.getSecond())
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

        try:
            m.getConversionFactor(None)
            self.fail("None")
        except:
            pass

        try:
            m.multiply(None)
            self.fail("None")
        except:
            pass

        # scalar
        bd = m.getConversionFactor(m)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(m == m)

        bd = m.getConversionFactor(cm)
        self.assertAlmostEqual(bd, 100.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(m == m)
        self.assertTrue(cm == cm)
        self.assertTrue(m != cm)

        bd = m.getConversionFactor(cm)
        self.assertAlmostEqual(bd, 100.0, None, None, TestingUtils.DELTA6)

        bd = cm.getConversionFactor(m)
        self.assertAlmostEqual(bd, 0.01, None, None, TestingUtils.DELTA6)

        bd = m.getConversionFactor(cm)
        self.assertAlmostEqual(bd, 100.0, None, None, TestingUtils.DELTA6)

        bd = m.getConversionFactor(inch)
        self.assertAlmostEqual(bd, 39.37007874015748, None, None, TestingUtils.DELTA6)

        bd = inch.getConversionFactor(m)
        self.assertAlmostEqual(bd, 0.0254, None, None, TestingUtils.DELTA6)

        bd = m.getConversionFactor(ft)
        self.assertAlmostEqual(bd, 3.280839895013123, None, None, TestingUtils.DELTA6)

        bd = ft.getConversionFactor(m)
        self.assertAlmostEqual(bd, 0.3048, None, None, TestingUtils.DELTA6)

        g = msys.getQuantity(Constant.GRAVITY).convert(msys.getUOM(Unit.FEET_PER_SEC_SQUARED))
        self.assertAlmostEqual(g.amount, 32.17404855, None, None, TestingUtils.DELTA6)

        bd = lbf.getConversionFactor(N)
        self.assertAlmostEqual(bd, 4.448221615, None, None, TestingUtils.DELTA6)

        bd = N.getConversionFactor(lbf)
        self.assertAlmostEqual(bd, 0.2248089430997105, None, None, TestingUtils.DELTA6)

        # product
        bd = Nm.getConversionFactor(ftlb)
        self.assertAlmostEqual(bd, 0.7375621492772656, None, None, TestingUtils.DELTA6)

        bd = ftlb.getConversionFactor(Nm)
        self.assertAlmostEqual(bd, 1.3558179483314004, None, None, TestingUtils.DELTA6)

        # quotient
        one = msys.getOne()
        bd = minOverSec.getConversionFactor(one)
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

        bd = one.getConversionFactor(minOverSec)
        self.assertAlmostEqual(bd, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        bd = mps.getConversionFactor(fph)
        self.assertAlmostEqual(bd, 11811.02362204724, None, None, TestingUtils.DELTA6)

        bd = fph.getConversionFactor(mps)
        self.assertAlmostEqual(bd, 8.46666666666667E-05, None, None, TestingUtils.DELTA6)

        # power
        bd = sqm.getConversionFactor(sqft)
        self.assertAlmostEqual(bd, 10.76391041670972, None, None, TestingUtils.DELTA6)

        bd = sqft.getConversionFactor(sqm)
        self.assertAlmostEqual(bd, 0.09290304, None, None, TestingUtils.DELTA6)

        # mixed
        bd = mm.getConversionFactor(sqm)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = sqm.getConversionFactor(mm)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = mcm.getConversionFactor(sqm)
        self.assertAlmostEqual(bd, 0.01, None, None, TestingUtils.DELTA6)

        bd = sqm.getConversionFactor(mcm)
        self.assertAlmostEqual(bd, 100.0, None, None, TestingUtils.DELTA6)

        bd = minTimesSec.getConversionFactor(s2)
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

        bd = s2.getConversionFactor(minTimesSec)
        self.assertAlmostEqual(bd, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        bd = minTimesSec.getConversionFactor(sqMin)
        self.assertAlmostEqual(bd, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        bd = sqMin.getConversionFactor(minTimesSec)
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

        bd = minOverSecTimesSec.getConversionFactor(msys.getSecond())
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

    def testConversions2(self):
        msys = MeasurementSystem.instance()

        CacheManager.instance().unregisterUOM(msys.getUOM(Unit.CUBIC_INCH))
        
        ft = msys.getUOM(Unit.FOOT)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)
        ft3 = msys.getUOM(Unit.CUBIC_FOOT)

        cubicFt = ft2.multiply(ft)
        bd = cubicFt.getConversionFactor(ft3)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        m3 = msys.getUOM(Unit.CUBIC_METRE)
        degree = msys.getUOM(Unit.DEGREE)
        arcsec = msys.getUOM(Unit.ARC_SECOND)
        radian = msys.getUOM(Unit.RADIAN)
        kgPerM3 = msys.getUOM(Unit.KILOGRAM_PER_CU_METRE)
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        pascal = msys.getUOM(Unit.PASCAL)
        s2 = msys.getUOM(Unit.SQUARE_SECOND)
        joule = msys.getUOM(Unit.JOULE)
        rpm = msys.getUOM(Unit.REV_PER_MIN)
        rps = msys.getUOM(Unit.RAD_PER_SEC)
        m3s = msys.getUOM(Unit.CUBIC_METRE_PER_SEC)
        ms2 = msys.getUOM(Unit.METRE_PER_SEC_SQUARED)

        lbm = msys.getUOM(Unit.POUND_MASS)
        acreFoot = msys.createProductUOM(UnitType.VOLUME, None, "acreFoot", "ac-ft", "", msys.getUOM(Unit.ACRE),
                msys.getUOM(Unit.FOOT))
        lbmPerFt3 = msys.createQuotientUOM(UnitType.DENSITY, None, "lbmPerFt3", "lbm/ft^3", None, lbm, ft3)
        fps = msys.getUOM(Unit.FEET_PER_SEC)
        knot = msys.getUOM(Unit.KNOT)
        btu = msys.getUOM(Unit.BTU)

        miphs = msys.createScalarUOM(UnitType.ACCELERATION, None, "mph/sec", "mi/hr-sec",
            "mile per hour per second")
        miphs.setConversion(1.466666666666667, msys.getUOM(Unit.FEET_PER_SEC_SQUARED))

        inHg = msys.createScalarUOM(UnitType.PRESSURE, None, "inHg", "inHg", "inHg")
        inHg.setConversion(3386.389, pascal)

        atm = Quantity(1.0, msys.getUOM(Unit.ATMOSPHERE)).convert(msys.getUOM(Unit.PASCAL))
        self.assertAlmostEqual(atm.amount, 101325, None, None, TestingUtils.DELTA6)

        ft2ft = msys.createProductUOM(UnitType.VOLUME, None, "ft2ft", "ft2ft", None, ft2, ft)

        hrsec = msys.createScalarUOM(UnitType.TIME_SQUARED, None, "", "hr.sec", "")
        hrsec.setConversion(3600.0, msys.getUOM(Unit.SQUARE_SECOND))
        bd = hrsec.getConversionFactor(s2)
        self.assertAlmostEqual(bd, 3600.0, None, None, TestingUtils.DELTA6)

        bd = s2.getConversionFactor(hrsec)
        self.assertAlmostEqual(bd, 2.777777777777778E-04, None, None, TestingUtils.DELTA6)

        bd = ft2ft.getConversionFactor(m3)
        self.assertAlmostEqual(bd, 0.028316846592, None, None, TestingUtils.DELTA6)

        bd = m3.getConversionFactor(ft2ft)
        self.assertAlmostEqual(bd, 35.31466672148859, None, None, TestingUtils.DELTA6)

        bd = acreFoot.getConversionFactor(m3)
        self.assertAlmostEqual(bd, 1233.48183754752, None, None, TestingUtils.DELTA6)

        bd = m3.getConversionFactor(acreFoot)
        self.assertAlmostEqual(bd, 8.107131937899125E-04, None, None, TestingUtils.DELTA6)

        bd = degree.getConversionFactor(radian)
        self.assertAlmostEqual(bd, 0.01745329251994329, None, None, TestingUtils.DELTA6)

        bd = radian.getConversionFactor(degree)
        self.assertAlmostEqual(bd, 57.29577951308264, None, None, TestingUtils.DELTA6)

        bd = arcsec.getConversionFactor(degree)
        self.assertAlmostEqual(bd, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        bd = degree.getConversionFactor(arcsec)
        self.assertAlmostEqual(bd, 3600.0, None, None, TestingUtils.DELTA6)

        bd = lbmPerFt3.getConversionFactor(kgPerM3)
        self.assertAlmostEqual(bd, 16.01846337, None, None, TestingUtils.DELTA6)

        bd = kgPerM3.getConversionFactor(lbmPerFt3)
        self.assertAlmostEqual(bd, 0.0624279605915783, None, None, TestingUtils.DELTA6)

        bd = rpm.getConversionFactor(rps)
        self.assertAlmostEqual(bd, 0.104719755, None, None, TestingUtils.DELTA6)

        bd = rps.getConversionFactor(rpm)
        self.assertAlmostEqual(bd, 9.549296596425383, None, None, TestingUtils.DELTA6)

        bd = mps.getConversionFactor(fps)
        self.assertAlmostEqual(bd, 3.280839895013123, None, None, TestingUtils.DELTA6)

        bd = fps.getConversionFactor(mps)
        self.assertAlmostEqual(bd, 0.3048, None, None, TestingUtils.DELTA6)

        bd = knot.getConversionFactor(mps)
        self.assertAlmostEqual(bd, 0.5147733333333333, None, None, TestingUtils.DELTA6)

        bd = mps.getConversionFactor(knot)
        self.assertAlmostEqual(bd, 1.942602569415665, None, None, TestingUtils.DELTA6)

        usGal = msys.getUOM(Unit.US_GALLON)
        gph = msys.createQuotientUOM(UnitType.VOLUMETRIC_FLOW, None, "gph", "gal/hr", "gallons per hour", usGal,
            msys.getHour())

        bd = gph.getConversionFactor(m3s)
        self.assertAlmostEqual(bd, 1.051503273E-06, None, None, TestingUtils.DELTA6)

        bd = m3s.getConversionFactor(gph)
        self.assertAlmostEqual(bd, 951019.3884893342, None, None, TestingUtils.DELTA6)

        bd = miphs.getConversionFactor(ms2)
        self.assertAlmostEqual(bd, 0.44704, None, None, TestingUtils.DELTA6)

        bd = ms2.getConversionFactor(miphs)
        self.assertAlmostEqual(bd, 2.236936292054402, None, None, TestingUtils.DELTA6)

        bd = pascal.getConversionFactor(inHg)
        self.assertAlmostEqual(bd, 2.952998016471232E-04, None, None, TestingUtils.DELTA6)

        bd = inHg.getConversionFactor(pascal)
        self.assertAlmostEqual(bd, 3386.389, None, None, TestingUtils.DELTA6)

        bd = atm.convert(inHg).amount
        self.assertAlmostEqual(bd, 29.92125240189478, None, None, TestingUtils.DELTA6)

        bd = inHg.getConversionFactor(atm.uom)
        self.assertAlmostEqual(bd, 3386.389, None, None, TestingUtils.DELTA6)

        bd = btu.getConversionFactor(joule)
        self.assertAlmostEqual(bd, 1055.05585262, None, None, TestingUtils.DELTA6)

        bd = joule.getConversionFactor(btu)
        self.assertAlmostEqual(bd, 9.478171203133172E-04, None, None, TestingUtils.DELTA6)

    def testConversions3(self):
        msys = MeasurementSystem.instance()

        weber = msys.getUOM(Unit.WEBER)
        coulomb = msys.getUOM(Unit.COULOMB)
        second = msys.getSecond()
        volt = msys.getUOM(Unit.VOLT)
        watt = msys.getUOM(Unit.WATT)
        amp = msys.getUOM(Unit.AMPERE)
        farad = msys.getUOM(Unit.FARAD)
        ohm = msys.getUOM(Unit.OHM)
        henry = msys.getUOM(Unit.HENRY)
        sr = msys.getUOM(Unit.STERADIAN)
        cd = msys.getUOM(Unit.CANDELA)
        lumen = msys.getUOM(Unit.LUMEN)
        gray = msys.getUOM(Unit.GRAY)
        sievert = msys.getUOM(Unit.SIEVERT)

        weberPerSec = msys.createQuotientUOM(UnitType.ELECTROMOTIVE_FORCE, None, "W/s", "W/s", None, weber,
                second)
        weberPerAmp = msys.createQuotientUOM(UnitType.ELECTRIC_INDUCTANCE, None, "W/A", "W/A", None, weber, amp)
        fTimesV = msys.createProductUOM(UnitType.ELECTRIC_CHARGE, None, "FxV", "FxV", None, farad, volt)
        WPerAmp = msys.createQuotientUOM(UnitType.ELECTROMOTIVE_FORCE, None, "Watt/A", "Watt/A", None, watt,
                amp)
        VPerA = msys.createQuotientUOM(UnitType.ELECTRIC_RESISTANCE, None, "V/A", "V/A", None, volt, amp)
        CPerV = msys.createQuotientUOM(UnitType.ELECTRIC_CAPACITANCE, None, "C/V", "C/V", None, coulomb, volt)
        VTimesSec = msys.createProductUOM(UnitType.MAGNETIC_FLUX, None, "Vxs", "Vxs", None, volt, second)
        cdTimesSr = msys.createProductUOM(UnitType.LUMINOUS_FLUX, None, "cdxsr", "cdxsr", None, cd, sr)

        bd = fTimesV.getConversionFactor(coulomb)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = coulomb.getConversionFactor(fTimesV)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = weberPerSec.getConversionFactor(volt)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = volt.getConversionFactor(weberPerSec)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = volt.getConversionFactor(WPerAmp)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = WPerAmp.getConversionFactor(volt)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = ohm.getConversionFactor(VPerA)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = VPerA.getConversionFactor(ohm)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = farad.getConversionFactor(CPerV)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = CPerV.getConversionFactor(farad)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = weber.getConversionFactor(VTimesSec)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = VTimesSec.getConversionFactor(weber)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = henry.getConversionFactor(weberPerAmp)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = weberPerAmp.getConversionFactor(henry)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = lumen.getConversionFactor(cdTimesSr)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = cdTimesSr.getConversionFactor(lumen)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        try:
            bd = gray.getConversionFactor(sievert)
            self.fail("No conversion")
        except:
            pass

        try:
            bd = sievert.getConversionFactor(gray)
            self.fail("No conversion")
        except:
            pass

    def testConversions4(self):
        msys = MeasurementSystem.instance()

        K = msys.getUOM(Unit.KELVIN)
        C = msys.getUOM(Unit.CELSIUS)

        R = msys.getUOM(Unit.RANKINE)
        F = msys.getUOM(Unit.FAHRENHEIT)

        fiveNinths = 5.0 / 9.0
        nineFifths = 1.8

        # K to C
        bd = K.getConversionFactor(C)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = C.getConversionFactor(K)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        # R to F
        bd = R.getConversionFactor(F)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = F.getConversionFactor(R)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        # C to F
        bd = F.getConversionFactor(C)
        self.assertAlmostEqual(bd, fiveNinths, None, None, TestingUtils.DELTA6)

        bd = C.getConversionFactor(F)
        self.assertAlmostEqual(bd, nineFifths, None, None, TestingUtils.DELTA6)

        # K to R
        bd = K.getConversionFactor(R)
        self.assertAlmostEqual(bd, nineFifths, None, None, TestingUtils.DELTA6)

        bd = F.getConversionFactor(K)
        self.assertAlmostEqual(bd, fiveNinths, None, None, TestingUtils.DELTA6)

        # invert diopters to metre
        qFrom = Quantity(10.0, msys.getUOM(Unit.DIOPTER))
        inverted = qFrom.invert()
        self.assertAlmostEqual(inverted.amount, 0.1, None, None, TestingUtils.DELTA6)

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "t*4", "t*4", "", K, 4)
        self.assertTrue(u is not None)

        try:
            u = C.multiply(C)
            self.fail("Can't multiply Celcius")
        except:
            pass

        u = K.divide(K)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        # hectare to acre
        ha = msys.getUOM(Unit.HECTARE)
        qFrom = Quantity(1.0, ha)
        to = qFrom.convert(msys.getUOM(Unit.ACRE))
        self.assertAlmostEqual(to.amount, 2.47105, None, None, TestingUtils.DELTA5)

    def testPerformance(self):
        msys = MeasurementSystem.instance()
        its = 500

        metre = msys.getUOM(Unit.METRE)
        cm = msys.createPrefixedUOM(Prefix.centi(), msys.getUOM(Unit.METRE))
        ft = msys.getUOM(Unit.FOOT)

        q1 = Quantity(10.0, metre)
        q2 = Quantity(2.0, cm)

        for _i in range(its):
            q1.add(q2)

        for _i in range(its):
            q1.subtract(q2)

        for _i in range(its):
            q1.multiply(q2)

        for _i in range(its):
            q1.divide(q2)

        for _i in range(its):
            q1.convert(ft)

    def testScaledUnits(self):
        msys = MeasurementSystem.instance()

        m = msys.getUOM(Unit.METRE)

        # mega metre
        mm = msys.createPrefixedUOM(Prefix.mega(), m)

        qmm = Quantity(1.0, mm)
        qm = qmm.convert(m)
        self.assertAlmostEqual(qm.amount, 1.0E+06, None, None, TestingUtils.DELTA5)

        mm2 = msys.createPrefixedUOM(Prefix.mega(), m)
        self.assertTrue(mm == mm2)

        # centilitre
        litre = msys.getUOM(Unit.LITRE)
        cL = msys.createPrefixedUOM(Prefix.centi(), litre)
        qL = Quantity(1.0, litre)
        qcL = qL.convert(cL)
        self.assertAlmostEqual(qcL.amount, 100.0, None, None, TestingUtils.DELTA5)

        # a mega buck
        buck = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "buck", "$", "one US dollar")
        megabuck = msys.createPrefixedUOM(Prefix.mega(), buck)
        qmb = Quantity(10.0, megabuck)
        qb = qmb.convert(buck)
        self.assertAlmostEqual(qb.amount, 1.0E+07, None, None, TestingUtils.DELTA5)

        # kilogram vs. scaled gram
        kgm = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.GRAM))
        kg = msys.getUOM(Unit.KILOGRAM)
        self.assertTrue(kgm == kg)

        # kilo and megabytes
        kiB = msys.createPrefixedUOM(Prefix.kibi(), msys.getUOM(Unit.BYTE))
        miB = msys.createPrefixedUOM(Prefix.mebi(), msys.getUOM(Unit.BYTE))
        qmB = Quantity(1.0, miB)
        qkB = qmB.convert(kiB)
        self.assertAlmostEqual(qkB.amount, 1024.0, None, None, TestingUtils.DELTA5)
