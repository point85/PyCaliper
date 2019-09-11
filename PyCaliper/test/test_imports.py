import unittest
import sys
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType
from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.prefix import Prefix
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.test.base import BaseTest
    
class TestImports(unittest.TestCase):    
    def test1(self):
        try:
            #messages = gettext.translation('units', localedir='locales', languages=[Localizer.getLC()])
            #messages.install()
            #print(messages.gettext("us_tsp.desc"))
            
            ms = MeasurementSystem.instance()
            #uom = ms.createScalarUOM(UnitType.VOLUME, None, "name", "symbol", "description")
            #uom = ms.createUOM(UnitType.VOLUME, None, "name", "symbol", "description")
            #CacheManager.instance().registerUnit(uom)
            #print(str(uom))
            #uom = ms.createScalarUOM(UnitType.VOLUME, Unit.BR_GALLON, Localizer.instance().langStr("br_gallon.name"), Localizer.instance().langStr("br_gallon.symbol"), Localizer.instance().langStr("br_gallon.desc"))
            #uom.setConversion(277.4194327916215, self.getUOM(Unit.CUBIC_INCH), 0.0) 
            #uom = ms.getUOM(Unit.ONE)
            #print(str(uom)) 
            #uom = ms.getUOM(Unit.ONE)
            #print(str(uom)) 
            #uom = ms.getUOM(Unit.FOOT)
            #print(str(uom))  
            #uom = ms.getUOM(Unit.CUBIC_INCH)
            #print(str(uom))
            #print(str(uom)) 
            #q = Quantity(10.1, uom)
            
            prefix = Prefix.kilo()
            uom = ms.getUOM(Unit.NEWTON)
            uom = ms.createPrefixedUOM(prefix, uom)
            #print(str(uom)) 

            bt = BaseTest()
            #bt.snapshotSymbolCache()
            #bt.snapshotBaseSymbolCache()
            bt.snapshotUnitEnumerationCache()
           
            #uom = ms.getUOM(Unit.BR_BUSHEL)
            #print(str(uom))  
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
        
