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

def nextFreeName(baseName, taken, sep='_', startingNumber=1):
    for i in xrange(startingNumber, sys.maxint):
        candidate = baseName + sep + str(i)
        if candidate not in taken:
            return candidate
    return None

def numberDuplicates(L, taken=None, sep='_'):
    '''
    Numbers a list of duplicated strings. Example:

        numberDuplicates(['a', 'a', 'b', 'a']) == ['a_1', 'a_2', 'b', 'a_3']
    '''
    if taken is None: taken = set()

    L = list(L)
    T = set(taken)
    D = getDuplicates(L) | T
    N = [] # Numbered list

    T = T | (set(L) - set(D))

    for l in L:
        if l in D: N.append(nextFreeName(l, T, sep))
        else:      N.append(l)

        T.add(N[-1])

    return N
