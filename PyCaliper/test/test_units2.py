import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType, Constant, MeasurementType
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
        
    def testPowers(self):
        msys = MeasurementSystem.instance()

        minute = msys.getMinute()
        s = msys.getSecond()
        sm1 = s.invert()
        s2 = msys.getUOM(Unit.SQUARE_SECOND)
        min2 = msys.createPowerUOM(UnitType.TIME_SQUARED, None, "sqMin", "min'2", None, minute, 2)
        sqs = msys.createPowerUOM(UnitType.TIME_SQUARED, None, "sqSec", "s'2", None, s, 2)
        sminus1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None,"sminus1", "s'-1", None, s, -1)
        minminus1Q = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "minminus1Q", "minQ'-1", None, msys.getOne(), minute)
        minminus1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "minminus1", "min'-1", None, minute, -1)
        newton = msys.getUOM(Unit.NEWTON)
        newtonm1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "Nminus1", "N'-1", None, newton, -1)
        inch = msys.getUOM(Unit.INCH)
        ft = msys.getUOM(Unit.FOOT)
        ftm1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "ftm1", "ft'-1", None, ft, -1)
        inm1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "inm1", "in'-1", None, inch, -1)
        ui = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "ui", "ui", "")
        uj = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "uj", "uj", "")
        ixj = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "ixj", "ixj", "", ui, uj)
        oneOveri = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "oneOveri", "oneOveri", "", msys.getOne(), ui)
        oneOverj = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "oneOverj", "oneOverj", "", msys.getOne(), uj)
        ixjm1 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "ixjm1", "ixjm1", "", ixj, -1)
        hz = msys.getUOM(Unit.HERTZ)

        ij = oneOveri.multiply(oneOverj)
        self.assertTrue(ij.getBaseSymbol() == ixjm1.getBaseSymbol())

        bd = min2.getConversionFactor(s2)
        self.assertAlmostEqual(bd, 3600.0, None, None, TestingUtils.DELTA6)

        bd = s2.getConversionFactor(min2)
        self.assertAlmostEqual(bd, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        u = CacheManager.instance().getBaseUOM(sm1.symbol)
        self.assertTrue(u is not None)
        u = msys.getUOMBySymbol(sm1.getBaseSymbol())

        u = msys.getOne().divide(minute)
        bd = u.scalingFactor
        self.assertAlmostEqual(bd, 1.0/60.0, None, None, TestingUtils.DELTA6)
        
        bd = u.getConversionFactor(sm1)
        self.assertAlmostEqual(bd, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = ftm1.multiply(ft)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        u = ft.multiply(inm1)
        self.assertAlmostEqual(u.scalingFactor, 12.0, None, None, TestingUtils.DELTA6)

        u = inm1.multiply(ft)
        self.assertAlmostEqual(u.scalingFactor, 12.0, None, None, TestingUtils.DELTA6)

        u = s.multiply(minminus1)
        self.assertAlmostEqual(u.scalingFactor, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = minminus1.multiply(s)
        self.assertAlmostEqual(u.scalingFactor, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = s.multiply(minminus1Q)
        self.assertAlmostEqual(u.scalingFactor, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = minminus1Q.multiply(s)
        self.assertAlmostEqual(u.scalingFactor, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = ftm1.multiply(inch)
        self.assertAlmostEqual(u.scalingFactor, 1.0/12.0, None, None, TestingUtils.DELTA6)

        u = inch.multiply(ftm1)
        self.assertAlmostEqual(u.scalingFactor, 1.0/12.0, None, None, TestingUtils.DELTA6)

        u = newtonm1.multiply(newton)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        u = newton.multiply(newtonm1)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        u = minminus1.multiply(s)
        self.assertAlmostEqual(u.scalingFactor, 1.0/60.0, None, None, TestingUtils.DELTA6)

        CacheManager.instance().unregisterUOM(msys.getUOM(Unit.HERTZ))
        min1 = minute.invert()
        bd = min1.scalingFactor
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        bd = sqs.scalingFactor
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        u = sminus1.multiply(s)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        u = msys.getOne().divide(minute)
        bd = u.scalingFactor
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)
        bd = u.getConversionFactor(sm1)
        self.assertAlmostEqual(bd, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = msys.getOne().multiply(minute)
        bd = u.getConversionFactor(s)

        u = min2.divide(minute)
        t = u.unitType
        self.assertTrue(t == UnitType.TIME)

        u = minute.multiply(minute)
        self.assertAlmostEqual(u.scalingFactor, 3600.0, None, None, TestingUtils.DELTA6)
        
        self.assertTrue(u.abscissaUnit.getBaseSymbol() == s2.getBaseSymbol())
        self.assertAlmostEqual(u.offset, 0.0, None, None, TestingUtils.DELTA6)
        t = u.unitType
        self.assertTrue(t == UnitType.TIME_SQUARED)

        u2 = msys.getOne().divide(minute)
        self.assertAlmostEqual(u2.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)

        q1 = Quantity(1.0, u2)
        q2 = q1.convert(hz)

        self.assertAlmostEqual(q2.amount, 0.0166666666666667, None, None, TestingUtils.DELTA6)

        u = u2.multiply(u2)
        self.assertAlmostEqual(u.scalingFactor, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        q1 = Quantity(1.0, u)
        q2 = q1.convert(s2.invert())
        self.assertAlmostEqual(q2.amount, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        u2 = u2.divide(minute)
        q1 = Quantity(1.0, u2)
        q2 = q1.convert(s2.invert())
        self.assertAlmostEqual(q2.amount, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        u2 = u2.invert()
        self.assertTrue(u2.getBaseSymbol() == min2.getBaseSymbol())

        q1 = Quantity(10.0, u2)
        bd = u2.getConversionFactor(s2)
        self.assertAlmostEqual(bd, 3600.0, None, None, TestingUtils.DELTA6)

        q2 = q1.convert(s2)
        self.assertTrue(q2.uom == s2)
        self.assertAlmostEqual(q2.amount, 36000.0, None, None, TestingUtils.DELTA6)

        bd = minute.getConversionFactor(msys.getSecond())
        self.assertAlmostEqual(bd, 60.0, None, None, TestingUtils.DELTA6)

        u = q2.uom
        bd = u.getConversionFactor(min2)
        self.assertAlmostEqual(bd, 2.777777777777778E-4, None, None, TestingUtils.DELTA6)

        q2 = q2.convert(min2)
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestingUtils.DELTA6)

    def testInversions(self):
        msys = MeasurementSystem.instance()
        
        metre = msys.getUOM(Unit.METRE)

        uom = msys.createUnclassifiedPowerUOM(metre, -3)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, 2)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, -2)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, 2)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, 1)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, -1)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, -2)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)

        uom = msys.createUnclassifiedPowerUOM(metre, -4)
        inverted = uom.invert()
        u = uom.multiply(inverted)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().symbol)
        
    def testMedicalUnits(self):
        msys = MeasurementSystem.instance()
        
        # Equivalent
        eq = msys.getUOM(Unit.EQUIVALENT)
        litre = msys.getUOM(Unit.LITRE)
        mEqPerL = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "milliNormal", "mEq/L",
            "solute per litre of solvent ", msys.createPrefixedUOM(Prefix.milli(), eq), litre)
        testResult = Quantity(4.9, mEqPerL)
        self.assertAlmostEqual(testResult.amount, 4.9, None, None, TestingUtils.DELTA6)

        # Unit
        u = msys.getUOM(Unit.UNIT)
        katal = msys.getUOM(Unit.KATAL)
        q1 = Quantity(1.0, u)
        q2 = q1.convert(msys.createPrefixedUOM(Prefix.nano(), katal))
        self.assertAlmostEqual(q2.amount, 16.6666667, None, None, TestingUtils.DELTA6)

        # blood cell counts
        k = msys.createPrefixedUOM(Prefix.kilo(), msys.getOne())
        uL = msys.createPrefixedUOM(Prefix.micro(), msys.getUOM(Unit.LITRE))
        kul = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "K/uL", "K/uL",
            "thousands per microlitre", k, uL)
        testResult = Quantity(6.6, kul)
        self.assertAlmostEqual(testResult.amount, 6.6, None, None, TestingUtils.DELTA6)

        fL = msys.createPrefixedUOM(Prefix.femto(), msys.getUOM(Unit.LITRE))
        testResult = Quantity(90.0, fL)
        self.assertAlmostEqual(testResult.amount, 90.0, None, None, TestingUtils.DELTA6)

        # TSH
        uIU = msys.createPrefixedUOM(Prefix.micro(), msys.getUOM(Unit.INTERNATIONAL_UNIT))
        mL = msys.createPrefixedUOM(Prefix.milli(), msys.getUOM(Unit.LITRE))
        uiuPerml = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "uIU/mL", "uIU/mL",
            "micro IU per millilitre", uIU, mL)
        testResult = Quantity(2.11, uiuPerml)
        self.assertAlmostEqual(testResult.amount, 2.11, None, None, TestingUtils.DELTA6)

    def testCategory(self):
        msys = MeasurementSystem.instance()
        
        category = "category"
        m = msys.getUOM(Unit.METRE)
        m.category = category
        self. assertTrue(m.category == category)
    
    def testMeasurementTypes(self):
        msys = MeasurementSystem.instance()
        
        m = msys.getUOM(Unit.METRE)
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        n = msys.getUOM(Unit.NEWTON_METRE)
        a = msys.getUOM(Unit.SQUARE_METRE)

        self.assertTrue(m.getMeasurementType() == MeasurementType.SCALAR)
        self.assertTrue(mps.getMeasurementType() == MeasurementType.QUOTIENT)
        self.assertTrue(n.getMeasurementType() == MeasurementType.PRODUCT)
        self.assertTrue(a.getMeasurementType() == MeasurementType.POWER)

    def testScaling(self):
        msys = MeasurementSystem.instance()
        
        # test scaling factors
        second = msys.getSecond()
        minute = msys.getMinute()
        s2 = msys.getUOM(Unit.SQUARE_SECOND)
        msec = msys.createPrefixedUOM(Prefix.milli(), second)
        k = msys.getUOM(Unit.KELVIN)
        r = msys.getUOM(Unit.RANKINE)
        m = msys.getUOM(Unit.METRE)
        km = msys.createPrefixedUOM(Prefix.kilo(), m)

        sf = m.getConversionFactor(km)
        self.assertAlmostEqual(sf, 0.001, None, None, TestingUtils.DELTA6)

        kinv = k.invert()
        sf = kinv.scalingFactor
        self.assertTrue(sf == 1.0)

        sf = r.getConversionFactor(k)
        self.assertAlmostEqual(sf, 5.0 / 9.0, None, None, TestingUtils.DELTA6)

        sf = k.getConversionFactor(r)
        self.assertAlmostEqual(sf, 1.8, None, None, TestingUtils.DELTA6)

        sf = second.getConversionFactor(msec)
        self.assertAlmostEqual(sf, 1000.0, None, None, TestingUtils.DELTA6)

        sf = minute.scalingFactor
        self.assertTrue(sf == 60.0)

        # inversions
        mininv = minute.invert()
        sf = mininv.scalingFactor
        self.assertTrue(sf == 1.0)
        sf = mininv.getConversionFactor(msys.getUOM(Unit.HERTZ))
        self.assertTrue(sf == 1.0 / 60.0)

        # quotient UOM
        q = msys.createUnclassifiedQuotientUOM(msys.getOne(), minute)
        sf = q.scalingFactor
        self.assertTrue(sf == 1.0)

        # power UOM
        p = msys.createUnclassifiedPowerUOM(minute, -1)
        sf = p.scalingFactor
        self.assertTrue(sf == 1.0)

        sf = p.getConversionFactor(msys.getUOM(Unit.HERTZ))
        self.assertTrue(sf == 1.0 / 60.0)

        u = p.invert()
        sf = u.scalingFactor
        self.assertTrue(sf == 60.0)

        sf = minute.getConversionFactor(u)
        self.assertAlmostEqual(sf, 1.0, None, None, TestingUtils.DELTA6)

        sf = u.getConversionFactor(minute)
        self.assertAlmostEqual(sf, 1.0, None, None, TestingUtils.DELTA6)

        min2 = mininv.invert()
        sf = min2.scalingFactor
        self.assertTrue(sf == 60.0)

        # divisions
        perMin = msys.getOne().divide(minute)

        num = perMin.getDividend()
        denom = perMin.getDivisor()
        min2 = denom.divide(num)
        sf = min2.scalingFactor
        self.assertTrue(sf == 60.0)

        sf = perMin.scalingFactor
        self.assertTrue(sf == 1.0 / 60.0)

        perMin1 = perMin.divide(msys.getOne())
        self.assertTrue(perMin1 == perMin)

        min2 = perMin.invert()
        sf = min2.scalingFactor
        self.assertTrue(sf == 60.0)

        min2 = msys.getOne().divide(perMin)
        sf = min2.scalingFactor
        self.assertTrue(sf == 60.0)

        count = 4
        inversions = [None]*(count + 1)
        divides = [None]*(count + 1)

        inversions[0] = minute
        divides[0] = minute
        for i in range(count):
            inversions[i + 1] = inversions[i].invert()
            divides[i + 1] = msys.getOne().divide(divides[i])
    
        sf = inversions[count].scalingFactor
        self.assertTrue(sf == 60.0)

        for i in range(count, 0, -1):
            last = divides[i].invert()
        
        self.assertTrue(last == minute)

        # multiply
        minsq = minute.multiply(minute)
        sf = minsq.scalingFactor
        self.assertTrue(sf == 3600.0)

        sf = minsq.getConversionFactor(s2)
        self.assertAlmostEqual(sf, 3600.0, None, None, TestingUtils.DELTA6)

        sf = s2.getConversionFactor(minsq)
        self.assertAlmostEqual(sf, 1.0 / 3600.0, None, None, TestingUtils.DELTA6)

        # power of 2
        p2 = msys.createUnclassifiedPowerUOM(minute, 2)
        sf = p2.scalingFactor
        self.assertTrue(sf == 1.0)

        sf = p2.getConversionFactor(s2)
        self.assertTrue(sf == 3600.0)

        sf = p2.getConversionFactor(minsq)
        self.assertTrue(sf == 1.0)

        sf = minsq.getConversionFactor(p2)
        self.assertTrue(sf == 1.0)

    def testPerm(self):
        msys = MeasurementSystem.instance()
        
        inHg = msys.getUOM(Unit.IN_HG)
        hr = msys.getUOM(Unit.HOUR)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)
        s = msys.getUOM(Unit.SECOND)
        day = msys.getUOM(Unit.DAY)
        msq = msys.getUOM(Unit.SQUARE_METRE)
        Pa = msys.getUOM(Unit.PASCAL)
        ng = msys.createPrefixedUOM(Prefix.nano(), msys.getUOM(Unit.GRAM))
        g = msys.getUOM(Unit.GRAM)
        grain = msys.getUOM(Unit.GRAIN)

        mmHg = msys.createScalarUOM(UnitType.PRESSURE, None, "mmHg", "mmHg", "")
        mmHg.setConversion(133.3223684, Pa)

        # US perm
        us1 = msys.createUnclassifiedQuotientUOM(grain, inHg)      
        us2 = msys.createUnclassifiedQuotientUOM(us1, ft2)
        perm = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "perm", "perm", "gn/hr/ft2/inHg", us2, hr)
    
        # metric perm
        m1 = msys.createUnclassifiedQuotientUOM(g, day)
        m2 = msys.createUnclassifiedQuotientUOM(m1, msq)
        mperm = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "mperm", "mperm", "g/day/m2/mmHg", m2, mmHg)        
        
        # Equivalent SI unit
        si1 = msys.createUnclassifiedQuotientUOM(ng, s)
        si2 = msys.createUnclassifiedQuotientUOM(si1, msq)
        eqSI = msys.createUnclassifiedQuotientUOM(si2, Pa)
        eqSI = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "eqSI", "eqSI", "equivalent SI", si2, Pa)  

        # US perm to equivalent SI
        f = perm.getConversionFactor(eqSI)
        self.assertAlmostEqual(f, 57.214184, None, None, TestingUtils.DELTA6)
        f = eqSI.getConversionFactor(perm)
        self.assertAlmostEqual(f, 0.0174781, None, None, TestingUtils.DELTA6)    
        
        # metric perm to US perm
        f = perm.getConversionFactor(mperm)
        self.assertAlmostEqual(f, 0.659053, None, None, TestingUtils.DELTA6)
        f = mperm.getConversionFactor(perm)
        self.assertAlmostEqual(f, 1.517328, None, None, TestingUtils.DELTA6)        
        
        # metric perm to equivalent SI
        f = mperm.getConversionFactor(eqSI)
        self.assertAlmostEqual(f, 86.812694, None, None, TestingUtils.DELTA6)
        f = eqSI.getConversionFactor(mperm)
        self.assertAlmostEqual(f, 0.0115190, None, None, TestingUtils.DELTA6)        
    