#!/usr/bin/env python2
import sqlite3
import sys
from pylab import *

# Parse args
if len(sys.argv) < 3:
    print "usage: ./sql2plot.py path/to/db.sqlite query [OPTIONS]"
    print "    OPTIONS"
    print "        -f Show the least squares line of best fit."
    print "        -l Draw lines between data points."
    print "        -o Don't append ORDER BY 1 to the query."
    exit()

dbFile  = sys.argv[1]
query   = sys.argv[2]
showBfl = len(sys.argv) >= 4 and '-f' in sys.argv[-3:]
addLine = len(sys.argv) >= 4 and '-l' in sys.argv[-3:]
noOrder = len(sys.argv) >= 4 and '-o' in sys.argv[-3:]

# Augment query
query = query.replace('duration',       '(queryStopMs - queryStartMs)')
query = query.replace('timefromstart',  '(queryStartMs - sessStartMs)')
query = query.replace('timesincestart', '(queryStartMs - sessStartMs)')
if not noOrder:
    query += ' ORDER BY 1'

# Execute query, fetch results
conn = sqlite3.connect(dbFile)
c = conn.cursor()
c.execute(query)

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
