#!/usr/bin/env python2
import sqlite3
import sys
from pylab import *

if len(sys.argv) < 3:
    print "usage: ./sql2plot.py path/to/db.sqlite query [-f]"
    print "    OPTIONS"
    print "        -f Show the least squares line of best fit."
    exit()

dbFile  = sys.argv[1]
query   = sys.argv[2]
showBfl = True if len(sys.argv) >= 4 and sys.argv[3] == '-f' else False

conn = sqlite3.connect(dbFile)
c = conn.cursor()
c.execute(query)

colNames = [d[0] for d in c.description]
x, y = [], []
for row in c.fetchall():
    x.append(float(row[0]))
    y.append(float(row[1]))

# Best-fit coefficients
m, b = np.polyfit(x, y, 1)

# Plot figure
figure()
plot(x, y, 'g*-', label='Data')
if showBfl:
    plot(
            np.unique(x),
            np.poly1d((m, b))(np.unique(x)),
            label='y = {0:.5f}x{1:+.5f}'.format(m, b)
    )
    legend()
xlabel(colNames[0])
ylabel(colNames[1])
title(query)
show()
