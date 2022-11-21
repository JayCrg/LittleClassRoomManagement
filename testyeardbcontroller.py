import unittest
import sqlite3
from group import Group
from student import Student
from year import Year
from yeardbcontroller import YearDBController 



class YearDBControllerTest(unittest.TestCase):
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
            mydbcontroller = YearDBController(self.connection)
            #When

            # Then
            self.assertIsNotNone(mydbcontroller)
            self.assertIsInstance(mydbcontroller, YearDBController)
            

      def test_load_Ok(self):
            # Given
            self.cur.execute('SELECT Periodo FROM Anio')
            anio = self.cur.fetchone()
            numeroanio = anio['Periodo']
                  # print(numeroanio)
            self.cur.execute('SELECT id, nombre, anio FROM Grupo WHERE anio = ?',(numeroanio,))
            lineagrupo = self.cur.fetchone()
            grupoid = lineagrupo['id']
                  # print(grupoid)
            sql = 'SELECT a.id AS ida, a.nombre as nombrea, apellidos, telefono, direccion '
            sql += 'FROM Alumno a, GrupoAlumno gp, Grupo g WHERE a.id = gp.idAlumno AND ? = gp.IdGrupo'
            self.cur.execute(sql, (grupoid,))
            lineaslumno = self.cur.fetchall()
            idalumno = lineaslumno[0]['ida']
            nombre = lineaslumno[0]['nombrea']
                  # print(idalumno)
            sql = 'SELECT p.id as idp, p.nombre as nombrep, apellidos, telefono, asg.nombre as nombrea '
            sql += 'FROM Profesor p, Imparte i, Grupo g, Asignatura asg WHERE p.id = i.idProfesor AND ? = i.IdGrupo '
            sql += 'AND asg.id = i.idAsignatura'
            self.cur.execute(sql, (grupoid,))
            lineaclase = self.cur.fetchone()
            nombre_prof = lineaclase['nombrep']
            nombre_asig = lineaclase['nombrea']

            myAnio = YearDBController(self.connection)
            # When
            aniosDict = myAnio.loadYearsDict()
            # Then
            self.assertIsInstance(aniosDict, dict)
            self.assertIsInstance(aniosDict[numeroanio], Year)
            self.assertIsInstance(aniosDict[numeroanio].groups[(grupoid, numeroanio)], Group)
            self.assertIsInstance(aniosDict[numeroanio].groups[(grupoid, numeroanio)].attendants[idalumno], Student)            
            self.assertEqual(aniosDict[numeroanio].groups[(grupoid, numeroanio)].attendants[idalumno].getName(), nombre)
            self.assertEqual(list(aniosDict[numeroanio].groups[(grupoid, numeroanio)].impartDict.values())[0].getName(), nombre_prof)
            self.assertEqual(list(aniosDict[numeroanio].groups[(grupoid, numeroanio)].impartDict.keys())[0].getName(), nombre_asig)
            

      def test_SaveStudent_Ok(self):
            # Given
            id = '333333'
            nombre = 'maria'
            apellidos = 'alcaide'
            dir = '87ijhk'
            tel = '976987'
            anio = '2022/2023'
            grupo = 1
            myAnio = YearDBController(self.connection)
            
            #When
            myAnio.saveStudent(anio, grupo, id, nombre, apellidos, dir, tel)

            # Then
            info = myAnio.loadYearsDict()
            self.cur.execute('SELECT id, nombre, apellidos, telefono, direccion FROM Alumno WHERE id = ?',(id,))
            result = self.cur.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result['id'], info[anio].groups[grupo, anio].attendants[id].getId())
            self.assertEqual(result['direccion'], info[anio].groups[grupo, anio].attendants[id].getDirection())
            self.assertEqual(result['nombre'], info[anio].groups[grupo, anio].attendants[id].getName())
            self.assertEqual(result['apellidos'], info[anio].groups[grupo, anio].attendants[id].getSurname())
            self.assertEqual(result['telefono'], info[anio].groups[grupo, anio].attendants[id].getTel())
            self.cur.execute('DELETE FROM Alumno WHERE id = ?',(id,))
            self.cur.execute('DELETE FROM GrupoAlumno WHERE idAlumno = ? AND anio = ? AND idGrupo = ?',(id, anio, grupo))

      def test_SaveStudent_from_file_Ok(self):
            # Given
            insert = [('333333','rosa','guerrero','gerge','1312413'),('44444','pedro','alonso','4erge','976987'),
            ('55555','miguel','prieto','rwrh','23456'),('66666','beatriz','sanchez','kjhgf','098421')]
            idgrupo = 1
            anio = '2022/2023'
            idtuple = ('333333', '44444', '55555', '66666')
            auxlist = []
            for id in idtuple:
                  auxlist.append((id, anio, idgrupo))
            print(auxlist)
            # When
            myAnio = YearDBController(self.connection)
            myAnio.insert_from_file(insert, idgrupo, anio)

            # Then
            info = myAnio.loadYearsDict()
            self.cur.execute('SELECT id, nombre, apellidos, telefono, direccion FROM Alumno')
            rows = self.cur.fetchall()
            for row in rows:
                  self.assertEqual(row['id'], info[anio].groups[idgrupo, anio].attendants[row['id']].getId())
                  self.assertEqual(row['direccion'], info[anio].groups[idgrupo, anio].attendants[row['id']].getDirection())
                  self.assertEqual(row['nombre'], info[anio].groups[idgrupo, anio].attendants[row['id']].getName())
                  self.assertEqual(row['apellidos'], info[anio].groups[idgrupo, anio].attendants[row['id']].getSurname())
                  self.assertEqual(row['telefono'], info[anio].groups[idgrupo, anio].attendants[row['id']].getTel())
            self.cur.execute(f'DELETE FROM Alumno WHERE id IN {idtuple}')
            self.cur.executemany('DELETE FROM GrupoAlumno WHERE idAlumno = ? AND anio = ? AND idGrupo = ?',(auxlist))




      
if __name__ == '__main__':
      unittest.main()