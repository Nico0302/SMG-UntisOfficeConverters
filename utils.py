from unidecode import unidecode
from re import sub

UMLAUT_TRANSLATION = { 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss' }

def to_ascii(string):
    a = string  # a new string to store the replaced string
    for i in string:
        if i in UMLAUT_TRANSLATION:
            a = a.replace(i, UMLAUT_TRANSLATION[i])
    return unidecode(a)

def to_grade_number(gardestring):
    return int(sub('[^0-9]', '', gardestring))

def to_sds_date(untisdate):
    return '/'.join([untisdate[4:6], untisdate[6:8], untisdate[0:4]])