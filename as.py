#!/usr/bin/env python2

# "as.py" = "Arch16n Substitutor"

import sys

def parseArchFile(filename):
    archKV = {}

    # Load arch16n file into dict
    for line in open(archFilename, 'r'):
        k, v = parseArchLine(line)

        if not k: continue
        if not v: continue

        archKV[k] = v

    return archKV

def parseArchLine(line):
    parsed = line.split('=')

    # Normalisation steps
    if len(parsed) != 2: parsed = ['', '']

    parsed[1] = parsed[1].replace('\n', '')

    return parsed

def substituteArch16nInLine(archKV, line):
    for k, v in archKV.iteritems():
        line = line.replace("{%s}" % k, v)
    return line

def substituteArch16n(archKV, lines):
    return [substituteArch16nInLine(archKV, line) for line in lines]

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 3:
    sys.stderr.write('USAGE:')
    sys.stderr.write('  as.py ARCH16N TARGET\n')
    exit()

archFilename = sys.argv[1]
targFilename = sys.argv[2]

archKV = parseArchFile(archFilename)
target = [line.rstrip('\n') for line in open(targFilename)]

targetWithSubstitutions = substituteArch16n(archKV, target)

print '\n'.join(targetWithSubstitutions)
