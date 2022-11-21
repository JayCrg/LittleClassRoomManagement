class Course:

    def __init__(self, id=None, name=None):
        self.__name = name
        self.__id = id

    def getId(self):
        return self.__id
    
    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def setId(self, id):
        self.__id = id



    