import re

def normaliseSpace(str):
    str = str.split()
    str = ' '.join(str)
    return str

def isNonLower(s):
    return bool(re.search('[^a-z]', s))
