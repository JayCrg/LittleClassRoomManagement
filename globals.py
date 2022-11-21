from interfacecontroller import InterfaceController
from generaldbcontroller import GeneralDBController
from yearcollection import YearCollection
from courseCollection import CourseCollection
from professorcollection import ProfessorCollection
import sqlite3

con = sqlite3.connect('highschool.db')

generalDBManger = GeneralDBController(con)

yearcollec = YearCollection(generalDBManger)
coursecollec = CourseCollection(generalDBManger)
profcollec = ProfessorCollection(generalDBManger)

controller = InterfaceController(yearcollec, profcollec, coursecollec)


