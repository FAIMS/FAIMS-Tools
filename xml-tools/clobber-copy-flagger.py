#! /usr/bin/env python

import sys
import xmltools
from   lxml import etree
from   copy import deepcopy

def expandToXPath(shorthand):
    reserved = []
    reserved.append('description')
    reserved.append('formatString')
    reserved.append('appendCharacterString')

    shorthand = shorthand.split('/')
    if len(shorthand) >= 2:
        shorthand[0] = 'ArchaeologicalElement[@name="%s"]' % shorthand[0]
        if shorthand[1] not in reserved:
            shorthand[1] = 'property[@name="%s"]'          % shorthand[1]
        shorthand.insert(0, '/dataSchema')
    return '/'.join(shorthand)

def parseFlagsFromFile(filename):
    with open(filename) as f:
        flagPaths = f.readlines()
    for i in xrange(len(flagPaths)):
        flagPaths[i] = expandToXPath(flagPaths[i])
    return flagPaths

################################################################################
#                                     MAIN                                     #
################################################################################
reservedCopy = '__RESERVED_CP__'

if len(sys.argv) < 2:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s XML\n'          % sys.argv[0])
    sys.stderr.write('       python %s XML -f FLAGS\n' % sys.argv[0])
    sys.stderr.write('       python %s XML -x XPATH\n' % sys.argv[0])
    sys.stderr.write('\n')
    sys.stderr.write('DESCRIPTION\n')
    sys.stderr.write('   Adds the attribute __RESERVED__CP__="true" to each node of XML specified\n')
    sys.stderr.write('   in FLAGS or XPATH. If FLAGS is not given, all leaf nodes are marked.\n')
    sys.stderr.write('\n')
    sys.stderr.write('OPTIONS\n')
    sys.stderr.write('   -f FLAGS\n')
    sys.stderr.write('       Flag the nodes in XML according to the paths in the file given by FLAGS.\n')
    sys.stderr.write('\n')
    sys.stderr.write('       Nodes in the FLAGS file are specified in the format:\n')
    sys.stderr.write('           tabgroup/tab/xpath-expression\n')
    sys.stderr.write('       For example, writing\n')
    sys.stderr.write('           Diary/AreaCode/lookup\n')
    sys.stderr.write('       is equivalent to the following XPath expression:\n')
    sys.stderr.write('               dataSchema/ArchaeologicalElement[@name="Diary"]/property[@name="A\n')
    sys.stderr.write('reaCode]/lookup\n')
    sys.stderr.write('\n')
    sys.stderr.write('   -x XPATH\n')
    sys.stderr.write('       Flag the nodes in XML according to the XPath expression in XPATH.')
    exit()

# Parse XML
parser = etree.XMLParser(strip_cdata=False)
tree = etree.parse(sys.argv[1], parser)
tree = tree.getroot()

# Generate or parse XPath expressions indicating which nodes should be marked
flagPaths = []
if len(sys.argv) == 2:
    flagPaths.append('//*[not(*)]') # Leaf nodes
elif len(sys.argv) == 4 and sys.argv[2] == '-f':
    flagPaths = parseFlagsFromFile(sys.argv[3])
elif len(sys.argv) == 4 and sys.argv[2] == '-x':
    flagPaths.append(sys.argv[3])
else:
    exit()

# Mark nodes
for xp in flagPaths:
    xmltools.markNodesToCopy(tree, xp)

# Collect your prize
print etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')
