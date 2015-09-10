#! /usr/bin/env python

# Copy the attributeLocation from SOURCE to TARGET. Output to stdout.

import sys

def addToEntNames(prop2EntNames, prop, entName):
    if prop not in prop2EntNames:
        prop2EntNames[prop] = set()
    prop2EntNames[prop].add(entName)

if len(sys.argv) < 3:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s SOURCE TARGET\n' % sys.argv[0])
    exit()

source = sys.argv[1]
target = sys.argv[2]

prop2EntNames = {}

# Read CSV's into lists
with open(source) as f:
    linesS = f.read().splitlines()
with open(target) as f:
    linesT = f.read().splitlines()

# Transform each CSV row to a list too
for i in range(len(linesS)):
    linesS[i] = linesS[i].split(',')
for i in range(len(linesT)):
    linesT[i] = linesT[i].split(',')

# Extract the faimsEntityAttributeName/attributeLocation pairs from the source
for i in range(len(linesS)):
    propS    = linesS[i][3]
    entNameS = linesS[i][5]
    addToEntNames(prop2EntNames, propS, entNameS)

# Transform prop2EntNames from a string -> set() map to a string -> string map
for k in prop2EntNames.iterkeys():
    prop2EntNames[k] = ';'.join(prop2EntNames[k])

# Augment the target CSV to include attributeLocations which were extracted
insertionPos = 2
linesT[0].insert(insertionPos, 'attributeLocation')
for i in range(1, len(linesT)):
    propT = linesT[i][1]
    if propT in prop2EntNames:
        entName = prop2EntNames[propT]
        linesT[i].insert(insertionPos, entName)
    else:
        linesT[i].insert(insertionPos, '')

# Transform each list representing a row in the target to a string
for i in range(len(linesT)):
    linesT[i] = ','.join(linesT[i])

# Print the result: the transformed target
for i in range(len(linesT)):
    sys.stdout.write(linesT[i] + '\n')
