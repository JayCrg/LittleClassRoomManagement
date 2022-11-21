from coursedbcontroller import CourseDBController
from yeardbcontroller import YearDBController
from professordbcontroller import ProfessorDBController

class GeneralDBController:

    def __init__(self, connection):
        self.__connection = connection
        self.yearController = YearDBController(self.__connection)
        self.courseController = CourseDBController(self.__connection)
        self.professorController = ProfessorDBController(self.__connection)

    ############ año

    def loadYearsDict(self):
        return self.yearController.loadYearsDict()

    ############# profesor

    def saveProfessor(self, name, surname, tel):
        self.professorController.saveProfessor(name, surname, tel)

    def loadProfessors(self):
        return self.professorController.loadProfessor()
    
    #############3 asignatura

    def loadCourses(self):
        return self.courseController.loadCourses()

    def saveCourse(self, id, name):
        self.courseController.saveCourse(id, name)
    
    ############ students

    def loadGroup(self):
        return self.yearController.loadGroup()

    def saveStudent(self, year, idgroup, id, name, surname, direction, tel, ):
        self.yearController.saveStudent(year, idgroup, id, name, surname, direction, tel)

    def saveStudentForGroup(self, id, idgroup, year):
        self.yearController.saveStudentForGroup(id, idgroup, year)

    def insert_from_file(self, students_list, groupid, year):
        self.yearController.insert_from_file(students_list, groupid, year)

