import unittest
import sqlite3
from group import Group
from professor import Professor
from course import Course
from student import Student
from yeardbcontroller import YearDBController




class GroupTest(unittest.TestCase):
      @classmethod
      def setUpClass(cls):
            cls.connection =  sqlite3.connect(':memory:')
            cls.connection.row_factory = sqlite3.Row
            cls.cur = cls.connection.cursor()
            cls.cur.execute('''CREATE TABLE "Alumno" (
	"Id"	TEXT,
	"Nombre"	TEXT,
	"Apellidos"	TEXT,
	"Telefono"	INTEGER,
	"Direccion"	TEXT,
	PRIMARY KEY("Id")
);''')
            cls.cur.execute('''INSERT INTO Alumno VALUES ('111111','juan','perez','1234567','#~@#12')''')
            cls.cur.execute('''INSERT INTO Alumno VALUES ('222222','jose','rodriguez','9870987','fas#afa@f' )''')
            cls.cur.execute('''CREATE TABLE "Anio" (
	"Periodo"	TEXT,
	PRIMARY KEY("Periodo")
);''')
            cls.cur.execute('''INSERT INTO Anio VALUES ('2022/2023')''')
            cls.cur.execute('''CREATE TABLE "Asignatura" (
	"Id"	INTEGER,
	"Nombre"	TEXT,
	PRIMARY KEY("Id")
);''')
            cls.cur.execute('''INSERT INTO Asignatura VALUES (1, 'Matematicas')''')
            cls.cur.execute('''INSERT INTO Asignatura VALUES (2, 'Literatura')''')
            cls.cur.execute('''CREATE TABLE "Grupo" (
	"Nombre"	TEXT,
	"Id"	INTEGER,
	"anio"	TEXT,
	PRIMARY KEY("Id","anio")
);''')
            cls.cur.execute('''INSERT INTO Grupo VALUES ('1eso', 1,'2022/2023')''')

            cls.cur.execute('''CREATE TABLE "GrupoAlumno" (
	"IdAlumno"	TEXT,
	"IdGrupo"	INTEGER,
	"Anio"	TEXT,
	PRIMARY KEY("IdAlumno","IdGrupo","Anio")
);''')
            cls.cur.execute('''INSERT INTO GrupoAlumno VALUES ('111111', 1, '2022/2023')''')
            cls.cur.execute('''INSERT INTO GrupoAlumno VALUES ('222222', 1, '2022/2023')''')

            cls.cur.execute('''CREATE TABLE "Profesor" (
	"Id"	INTEGER,
	"Nombre"	TEXT,
	"Apellidos"	TEXT,
	"Telefono"	TEXT,
	PRIMARY KEY("Id")
);''')
            cls.cur.execute('''INSERT INTO Profesor(id, nombre, apellidos, telefono) VALUES (1, 'Macarena','Díaz', '345345')''')
            cls.cur.execute('''CREATE TABLE "Imparte" (
	"IdGrupo"	INTEGER,
	"Anio"	TEXT,
	"IdProfesor"	INTEGER,
	"IdAsignatura"	INTEGER,
	PRIMARY KEY("IdGrupo","IdProfesor","IdAsignatura","Anio")
);''')
            cls.cur.execute('''INSERT INTO Imparte VALUES (1, '2022/2023', 1, 1)''')

      @classmethod
      def tearDownClass(cls):
            cls.cur.execute('''DROP TABLE Alumno''')
            cls.cur.execute('''DROP TABLE Grupo''')
            cls.cur.execute('''DROP TABLE Anio''')
            cls.cur.execute('''DROP TABLE Profesor''')
            cls.cur.execute('''DROP TABLE Asignatura''')
            cls.cur.execute('''DROP TABLE Imparte''')
            cls.cur.execute('''DROP TABLE GrupoAlumno''')
            cls.connection.close()


      def test_constructor_All_Ok(self):
            # Given
            name = '1eso',
            year = '2022/2023', 
            id = 1, 
            dbmanager = self.connection
            # When
            grupo = Group(name, year, id, dbmanager)

            #Then
            self.assertIsNotNone(grupo)
            self.assertIsInstance(grupo, Group)
            self.assertIsInstance(grupo.attendants, dict)
            self.assertIsInstance(grupo.impartDict, dict)
            self.assertEqual(grupo.getId(), id)
            self.assertEqual(grupo.getName(), name)
            self.assertEqual(grupo.getYear(), year)

      def test_set_StudentClass_OK(self):
            # Given
            student_dict = {'5':Student('Juan', 'Perez', '3424352', 'q3qtg4', '5'),
            '9':Student('Julia', 'Martin', '987654', 'qqqqq', '9')}

            class_dict = {Course(1, 'Lengua'):Professor('Martin', 'Martin', '423423')}

            name = '1eso',
            year = '2022/2023', 
            id = 1, 
            dbmanager = self.connection
            grupo = Group(name, year, id, dbmanager)


           #Then
            grupo.setStudents(student_dict)
            grupo.setClasses(class_dict)

            #Then
            self.assertEqual(grupo.getAttendant('5'), student_dict['5'])
            self.assertEqual(list(grupo.getImpart().values())[0], list(class_dict.values())[0])
            self.assertEqual(list(grupo.getImpart().keys())[0], list(class_dict.keys())[0])

      @unittest.expectedFailure
      def test_set_StudentClass_Fail(self):
            # Given
            student_list = ('5',Student('Juan', 'Perez', '3424352', 'q3qtg4', '5'),
            '9',Student('Julia', 'Martin', '987654', 'qqqqq', '9'))

            student_dict = {'5':('Juan', 'Perez', '3424352', 'q3qtg4', '5'),
            '9':('Julia', 'Martin', '987654', 'qqqqq', '9')}

            class_list = (Course(1, 'Lengua'),Professor('Martin', 'Martin', '423423'))
            class_dict = {(1, 'Lengua'):('Martin', 'Martin', '423423')}


            name = '1eso',
            year = '2022/2023', 
            id = 1, 
            dbmanager = self.connection
            grupo = Group(name, year, id, dbmanager)

            #Then
            grupo.setStudents(student_dict)
            grupo.setClasses(class_dict)
            grupo.setStudents(student_list)
            grupo.setClasses(class_list)

      def test_loadGroup(self):
            # Given
            idg = 1
            yearg='2022/2023'
            manager = YearDBController(self.connection)
            grupo = Group(id=idg, year=yearg, dbmanager=manager)

            #When 
            grupo.loadGroup()

            #Then
            self.assertIsInstance(grupo.attendants['111111'], Student)
            self.assertIsInstance(list(grupo.impartDict.keys())[0], Course)
            self.assertIsInstance(list(grupo.impartDict.values())[0], Professor)            
            self.assertEqual(grupo.attendants['111111'].getName(), 'juan')
            self.assertEqual(list(grupo.impartDict.values())[0].getName(), 'Macarena')
            self.assertEqual(list(grupo.impartDict.keys())[0].getName(), 'Matematicas')
            self.assertEqual(len(grupo.impartDict.keys()), 1)
            self.assertEqual(len(grupo.impartDict.values()), 1)

      def test_saveStudent(self):
            # Given
            id = '333333'
            nombre = 'maria'
            apellidos = 'alcaide'
            dir = '87ijhk'
            tel = '976987'
            
            manager = YearDBController(self.connection)
            name = '1eso'
            year = '2022/2023'
            idg = 1
            grupo = Group(name, year, idg, manager)

            # When
            grupo.saveStudent(id, nombre, apellidos, dir, tel)

            # Then
            self.assertEqual(grupo.attendants[id].getName(), nombre)
            grupo.loadGroup()
            self.assertEqual(grupo.attendants[id].getName(), nombre)
            self.cur.execute('DELETE FROM Alumno WHERE id = ?',(id,))
            self.cur.execute('DELETE FROM GrupoAlumno WHERE idAlumno = ? AND anio = ? AND idGrupo = ?',(id, year, idg))


      def test_save_from_file(self):
            # Given
            insert = [('333333','rosa','guerrero','gerge','1312413'),('44444','pedro','alonso','4erge','976987'),
            ('55555','miguel','prieto','rwrh','23456'),('66666','beatriz','sanchez','kjhgf','098421')]
            
            manager = YearDBController(self.connection)
            name = '1eso'
            year = '2022/2023'
            idg = 1
            grupo = Group(name, year, idg, manager)

            # When
            grupo.saveStudentFromFile(insert)

            # Then
            self.assertEqual(grupo.attendants[insert[0][0]].getName(), insert[0][1])
            grupo.loadGroup()
            self.assertEqual(grupo.attendants[insert[1][0]].getName(), insert[1][1])





      
if __name__ == '__main__':
      unittest.main()