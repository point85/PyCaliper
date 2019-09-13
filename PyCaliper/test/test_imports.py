#import unittest
#import sys
from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
#, UnitType, Constant
#from PyCaliper.uom.quantity import Quantity
#from PyCaliper.uom.prefix import Prefix
#from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.test.base import BaseTest
#from PyCaliper.uom.localizer import Localizer
    
class TestImports(BaseTest):    
    def test1(self):
        #try:
            
            ms = MeasurementSystem.instance()
            """
            ft = ms.getUOM(Unit.FOOT)
            self.snapshotBaseSymbolCache()
            self.snapshotSymbolCache()
            self.snapshotUnitEnumerationCache()
            """
            
            ft2 = ms.getUOM(Unit.SQUARE_FOOT)
            self.snapshotSymbolCache()
            self.snapshotUnitEnumerationCache()
            self.snapshotBaseSymbolCache()
            
            """
            n = Localizer.instance().langStr("acre.name")
            s = Localizer.instance().langStr("acre.symbol")
            d = Localizer.instance().langStr("acre.desc")
            
            uom = ms.createScalarUOM(UnitType.AREA, Unit.ACRE, n, s, d)
            #s = uom.getBaseSymbol()
            ft2 = ms.getUOM(Unit.SQUARE_FOOT)
            print("$$$ setting conversion $$$")
            uom.setConversion(43560.0, ft2)
            self.snapshotBaseSymbolCache()
            #uom = ms.getUOM(Unit.ACRE)
            
            print(str(uom)) 
            """
            """
            m = MeasurementSystem.instance().getUOM(Unit.METRE)
            print(str(m))
            km = MeasurementSystem.instance().createPrefixedUOM(Prefix.kilo(), m)
            print(str(km))
            litre = MeasurementSystem.instance().getUOM(Unit.LITRE)
            print(str(litre))
            
            N = MeasurementSystem.instance().getUOM(Unit.NEWTON)
            print(str(N))
            m3 = MeasurementSystem.instance().getUOM(Unit.CUBIC_METRE)
            print(str(m3))
            m2 = MeasurementSystem.instance().getUOM(Unit.SQUARE_METRE)
            Nm = MeasurementSystem.instance().getUOM(Unit.NEWTON_METRE) 
            pa = MeasurementSystem.instance().getUOM(Unit.PASCAL) 
            kPa = MeasurementSystem.instance().createPrefixedUOM(Prefix.kilo(), pa)  
            print(str(kPa))     
            celsius = MeasurementSystem.instance().getUOM(Unit.CELSIUS)   
            print(str(celsius)) 
            
            # US
            lbm = MeasurementSystem.instance().getUOM(Unit.POUND_MASS)
            print(str(lbm)) 
             
            lbf = MeasurementSystem.instance().getUOM(Unit.POUND_FORCE)
            print(str(lbf))  
            mi = MeasurementSystem.instance().getUOM(Unit.MILE)
            print(str(mi))
            
            ft = MeasurementSystem.instance().getUOM(Unit.FOOT)
            print(str(ft))
            
            gal = MeasurementSystem.instance().getUOM(Unit.US_GALLON)
            print(str(gal))
            
            ft2 = MeasurementSystem.instance().getUOM(Unit.SQUARE_FOOT)
            print(str(ft2))
            ft3 = MeasurementSystem.instance().getUOM(Unit.CUBIC_FOOT)
            print(str(ft3))
            
            acre = MeasurementSystem.instance().getUOM(Unit.ACRE)
            print(str(acre))
            
            ftlbf = MeasurementSystem.instance().getUOM(Unit.FOOT_POUND_FORCE)
            print(str(ftlbf))
            """
            
            """
            psi = MeasurementSystem.instance().getUOM(Unit.PSI)
            print(str(psi))
            fahrenheit = MeasurementSystem.instance().getUOM(Unit.FAHRENHEIT)
            print(str(fahrenheit)) 
            """ 
            #self.assertEqual(ft.bridgeOffset, 0.0)

        
