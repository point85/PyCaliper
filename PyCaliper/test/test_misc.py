import unittest

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.enums import Unit
from PyCaliper.uom.enums import UnitType
from PyCaliper.uom.enums import Constant
from PyCaliper.uom.quantity import Quantity
from PyCaliper.test.testing_utils import TestingUtils


class TestFinancial(unittest.TestCase): 
    def testStocks(self):
        msys = MeasurementSystem.instance()
        
        # John has 100 shares of Alphabet Class A stock. How much is his
        # portfolio worth in euros when the last trade was $838.96 and a US
        # dollar is worth 0.94 euros?
        euro = msys.getUOM(Unit.EURO)
        usd = msys.getUOM(Unit.US_DOLLAR)
        usd.setConversion(0.94, euro)

        googl = msys.createScalarUOM(UnitType.CURRENCY, None, "Alphabet A", "GOOGL", "Alphabet (formerly Google) Class A shares")
        googl.setConversion(838.96, usd)
        portfolio = Quantity(100.0, googl)
        value = portfolio.convert(euro)
        self.assertAlmostEqual(value.amount, 78862.24, None, None, TestingUtils.DELTA6)
        
    def testNamedQuantity(self):
        msys = MeasurementSystem.instance()
        
        for value in Constant:
            q = msys.getQuantity(value)
            self.assertTrue(q.name is not None)
            self.assertTrue(q.symbol is not None)
            self.assertTrue(q.description is not None)
            self.assertTrue(q.uom is not None)
            self.assertTrue(str(q) is not None)

        