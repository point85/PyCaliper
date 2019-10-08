import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import  Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.prefix import Prefix

class TestSnippet(unittest.TestCase):
    def testOne(self):
        msys = MeasurementSystem.instance()
             
        mkg = Quantity(1, msys.getUOM(Unit.KILOGRAM))
        f = mkg.multiply(msys.getQuantity(Constant.GRAVITY)).convert(msys.getUOM(Unit.POUND_FORCE))
            
        print(f)
        
