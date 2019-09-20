import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.test_utils import TestUtils
from PyCaliper.uom.prefix import Prefix

class TestPrefix(unittest.TestCase):
    def testSnippet(self):
        msys = MeasurementSystem.instance()
        
