import unittest
#from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.unit_type import UnitType

class TestImports(unittest.TestCase):
    
    def test1(self):
        #sys = MeasurementSystem.instance()
        uom = UnitOfMeasure(UnitType.LENGTH, "n", "cat", "d")
        b = uom.getBaseSymbol()
        #category = Localizer.instance().unitStr("default.category.text")
        print(str(uom))