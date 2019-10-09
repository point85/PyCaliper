import unittest, math

from PyCaliper.uom.measurement_system import MeasurementSystem
from PyCaliper.uom.cache_manager import CacheManager
from PyCaliper.uom.enums import Unit, UnitType, Constant
from PyCaliper.uom.quantity import  Quantity
from PyCaliper.test.testing_utils import TestingUtils
from PyCaliper.uom.prefix import Prefix


class TestSnippet(unittest.TestCase):
    def testOne(self):
        msys = MeasurementSystem.instance()
             
        # convert Unit to nanokatal
        u = msys.getUOM(Unit.UNIT)
        katal = msys.getUOM(Unit.KATAL)
        q1 = Quantity(1.0, u)
        q2 = q1.convert(msys.createPrefixedUOM(Prefix.nano(), katal))
        
        # test result Equivalent
        eq = msys.getUOM(Unit.EQUIVALENT)
        litre = msys.getUOM(Unit.LITRE)
        mEqPerL = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "milliNormal", "mEq/L",
            "solute per litre of solvent ", msys.createPrefixedUOM(Prefix.milli(), eq), litre)
        testResult = Quantity(5.0, mEqPerL)
        
        # blood cell count test results
        k = msys.createPrefixedUOM(Prefix.kilo(), msys.getOne())
        uL = msys.createPrefixedUOM(Prefix.micro(), litre)
        kul = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "K/uL", "K/uL",
            "thousands per microlitre", k, uL)
        testResult = Quantity(7.0, kul)
        
        fL = msys.createPrefixedUOM(Prefix.femto(), litre)
        testResult = Quantity(90, fL)
        
        # TSH test result
        uIU = msys.createPrefixedUOM(Prefix.micro(), msys.getUOM(Unit.INTERNATIONAL_UNIT))
        mL = msys.createPrefixedUOM(Prefix.milli(), litre)
        uiuPerml = msys.createQuotientUOM(UnitType.MOLAR_CONCENTRATION, None, "uIU/mL", "uIU/mL",
            "micro IU per millilitre", uIU, mL)
        testResult = Quantity(2.0, uiuPerml)
        
        print(testResult)
        
