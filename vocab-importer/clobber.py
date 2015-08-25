import sys
from   lxml import etree
from   copy import deepcopy

def normaliseTree(t):
    if t == None:
        return t
    if t.xpath('ancestor::*[@__RESERVED_CP__]'):
        deleteAttribFromTree('__RESERVED_CP__', t)
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
        if isEquivalent(targetNode[i], sourceNode):
            targetNode[i] = sourceNode
            return
    targetNode.append(sourceNode)

# Returns true iff the roots of the trees share the same names and attributes.
def isEquivalent(t1, t2):
    if t1 == None or t2 == None:
        return t1 == t2

    attribT1 = dict(t1.attrib)
    attribT2 = dict(t2.attrib)
    attribT1.pop('__RESERVED_CP__', None)
    attribT2.pop('__RESERVED_CP__', None)

    return t1.tag == t2.tag and attribT1 == attribT2

# Returns true iff `t1` and `t2` have equivalent paths.
def isEquivalentPathwise(t1, t2):
    p1 = t1.getparent()
    p2 = t2.getparent()

    if p1 == None or p2 == None:
        return isEquivalent(p1, p2) and isEquivalent(t1, t2)
    return isEquivalentPathwise(p1, p2) and isEquivalent(t1, t2)

def copyPathwise(n, target):
    result = deepcopyNoChildren(n)
    for n_ in n.iterancestors():
        cpyN_ = deepcopyNoChildren(n_)
        cpyN_.append(result)
        result = cpyN_

    target = mergeTrees(result, target)

def deepcopyNoChildren(n):
    result = deepcopy(n)
    for n_ in result:
        n_.getparent().remove(n_)
    return result

# This thing's time complexity could be better...
# t2 is modified during the call
def mergeTrees(t1, t2):
    if t1 == None:
        return t2
    if t2 == None:
        return t1

    t2NodesToDelete = []
    shallowCopyChildren(t1, t2)
    for i in range(0, len(t2)):
        for j in range(i+1, len(t2)):
            if isEquivalent(t2[i], t2[j]):
                mergeTrees( t2[i], t2[j])
                t2NodesToDelete.append(i)

    t2NodesToDelete.sort(reverse=True) # Needs to be sorted in reverse order to
                                       # prevent elements' indices getting moved
                                       # after each `del`.
    for index in t2NodesToDelete:
        del t2[index]

    return t2

def shallowCopyChildren(src, dest):
    for child in src:
        dest.append(child)
    return dest

def deleteAttribFromTree(attrib, t):
    if t == None:
        return t
    if attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(attrib, e)
    return t

################################################################################
#                                     MAIN                                     #
################################################################################
reservedCopy = '__RESERVED_CP__'

if len(sys.argv) < 3:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s SOURCE TARGET\n' % sys.argv[0])
    sys.stderr.write('\n')
    sys.stderr.write('DESCRIPTION\n')
    sys.stderr.write('       Copy the nodes from the SOURCE xml file to the TARGET.\n')
    exit()

sourceTree = etree.parse(sys.argv[1])
targetTree = etree.parse(sys.argv[2])
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

# Clean up
deleteAttribFromTree('__RESERVED_CP__', targetTree)

# Collect your prize
print etree.tostring(targetTree, pretty_print=True)
