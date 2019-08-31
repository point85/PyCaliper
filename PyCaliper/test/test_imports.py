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
            #uom = ms.finDict[Unit.US_DOLLAR]()
            uom = ms.brDict[Unit.BR_GALLON]()
            #uom = ms.createScalarUOM(UnitType.MASS, Unit.BR_TON, Localizer.instance().langStr("br_ton.name"), \
            #    Localizer.instance().langStr("br_ton.symbol"), Localizer.instance().langStr("br_ton.desc"))
            #uom.setConversion(2240.0, ms.getUOM(Unit.POUND_MASS))
            #uom = sys.usDollar()
            #uom = sys.createUOMForUnit(Unit.US_DOLLAR)
    
            #uom = sys.createUOMForUnit(Unit.BR_GALLON)
            print(str(uom))
        
            """
            uom = sys.createScalarUOM(UnitType.UNITY, Unit.ONE, \
                Localizer.instance().langStr("one.name"), Localizer.instance().langStr("one.symbol"), Localizer.instance().langStr("one.desc"))
            s = uom.symbol
            b = uom.getBaseSymbol()
            print(str(uom))
            
            uom = sys.createScalarUOM(UnitType.LENGTH, None, "n", "cat", "d")
            s = uom.symbol
            b = uom.getBaseSymbol()
            print(str(uom))
            
            uom = UnitOfMeasure(UnitType.LENGTH, "name", "symbol", "desc")
            #uom.isTerminal()
                    
            reducer = Reducer()
            reducer.explode(uom)
            
            
            print (uom.getBaseSymbol())
            
            s = self.toString(uom)
            #print("UOM" + str(uom))
            
            cm = CacheManager.instance() 
            
            one = cm.getUOMByUnit(Unit.ONE)
            print("One: " + str(one))
    
            value = Localizer.instance().langStr("unit.type.text") + " " + str(UnitType.LENGTH) + ", "
            print(value)
    
            q = Quantity(1.1, None)
            q.amount = 2.2
            print(str(q))
    
            uom = cm.getUOMBySymbol("m")
            print(uom)
            
            r = Reducer()
            print(r.MAX_RECURSIONS)
            o = Operands()
            print(o.multOp())
            """
            
            print ("Done!")
        except:
            print("Exception: ", sys.exc_info()[1])
        
