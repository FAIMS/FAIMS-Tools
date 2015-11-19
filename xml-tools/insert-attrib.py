#! /usr/bin/env python

import sys
import xmltools
from   lxml import etree
from   copy import deepcopy

def parseXpathExpressions(filename):
    with open(filename) as f:
        flagPaths = f.readlines()
    return flagPaths

def selectAllNodes(tree, expressions):
    allNodes = []
    for e in expressions:
        someNodes = tree.xpath(e)
        allNodes.extend(someNodes)
    return allNodes

def parseAttrib(str):
    s = str.split('=')
    if len(s) != 2:
        return None
    return s

################################################################################
#                                     MAIN                                     #
################################################################################
reservedCopy = '__RESERVED_CP__'

if len(sys.argv) < 4:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s XML NODES ATTRIB\n' % sys.argv[0])
    sys.stderr.write('\n')
    sys.stderr.write('DESCRIPTION\n')
    sys.stderr.write('   Adds the attribute ATTRIB to each XML node specified\n')
    sys.stderr.write('   in NODES\n')
    sys.stderr.write('\n')
    exit()

XML    = sys.argv[1]
NODES  = sys.argv[2]
ATTRIB = sys.argv[3]

if not parseAttrib(ATTRIB):
    sys.stderr.write('Attribute could not be parsed.\n')
    exit()

# Parse XML
parser = etree.XMLParser(strip_cdata=False)
tree = etree.parse(XML, parser)
tree = tree.getroot()

expressions = parseXpathExpressions(NODES)
nodes = selectAllNodes(tree, expressions)

# Mark each node
key, val = parseAttrib(ATTRIB)
for n in nodes:
    n.attrib[key] = val

# Collect your prize
print etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')
