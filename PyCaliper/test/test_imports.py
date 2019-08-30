import unittest
#from PyCaliper.uom.localizer import Localizer
#from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.unit_type import UnitType
from PyCaliper.uom.reducer import Reducer
from PyCaliper.uom.operands import Operands
from PyCaliper.uom.cache_manager import CacheManager
#from PyCaliper.uom.quantity import Quantity
from PyCaliper.uom.unit_of_measure import UnitOfMeasure
from PyCaliper.uom.unit import Unit
from PyCaliper.uom.localizer import Localizer
from PyCaliper.uom.symbolic import Symbolic
import math

class TestUnitOfMeasure(Symbolic):
    def __init__(self, unitType, name, symbol, description):
        super().__init__(name, symbol, description)
        
        self.conversionRegistry = {}
        self.category = Localizer.instance().unitStr("default.category.text")
        self.unit = None
        self.unitType = UnitType.UNCLASSIFIED     
        self.abscissaUnit = self
        self.scalingFactor = 1.0
        self.offset = 0.0
        self.uom1 = None
        self.uom2 = None
        self.exponent1 = None
        self.exponent2 = None
        self.bridgeScalingFactor = None
        self.bridgeOffset = None
        self.bridgeAbscissaUnit = None
        self.unitType = unitType
        self.baseSymbol = None
        
    def isTerminal(self):
        return True if self == self.abscissaUnit else False

class TestImports(unittest.TestCase):
    def toString(self, uom):
        # type
        value = Localizer.instance().unitStr("unit.type.text") + " " + str(uom.unitType) + ", "
        
        """
        # enumeration
        if (self.unit is not None):
            value = value + Localizer.instance().unitStr("enum.text") + " " + str(uom.unit) + ", "
            
        # symbol
        value = value + Localizer.instance().unitStr("symbol.text") + " " + uom.symbol + ", "
        value = value + Localizer.instance().unitStr("conversion.text") + " "
        
        # scaling factor
        if (not math.isclose(self.scalingFactor, 1.0)):
            value = value + str(self.scalingFactor) + Operands.mult()
            
        # abscissa unit
        if (self.abscissaUnit is not None) :
            value = value + uom.abscissaUnit.symbol
            
        # offset
        if (not math.isclose(uom.offset, 0.0)):   
            value = value + " + " + str(uom.offset) + ", " + Localizer.instance().unitStr("base.text") + " "
            
        # base symbol
        value = value + uom.getBaseSymbol()
        """    
        return value
    
    def test1(self):
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

        value = Localizer.instance().unitStr("unit.type.text") + " " + str(UnitType.LENGTH) + ", "
        print(value)
        """
        q = Quantity(1.1, None)
        q.amount = 2.2
        print(str(q))
        """

        uom = cm.getUOMBySymbol("m")
        print(uom)
        
        r = Reducer()
        print(r.MAX_RECURSIONS)
        o = Operands()
        print(o.mult())
        
        print ("Done!")
        
        #sys = MeasurementSystem.instance()
        #uom = sys.createScalarUOM(UnitType.LENGTH, None, "n", "cat", "d")
        #s = uom.symbol
        #b = uom.getBaseSymbol()
        #category = Localizer.instance().unitStr("default.category.text")
        #print(str(uom))