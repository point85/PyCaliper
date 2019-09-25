import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.test_utils import TestUtils
from PyCaliper.uom.prefix import Prefix

class TestPrefix(unittest.TestCase):
    def testSnippet(self):
        msys = MeasurementSystem.instance()
        
        # A nutrition label says the energy content is 1718 KJ.  What is this amount in kilo-calories?
        kJ = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.JOULE))
        kcal = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.CALORIE))
        kcalQ = Quantity(1718.0, kJ).convert(kcal)
        self.assertAlmostEqual(kcalQ.amount, 410.6, None, None, TestUtils.DELTA1)
        
        # A Tesla Model S battery has a capacity of 100 KwH.  
        # When fully charged, how many electrons are in the battery?
        c = msys.getQuantity(Constant.LIGHT_VELOCITY)
        me = msys.getQuantity(Constant.ELECTRON_MASS)   
        kwh = msys.createPrefixedUOM(Prefix.kilo(), msys.getUOM(Unit.WATT_HOUR))
        kwhQ = Quantity(100.0, kwh)
        
        wh = kwhQ.convert(msys.getUOM(Unit.WATT_HOUR))
        self.assertTrue(wh.amount == 1.0E+05)
        
        electrons = kwhQ.divide(c).divide(c).divide(me)
        d = electrons.amount / 1.221E12
        self.assertAlmostEqual(d, 1.0, None, None, TestUtils.DELTA1)
        print("Done")
        
