#! /usr/bin/env python

import json
import sys
import urllib2

def getRowValue(row, *columnNames):
    for n in columnNames:
        val = getRowValue_(row, n)
        if val:
            return val
    return ''

def getRowValue_(row, columnName):
    columnName = columnName.lower()
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
