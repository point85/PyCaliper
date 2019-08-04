class MeasurementSystem:
    # single instance
    __instance = None

    @staticmethod
    def instance():
        if MeasurementSystem.__instance == None:
            MeasurementSystem()
        return MeasurementSystem.__instance 

    def __init__(self):
            MeasurementSystem.__instance = self


