import sqlite3
from professor import Professor
from course import Course
from student import Student
from group import Group
from year import Year

class YearDBController:

    def __init__(self, connection):
        self.__connection = connection
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

    ##################################
    # SECCION COLECCION DE AÑOS
    #################################

    def loadYearsDict(self):
        sql = 'SELECT g.id as idg, g.nombre as nombreg, '
        sql += 'g.anio as aniog, p.id as idp, p.nombre as nombrep, '
        sql += 'p.apellidos as apellidosp, p.telefono as telefonop, '
        sql += 'a.id as idasig, a.nombre as nombreasig, '
        sql += 'al.id AS idal, al.nombre AS nombreal, '
        sql += 'al.apellidos AS apellidosal, al.Telefono AS telefonoal, al.direccion AS direccional, '
        sql += 'periodo '
        sql += 'FROM Grupo g, Profesor p, Asignatura a, Imparte i, Alumno al, GrupoAlumno gp, Anio '
        sql += 'WHERE periodo = g.anio AND i.anio = g.anio AND gp.anio = g.anio AND g.id = i.IdGrupo AND a.id = i.idasignatura '
        sql += 'AND p.id = i.idprofesor AND gp.IdAlumno = al.id and gp.IdGrupo = g.id'        
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        auxYearDict = {}
        if rows == None:
            return {}
        for data in rows:
            if data['periodo'] not in auxYearDict:
                year = Year(
                            data['periodo'],
                            self
                            )
                year.groups = self.__getGroupsDict(rows, data['periodo'])
                auxYearDict.setdefault(data['periodo'], year)
        return auxYearDict
        
    def  __getGroupsDict(self, rows, year):
        auxGroupDict = {}
        for data in rows:
            if data['periodo'] == year:
                if (data['idg'], data['aniog']) not in auxGroupDict.keys():
                    group = Group(
                            data['nombreg'],
                            data['aniog'],
                            data['idg'],
                            self
                            )
                    group.setStudents(self.__getStudentsForGroupDict(rows, data['idg'], data['periodo']))
                    group.setClasses(self.__getClassesDict(rows, data['idg'], data['periodo']))
                    auxGroupDict.setdefault((data['idg'], data['aniog']), group)
        return auxGroupDict

    def __getClassesDict(self, rows, groupIdentify, groupYear):
        '''Crea un diccionario de asignatura/profesor a partir
        de registros de la base de datos para el grupo

        rows: lista de registros de la base datos (con información del 
        profesor, grupo y asignatura)
        Resultado: diccionario de formado por profesor:asignatura (dict)

        De no haber coincidencia devuelve un diccionario vacío'''
        imparting = {}
        auxProfDict = {}
        auxCourseDict = {}
        if rows is None:
            return {}
        for data in rows:
            if data['idg'] == groupIdentify and data['periodo'] == groupYear:
                self.__getProfCourse(data,
                                    auxProfDict,
                                    auxCourseDict,
                                    )
                selectedProf = auxProfDict.get(data['idp'])
                selectedCourse = auxCourseDict.get(data['idasig'])
                imparting.setdefault(selectedCourse, selectedProf)
        return imparting

    def __getStudentsForGroupDict(self, rows, groupIdentify, groupYear):
        '''Crea un conjunto de alumnos a partir
        de registros de la base de datos para el grupo

        rows: lista de registros de la base datos (con información del 
        profesor, grupo y asignatura)
        Resultado: conjunto de formado por alumnos (set)

        De no haber coincidencia devuelve un conjunto vacío'''
        auxStudentDict = {}
        for data in rows:
            if data['idg'] == groupIdentify and data['periodo'] == groupYear:
                if data['idal'] not in auxStudentDict.keys():
                    student = Student(
                                    data['nombreal'],
                                    data['apellidosal'],
                                    data['telefonoal'],
                                    data['direccional'],
                                    data['idal'],
                                    )
                    auxStudentDict.setdefault(data['idal'], student)
        return auxStudentDict

    def __getProfCourse(self, data, profDict, courseDict):
        '''
        Crea un profesor y una asignatura en base a un curso
        guardandolos en su respectivo diccionario

        data: registro de la base datos (con información de Profesor
        y Asignaturasus con contactos correspondientes)
        profDict: diccionario pasado por referencia
        courseDict: diccionario pasado por referencia
        '''
        if data['idp'] not in profDict.keys():
            prof = Professor(
                data['nombrep'],
                data['apellidosp'],
                data['telefonop'],
                data['idp'],
                )
            profDict.setdefault(data['idp'], prof)
        if data['idasig'] not in courseDict.keys():
            course = Course(
                             data['idasig'],
                             data['nombreasig'],
                            )
            courseDict.setdefault(data['idasig'], course)
    
    ################################
    #SECCION GRUPOS
    ############################

    def saveStudent(self, year, idgroup, id, name, surname, direction, tel):
        '''
        Guarda en la base de datos la informacion del alumno
        '''
        sql = "INSERT INTO Alumno "
        sql += '(id, nombre, apellidos, telefono, direccion) '
        sql += 'VALUES(?, ?, ?, ?, ?)'
        values = (
            id,
            name,
            surname,
            tel,
            direction,
        )
        self.__cursor.execute(sql, (values))
        self.__connection.commit()
        self.saveStudentForGroup(id, idgroup, year )

    def saveStudentForGroup(self, id, idgroup, year):
        '''Insert en la base de datos la relacion entre los alumnos
        y el grupo'''
        sql = 'INSERT INTO GrupoAlumno (IdGrupo, IdAlumno, anio) '
        sql += 'VALUES(?, ?, ?);'
        values = (
            idgroup,
            id,
            year,
        )
        self.__cursor.execute(sql, values)
        self.__connection.commit()


    def insert_from_file(self, students_list, groupid, year):
        '''Inserta en la base de datos nuevos alumnos pasados por
        archivo de texto
        Toma:
        students_list --  lista de alumnos en forma de tupla'''

        sql = 'INSERT INTO Alumno '
        sql += '(id, nombre, apellidos, telefono, direccion) '
        sql += 'VALUES (?, ?, ?, ?, ?);'
        try:
            self.__cursor.executemany(sql, students_list)
            self.__connection.commit()
        except sqlite3.IntegrityError:
            None
        finally:
            relationList = []
            for studentTuple in students_list:
                relationList.append((studentTuple[0], groupid, year))
            self.saveStudentForGroup_from_file(relationList)

    def saveStudentForGroup_from_file(self, relationList):
        '''Inserta en la base de datos la relacion entre los alumnos
        y el grupo'''
        sql = 'INSERT INTO GrupoAlumno (IdAlumno, IdGrupo, anio) '
        sql += 'VALUES(?, ?, ?)'
        print(relationList)
        self.__cursor.executemany(sql, relationList)
        self.__connection.commit()

    def loadGroup(self, groupid, year):
        if groupid is None or year is None:
            raise ValueError('El atributo id no puede ser nulo')
        sql = 'SELECT g.id as idg, g.nombre as nombreg, '
        sql += 'g.anio as aniog, p.id as idp, p.nombre as nombrep, '
        sql += 'p.apellidos as apellidosp, p.telefono as telefonop, '
        sql += 'a.id as idasig, a.nombre as nombreasig, '
        sql += 'al.id AS idal, al.nombre AS nombreal, periodo, '
        sql += 'al.apellidos AS apellidosal, al.Telefono AS telefonoal, al.direccion AS direccional '
        sql += 'FROM Grupo g, Profesor p, Asignatura a, Imparte i, Alumno al, GrupoAlumno gp, Anio '
        sql += 'WHERE ? = g.Id AND ? = g.anio AND g.id = i.IdGrupo AND a.id = i.idasignatura '
        sql += 'AND p.id = i.idprofesor AND i.anio = g.anio '
        sql += 'AND gp.IdAlumno = al.id and gp.IdGrupo = g.id AND gp.anio = g.anio'
        self.__cursor.execute(sql, (groupid, year,))
        rows = self.__cursor.fetchall()
        name = rows[0]['nombreg']
        year = rows[0]['aniog']
        imparted = self.__getClassesDict(rows, rows[0]['idg'], year)
        students = self.__getStudentsForGroupDict(rows, rows[0]['idg'], year)
        return (name, imparted, students)
        