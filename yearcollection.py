
class YearCollection:

    def __init__(self, manager):
        self.__manager = manager
        self.yearsDict = self.load()

    def getYear(self, period):
        try:
            return self.yearsDict[period]
        except KeyError:
            return None
        
    def load(self):
        return self.__manager.loadYearsDict()