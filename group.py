from sqlite3 import IntegrityError
from professor import Professor
from course import Course
from student import Student

class Group:
    '''Representa un grupo académico al que se le asignan
    unos profesores y unas asignaturas'''
    def __init__(self, name=None, year=None, id=None, dbmanager=None):
        self.__name = name
        self.__id = id
        self.__year = year
        self.__dbmanager = dbmanager
        self.impartDict = {}
        self.attendants = {}

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name
    
    def getYear(self):
        return self.__year

    def getImpart(self):
        return self.impartDict
    
    def getAttendant(self, id):
        return self.attendants[id]

    def setClasses(self, ProfCouseDict):
        '''Guarda en un diccionario la pareja de asignatura-profesor
        que corresponde al grupo
        '''
        if not isinstance(ProfCouseDict, dict):
            raise TypeError('No es un diccionario')
        else:
            for course, prof in ProfCouseDict.items():
                if not isinstance(prof, Professor) or \
                    not isinstance(course, Course):
                    error = 'Elementos del diccionario de clase errónea'
                    raise TypeError(error)
            self.impartDict = ProfCouseDict

    def setStudents(self, StudentsDict):
        if not isinstance(StudentsDict, dict):
            raise TypeError('No es un diccionario')
        else:
            for student in StudentsDict.values():
                if not isinstance(student, Student):
                    error = 'Elementos del diccionario de clase errónea'
                    raise TypeError(error)
            self.attendants = StudentsDict

    def setName(self, name):
        if not isinstance(name, str):
            raise TypeError('No es una cadena de texto')
        self.__name = name

    def setYear(self, year):
        if not isinstance(year, str):
            raise TypeError('No es una cadena de texto')
        self.__year = year

    def loadGroup(self):
        auxtuple = self.__dbmanager.loadGroup(self.__id, self.__year)
        self.__name = auxtuple[0]
        self.impartDict = auxtuple[1]
        self.attendants = auxtuple[2]

    def saveStudent(self, idstudent, name, surname, direction, tel):
        if idstudent in self.attendants:
            raise IntegrityError
        self.attendants.setdefault(idstudent, Student(name, surname, tel, direction, idstudent))
        self.__dbmanager.saveStudent(self.__year, self.__id, idstudent, name, surname, direction, tel)

    def saveStudentFromFile(self, studentList):
        '''Toma una lista de tuplas en las que están registrados los datos de cada alumno
        en el siguiente orden: DNI - Nombre - Apellidos - Telefono - Direccion; crea el alumno
        con los datos correcondientes y lo guarda en memoria y en la base de datos'''
        for student in studentList:
            if student[0] in self.attendants:
                raise IntegrityError
            self.attendants.setdefault(student[0], Student(student[1], student[2], student[3], student[4], student[0]))
        self.__dbmanager.insert_from_file(studentList, self.__id, self.__year)
