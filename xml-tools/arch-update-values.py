#! /usr/bin/env python

import json
import sys
import urllib2
import spreadsheettools as sheets

def readArch16n(filename):
    ''' Returns [[str, str], ..., [str, str]]'''
    with open(filename) as f:
        file = f.readlines()
    file = [line for line in file if line.strip() != '']
    for i in range(len(file)):
        file[i] = file[i].strip().split('=')
    return file

def printArch16n(arch16nData):
    for line in arch16nData:
        print '%s=%s' % (line[0], line[1])

def getValUpdates(html):
    ''' Returns mapping from old val -> new val'''
    archKK = {}
    for row in html['feed']['entry']:
        colNameOld = 'Suggested English Translation'
        colNameNew = 'French'

        valOld = sheets.getRowValue(row, colNameOld)
        valNew = sheets.getRowValue(row, colNameNew)

        archKK[valOld] = valNew
    return archKK

def findUpdate(updates, oldVal):
    if oldVal in updates:
        return updates[oldVal]
    else:
        return None

def applyValUpdates(arch16nData, updates):
    for i in range(len(arch16nData)):
        valOld = arch16nData[i][1]
        valNew = findUpdate(updates, valOld)
        if valNew == None:
            continue
        arch16nData[i][1] = valNew
    return arch16nData

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 3:
    sys.stderr.write('Usage: SPREADSHEET ARCH16N\n')
    exit()

# Read the arch16n into lines
filename = sys.argv[2]
arch16n  = readArch16n(filename)

# Download the spreadsheet and interpret as JSON object
sheetId = sys.argv[1]
html    = sheets.id2Html(sheetId)

# Get the key updates from the spreadsheet
archKK = getValUpdates(html)

# Update
archKK = applyValUpdates(arch16n, archKK)

# Print
printArch16n(archKK)
