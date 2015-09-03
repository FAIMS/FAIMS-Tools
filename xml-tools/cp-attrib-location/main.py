# Copy the attributeLocation from draft3.csv to attributes.csv.  Output to
# stdout.
# TODO specify which column to join on
import sys

if len(sys.argv) < 3:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s SOURCE TARGET\n' % sys.argv[0])
    exit()

source = sys.argv[1]
target = sys.argv[2]

id2EntName = {}

with open(source) as f:
    linesS = f.read().splitlines()
with open(target) as f:
    linesT = f.read().splitlines()

for i in range(len(linesS)):
    linesS[i] = linesS[i].split(',')
for i in range(len(linesT)):
    linesT[i] = linesT[i].split(',')

for i in range(len(linesS)):
    idS   = linesS[i][0]
    nameS = linesS[i][2]
    id2EntName[idS] = nameS

linesT[0].insert(2, 'attributeLocation')
for i in range(1, len(linesT)):
    idT = linesT[i][0]
    if idT in id2EntName:
        nameS = id2EntName[idT]
        linesT[i].insert(2, nameS)
    else:
        linesT[i].insert(2, '')

for i in range(len(linesT)):
    linesT[i] = ','.join(linesT[i])

for i in range(len(linesT)):
    sys.stdout.write(linesT[i] + '\n')
