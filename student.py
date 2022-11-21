class Student:
    def __init__(self, name=None,
                 surname=None, tel=None,
                 direction=None, id=None):
        self.__name = name
        self.__surname = surname
        self.__tel = tel
        self.__direction = direction
        self.__id = id

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def getDirection(self):
        return self.__direction

    def getTel(self):
        return self.__tel