import unittest
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.constant import Constant
from PyCaliper.uom.measurement_system import MeasurementSystem

class TestPrefix(unittest.TestCase):

    def test(self):
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

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()