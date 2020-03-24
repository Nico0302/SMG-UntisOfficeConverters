from unidecode import unidecode
from re import sub

UMLAUT_TRANSLATION = str.maketrans({ 'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss' })

def to_ascii(string):
    return unidecode(string.translate(UMLAUT_TRANSLATION))

def to_grade_number(gardestring):
    return int(sub('[^0-9]', '', gardestring))

def to_sds_date(untisdate):
    return '/'.join([untisdate[4:6], untisdate[6:8], untisdate[0:4]])