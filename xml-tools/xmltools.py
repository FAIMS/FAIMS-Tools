#! /usr/bin/env python

import sys
from   copy import deepcopy

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
            if isEquivalent(t2[j], t2[i]):
                mergeTrees( t2[j], t2[i])
                t2NodesToDelete.append(j)

    t2NodesToDelete.sort(reverse=True) # Needs to be sorted in reverse order to
                                       # prevent elements' indices getting moved
                                       # after each `del`.
    for index in t2NodesToDelete:
        del t2[index]

    return t2

# Copies each child from `src` to within `dest`. I.e. makes the children of
# `src` into the children of `dest`.
def shallowCopyChildren(src, dest):
    for child in src:
        dest.append(child)
    return dest

# Returns a deep copy of the node `n` without any children
def deepCopyNoChildren(n):
    result = deepcopy(n)
    for n_ in result:
        n_.getparent().remove(n_)
    return result

# Recursively sorts the siblings having the attribute `attrib`. Nodes not having
# This attribute are placed after those possessing it.
def sortSiblings(t, attrib):
    t[:] = sorted(t, key=lambda n: getPositionOfNode(n, attrib))
    for e in t:
        e = sortSiblings(e, attrib)
    return t

def deleteAttribFromTree(attrib, t):
    if t == None:
        return t
    if attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(attrib, e)
    return t

def getPositionOfNode(n, attrib):
    if attrib in n.attrib:
        return n.attrib[attrib]
    else:
        return sys.maxint

# Returns true iff the roots of the trees share the same names and attributes.
def isEquivalent(t1, t2, ignoreText=False):
    if t1 == None or t2 == None:
        return t1 == t2

    ignored = []
    ignored.append('__RESERVED_ATTR_ORDER__')
    ignored.append('__RESERVED_CP__')
    ignored.append('__RESERVED_PAR__')
    ignored.append('file')
    ignored.append('thumbnail')
    ignored.append('type')

    attribT1 = dict(t1.attrib)
    attribT2 = dict(t2.attrib)
    for r in ignored:
        attribT1.pop(r, None)
        attribT2.pop(r, None)

    t1Text = t1.text
    t2Text = t2.text
    if not t1Text:
        t1Text = ''
    if not t2Text:
        t2Text = ''
    t1Text = t1Text.strip()
    t2Text = t2Text.strip()

    if ignoreText:
        return t1.tag == t2.tag and attribT1 == attribT2
    else:
        return t1.tag == t2.tag and attribT1 == attribT2 and t1Text == t2Text

def markNodesToCopy(tree, xPathExpr):
    ns = tree.xpath(xPathExpr)
    for n in ns:
        n.attrib['__RESERVED_CP__'] = 'true'

# Nests the hierarchical vocab entries appropriately
def nestTerms(t):
    positionAttribute = '__RESERVED_PAR__'

    # If there aren't an elements with a `positionAttribute`, there's nothing to
    # do.
    source = t.xpath('(//*[@%s])[1]' % positionAttribute)
    if len(source) == 0:
        return t
    source = source[0]

    # The desired parent node
    destPath = '//ArchaeologicalElement[@name="%s"]/property[@name="%s"]//term[text()="%s"]' % nestTermsHelper(source)
    dest = t.xpath(destPath)
    if len(dest) < 1:
        return t
    dest = dest[0]

    dest.append(source) # Move (not copy) source to dest
    source = deleteAttribFromTree(positionAttribute, source)
    return nestTerms(t)

# Returns a tuple containing entries used to uniquely identify a child term's
# proper parent.
def nestTermsHelper(t):
    positionAttribute = '__RESERVED_PAR__'

    archentName  = t.xpath('ancestor::ArchaeologicalElement')[0].attrib['name']
    propertyName = t.xpath('ancestor::property')[0].attrib['name']
    text         = t.attrib[positionAttribute]
    return archentName, propertyName, text
