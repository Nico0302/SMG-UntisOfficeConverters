import untis
import sds
import os
import errno

SCHOOLNAME = 'Sebastian-Münster-Gymnasium'
SCHOOLYEAR = 2020 # Jahreszahl des zweiten Halbjahres
LESSON_FILENAME = './untis/GPU002.TXT'
STUDENT_FILENAME = './untis/GPU010.TXT'
ENROLLMENT_FILENAME = './untis/GPU015.TXT'
TEACHER_FILENAME = './untis/GPU004.TXT'
DIF_DELIMITER = ','
GRADE_FILTER = { 'min_grade': 11, 'max_grade': 12 }
OUTPUT_DIRECTORY = './sds_tabels/'

def open_output_write(filename):
    if not os.path.exists(os.path.dirname(OUTPUT_DIRECTORY)):
        try:
            os.makedirs(os.path.dirname(OUTPUT_DIRECTORY))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    return open(os.path.dirname(OUTPUT_DIRECTORY) + '/' + filename, 'w', newline='')

# open Untis DIF-file readers
lesson_reader = untis.LessonReader(open(LESSON_FILENAME, newline=''), delimiter=DIF_DELIMITER)
student_reader = untis.StudentReader(open(STUDENT_FILENAME, newline=''), delimiter=DIF_DELIMITER)
teacher_reader = untis.TeacherReader(open(TEACHER_FILENAME, newline=''), delimiter=DIF_DELIMITER)
enrollment_reader = untis.StudentEnrollmentReader(open(ENROLLMENT_FILENAME, newline=''), delimiter=DIF_DELIMITER)

# populate data from files
lesson_reader.populate(**GRADE_FILTER)
student_reader.populate(**GRADE_FILTER)
teacher_reader.populate()
enrollment_reader.populate(**GRADE_FILTER)

# open SDS CSV-file writers
school_writer = sds.School(open_output_write(sds.SCHOOL_FILENAME), SCHOOLNAME)
section_writer = sds.Section(open_output_write(sds.SECTION_FILENAME), lesson_reader.data)
student_writer = sds.Student(open_output_write(sds.STUDENT_FILENAME), student_reader.data)
teacher_writer = sds.Teacher(open_output_write(sds.TEACHER_FILENAME), teacher_reader.data)
enrollment_writer = sds.StudentEnrollment(open_output_write(sds.STUDENT_ENROLLMENT_FILENAME), enrollment_reader.data)
roster_writer = sds.TeacherRoaster(open_output_write(sds.TEACHER_ROSTER_FILENAME), lesson_reader.data)

# generate SDS csv-files
school_writer.generate()
section_writer.generate(schoolyear=SCHOOLYEAR)
student_writer.generate()
teacher_writer.generate()
enrollment_writer.generate(schoolyear=SCHOOLYEAR)
roster_writer.generate(schoolyear=SCHOOLYEAR)