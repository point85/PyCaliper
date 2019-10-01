import unittest
import uuid

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.cache_manager import CacheManager

class TestSystem(unittest.TestCase):
    def testUnifiedSystem(self):
        msys = MeasurementSystem.instance()
        
        self.assertIsNotNone(msys)

        unitMap = {}

        # check the SI units
        for unit in Unit:
            uom = msys.getUOM(unit)

            self.assertIsNotNone(uom)
            self.assertIsNotNone(uom.name)
            self.assertIsNotNone(uom.symbol)
            self.assertIsNotNone(uom.description)
            self.assertIsNotNone(str(uom))
            self.assertIsNotNone(uom.getBaseSymbol())
            self.assertIsNotNone(uom.abscissaUnit)
            self.assertIsNotNone(uom.scalingFactor)
            self.assertIsNotNone(uom.offset)

            # symbol uniqueness
            self.assertFalse(uom.symbol in unitMap)
            unitMap[uom.symbol] = uom

        allUnits = []

        for unit in Unit:
            allUnits.append(unit)

        for uom in msys.getRegisteredUOMs():
            if (uom.unit is not None):
                self.assertTrue(uom.unit in allUnits)

        for unitType in UnitType:
            found = None
            for u in msys.getRegisteredUOMs():
                if (u.unitType == unitType):
                    found = u.unitType
                    break

            if (found == None and unitType != UnitType.UNCLASSIFIED):
                self.fail("No unit found for type " + unitType)

        # constants
        for c in Constant:
            self.assertIsNotNone(msys.getQuantity(c))

    def testCache(self):
        msys = MeasurementSystem.instance()
        
        # unit cache
        msys.getOne()

        before = len(msys.getRegisteredUOMs())

        for _i in range(0, 10):
            msys.createScalarUOM(UnitType.UNCLASSIFIED, None, None, str(uuid.uuid1()), None)

        after = len(msys.getRegisteredUOMs())

        self.assertTrue(after == (before + 10))

    def testGetUnits(self):
        msys = MeasurementSystem.instance()
        
        for unitType in UnitType:
            uoms = msys.getUnitsOfMeasure(unitType)
            
            if (unitType != UnitType.UNCLASSIFIED):
                self.assertTrue(len(uoms) > 0)
