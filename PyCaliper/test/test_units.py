import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.unit_of_measure import Reducer

class TestUnits(unittest.TestCase):
    def testBaseUnits(self):
        msys = MeasurementSystem.instance()
        
        terms = msys.getUOM(Unit.NEWTON).getBaseUnitsOfMeasure()
        self.assertTrue(len(terms)== 3)

        for entry in terms.items():
            if (entry[0].unitType == UnitType.MASS):
                self.assertTrue(entry[1] == 1)
            elif (entry[0].unitType == UnitType.TIME):
                self.assertTrue(entry[1] == -2)
            elif (entry[0].unitType == UnitType.LENGTH):
                self.assertTrue(entry[1] == 1)

        m = msys.getUOM(Unit.METRE)
        m2 = msys.createUnclassifiedPowerUOM(m, 2)
        self.assertTrue(m2.getPowerExponent() == 2)
        
    def testPrefixes(self):
        _milli = Prefix.milli()
        _kilo = Prefix.kilo()
        _nano = Prefix.nano()
        
        for prefix in Prefix.prefixes:
            self.assertTrue(len(prefix.name) > 0)
            self.assertTrue(len(prefix.symbol) > 0)
            self.assertTrue(prefix.factor != 1.0)
            self.assertTrue(len(str(prefix)) > 0)
            self.assertTrue(Prefix.fromName(prefix.name) == prefix)
            
    def testExceptions(self):
        msys = MeasurementSystem.instance()

        uom1 =  msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "uom1", "uom1", "")
        uom2 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "uom2", "uom2", "")
        uom3 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "uom3", "uom3", "")

        uom1.setConversion(1.0, uom3, 10.0)
        uom2.setConversion(1.0, uom3, 1.0)
        self.assertFalse(uom1 == uom2)

        try:
            msys.createUnclassifiedPowerUOM(None, 0)
            self.fail()
        except:
            pass

        try:
            msys.createUnclassifiedProductUOM(None, msys.getOne())
            self.fail()
        except:
            pass

        try:
            msys.createUnclassifiedProductUOM(msys.getOne(), None)
            self.fail()
        except:
            pass

        try:
            msys.createUnclassifiedProductUOM(None, msys.getOne())
            self.fail()
        except:
            pass

        try:
            msys.createUnclassifiedProductUOM(msys.getOne(), None)
            self.fail()
        except:
            pass

        try:
            msys.createQuotientUOM(UnitType.UNCLASSIFIED, "uom4", "uom4", "", msys.getUOM(Unit.METRE), None)
            self.fail()
        except:
            pass

        try:
            msys.createQuotientUOM(UnitType.UNCLASSIFIED, "uom4", "uom4", "", None, msys.getUOM(Unit.METRE))
            self.fail()
        except:
            pass

        try:
            msys.createProductUOM(UnitType.UNCLASSIFIED, "uom4", "uom4", "", msys.getUOM(Unit.METRE), None)
            self.fail()
        except:
            pass

        try:
            msys.createProductUOM(UnitType.UNCLASSIFIED, "uom4", "uom4", "", None, msys.getUOM(Unit.METRE))
            self.fail()
        except:
            pass

        try:
            q = Quantity(10.0, msys.getUOM(Unit.METRE))
            q.convert(msys.getUOM(Unit.SECOND))
            self.fail("no conversion")
        except:
            pass

        CacheManager.instance().unregisterUOM(None)

        try:
            msys.createScalarUOM(UnitType.UNCLASSIFIED, "456", None, "description")
            self.fail("no symbol")
        except:
            pass

        try:
            msys.createScalarUOM(UnitType.UNCLASSIFIED, "456", "", "description")
            self.fail("no symbol")
        except:
            pass

        try:
            msys.createProductUOM(UnitType.UNCLASSIFIED, None, "abcd", "", None, None)
            self.fail("None")
        except:
            pass

        try:
            msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "abcd", "", None, None)
            self.fail("None")
        except:
            pass

        try:
            msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "abcd", "", None, 2)
            self.fail("None")
        except:
            pass

        try:
            msys.createScalarUOM(None, "1/1", "1/1", "")
            self.fail("no type")
        except:
            pass

        try:
            msys.createScalarUOM(UnitType.UNCLASSIFIED, "", None, "")
            msys.createScalarUOM(UnitType.UNCLASSIFIED, "", "", "")
            self.fail("already created")
        except:
            pass

        u = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "1/1", "1/1", "", msys.getOne(), msys.getOne())
        q1 = Quantity(10.0, u)
        q2 = q1.convert(msys.getOne())
        self.assertAlmostEqual(q2.amount, 10.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(q2.uom == msys.getOne())

        u = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "1x1", "1x1", "", msys.getOne(), msys.getOne())
        bd = u.getConversionFactor(msys.getOne())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        u = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "1x1", "1x1", "", msys.getOne(), msys.getOne())
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "1^2", "1^2", "", msys.getOne(), 2)
        bd = u.getConversionFactor(msys.getOne())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "1^2", "1^2", "", msys.getOne(), 2)
        bd = u.getConversionFactor(msys.getOne())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "1^0", "1^0", "", msys.getOne(), 0)
        bd = u.getConversionFactor(msys.getOne())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "1^0", "1^0", "", msys.getOne(), 0)
        bd = u.getConversionFactor(msys.getOne())
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)

        uno = msys.getOne()
        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m^0", "m^0", "", msys.getUOM(Unit.METRE), 0)
        bd = u.getConversionFactor(uno)
        self.assertAlmostEqual(bd, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        m1 = msys.getUOM(Unit.METRE)
        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m^1", "m^1", "", msys.getUOM(Unit.METRE), 1)
        self.assertTrue(u.getBaseSymbol() == m1.getBaseSymbol())

        m2 = msys.getUOM(Unit.SQUARE_METRE)
        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m^2", "m^2", "", msys.getUOM(Unit.METRE), 2)
        self.assertTrue(u.getBaseSymbol() == m2.getBaseSymbol())

        perMetre = m1.invert()
        diopter = msys.getUOM(Unit.DIOPTER)
        self.assertTrue(perMetre.getBaseSymbol() == diopter.getBaseSymbol())

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m*-1", "m*-1", "", msys.getUOM(Unit.METRE), -1)
        mult = u.multiply(m1)
        self.assertTrue(mult.getBaseSymbol() == msys.getUOM(Unit.ONE).getBaseSymbol())

        perMetre2 = m2.invert()
        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m*-2", "m*-2", "", msys.getUOM(Unit.METRE), -2)
        self.assertTrue(u.getBaseSymbol() == perMetre2.getBaseSymbol())

        u = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "m^0", "m^0", "", msys.getUOM(Unit.METRE), 0)

        try:
            abscissaUnit = None
            uno.setConversion(abscissaUnit)
            self.fail()
        except:
            pass
        
    def testOne(self):
        msys = MeasurementSystem.instance()

        metre = msys.getUOM(Unit.METRE)

        u = metre.multiply(msys.getOne())
        self.assertTrue(u == metre)

        u = metre.divide(msys.getOne())
        self.assertTrue(u == metre)

        oneOverM = metre.invert()
        u = oneOverM.invert()
        self.assertTrue(u == metre)

        u = oneOverM.multiply(metre)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        u = metre.divide(metre)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        u = msys.getOne().divide(metre).multiply(metre)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        uom = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "1/1", "1/1", "")
        uom.setConversion(1.0, msys.getOne(), 1.0)

        self.assertAlmostEqual(uom.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(uom.abscissaUnit == msys.getOne())
        self.assertAlmostEqual(uom.offset, 1.0, None, None, TestingUtils.DELTA6)

        u = msys.getOne().invert()
        self.assertTrue(u.abscissaUnit.getBaseSymbol() == msys.getOne().getBaseSymbol())

        one = msys.getOne()
        self.assertTrue(one.getBaseSymbol() == "1")
        self.assertTrue(one == one)

        uno = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "", ".1", "", one, one)
        self.assertTrue(uno.getBaseSymbol() == one.getBaseSymbol())

        p = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "", "..1", "", one, one)
        self.assertTrue(p.getBaseSymbol() == one.getBaseSymbol())

        p3 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "", "...1", "", one, 3)
        self.assertTrue(p3.getBaseSymbol() == one.getBaseSymbol())

        p3 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "", "...1", "", one, -1)
        self.assertTrue(p3.getBaseSymbol() == one.getBaseSymbol())

        a1 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "a1", "a1", "A1")
        self.assertTrue(a1.getBaseSymbol() == "a1")

        uno = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "one", "one", "", a1, a1)
        self.assertTrue(uno.getBaseSymbol() == one.getBaseSymbol())
    
    def testGeneric(self):
        msys = MeasurementSystem.instance()

        b = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "b", "beta", "Beta")
        self.assertFalse(b == None)

        # scalar
        ab1 = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "a=2b+1", "a=2b+1", "custom")
        ab1.setConversion(2.0, b, 1.0)

        self.assertAlmostEqual(ab1.scalingFactor, 2.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(ab1.abscissaUnit == b)
        self.assertAlmostEqual(ab1.offset, 1.0, None, None, TestingUtils.DELTA6)

        # quotient
        a = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "a", "alpha", "Alpha")
        self.assertTrue(a.abscissaUnit == a)

        aOverb = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "a/b", "a/b", "", a, b)
        aOverb.scalingFactor = 2.0

        self.assertAlmostEqual(aOverb.scalingFactor, 2.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(aOverb.getDividend() == a)
        self.assertTrue(aOverb.getDivisor() == b)
        self.assertAlmostEqual(aOverb.offset, 0.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(aOverb.abscissaUnit == aOverb)

        bOvera = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "b/a", "b/a", "", b, a)
        bOveraI = bOvera.invert()
        self.assertTrue(bOveraI.getBaseSymbol() == aOverb.getBaseSymbol())

        # multiply2
        uom = aOverb.multiply(b)
        self.assertTrue(uom.abscissaUnit.getBaseSymbol() == a.getBaseSymbol())
        self.assertAlmostEqual(uom.scalingFactor, 2.0, None, None, TestingUtils.DELTA6)
        bd = uom.getConversionFactor(a)
        self.assertAlmostEqual(bd, 2.0, None, None, TestingUtils.DELTA6)

        # divide2
        uom2 = uom.divide(b)
        self.assertAlmostEqual(uom2.scalingFactor, 2.0, None, None, TestingUtils.DELTA6)
        self.assertAlmostEqual(uom2.offset, 0.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(uom2.getBaseSymbol() == aOverb.getBaseSymbol())

        # invert
        uom3 = uom2.invert()
        u = uom3.multiply(uom2)
        self.assertTrue(u.getBaseSymbol() == msys.getOne().getBaseSymbol())

        # product
        ab = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "name", "symbol", "custom", a, b)
        ab.offset = 1.0

        self.assertAlmostEqual(ab.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(ab.getMultiplier() == a)
        self.assertTrue(ab.getMultiplicand() == b)
        self.assertAlmostEqual(ab.offset, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(ab.abscissaUnit == ab)

        ab.offset = 0.0

        uom4 = ab.divide(a)
        self.assertAlmostEqual(uom4.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(uom4.abscissaUnit.getBaseSymbol() == b.getBaseSymbol())

        uom5 = uom4.multiply(a)
        self.assertAlmostEqual(uom5.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        u = uom5.abscissaUnit
        self.assertTrue(u.getBaseSymbol() == ab.getBaseSymbol())

        # invert
        uom6 = ab.invert()
        self.assertAlmostEqual(uom6.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(uom6.getDividend() == msys.getOne())
        self.assertTrue(uom6.getDivisor() == ab)
        self.assertAlmostEqual(uom6.offset, 0.0, None, None, TestingUtils.DELTA6)

        # power
        a2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "name", "a**2", "custom", a, 2)
        self.assertAlmostEqual(a2.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(a2.getPowerBase() == a)
        self.assertTrue(a2.getPowerExponent() == 2)
        self.assertAlmostEqual(a2.offset, 0.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(a2.abscissaUnit == a2)

        uom8 = a2.divide(a)
        self.assertAlmostEqual(uom8.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertAlmostEqual(uom.offset, 0.0, None, None, TestingUtils.DELTA6)
        self.assertTrue(uom8.abscissaUnit.getBaseSymbol() == a.getBaseSymbol())

        uom9 = uom8.multiply(a)
        self.assertAlmostEqual(uom9.scalingFactor, 1.0, None, None, TestingUtils.DELTA6)
        self.assertAlmostEqual(uom9.offset, 0.0, None, None, TestingUtils.DELTA6)
        u = uom9.abscissaUnit
        self.assertTrue(u.getBaseSymbol() == a2.getBaseSymbol())

        u = CacheManager.instance().getUOMBySymbol(a.symbol)
        self.assertFalse(uom == None)

        # again
        c = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "c", "cUnit", "C")
        x = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "x", "xUnit", "X")
        e = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, "e", "eUnit", "E")

        aTimesa = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "", "aUnit*2", "", a, a)
        u = aTimesa.divide(a)
        self.assertTrue(u.getBaseSymbol() == a.getBaseSymbol())

        u = aOverb.multiply(b)
        self.assertTrue(u.getBaseSymbol() == a.getBaseSymbol())

        cOverx = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "", "c/x", "", c, x)
        alpha = aOverb.divide(cOverx)
        beta = alpha.multiply(cOverx)
        self.assertTrue(beta.getBaseSymbol() == aOverb.getBaseSymbol())

        u = aOverb.multiply(cOverx).divide(cOverx)
        self.assertTrue(u.abscissaUnit.getBaseSymbol() == aOverb.getBaseSymbol())

        axb = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "", "a.b", "", a, b)
        u = CacheManager.instance().getUOMBySymbol(axb.symbol)
        self.assertTrue(u == axb)
        u = axb.divide(a)
        self.assertTrue(u.getBaseSymbol() == b.getBaseSymbol())

        symbol = axb.symbol + "." + axb.symbol
        axbsq = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "", symbol, "", axb, axb)
        u = axbsq.divide(axb)
        self.assertTrue(u.getBaseSymbol() == axb.getBaseSymbol())

        b2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "b2", "b*2", "", b, 2)

        symbol = axb.getBaseSymbol()
        u = CacheManager.instance().getBaseUOM(symbol)
        self.assertTrue(u is not None)

        axb2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "axb2", "(a.b)*2", "", axb, 2)
        u = axb2.divide(axb)
        self.assertTrue(u.getBaseSymbol() == axb.getBaseSymbol())

        aOverb2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "aOverb2", "(a/b)*2", "", aOverb, 2)
        u = aOverb2.multiply(b2)
        self.assertTrue(u.getBaseSymbol() == aTimesa.getBaseSymbol())

        symbol = axb.symbol + "^-2"
        axbm2 = msys.createPowerUOM(UnitType.UNCLASSIFIED, None, "", symbol, "", axb, -2)
        uom = axbm2.multiply(axb2)
        self.assertTrue(uom.getBaseSymbol() == msys.getOne().symbol)
        cxd = msys.createProductUOM(UnitType.UNCLASSIFIED, None, "", "c.D", "", c, x)
        s = "cUnit" + Reducer.MULT + "xUnit"
        cxbase = cxd.getBaseSymbol()
        self.assertTrue(cxbase.index(s) != -1)

        abdivcd = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "", "(a.b)/(c.D)", "", axb, cxd)
        self.assertTrue(abdivcd.getDividend() == axb)
        self.assertTrue(abdivcd.getDivisor() == cxd)

        cde = msys.createQuotientUOM(UnitType.UNCLASSIFIED, None, "", "(c.D)/(e)", "", cxd, e)
        s = "cUnit" + Reducer.MULT + "xUnit/eUnit"
        self.assertTrue(cde.getBaseSymbol().index(s) != -1)

        u = msys.createScalarUOM(UnitType.UNCLASSIFIED, None, None, "not None", None)
        self.assertTrue(str(u) is not None)
