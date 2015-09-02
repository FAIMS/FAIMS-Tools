# Copy the attributeLocation from draft3.csv to attributes.csv.  Output to
# stdout.

import sys

id2EntName = {}

with open('draft3.csv') as f:
    linesD = f.read().splitlines()
with open('attributes.csv') as f:
    linesA = f.read().splitlines()

for i in range(len(linesD)):
    linesD[i] = linesD[i].split(',')
for i in range(len(linesA)):
    linesA[i] = linesA[i].split(',')

for i in range(len(linesD)):
    idD   = linesD[i][0]
    nameD = linesD[i][2]
    id2EntName[idD] = nameD

linesA[0].insert(2, 'attributeLocation')
for i in range(1, len(linesA)):
    idA = linesA[i][0]
    if idA in id2EntName:
        nameD = id2EntName[idA]
        linesA[i].insert(2, nameD)
    else:
        linesA[i].insert(2, '')

for i in range(len(linesA)):
    linesA[i] = ','.join(linesA[i])

for i in range(len(linesA)):
    sys.stdout.write(linesA[i] + '\n')
