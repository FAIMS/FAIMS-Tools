#!/usr/bin/env python2

from   lxml import etree
import sys
import util.arch16n
import util.schema
import util.table
import util.xml

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithTypes(tree)
util.schema.expandCompositeElements(tree)

################################################################################
#                         GENERATE AND OUTPUT ARCH16N                          #
################################################################################
exp     = '//*'
matches = tree.xpath(exp)

# Generate
arch16n = util.table.ARCH16N
for m in matches:
    k = util.arch16n.getArch16nKey(m)
    v = util.arch16n.getArch16nVal(m)
    if k and v:
        line = '%s=%s' % (k, v)
        arch16n.append(line)
arch16n = set(arch16n)
arch16n = sorted(arch16n)

# Print
for line in arch16n:
    print line