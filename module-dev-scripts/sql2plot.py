#!/usr/bin/env python2
import sqlite3
import sys
from pylab import *
import math

aliasToReal = {
    'duration':       '(queryStopMs - queryStartMs)',
    'timefromstart':  '(queryStartMs - sessStartMs)',
    'timesincestart': '(queryStartMs - sessStartMs)',
}

# Helper functions
def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

def substCost(x,y):
    if x.lower() == y.lower():
        return 0.0
    if len(x) != len(y):
        return 1.0 - math.log(abs(len(x) - len(y)))*0.2
    return 2.0

@memoize
def  minEditDistR(target, source):
   """ Minimum edit distance. Straight from the recurrence. """

   i = len(target)
   j = len(source)

   if i == 0: return j
   if j == 0: return i

   return(min(minEditDistR(target[:i-1], source      )+substCost(source     , target[i-1]),
              minEditDistR(target      , source[:j-1])+substCost(source[j-1], target     ),
              minEditDistR(target[:i-1], source[:j-1])+substCost(source[j-1], target[i-1])))

def sortByStringSimilarity(string, candidates):
    if len(candidates) == 0:
        return None

    dists = [minEditDistR(string, candidate) for candidate in candidates]
    canDistPairs = zip(candidates, dists)
    canDistPairs.sort(key=lambda n: n[1])
    return zip(*canDistPairs)[0]

def getColumnNames(cursor):
    cursor.execute('SELECT * FROM perflog LIMIT 1')
    c.fetchone()
    return [f[0] for f in c.description] + aliasToReal.keys()

def getColumnNamesBySimilarity(cursor, string):
    return sortByStringSimilarity(string, getColumnNames(cursor))

# Parse args
if len(sys.argv) < 3:
    print "USAGE: ./sql2plot.py path/to/db.sqlite query [OPTIONS]"
    print
    print "OPTIONS"
    print "    -f Show the least squares line of best fit."
    print "    -l Draw lines between data points."
    print "    -o Don't append ORDER BY 1 to the query."
    exit()

dbFile  = sys.argv[1]
query   = sys.argv[2]
showBfl = len(sys.argv) >= 4 and '-f' in sys.argv[-3:]
addLine = len(sys.argv) >= 4 and '-l' in sys.argv[-3:]
noOrder = len(sys.argv) >= 4 and '-o' in sys.argv[-3:]

# Augment query
for alias, real in aliasToReal.iteritems():
    query = query.replace(alias, real)
if not noOrder:
    query += ' ORDER BY 1'

conn = sqlite3.connect(dbFile)
c = conn.cursor()

# Execute query, fetch results
try:
    c.execute(query)
except sqlite3.OperationalError, e:
    eStr = str(e).capitalize()

    # Get the name of the column which doesn't exist
    msg = 'No such column: '
    if msg in eStr:
        invalidColName = eStr.replace(msg, '')

        print eStr + '. Valid column names:'
        for colName in getColumnNamesBySimilarity(c, invalidColName):
            print '    ' + colName
    else:
        print eStr

    exit()

colNames = [d[0] for d in c.description]
x, y = [], []
for row in c.fetchall():
    x.append(float(row[0]))
    y.append(float(row[1]))

# Plot figure
markerStyle = 'o' + ('-' if addLine else '')

figure()
plot(x, y, markerStyle, markeredgewidth=0.0, alpha=0.33, label='Data')
if showBfl:
    m, b = np.polyfit(x, y, 1) # Best fit coefficients
    plot(
            np.unique(x),
            np.poly1d((m, b))(np.unique(x)),
            'r-',
            label='y = {0:.5f}x{1:+.5f}'.format(m, b)
    )
    legend()
xlabel(colNames[0])
ylabel(colNames[1])
title(query)
show()
