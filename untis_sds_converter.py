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
DIF_ENCODING = 'utf-8'
GRADE_FILTER = { 'min_grade': 11, 'max_grade': 12 }
OUTPUT_DIRECTORY = './sds_tabels/'
OUTPUT_ENCODING = 'utf-8'

def open_output_write(filename):
    if not os.path.exists(os.path.dirname(OUTPUT_DIRECTORY)):
        try:
            os.makedirs(os.path.dirname(OUTPUT_DIRECTORY))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    return open(os.path.dirname(OUTPUT_DIRECTORY) + '/' + filename, 'w', encoding=OUTPUT_ENCODING, newline='')

lesson_file = open(LESSON_FILENAME, encoding=DIF_ENCODING, newline='')
student_file = open(STUDENT_FILENAME,encoding=DIF_ENCODING, newline='')
teacher_file = open(TEACHER_FILENAME, encoding=DIF_ENCODING, newline='')
enrollment_file = open(ENROLLMENT_FILENAME, encoding=DIF_ENCODING, newline='')

lesson_reader = untis.LessonReader(lesson_file, delimiter=DIF_DELIMITER)
student_reader = untis.StudentReader(student_file, delimiter=DIF_DELIMITER)
teacher_reader = untis.TeacherReader(teacher_file, delimiter=DIF_DELIMITER)
enrollment_reader = untis.StudentEnrollmentReader(enrollment_file, delimiter=DIF_DELIMITER)

# populate data from files
lesson_reader.populate(**GRADE_FILTER)
student_reader.populate(**GRADE_FILTER)
teacher_reader.populate()
enrollment_reader.populate(**GRADE_FILTER)

# close filestreams
lesson_file.close()
student_file.close()
teacher_file.close()
enrollment_file.close()

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