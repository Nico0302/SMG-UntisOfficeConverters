""" Generieren von Nutzer CSV-Tabellen zum import einer Mittelstufenklasse in Office 365. """

import csv, untis

EXISTING_USERS_FILENAME = 'users_export.csv'
STUDENT_FILENAME = './untis/GPU010.TXT'
DIF_DELIMITER = ','
DIF_ENCODING = 'utf-8'
STUDENT_OUTPUT_PREFIX = 'students'
STUDENT_DOMAIN = 'smg-schueler.de'

OFFICE_TABLE_HEADER = ['User Name', 'First Name', 'Last Name', 'Display Name', 'Job Title', 'Department', 'Office Number', 'Office Phone', 'Mobile Phone', 'Fax', 'Address', 'City', 'State or Province', 'ZIP or Postal Code', 'Country or Region']

grade = input('Klassenname zum importieren (z.B. 10g): ')

existing_users = []

with open(EXISTING_USERS_FILENAME, encoding='utf-8', newline='') as users_file:
    existing_reader = csv.reader(users_file, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in existing_reader:
        existing_users.append(row[30])

with open(STUDENT_FILENAME, encoding=DIF_ENCODING, newline='') as student_file:
    student_reader = untis.StudentReader(student_file, delimiter=DIF_DELIMITER)
    student_reader.populate({ 'grade_name': grade })
    filename = '{0}_{1}.csv'.format(STUDENT_OUTPUT_PREFIX, grade)
    with open(filename, 'w', encoding='utf-8', newline='') as student_output:
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
