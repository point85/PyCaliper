import unittest
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.constant import Constant
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.resource_bundle import ResourceBundle

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

    def test_bundle(self):
        messages = ResourceBundle("messages")
        print (messages.getString("must.be.same.as"))

if __name__ == '__main__':
    unittest.main()