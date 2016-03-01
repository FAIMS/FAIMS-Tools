#!/usr/bin/env python

from   lxml import etree
import helpers
import tables
import sys

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = helpers.parseXml(filenameModule)
helpers.normaliseAttributes(tree)
helpers.expandCompositeElements(tree)

################################################################################
#                         GENERATE AND OUTPUT ARCH16N                          #
################################################################################
exp     = '//*'
matches = tree.xpath(exp)

# Generate
arch16n = tables.ARCH16N
for m in matches:
    k = helpers.getArch16nKey(m)
    v = helpers.getArch16nVal(m)
    if k and v:
        line = '%s=%s' % (k, v)
        arch16n.append(line)
arch16n = set(arch16n)
arch16n = sorted(arch16n)

# Print
for line in arch16n:
    print line
