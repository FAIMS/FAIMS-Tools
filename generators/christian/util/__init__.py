import re
import sys
from copy import deepcopy

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

class Tree(object):
    def __init__(self, data=None, children=None):
        children = children or []

        self.i        = None
        self.data     = data
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, key):
        return self.children[key]

    def __str__repr__(self, fun):
        s = "\n- " + fun(self.data)
        if self.children != None:
            for c in self.children:
                s += fun(c).replace("\n", "\n  ")
        return s

    def __repr__(self): return self.__str__repr__(repr)
    def __str__ (self): return self.__str__repr__(str)

    def apply(self, fun, recursive=True):
        fun(self)
        for c in self.children:
            c.apply(fun, recursive)

    def applyNumbering(self):
        flat = self.flattened()
        for i, f in enumerate(flat):
            f.i = i

    def flattened(self):
        return [self] + sum([t.flattened() for t in self.children], [])
