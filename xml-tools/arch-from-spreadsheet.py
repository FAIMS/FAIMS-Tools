#! /usr/bin/env python

import json
import sys
import urllib2
import spreadsheettools as sheets

def normaliseKey(key):
    key = key.replace('{', '')
    key = key.replace('}', '')
    key = key.replace(' ', '_')
    return key

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify Google Spreadsheet ID as argument\n')
    exit()

# Download the spreadsheet and interpret as JSON object
sheetId = sys.argv[1]
html = sheets.id2Html(sheetId)

archKV = {} # Arch16n key-value pairs

# Load arch16n contents into the `archKV` dict
for row in html['feed']['entry']:
    kColName = 'faimsVocab'
    vColName = 'mungoVocab'

    key = sheets.getRowValue(row, kColName)
    val = sheets.getRowValue(row, vColName)

    # Normalisation steps
    if key == '':                                                            # 1
        continue
    key = normaliseKey(key)                                                  # 2

    archKV[key] = val

# Transform dict to sorted list
archLines = []
for k, v in archKV.iteritems():
    archLines.append(k + "=" + v)
archLines.sort()

# Print list of arch16n entires
for line in archLines:
    print line
