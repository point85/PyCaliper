import unittest
import sys

from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.measurement_system import MeasurementSystem
#from PyCaliper.uom.reducer import Reducer
#from PyCaliper.uom.operands import Operands
#from PyCaliper.uom.cache_manager import CacheManager
#from PyCaliper.uom.quantity import Quantity
#from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.unit_type import UnitType
    
class TestImports(unittest.TestCase):    
    def test1(self):
        try:
            ms = MeasurementSystem.instance()
            uom = ms.createScalarUOM(UnitType.VOLUME, Unit.BR_GALLON, Localizer.instance().langStr("br_gallon.name"), Localizer.instance().langStr("br_gallon.symbol"), Localizer.instance().langStr("br_gallon.desc"))
            #uom.setConversion(277.4194327916215, self.getUOM(Unit.CUBIC_INCH), 0.0) 
            #uom = ms.getUOM(Unit.METRE)
            #print(str(uom)) 
            #uom = ms.getUOM(Unit.FOOT)
            #print(str(uom))  
            #uom = ms.getUOM(Unit.CUBIC_INCH)
            #print(str(uom))     
            #uom = ms.getUOM(Unit.BR_GALLON)
            print(str(uom)) 
            #uom = ms.getUOM(Unit.BR_BUSHEL)
            print(str(uom))  
            #uom = ms.createUOMForUnit(Unit.BR_GALLON)
            #uom = ms.finDict[Unit.US_DOLLAR]()
            #uom = ms.brDict[Unit.BR_GALLON]()
            #uom = ms.createScalarUOM(UnitType.MASS, Unit.BR_TON, Localizer.instance().langStr("br_ton.name"), \
            #    Localizer.instance().langStr("br_ton.symbol"), Localizer.instance().langStr("br_ton.desc"))
            #uom.setConversion(2240.0, ms.getUOM(Unit.POUND_MASS))
            #uom = sys.usDollar()
            #uom = sys.createUOMForUnit(Unit.US_DOLLAR)
    
            #uom = sys.createUOMForUnit(Unit.BR_GALLON)
            #print(str(uom))
            
            print ("Done!")
        except:
            print("Exception: ", sys.exc_info()[1])
        
