#! /usr/bin/env python

import sys
import xmltools
from   lxml import etree
from   copy import deepcopy

def parseXpathExpressions(filename):
    with open(filename) as f:
        flagPaths = f.readlines()
    for i in range(len(flagPaths)):
        flagPaths[i] = flagPaths[i].strip()
    return flagPaths

def selectAllNodes(tree, expressions):
    allNodes = []
    for e in expressions:
        someNodes = tree.xpath(e)
        allNodes.extend(someNodes)
        if len(someNodes) != 1:
            warn = 'WARNING: "%s" matches %s nodes, which isn\'t exactly 1' % \
                    (e, len(someNodes))
            sys.stderr.write(warn)
    return allNodes

def filterUINodes(nodes):
    UInodes = []
    for n in nodes:
        if 'faims_attribute_name' in n.attrib:
            UInodes.append(n)
    return UInodes

def getEntProps(nodes):
    entProps = []
    for n in nodes:
        entProps.append(getEntProp(n))
    return entProps

def getEntProp(node):
    if not hasattr(node, 'attrib'):
        return None

    archentNode = node.xpath('ancestor::*[@faims_archent_type]')
    if archentNode:
        archentNode = archentNode[0]
    else:
        archentNode = node

    if 'faims_attribute_name' not in node.attrib:
        return None
    if 'faims_archent_type'   not in archentNode.attrib:
        return None

    prop = node       .attrib['faims_attribute_name']
    ent  = archentNode.attrib['faims_archent_type']

    return (ent, prop)

################################################################################
#                                     MAIN                                     #
################################################################################
reservedCopy = '__RESERVED_CP__'

if len(sys.argv) < 3:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s UISCHEMA NODES\n' % sys.argv[0])
    sys.stderr.write('\n')
    sys.stderr.write('DESCRIPTION\n')
    sys.stderr.write('   Prints the archent and property for each UI element matched by the XPath\n')
    sys.stderr.write('   expressions in NODES.\n')
    sys.stderr.write('\n')
    exit()

UISCHEMA = sys.argv[1]
NODES    = sys.argv[2]

# Parse UISCHEMA
parser = etree.XMLParser(strip_cdata=False)
tree = etree.parse(UISCHEMA, parser)
tree = tree.getroot()

expressions = parseXpathExpressions(NODES)
nodes = selectAllNodes(tree, expressions)
nodes = filterUINodes(nodes)
entProps = getEntProps(nodes)

# Output
for ep in entProps:
    out = '%s, %s' % ep
    print out
