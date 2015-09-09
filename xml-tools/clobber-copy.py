#! /usr/bin/env python

import sys
import xmltools
from   lxml import etree

def normaliseTree(t):
    if t == None:
        return t
    if t.xpath('ancestor::*[@__RESERVED_CP__]'):
        xmltools.deleteAttribFromTree('__RESERVED_CP__', t)
    if '__RESERVED_CP__' in t.attrib:
        t.attrib['__RESERVED_CP__'] = t.attrib['__RESERVED_CP__'].strip().lower()

    for e in t:
         normaliseTree(e)
    return t

# Return the node in the `targetTree` which the `sourceNode` should be copied to
def getTargetNode(sourceNode, targetTree):
    candidateNodes = targetTree.xpath('//*')
    for cn in candidateNodes:
        if isEquivalentPathwise(cn, sourceNode):
            return cn.getparent()
    return None

def getSourceNodes(sourceTree):
    reservedCopy = '__RESERVED_CP__'
    toCopy = sourceTree.xpath('//*[@%s]' % reservedCopy)
    for n in toCopy: # Remove nodes whose attribute isn't "true" (or similar)
        if n.attrib[reservedCopy] != 'true':
            n.getparent().remove(n)
    return toCopy

# Append the sourceNode as a child of the targetNode. Overwrite the (first)
# equivalent node, if present. "Equivalent" is defined by the `isEquivalent`
# function.
def clobber(sourceNode, targetNode):
    for i in range(len(targetNode)):
        if xmltools.isEquivalent(targetNode[i], sourceNode):
            targetNode[i] = sourceNode
            return
    targetNode.append(sourceNode)

# Returns true iff `t1` and `t2` have equivalent paths.
def isEquivalentPathwise(t1, t2):
    p1 = t1.getparent()
    p2 = t2.getparent()

    if p1 == None or p2 == None:
        return xmltools.isEquivalent(p1, p2) and xmltools.isEquivalent(t1, t2)
    return isEquivalentPathwise(p1, p2) and xmltools.isEquivalent(t1, t2)

def copyPathwise(n, target):
    result = xmltools.deepCopyNoChildren(n)
    for n_ in n.iterancestors():
        cpyN_ = xmltools.deepCopyNoChildren(n_)
        cpyN_.append(result)
        result = cpyN_

    target = xmltools.mergeTrees(result, target)

################################################################################
#                                     MAIN                                     #
################################################################################
reservedCopy = '__RESERVED_CP__'

if len(sys.argv) < 3:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s SOURCE TARGET\n' % sys.argv[0])
    sys.stderr.write('\n')
    sys.stderr.write('DESCRIPTION\n')
    sys.stderr.write('       Copy the nodes from the SOURCE xml file, whose __RESERVED_CP__ attribute\n')
    sys.stderr.write('       is "true", to the TARGET.\n')
    exit()

parser = etree.XMLParser(strip_cdata=False)
sourceTree = etree.parse(sys.argv[1], parser)
targetTree = etree.parse(sys.argv[2], parser)
sourceTree = sourceTree.getroot()
targetTree = targetTree.getroot()

sourceTree = normaliseTree(sourceTree)
targetTree = normaliseTree(targetTree)

# Copy the nodes, clobbering existing equivalent ones in the target
toCopy = getSourceNodes(sourceTree)
for sourceNode in toCopy:
    targetNode = getTargetNode(sourceNode, targetTree)
    if targetNode == None:
        copyPathwise(sourceNode, targetTree)

    targetNode = getTargetNode(sourceNode, targetTree)
    clobber(sourceNode, targetNode)

# Make terms hierarchical where needed and remove temporary attribute
targetTree = xmltools.nestTerms(targetTree)

# Clean up
xmltools.deleteAttribFromTree('__RESERVED_CP__', targetTree)

# Collect your prize
print etree.tostring(targetTree, pretty_print=True, xml_declaration=True, encoding='utf-8')
