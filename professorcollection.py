from sqlite3 import IntegrityError
from professor import Professor

class ProfessorCollection:

    def __init__(self, dbmanager):
        self.__dbmanager = dbmanager
        self.professorDict = self.loadProfessors()

    def getYear(self, id):
        try:
            return self.professorDict[id]
        except KeyError:
            return None
        
    def loadProfessors(self):
        return self.__dbmanager.loadProfessors()

    def saveProfessor(self, name, surname, tel):
        id = max(self.professorDict.keys()) + 1 if len(self.professorDict.keys()) > 0 else 1
        self.professorDict.setdefault(id, Professor(name, surname, tel, id))
        self.__dbmanager.saveProfessor(name, surname, tel)
