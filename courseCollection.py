from course import Course


class CourseCollection:

    def __init__(self, dbmanager):
        self.__dbmanager = dbmanager
        self.courseDict = self.loadCourses()

    def getYear(self, id):
        try:
            return self.courseDict[id]
        except KeyError:
            return None
        
    def loadCourses(self):
        return self.__dbmanager.loadCourses()

    def saveCourse(self, name):
        id = max(self.courseDict.keys()) + 1 if len(self.courseDict.keys()) > 0 else 1
        self.courseDict.setdefault(id, Course(id, name))
        self.__dbmanager.saveCourse(id, name)

