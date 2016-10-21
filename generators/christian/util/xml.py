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

def hasAttrib(e, a):
    try:
        if a in e.attrib:
            return True
    except:
        return False

def deleteAttribFromTree(t, attrib):
    if t == None:
        return
    if hasattr(t, 'attrib') and attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(e, attrib)

def getAttribVal(node, attribName):
    if hasattr(node, 'attrib') and attribName in node.attrib:
        return node.attrib[attribName]
    return None

def appendToAttrib(node, attribName, attribVal):
    oldAttribVal = getAttribVal(node, attribName)
    if oldAttribVal == None:
        oldAttribVal = ''
    if not attribVal:
        return
    if attribVal in oldAttribVal.split():
        return

    if oldAttribVal:
        newAttribVal = oldAttribVal + ' ' + attribVal
    else:
        newAttribVal = attribVal

    node.attrib[attribName] = newAttribVal

def setSourceline(t, sourceline):
    if t == None:
        return

    t.sourceline = sourceline
    for e in t:
        setSourceline(e, sourceline)

def getAll(node, keep=None, descendantOrSelf=True):
    keepIsNone     = type(keep) == None
    keepIsFunction = hasattr(keep, '__call__')
    assert keepIsNone or keepIsFunction

    # Get all nodes
    all = []
    if descendantOrSelf: all = node.xpath('.//*')
    else:                all = node.xpath(' //*')

    # Keep nodes in `all` for which keep(node) evaluates to true
    if keep:
        all = filter(keep, all)

    return all

def getNonLower(t):
    nodes = [i for i in t if re.search('[^a-z]', i.tag)] # TODO: Might be failing due to comments
    return nodes

def appendNotNone(src, dst):
    if src == None:
        return
    dst.append(src)

def extendFlatly(node, children):
    '''
    Acts like `lxml.etree._Element.extend`, except it flattens the list of
    `children`. For example, calling `extendFlatly(node, [a, [b, c]])` is
    equivalent to `node.extend([a, b, c, d])` if `node`, `a`, `b` and `c` are
    instances of `lxml.etree._Element.extend`.
    '''

    listTypes = [list, tuple]
    okTypes   = listTypes + [etree._Element]

    assert type(children) in okTypes
    if node is None:
        return

    if type(children) == etree._Element:
        children = [children]

    for child in children:
        if type(child) == etree._Element: node.append(child)
        if type(child) in listTypes:      node.extend(child)

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
    if replacements is None:
        return

    # Canonicalise input
    if type(replacements) in (list, tuple):
        container = etree.Element('container')
        for r in replacements:
            container.append(r)
        replacements = container

    # Insert each element in `replacements` at the location of `element`. The
    # phrasing is a bit opaque here because lxml *moves* nodes from
    # `replacements` instead of copying them, when `insert(index, r)` is called.
    returnVal = []
    index = element.getparent().index(element) # Index of `element`
    while len(replacements):
        r = replacements[-1]
        element.getparent().insert(index, r)

        returnVal.append(r)

    element.getparent().remove(element)
    return returnVal

def insertAfter(node, nodeToInsert):
    '''
    Inserts `nodeToInsert` immediately after `node`.
    '''
    index = node.getparent().index(node) # Index of `node`
    node.getparent().insert(index+1, nodeToInsert)
