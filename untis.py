import csv, re
from utils import to_ascii, to_grade_number

class Reader:
    def __init__(self, diffile, delimiter=',',  quotechar='"'):
        self.difreader = csv.reader(diffile, delimiter=delimiter, quotechar=quotechar)
        self.data = []

    def row_validator(self, row, *args, **kwargs):
        return True

    def row_iterator(self, row, *args, **kwargs):
        pass

    def populate(self, *args, **kwargs):
        for row in self.difreader:
            if self.row_validator(row, *args, **kwargs):
                self.data.append(self.row_iterator(row))

class GradeValidationReader(Reader):

    GRADE_INDEX = None

    def __init__(self, diffile, delimiter=',', quotechar='"'):
        super().__init__(diffile, delimiter=delimiter, quotechar=quotechar)

    def row_validator(self, row, grade_name=None, min_grade=None, max_grade=None):
        try:
            if (grade_name is not None) and (grade_name != row[self.GRADE_INDEX]):
                return False

            if (min_grade is not None) or (max_grade is not None):
                grade_number = to_grade_number(row[self.GRADE_INDEX])
                if (min_grade is not None) and (grade_number < min_grade):
                    return False
                if (max_grade is not None) and (grade_number > max_grade):
                    return False

            return True
        except ValueError:
            return False

class Course:
    def __init__(self, course, grade):
        self.course = course
        self.grade = grade

    def get_id(self, schoolyear):
        abi = schoolyear + (13 - self.grade)
        return str(abi) + '-' + self.course

class Lesson(Course):
    def __init__(self, course, grade, teacher):
        super(Lesson, self).__init__(course, grade)
        self.teacher = teacher

class LessonReader(GradeValidationReader):
    """ GPU002.TXT (Unterricht) """

    COURSE_INDEX = 6
    GRADE_INDEX = 4
    TEACHER_INDEX = 5
    STARTDATE_INDEX = 14
    ENDDATE_INDEX = 15

    def __init__(self, diffile, delimiter=',', quotechar='"'):
        super().__init__(diffile, delimiter=delimiter, quotechar=quotechar)

    def row_iterator(self, row):
        return Lesson(
            course=row[self.COURSE_INDEX],
            grade=to_grade_number(row[self.GRADE_INDEX]),
            teacher=row[self.TEACHER_INDEX]
        )

class Student:
    def __init__(self, shortname, sirname, firstname, grade):
        self.shortname = shortname
        self.sirname = sirname
        self.firstname = firstname
        self.grade = grade

    def get_username(self):
        return to_ascii(
            re.sub(r'\w\. ', '', self.firstname).split(' ')[0].lower() + 
            '.' + 
            re.sub(r'\w\. ', '', self.sirname.replace('von ', '')).split(' ')[0].lower()
        ).lower()

class StudentReader(GradeValidationReader):
    """ GPU010.TXT (Studenten) """

    SHORTNAME_INDEX = 0
    SIRNAME_INDEX = 1
    FIRSTNAME_INDEX = 7
    GRADE_INDEX = 9
    BIRTHDATE_INDEX = 12

    def __init__(self, diffile, delimiter=',', quotechar='"'):
        super().__init__(diffile, delimiter=delimiter, quotechar=quotechar)

    def row_iterator(self, row):
        return Student(
                shortname=to_ascii(row[self.SHORTNAME_INDEX]),
                sirname=row[self.SIRNAME_INDEX],
                firstname=row[self.FIRSTNAME_INDEX],
                grade=to_grade_number(row[self.GRADE_INDEX])
            )

class Teacher:
    def __init__(self, shortname, sirname, firstname, email):
        self.shortname = shortname
        self.sirname = sirname
        self.firstname = firstname
        self.email = email
    
    def get_username(self):
        return self.email.split('@', 1)[0].lower()

class TeacherReader(Reader):
    """ GPU004.TXT (Lehrer) """

    SHORTNAME_INDEX = 0
    SIRNAME_INDEX = 1
    FIRSTNAME_INDEX = 28
    EMAIL_INDEX = 32

    def __init__(self, diffile, delimiter=',', quotechar='"'):
        super().__init__(diffile, delimiter=delimiter, quotechar=quotechar)

    def row_iterator(self, row):
        return Teacher(
            shortname=row[self.SHORTNAME_INDEX],
            sirname=row[self.SIRNAME_INDEX],
            firstname=row[self.FIRSTNAME_INDEX],
            email=row[self.EMAIL_INDEX]
        )

class StudentEnrollment(Course):
    def __init__(self, course, grade, student):
        super(StudentEnrollment, self).__init__(course, grade)
        self.student = student

class StudentEnrollmentReader(GradeValidationReader):
    """ GPU015.TXT (Kurswahl) """

    STUDENT_INDEX = 0
    COURSE_INDEX = 2
    GRADE_INDEX = 4

    def __init__(self, diffile, delimiter=',', quotechar='"'):
        super().__init__(diffile, delimiter=delimiter, quotechar=quotechar)

    def row_validator(self, row, *args, **kwargs):
        return row[self.COURSE_INDEX] != '' and super().row_validator(row, *args, **kwargs)

    def row_iterator(self, row, *args, **kwargs):
        return StudentEnrollment(
            student=to_ascii(row[self.STUDENT_INDEX]),
            course=row[self.COURSE_INDEX],
            grade=to_grade_number(row[self.GRADE_INDEX])
        )
