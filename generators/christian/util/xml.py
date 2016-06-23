from   lxml import etree
import hashlib
import re

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
    else:
        indexString = str(getIndex(node))
        return getPath(node.getparent()) + [indexString]

def getPathString(node, sep='/'):
    return sep.join(getPath(node))

def nodeHash(node, hashLen=10):
    path = getPathString(node)
    hash = hashlib.sha256(path)
    hash = hash.hexdigest()
    hash = hash[:hashLen]
    return hash
