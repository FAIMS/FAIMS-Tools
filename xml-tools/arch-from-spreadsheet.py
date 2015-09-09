#! /usr/bin/env python

import json
import sys
import urllib2

def getRowValue(row, columnName):
    columnName = columnName.lower()
    columnName = 'gsx$%s' % columnName
    if columnName in row:
        return row[columnName]['$t'].encode('utf-8').strip()
    return ''

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
sheet_id = sys.argv[1]
url      = 'https://spreadsheets.google.com/feeds/list/' + sheet_id + '/1/public/values?prettyprint=true&alt=json';
response = urllib2.urlopen(url)
html     = response.read()
html     = json.loads(html)

archKV = {} # Arch16n key-value pairs

# Load arch16n contents into the `archKV` dict
for row in html['feed']['entry']:
    kColName = 'faimsVocab'
    vColName = 'mungoVocab'

    key = getRowValue(row, kColName)
    val = getRowValue(row, vColName)

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
