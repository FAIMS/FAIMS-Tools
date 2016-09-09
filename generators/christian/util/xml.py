from   lxml import etree
import hashlib
import re
import consts

def parseXml(filename):
    parser = etree.XMLParser(strip_cdata=False)
    try:
        tree = etree.parse(filename, parser)
    except etree.XMLSyntaxError as e:
        print e
        exit()
    tree = tree.getroot()
    return tree

def deleteAttribFromTree(t, attrib):
    if t == None:
        return
    if hasattr(t, 'attrib') and attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(e, attrib)

def setSourceline(t, sourceline):
    if t == None:
        return

    t.sourceline = sourceline
    for e in t:
        setSourceline(e, sourceline)

def getNonLower(t):
    nodes = [i for i in t if re.search('[^a-z]', i.tag)] # TODO: Might be failing due to comments
    return nodes

def appendNotNone(src, dst):
    if src == None:
        return
    dst.append(src)

def flagAll(nodes, attrib, value):
    for n in nodes:
        n.attrib[attrib] = value

def getIndex(node):
    parent = node.getparent()
    if parent == None: return 0
    else:              return parent.index(node)

def getPath(node):
    if node == None:
        return []
    if node is node.getroottree().getroot():
        return []

    return getPath(node.getparent()) + [node.tag]

def getPathString(node, sep='/'):
    return sep.join(getPath(node))

def getPathIndex(node):
    nodes = getPath(node)
    return [str(getIndex(n)) for n in nodes]

def getPathIndexString(node, sep='/'):
    return sep.join(getPathIndex(node))

def nodeHash(node, hashLen=10):
    path = getPathString(node)
    hash = hashlib.sha256(path)
    hash = hash.hexdigest()
    hash = hash[:hashLen]
    return hash

def replaceElement(element, replacements):
    # Insert each element in `replacements` at the location of `element`. The
    # phrasing is a bit opaque here because lxml *moves* nodes from
    # `replacements` instead of copying them, when `insert(index, r)` is called.
    returnVal = []
    index = element.getparent().index(element)
    while len(replacements):
        r = replacements[-1]
        element.getparent().insert(index, r)

        returnVal.append(r)

    element.getparent().remove(element)
    return returnVal
