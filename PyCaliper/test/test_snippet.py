import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.test_utils import TestUtils
from PyCaliper.uom.prefix import Prefix

"""
def getUOMKey(elem):
    return elem.symbol 
"""
class TestPrefix(unittest.TestCase):
    def testSnippet(self):
        units = CacheManager.instance().getCachedUnits()
        sorted(units, key = TestUtils.getUOMKey)
        #units.sort(getUOMKey)
        print("Done")
        
