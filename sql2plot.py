#!/usr/bin/env python2
import sqlite3
import sys
from pylab import *

if len(sys.argv) != 3:
    print "usage: ./sql2plot.py path/to/db.sqlite query"
    exit()

dbFile = sys.argv[1]
query  = sys.argv[2]

conn = sqlite3.connect(dbFile)
c = conn.cursor()
c.execute(query)

colNames = [d[0] for d in c.description]
x, y = [], []
for row in c.fetchall():
    x.append(float(row[0]))
    y.append(float(row[1]))

figure()
plot(x, y, 'g*-')
xlabel(colNames[0])
ylabel(colNames[1])
title(query)
show()
