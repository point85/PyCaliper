import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem

class TestPrefix(unittest.TestCase):
    def testSnippet(self):
        msys = MeasurementSystem.instance()
        
