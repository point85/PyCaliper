import unittest

from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.measurement_system import MeasurementSystem
#from PyCaliper.uom.reducer import Reducer
#from PyCaliper.uom.operands import Operands
from PyCaliper.uom.cache_manager import CacheManager
#from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.unit_type import UnitType

class TestMeasurementSystem:    
    # single instance
    unifiedSystem = None
    
    def __init__(self):
        TestMeasurementSystem.unifiedSystem = self

    @staticmethod
    def instance():
        if (TestMeasurementSystem.unifiedSystem is None):
            TestMeasurementSystem()
        return TestMeasurementSystem.unifiedSystem 
    
    def createUOM(self, unitType, unit, name, symbol, description):
        if (symbol is None or len(symbol) == 0):
            msg = Localizer.instance().messageStr("symbol.cannot.be.null")
            raise Exception(msg)
        
        if (unitType is None):
            msg = Localizer.instance().messageStr("unit.type.cannot.be.null")
            raise Exception(msg)
        
        uom = CacheManager.instance().getUOMBySymbol(symbol)
        
        if (uom is None):
            # create a new one
            uom = UnitOfMeasure(unitType, name, symbol, description)
            
            uom.abscissaUnit = uom
            uom.unit = unit
            
        return uom
    
    def createScalarUOM(self, unitType, unit, name, symbol, description):
        uom = self.createUOM(unitType, unit, name, symbol, description)
        CacheManager.instance().registerUnit(uom)
        return uom

class TestImports(unittest.TestCase):
    
    def test1(self):
        #s = Localizer.instance().langStr("one.name")
        sys = TestMeasurementSystem.instance()
        uom = sys.createScalarUOM(UnitType.UNITY, Unit.ONE, \
            Localizer.instance().langStr("one.name"), Localizer.instance().langStr("one.symbol"), Localizer.instance().langStr("one.desc"))
        s = uom.symbol
        b = uom.getBaseSymbol()
        print(str(uom))
        """
        
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
        
