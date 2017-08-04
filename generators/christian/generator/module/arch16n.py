#!/usr/bin/env python2

from   lxml import etree
import sys
import util.arch16n
import util.schema
import util.table
import util.xml

if __name__ == '__main__':
    # PARSE XML
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    # GENERATE AND OUTPUT ARCH16N
    # Collect arch16n entries
    arch16n = util.table.ARCH16N # Dictionary
    for n in util.xml.getAll(tree):
        k = util.arch16n.getArch16nKey(n, doAddCurlies=False)
        v = util.arch16n.getArch16nVal(n)
        if k and v:
            arch16n[k] = v

    # Turn arch16n dictionary into a sorted list
    arch16n = sorted(arch16n.items())

    # Print arch16n list
    for lineTuple in arch16n:
        key, val = lineTuple

        if not key or not val:
            continue

        lineString = '%s=%s' % (key, val)
        lineString = lineString.encode('utf8')

        print lineString
