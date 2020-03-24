import csv
import untis

EXISTING_USERS_FILENAME = 'users_export.csv'
STUDENT_FILENAME = './untis/GPU010.TXT'
TEACHER_FILENAME = './untis/GPU004.TXT'
DIF_DELIMITER = ','
GRADE_FILTER = { 'min_grade': 11, 'max_grade': 12 }
STUDENT_OUTPUT_FILENAME = 'students.csv'
TEACHER_OUTPUT_FILENAME = 'teachers.csv'

OFFICE_TABLE_HEADER = ['User Name', 'First Name', 'Last Name', 'Display Name', 'Job Title', 'Department', 'Office Number', 'Office Phone', 'Mobile Phone', 'Fax', 'Address', 'City', 'State or Province', 'ZIP or Postal Code', 'Country or Region']

existing_users = []

existing_reader = csv.reader(open(EXISTING_USERS_FILENAME, newline=''), delimiter=',', quoting=csv.QUOTE_NONE)
for row in existing_reader:
    existing_users.append(row[30].split('@')[0])

student_reader = untis.StudentReader(open(STUDENT_FILENAME, newline=''), delimiter=DIF_DELIMITER)
student_reader.populate(**GRADE_FILTER)
student_writer = csv.writer(open(STUDENT_OUTPUT_FILENAME, 'w', newline=''), delimiter=',', quoting=csv.QUOTE_NONE)
student_writer.writerow(OFFICE_TABLE_HEADER)
for student in student_reader.data:
    username = student.get_username()
    if username not in existing_users:
        student_writer.writerow([username, student.firstname, student.sirname, student.firstname + ' ' + student.sirname])

teacher_reader = untis.TeacherReader(open(TEACHER_FILENAME, newline=''), delimiter=DIF_DELIMITER)
teacher_reader.populate(**GRADE_FILTER)
teacher_writer = csv.writer(open(TEACHER_OUTPUT_FILENAME, 'w', newline=''), delimiter=',', quoting=csv.QUOTE_NONE)
teacher_writer.writerow(OFFICE_TABLE_HEADER)
for teacher in teacher_reader.data:
    username = teacher.get_username()
    if username not in existing_users:
        teacher_writer.writerow([username, teacher.firstname, teacher.sirname, teacher.firstname + ' ' + teacher.sirname])