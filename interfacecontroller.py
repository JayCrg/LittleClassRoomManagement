

class InterfaceController:

    def __init__(self, yearCollection, profCollection, courseCollection):
        self.yearCollection = yearCollection
        self.profCollection = profCollection
        self.courseCollection = courseCollection
    
    def getYears(self):
        return self.yearCollection 
    
    def getProfs(self):
        return self.profCollection 

    def getCourses(self):
        return self.courseCollection 

    def __getIdForGroupName(self, groupName, year):
        '''devuelve el id de un grupo en funcion de su nombre (y año)'''
        for groupid, group in self.yearCollection.getYear(year).groups.items():
            if group.getName() == groupName:
                return groupid

    def saveStudent(self, year, groupname, id, name, surname, direction, tel):
        groupid = self.__getIdForGroupName(groupname, year)
        self.yearCollection.getYear(year).getGroup(groupid).saveStudent(id, name, surname, direction, tel)

    '''def saveStudentForGroup(self, id, groupName, year):
        groupid = self.__getIdForGroupName(groupName, year)
        self.yearCollection.saveStudentForGroup(id, groupid, year)
        print(groupid)'''
    
    def loadYearsTree(self, tree):
        '''establece el arbol jeranrquico de cursos-grupos-alumnos
        siendo tree un objeto de la clase PySimpleGUI.Tree'''
        for yearid, year in self.getYears().yearsDict.items():
            tree.Insert("", '_{yearid}_', yearid, [''])
            for groupidtuple, group in year.groups.items():
                groupname = group.getName()
                groupid = str(groupidtuple[0])
                tree.Insert("_{yearid}_", '_{yearid}{groupid}_', groupname, [''],)
                for studentid, student in group.attendants.items():
                    studentname = student.getName() if student.getName() is not None else '------'
                    studentsurname = student.getSurname() if student.getSurname() is not None else '------'
                    studentdirection = student.getDirection() if student.getDirection() is not None else '------'
                    studentTel = student.getTel() if student.getTel() is not None else '------'
                    studentId = student.getId() if student.getId() is not None else '------'
                    tree.Insert("_{yearid}{groupid}_", '_{yearid}{groupid}{studentid}_', '', 
                    [studentId, studentname, studentsurname, studentdirection, studentTel],)
        return tree
    def yearCombo(self, lista):
        '''Devuelve por referencia una lista sordenada y formada
        por los identificadores de los años academicos'''
        for yearName in self.yearCollection.yearsDict.keys():
            lista.append(yearName)
        lista.sort()

    def getGroupsNameForYear(self, year):
        '''devuelve una lista con los nombres de los cursos 
        que hay en un año
        siendo year el id de un año'''
        lista = []
        for group in self.yearCollection.yearsDict[year].groups.values():
            lista.append(group.getName())
        return lista

    def saveProfessor(self, name, surname, tel):
        self.profCollection.saveProfessor(name, surname, tel)

    def saveCourse(self, name):
        self.courseCollection.saveCourse(name)

    def importStudentsFromFile(self, textfile, groupName, year):
        '''
        Guarda en la base de datos nuevos alumnos pasados por
        archivo de texto para un determinado grupo
        Toma:
        textfile -- archivo de texto con alumnos
        groupName -- nombre del grupo
        year -- año academico
        Puede devolver FileNotFoundError si el arhcivo no existe
        '''
        groupid = self.__getIdForGroupName(groupName, year)
        students_list = []
        students = open(textfile)
        students_file = students.readlines()
        for line in students_file:
            student = line.strip()
            student = student.split(',')
            for student_info in range(len(student)):
                if student[student_info].strip() == '':
                    student[student_info] = None
                else:
                    student[student_info] = \
                            student[student_info].strip()
            if student != [None]:
                students_list.append(tuple(student))
        students.close()
        print(students_list)
        self.yearCollection.getYear(groupid[1]).getGroup(groupid).saveStudentFromFile(students_list)




    