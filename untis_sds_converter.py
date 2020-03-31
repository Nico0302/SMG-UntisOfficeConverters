""" Generieren von School-Data-Sync CSV-Tabellen. """

import untis, sds, os, errno

SCHOOLNAME = 'Sebastian-Münster-Gymnasium'
LESSON_FILENAME = './untis/GPU002.TXT'
STUDENT_FILENAME = './untis/GPU010.TXT'
ENROLLMENT_FILENAME = './untis/GPU015.TXT'
TEACHER_FILENAME = './untis/GPU004.TXT'
DIF_DELIMITER = ','
DIF_ENCODING = 'utf-8'
GRADE_FILTER = { 'min_grade': 11, 'max_grade': 12 }
OUTPUT_DIRECTORY = './sds_tabels/'
OUTPUT_ENCODING = 'utf-8'

schoolyear = int(input('Jahreszahl des zweiten Halbjahres: '))

def open_output_write(filename):
    if not os.path.exists(os.path.dirname(OUTPUT_DIRECTORY)):
        try:
            os.makedirs(os.path.dirname(OUTPUT_DIRECTORY))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    return open(os.path.dirname(OUTPUT_DIRECTORY) + '/' + filename, 'w', encoding=OUTPUT_ENCODING, newline='')

def open_input_read(filename):
    return open(filename, encoding=DIF_ENCODING, newline='')

# lessons (GPU002.TXT)
with open_input_read(LESSON_FILENAME) as lesson_file:
    lesson_reader = untis.LessonReader(lesson_file, delimiter=DIF_DELIMITER)
    lesson_reader.populate(**GRADE_FILTER)

    with open_output_write(sds.SECTION_FILENAME) as section_file:
        sds.Section(section_file, lesson_reader.data).generate(schoolyear=schoolyear)

    with open_output_write(sds.TEACHER_ROSTER_FILENAME) as roster_file:
        sds.TeacherRoaster(roster_file, lesson_reader.data).generate(schoolyear=schoolyear)

# students (GPU010.TXT)
with open_input_read(STUDENT_FILENAME) as student_file:
    student_reader = untis.StudentReader(student_file, delimiter=DIF_DELIMITER)
    student_reader.populate(**GRADE_FILTER)

    with open_output_write(sds.STUDENT_FILENAME) as student_file:
        sds.Student(student_file, student_reader.data).generate()

# teachers (GPU004.TXT)
with open_input_read(TEACHER_FILENAME) as teacher_file:
    teacher_reader = untis.TeacherReader(teacher_file, delimiter=DIF_DELIMITER)
    teacher_reader.populate()

    with open_output_write(sds.TEACHER_FILENAME) as teacher_file:
        sds.Teacher(teacher_file, teacher_reader.data).generate()

# student enrollment (GPU015.TXT)
with open_input_read(ENROLLMENT_FILENAME) as enrollment_file:
    enrollment_reader = untis.StudentEnrollmentReader(enrollment_file, delimiter=DIF_DELIMITER)
    enrollment_reader.populate(**GRADE_FILTER)

    with open_output_write(sds.STUDENT_ENROLLMENT_FILENAME) as enrollment_file:
        sds.StudentEnrollment(enrollment_file, enrollment_reader.data).generate()

# SDS school csv
with open_output_write(sds.SCHOOL_FILENAME) as school_file:
    sds.School(school_file, SCHOOLNAME).generate()

print('Untis-Dateien wurden erfolgreich konvertiert!')
print(OUTPUT_DIRECTORY)
input('Drücken Sie Enter um das Programm zu beenden ...')
