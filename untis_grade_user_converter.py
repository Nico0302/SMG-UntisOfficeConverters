""" Generieren von Nutzer CSV-Tabellen zum import der Oberstufe in Office 365. """

import csv, untis

EXISTING_USERS_FILENAME = 'users_export.csv'
STUDENT_FILENAME = './untis/GPU010.TXT'
TEACHER_FILENAME = './untis/GPU004.TXT'
DIF_DELIMITER = ','
DIF_ENCODING = 'utf-8'
GRADE_FILTER = { 'min_grade': 11, 'max_grade': 12 }
STUDENT_OUTPUT_FILENAME = 'students.csv'
TEACHER_OUTPUT_FILENAME = 'teachers.csv'
STUDENT_DOMAIN = 'smg-schueler.de'
TEACHER_DOMAIN = 'smg-ingelheim.de'

OFFICE_TABLE_HEADER = ['User Name', 'First Name', 'Last Name', 'Display Name', 'Job Title', 'Department', 'Office Number', 'Office Phone', 'Mobile Phone', 'Fax', 'Address', 'City', 'State or Province', 'ZIP or Postal Code', 'Country or Region']

existing_users = []

with open(EXISTING_USERS_FILENAME, encoding='utf-8', newline='') as users_file:
    existing_reader = csv.reader(users_file, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in existing_reader:
        existing_users.append(row[30])

with open(STUDENT_FILENAME, encoding=DIF_ENCODING, newline='') as student_file:
    student_reader = untis.StudentReader(student_file, delimiter=DIF_DELIMITER)
    student_reader.populate(**GRADE_FILTER)
    with open(STUDENT_OUTPUT_FILENAME, 'w', encoding='utf-8', newline='') as student_output:
        student_writer = csv.writer(student_output, delimiter=',', quoting=csv.QUOTE_NONE)
        student_writer.writerow(OFFICE_TABLE_HEADER)
        for student in student_reader.data:
            username = student.get_username()
            email = '{0}@{1}'.format(username, STUDENT_DOMAIN)
            if email not in existing_users:
                student_writer.writerow([
                    email,
                    student.firstname,
                    student.sirname,
                    student.firstname.split(' ')[0] + ' ' + student.sirname
                ])

with open(TEACHER_FILENAME, encoding=DIF_ENCODING, newline='') as teacher_file:
    teacher_reader = untis.TeacherReader(teacher_file, delimiter=DIF_DELIMITER)
    teacher_reader.populate(**GRADE_FILTER)
    with open(TEACHER_OUTPUT_FILENAME, 'w', encoding='utf-8', newline='') as teacher_output:
        teacher_writer = csv.writer(teacher_output, delimiter=',', quoting=csv.QUOTE_NONE)
        teacher_writer.writerow(OFFICE_TABLE_HEADER)
        for teacher in teacher_reader.data:
            username = teacher.get_username()
            email = '{0}@{1}'.format(username, TEACHER_DOMAIN)
            if email not in existing_users:
                teacher_writer.writerow([
                    email,
                    teacher.firstname,
                    teacher.sirname,
                    teacher.firstname.split(' ')[0] + ' ' + teacher.sirname
                ])
