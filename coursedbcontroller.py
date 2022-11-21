import sqlite3
from course import Course
class CourseDBController:

    def __init__(self, connection):
        self.__connection = connection
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

    def saveCourse(self, id, name):

        sql = "INSERT INTO Asignatura "
        sql += '(id, nombre) '
        sql += 'VALUES(?, ?)'
        values = (
            id,
            name,
        )
        self.__cursor.execute(sql, values)
        self.__connection.commit()
    
    def delete(self, id):
        
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'DELETE FROM Asignatura '
        sql += 'WHERE id = ?'
        self.__cursor.execute(sql, (id,))
        self.__connection.commit()
        self.deleteProfCourseAssociated()

    def deleteProfCourseAssociated(self, id):
        '''
        Borra la reacion entre profesor y asignatura
        con el grupo
        '''
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'DELETE FROM Imparte '
        sql += 'WHERE idAsignatura = ?'
        self.__cursor.execute(sql, (id,))
        self.__connection.commit()

    def update(self, id, name):
        '''
        Actualiza los datos de un Asignatura
        existente en la base de datos en base al id.
        '''
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'UPDATE Asignatura SET nombre = ? '
        sql += 'WHERE id = ?'
        values = (
            name,
            id,
        )
        self.__cursor.execute(sql, values)
        self.__connection.commit()

    def loadCourses(self):
        
        sql = 'SELECT id, nombre '
        sql += 'FROM Asignatura '
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        courseDict = {}
        for data in rows:
            course = Course(data['id'], data['nombre'])
            courseDict.setdefault(data['id'], course)
        return courseDict