import re
import sys

def normaliseSpace(s):
    s = s.split()
    s = ' '.join(s)
    return s

def isNonLower(s):
    return bool(re.search('[^a-z]', s))

def getDuplicates(list):
    seen       = set()
    duplicates = set()

    for l in list:
        if l in seen:
            duplicates.add(l)
        seen.add(l)

    return duplicates

def nextFreeName(baseName, takenNames, sep='_', startingNumber=1):
    for i in xrange(startingNumber, sys.maxint):
        candidate = baseName + sep + str(i)
        if candidate not in takenNames:
            return candidate
    return None
