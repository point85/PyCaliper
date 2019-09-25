import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.test_utils import TestUtils

class TestPrefix(unittest.TestCase):
    def testSnippet(self):
        msys = MeasurementSystem.instance()
        
        one = msys.getOne()
        mps = msys.getUOM(Unit.METRE_PER_SEC)
        fps = msys.getUOM(Unit.FEET_PER_SEC)
        nm = msys.getUOM(Unit.NEWTON_METRE)
        ft = msys.getUOM(Unit.FOOT)
        inch = msys.getUOM(Unit.INCH)
        mi = msys.getUOM(Unit.MILE)
        hr = msys.getUOM(Unit.HOUR)
        m = msys.getUOM(Unit.METRE)
        s = msys.getUOM(Unit.SECOND)
        n = msys.getUOM(Unit.NEWTON)
        lbf = msys.getUOM(Unit.POUND_FORCE)
        m2 = msys.getUOM(Unit.SQUARE_METRE)
        m3 = msys.getUOM(Unit.CUBIC_METRE)
        ft2 = msys.getUOM(Unit.SQUARE_FOOT)

        # test products and quotients
        #ftlbf = msys.getUOM(Unit.FOOT_POUND_FORCE)
        #CacheManager.instance().unregisterUOM(ftlbf)
        nmQ = Quantity(1.0, nm)
        lbfinQ = nmQ.convertToPowerProduct(lbf, inch)
        self.assertAlmostEqual(lbfinQ.amount, 8.850745791327183, None, None, TestUtils.DELTA6)
        print("Done")
        
