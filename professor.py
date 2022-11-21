class Professor:
    def __init__(self, name=None, surname=None,tel=None, id=None):
        self.__name = name
        self.__surname = surname
        self.__tel = tel
        self.__id = id

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname
    
    def getTel(self):
        return self.__tel

    def setName(self, name):
        self.__name = name

    def setSurname(self, surname):
        self.__surname = surname

    def setTel(self, tel):
        self.__tel = tel

    def setId(self, id):
        self.__id = id
