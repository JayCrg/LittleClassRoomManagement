import sqlite3
from professor import Professor
class ProfessorDBController:

    def __init__(self, connection):
        self.__connection = connection
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

    def saveProfessor(self, name, surname, tel):
        print(id)
        sql = "INSERT INTO Profesor "
        sql += '(nombre, apellidos, telefono) '
        sql += 'VALUES(?, ?, ?)'
        values = (
            name,
            surname,
            tel,
        )
        self.__cursor.execute(sql, values)
        self.__connection.commit()
    
    def deleteProfessor(self, id):
        
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'DELETE FROM Profesor '
        sql += 'WHERE id = ?'
        self.__cursor.execute(sql, (id,))
        self.__connection.commit()
        self.deleteProfCourseAssociated()

    def deleteProfCourseAssociated(self, id):
        '''
        Borra la reacion entre Asignaturas y Profesor
        con el grupo
        '''
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'DELETE FROM Imparte '
        sql += 'WHERE idProfesor = ?'
        self.__cursor.execute(sql, (id,))
        self.__connection.commit()

    def updateProfessor(self, id, name, surname, tel):
        '''
        Actualiza los datos de un Profesor
        existente en la base de datos en base al id.
        '''
        if id is None:
            raise TypeError('El atributo id debe tener valor')
        sql = 'UPDATE Profesor SET nombre = ?, apellidos = ?, telefono = ? '
        sql += 'WHERE id = ?'
        values = (
            name,
            id,
            surname,
            tel,
        )
        self.__cursor.execute(sql, values)
        self.__connection.commit()

    def loadProfessor(self):
        
        sql = 'SELECT id, nombre, apellidos, telefono '
        sql += 'FROM Profesor '
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        profDict = {}
        for data in rows:
            prof = Professor(data['nombre'], data['apellidos'], data['telefono'], data['id'])
            profDict.setdefault(data['id'], prof)
        return profDict