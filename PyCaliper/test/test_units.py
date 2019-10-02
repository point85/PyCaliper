import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.cache_manager import CacheManager

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
            self.self.fail()
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
