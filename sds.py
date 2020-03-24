import csv
from utils import to_sds_date

SCHOOL_ID = '1'

SCHOOL_FILENAME = 'School.csv'
SECTION_FILENAME = 'Section.csv'
STUDENT_FILENAME = 'Student.csv'
TEACHER_FILENAME = 'Teacher.csv'
STUDENT_ENROLLMENT_FILENAME = 'StudentEnrollment.csv'
TEACHER_ROSTER_FILENAME = 'TeacherRoster.csv'

class Writer:
    HEADERS = []

    def __init__(self, csvfile, datascource):
        self.csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
        self.datasource = datascource

    def row_iterator(self, sourcerow):
        return sourcerow

    def generate(self, *args, **kwargs):
        self.csvwriter.writerow(self.HEADERS)

        for sourcerow in self.datasource:
            self.csvwriter.writerow(self.row_iterator(sourcerow, *args, **kwargs))

class School(Writer):
    HEADERS = ['SIS ID', 'Name']

    def __init__(self, csvfile, schoolname):
        super(School, self).__init__(csvfile, [[SCHOOL_ID, schoolname]])

class Section(Writer):
    HEADERS = ['SIS ID', 'School SIS ID', 'Section Name', 'Term StartDate', 'Term EndDate']

    def __init__(self, csvfile, datascource):
        super(Section, self).__init__(csvfile, datascource)

    def row_iterator(self, sourcerow, schoolyear=2020):
        return [
            sourcerow.get_id(schoolyear),
            SCHOOL_ID,
            sourcerow.course.replace('_', ' '),
            to_sds_date(sourcerow.startdate),
            to_sds_date(sourcerow.enddate)
        ]

class Student(Writer):
    HEADERS = ['SIS ID', 'School SIS ID', 'Username', 'Grade', 'Birthdate']

    def __init__(self, csvfile, datascource):
        super(Student, self).__init__(csvfile, datascource)

    def row_iterator(self, sourcerow):
        return [sourcerow.shortname, SCHOOL_ID, sourcerow.get_username(), sourcerow.grade, to_sds_date(sourcerow.birthdate)]

class Teacher(Writer):
    HEADERS = ['SIS ID', 'School SIS ID', 'Username']

    def __init__(self, csvfile, datascource):
        super(Teacher, self).__init__(csvfile, datascource)

    def row_iterator(self, sourcerow):
        return [sourcerow.shortname, SCHOOL_ID, sourcerow.get_username()]

class StudentEnrollment(Writer):
    HEADERS = ['Section SIS ID', 'SIS ID']

    def __init__(self, csvfile, datascource):
        super(StudentEnrollment, self).__init__(csvfile, datascource)

    def row_iterator(self, sourcerow, schoolyear=2020):
        return [sourcerow.get_id(schoolyear), sourcerow.student]

class TeacherRoaster(Writer):
    HEADERS = ['Section SIS ID', 'SIS ID']

    def __init__(self, csvfile, datascource):
        super(TeacherRoaster, self).__init__(csvfile, datascource)

    def row_iterator(self, sourcerow, schoolyear=2020):
        return [sourcerow.get_id(schoolyear), sourcerow.teacher]