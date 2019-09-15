from PyCaliper.uom.cache_manager import CacheManager

class TestUtils():
    DELTA6 = 0.000001
    DELTA5 = 0.00001
    DELTA4 = 0.0001
    DELTA3 = 0.001
    DELTA2 = 0.01
    DELTA1 = 0.1
    DELTA0 = 1
    DELTA10 = 10
    
    @staticmethod
    def snapshotSymbolCache():
        print("Symbol cache ...")
        
        count = 0
        for entry in CacheManager.instance().symbolRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + entry[1].symbol)

    @staticmethod
    def snapshotBaseSymbolCache():
        print("Base symbol cache ...")
        
        count = 0
        for entry in CacheManager.instance().baseRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + entry[1].symbol)

    @staticmethod
    def snapshotUnitEnumerationCache():
        print("Enumeration cache ...")
        
        count = 0
        for entry in CacheManager.instance().unitRegistry.items():
            count = count + 1
            print("(" + str(count) + ") " + str(entry[0]) + ", " + entry[1].symbol)
    
    @staticmethod
    def isCloseTo(actualValue, expectedValue, delta):
        diff = abs(actualValue - expectedValue)
        return True if (diff <= delta) else False
    

