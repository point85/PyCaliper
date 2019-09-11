from PyCaliper.uom.cache_manager import CacheManager
import math

class BaseTest:
    __DELTA6 = 0.000001
    __DELTA5 = 0.00001
    __DELTA4 = 0.0001
    __DELTA3 = 0.001
    __DELTA2 = 0.01
    __DELTA1 = 0.1
    __DELTA0 = 1
    __DELTA_10 = 10
        
    """
    @staticmethod
    def initializeSystem(self):
        ms = MeasurementSystem.instance()
    """
    def __init__(self):
        pass
    
    def snapshotSymbolCache(self):
        print("Symbol cache ...")
        
        count = 0
        for entry in CacheManager.instance().symbolRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + str(entry[1]))

    def snapshotBaseSymbolCache(self):
        print("Base symbol cache ...")
        
        count = 0
        for entry in CacheManager.instance().baseRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + str(entry[1]))


    def snapshotUnitEnumerationCache(self):
        print("Enumeration cache ...")
        
        count = 0
        for entry in CacheManager.instance().unitRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + str(entry[1]))
    
    @staticmethod
    def isCloseTo(actualValue, expectedValue, delta):
        diff = abs(actualValue - expectedValue)
        return True if (diff <= delta) else False