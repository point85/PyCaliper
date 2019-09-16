import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.quantity import Quantity

class TestPerformance(unittest.TestCase):
    def testPerformance(self):
        self.unitListMap = {}

        msys = MeasurementSystem.instance()

        for u in Unit:
            uom = msys.getUOM(u)
            self.addUOM(uom)

        self.runSingleTest()

    def addUOM(self, uom):
        unitList = None
        
        if uom.unitType in self.unitListMap:
            unitList = self.unitListMap[uom.unitType]

        if unitList is None:
            unitList = []
            self.unitListMap[uom.unitType] = unitList
        
        unitList.append(uom)

    def runSingleTest(self):
        # for each unit type, execute the quantity operations with no exceptions
        for entry in self.unitListMap.items():
            # run the matrix
            for rowUOM in entry[1]:
                # row quantity
                rowQty = Quantity(10.0, rowUOM)

                for colUOM in entry[1]:
                    # column qty
                    colQty = Quantity(10.0, colUOM)

                    # arithmetic operations
                    rowQty.add(colQty)
                    rowQty.subtract(colQty)

                    # offsets are not supported
                    if (rowUOM.offset == 0.0 and colUOM.offset == 0.0):
                        rowQty.multiply(colQty)
                        rowQty.divide(colQty)
                        rowQty.invert()

                    rowQty.convert(colUOM)
                    
                    if (rowQty == colQty):
                        pass
                    
                    _ = rowQty.amount
                    _ = rowQty.uom
                    _ = str(rowQty)

        