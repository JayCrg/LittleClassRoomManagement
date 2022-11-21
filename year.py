class Year:
    def __init__(self, id=None, dbmanager=None):
        self.__id = id
        self.__dbmanager = dbmanager
        self.groups = {}

    def getId(self):
        return self.__id
    
    def getGroup(self, id):
        try:
            return self.groups[id]
        except KeyError:
            return None

