import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.prefix import Prefix

class TestSnippet(unittest.TestCase):
    def testOne(self):
        msys = MeasurementSystem.instance()

        second = msys.getSecond()
        msec = msys.createPrefixedUOM(Prefix.milli(), second)

        factor = second.getConversionFactor(msec)
        self.assertAlmostEqual(factor, 1000.0, None, None, TestingUtils.DELTA6)
        
