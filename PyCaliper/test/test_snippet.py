import unittest
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.enums import Constant
from PyCaliper.uom.measurement_system import MeasurementSystem

class TestPrefix(unittest.TestCase):

    def test_prefix(self):
        yotta = Prefix.yotta()
        print (yotta.name)
        print (Constant.AVAGADRO_CONSTANT)
        
        print (Prefix.fromName("yotta"))

    def test_singleton(self):
        first = MeasurementSystem.instance()
        print (first)
        
        second = MeasurementSystem.instance()
        print (second)
        
        self.assertEqual(first, second)

if __name__ == '__main__':
    unittest.main()