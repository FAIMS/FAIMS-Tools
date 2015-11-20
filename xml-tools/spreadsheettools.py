#! /usr/bin/env python

import json
import re
import sys
import urllib2

def setRowValue(row, columnName, value):
    columnName = columnName.lower()
    columnName = 'gsx$%s' % columnName
    if columnName not in row:
        return False

    value = str(value)
    value = value.encode('utf-8')
    row[columnName]['$t'] = value
    return True

def getRowValue(row, *columnNames):
    for n in columnNames:
        val = getRowValue_(row, n)
        if val:
            return val
    return ''

def getRowValue_(row, columnName):
    columnName = columnName.lower()
    columnName = re.sub('[^a-z]', '', columnName)
    columnName = 'gsx$%s' % columnName
    if columnName in row:
        return row[columnName]['$t'].encode('utf-8').strip()
    return ''

# Download spreadsheet and interpret as JSON object
def id2Html(sheetId):
    sheet_id = sys.argv[1]
    url      = 'https://spreadsheets.google.com/feeds/list/' + sheetId + '/1/public/values?prettyprint=true&alt=json';
    response = urllib2.urlopen(url)
    html     = response.read()
    html     = json.loads(html)
    return html
