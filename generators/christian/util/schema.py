################################################################################
#                                                                              #
# This file contains utility functions which are used with the module.xml      #
# schema but are, as much as possible, agnostic of any output format such as   #
# the so called data and UI "schemas".                                         #
#                                                                              #
################################################################################
from   lxml       import etree
from   lxml.etree import Element, SubElement
import consts
import hashlib
import re
import table
import xml
import util
import schema
import gui

def getPath(node):
    nodeTypes = ['GUI/data element', 'tab group', 'tab']

    if node == None:
        return []
    if consts.RESERVED_XML_TYPE not in node.attrib:
        return getPath(node.getparent()) + []
    if node.attrib[consts.RESERVED_XML_TYPE] not in nodeTypes:
        return getPath(node.getparent()) + []
    else:
        return getPath(node.getparent()) + [node.tag]

def getPathString(node, sep='/'):
    return sep.join(getPath(node))

def nodeHash(node, hashLen=10):
    path = getPathString(node)
    hash = hashlib.sha256(path)
    hash = hash.hexdigest()
    hash = hash[:hashLen]
    return hash

def filterUnannotated(nodes):
    cond = lambda e: isAnnotated(e)
    return filter(cond, nodes)

def isAnnotated(e):
    try:
        return e.attrib[consts.RESERVED_XML_TYPE] != ''
    except:
        pass
    return False

def isFlagged(element, flags, checkAncestors=True, attribName='f'):
    if type(flags) is list:
        return isFlaggedList(element, flags, checkAncestors, attribName)
    else:
        return isFlaggedStr (element, flags, checkAncestors, attribName)

def isFlaggedList(element, flags, checkAncestors=True, attribName='f'):
    for flag in flags:
        if isFlaggedStr(element, flag, checkAncestors, attribName):
            return True
    return False

def isFlaggedStr(element, flag, checkAncestors=True, attribName='f'):
    # Base case 1: We've iterated through all the ancestors
    if element is None:
        return False
    # Base case 2: The flag's been found in ancestor or self
    try:
        flags = element.attrib[attribName].split()
        if flag in flags: return True
    except:
        pass

    if checkAncestors:
        return isFlagged(element.getparent(), flag, checkAncestors, attribName)

def normalise(node):
    normaliseAttributes(node)
    stripComments(node)

def normaliseAttributes(node):
    # Don't normalise stuff in <rels>
    if node.xpath('./ancestor-or-self::rels'):
        return
    # Do normalise everything else
    for key, val in node.attrib.iteritems():
        val = val.split()
        val.sort()
        node.attrib[key] = ' '.join(val)

    for n in node:
        normaliseAttributes(n)

def stripComments(node):
    comments = node.xpath('.//comment()')

    for c in comments:
        p = c.getparent()
        p.remove(c)

# TODO: Choose better names for this and getType
def guessType(node):
    '''
    Returns the value of the node's `t` attribute if it has been defined.
    Otherwise, a guess of what it might have been intended to be is returned
    instead.
    '''
    # Don't guess the type if it's already there
    try:
        return node.attrib['t']
    except:
        pass

    # It doesn't have a type
    if not gui.isGuiElement(node):
        return ''

    # Go ahead and give 'er a guess.
    path = getPath(node)
    if len(path) == 1: return consts.TYPE_TAB_GROUP
    if len(path) == 2: return consts.TYPE_TAB

    isUser = 'f' in node.attrib and 'user' in node.attrib['f'].split()
    if isUser:
        return 'list'
    if node.xpath('opts') and     node.xpath('.//opt[@p]'):
        return 'picture'
    if node.xpath('opts') and not node.xpath('.//opt[@p]'):
        return 'dropdown'
    if 'ec' in node.attrib:
        return 'list'
    return 'input'

def hasElementFlaggedWith(tabGroup, flag):
    exp  = './/*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    cond = lambda e: isFlagged(e, flag)
    matches = tabGroup.xpath(exp)
    matches = filter(cond, matches)
    return len(matches) > 0

def hasElementFlaggedWithId(tabGroup):
    return hasElementFlaggedWith(tabGroup, 'id')

def getParentTabGroup(node):
    exp = './ancestor::*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab group')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentTab(node):
    exp = './ancestor::*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentGuiDataElement(node):
    exp = './ancestor::*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def annotateWithXmlTypes(node):
    if node == []:   return
    if node == None: return

    # Determine parent and its type
    parent = node.getparent()
    if parent != None and consts.RESERVED_XML_TYPE in parent.attrib:
        parentType = parent.attrib[consts.RESERVED_XML_TYPE]
    else:
        parentType = ''

    # Guess UI type
    guessedType = schema.guessType(node)

    # Determine XML type
    type = ''
    if   parent == None:
        type = consts.TYPE_MODULE
    elif parentType == consts.TYPE_MODULE:
        if   util.isNonLower(node.tag):          type = consts.TYPE_TAB_GROUP
        elif node.tag == consts.TYPE_LOGIC:      type = consts.TYPE_LOGIC
        elif node.tag == consts.TYPE_RELS:       type = consts.TYPE_RELS
    elif parentType == consts.TYPE_TAB_GROUP:
        if   util.isNonLower(node.tag):          type = consts.TYPE_TAB
        elif node.tag == consts.TYPE_LOGIC:      type = consts.TYPE_DESC
        elif node.tag == consts.TYPE_SEARCH:     type = consts.TYPE_SEARCH
    elif parentType == consts.TYPE_TAB:
        if   guessedType == consts.TYPE_GROUP:   type = consts.TYPE_GROUP
        elif util.isNonLower(node.tag):          type = consts.TYPE_GUI_DATA
        elif node.tag == consts.TYPE_AUTHOR:     type = consts.TYPE_AUTHOR
        elif node.tag == consts.TYPE_AUTONUM:    type = consts.TYPE_AUTONUM
        elif node.tag == consts.TYPE_COLS:       type = consts.TYPE_COLS
        elif node.tag == consts.TYPE_GPS:        type = consts.TYPE_GPS
        elif node.tag == consts.TYPE_TIMESTAMP:  type = consts.TYPE_TIMESTAMP
    elif parentType == consts.TYPE_GROUP:
        if   guessedType == consts.TYPE_GROUP:   type = consts.TYPE_GROUP
        elif util.isNonLower(node.tag):          type = consts.TYPE_GUI_DATA
    elif parentType == consts.TYPE_COLS:
        if   util.isNonLower(node.tag):          type = consts.TYPE_GUI_DATA
        elif node.tag == consts.TYPE_COL:        type = consts.TYPE_COL
    elif parentType == consts.TYPE_COL:
        if   util.isNonLower(node.tag):          type = consts.TYPE_GUI_DATA
    elif parentType == consts.TYPE_GUI_DATA:
        if   node.tag == consts.TYPE_DESC:       type = consts.TYPE_DESC
        elif node.tag == consts.TYPE_OPTS:       type = consts.TYPE_OPTS
        elif node.tag == consts.TYPE_STR:        type = consts.TYPE_STR
    elif parentType == consts.TYPE_STR:
        if   node.tag == consts.TYPE_APP:        type = consts.TYPE_APP
        elif node.tag == consts.TYPE_FMT:        type = consts.TYPE_FMT
        elif node.tag == consts.TYPE_STR:        type = consts.TYPE_STR
    elif parentType == consts.TYPE_OPTS:
        if   node.tag == consts.TYPE_OPT:        type = consts.TYPE_OPT
    elif parentType == consts.TYPE_OPT:
        if   node.tag == consts.TYPE_OPT:        type = consts.TYPE_OPT
        elif node.tag == consts.TYPE_DESC:       type = consts.TYPE_DESC

    # Annotate current node
    if type:
        node.attrib[consts.RESERVED_XML_TYPE] = type

        # Annotate child nodes
        for child in node:
            annotateWithXmlTypes(child)

def canonicalise(node):
    canonicaliseRec(node)
    canonicaliseCols(node)
    canonicaliseMedia(node)

# TODO: The roles of this and `schema.normalise` are easily confused
def canonicaliseRec(node):
    newNodes = None
    if getType(node) == consts.TYPE_AUTHOR:    newNodes = getAuthor   (node)
    if getType(node) == consts.TYPE_AUTONUM:   newNodes = getAutonum  (node)
    if getType(node) == consts.TYPE_GPS:       newNodes = getGps      (node)
    if getType(node) == consts.TYPE_SEARCH:    newNodes = getSearch   (node)
    if getType(node) == consts.TYPE_TIMESTAMP: newNodes = getTimestamp(node)
    newNodes = xml.replaceElement(node, newNodes)

    for n in node:
        canonicaliseRec(n)

def canonicaliseCols(node):
    colsList = xml.getAll(node, keep=lambda e: getType(e) == consts.TYPE_COLS)

    # 1. Transform this...
    #
    #       <cols __RESERVED_XML_TYPE__="cols">
    #         <My_Input b="decimal" __RESERVED_XML_TYPE__="GUI/data element"/>
    #       </cols>
    #
    # ...into this:
    #
    #       <cols __RESERVED_XML_TYPE__="cols">
    #         <col __RESERVED_XML_TYPE__="col">
    #           <My_Input b="decimal" __RESERVED_XML_TYPE__="GUI/data element"/>
    #         </col>
    #       </cols>
    #
    for cols in colsList:
        for child in cols:
            if getType(child) == consts.TYPE_GUI_DATA:
                newCol = Element(
                        'col',
                        { consts.RESERVED_XML_TYPE : consts.TYPE_COL }
                )

                xml.insertAfter(child, nodeToInsert=newCol)
                newCol.append(child) # Moves `child` into `newCol`

    # 2. Re-write the cols as t="group" elements.
    for cols in colsList:
        cols.tag = 'Colgroup'
        cols.attrib['t'] = 'group'
        cols.attrib['s'] = 'orientation'
        for col in cols:
            col.tag = 'Col'
            col.attrib['t'] = 'group'
            col.attrib['s'] = 'even'

    # 3. Rename the cols elements to eliminate duplicates
    pars = set([cols.getparent() for cols in colsList])
    for par in pars:
        numberDuplicates(par, consts.TYPE_COLS)

    # 4. Rename the col elements to eliminate duplicates
    pars = set(colsList)
    for par in pars:
        numberDuplicates(par, consts.TYPE_COL)

def canonicaliseMedia(node):
    mediaTypes = (
            consts.UI_TYPE_AUDIO,
            consts.UI_TYPE_VIDEO,
            consts.UI_TYPE_CAMERA,
            consts.UI_TYPE_FILE,
    )
    mediaList = xml.getAll(node, keep=lambda e: guessType(e) in mediaTypes)

    for media in mediaList:
        button = Element(
                media.tag + '_Button',
                { consts.RESERVED_XML_TYPE : 'tmp' },
                t='button'
        )
        xml.insertAfter(media, button)

    pars = set([media.getparent() for media in mediaList])
    for par in pars:
        numberDuplicates(par, 'tmp')

    # Re-annotate new buttons with their conventional XML type
    newButtons = xml.getAll(node, keep=lambda e: getType(e) == 'tmp')
    for button in newButtons:
        annotateWithXmlTypes(button)

def numberDuplicates(node, xmlType):
    '''
    Numbers each child in `node` whose XML type is `xmlType` such it does not
    share its name with any other child of `node`.
    '''
    children      = [n for n in node]
    typedChildren = [n for n in node if getType(n) == xmlType]

    # Names of children whose XML type is `xmlType`
    typedChildNames = [n.tag for n in typedChildren]

    # The elements whose names we cannot use
    taken      = set(children) - set(typedChildren)
    takenNames = [n.tag for n in taken]

    # New node names
    numbered = util.numberDuplicates(typedChildNames, takenNames)

    # Actually rename columns
    for cols, newName in zip(typedChildren, numbered):
        cols.tag = newName

def getAuthor(node):
    return Element(
            'Author',
            { consts.RESERVED_XML_TYPE : getType(node) },
            t='input',
            f='readonly nodata',
    ),

def getAutonum(node):
    #TODO
    return None

def getGps(node):
    gps = Element(
            'Colgroup_GPS',
            { consts.RESERVED_XML_TYPE : consts.TYPE_GROUP },
            t='group',
    )
    gps.append(Element('Latitude',  t='input', f='readonly'))
    gps.append(Element('Longitude', t='input', f='readonly'))
    gps.append(Element('Northing',  t='input', f='readonly'))
    gps.append(Element('Easting',   t='input', f='readonly'))

    for n in gps:
        annotateWithXmlTypes(n)
    gps.attrib[consts.RESERVED_XML_TYPE] = consts.TYPE_GPS

    return gps,

def getSearch(node):
    search = Element(
            'Search',
            { consts.RESERVED_XML_TYPE : consts.TYPE_TAB },
            f='readonly nodata noscroll'
    )
    cols = SubElement(search, 'Colgroup_0', t='group', s='orientation')
    lCol = SubElement(cols,   'Col_0',      t='group', s='even')
    rCol = SubElement(cols,   'Col_1',      t='group', s='large')

    term = SubElement(lCol,   'Search_Term',   t='input')
    btn  = SubElement(rCol,   'Search_Button', t='button')

    SubElement(search, 'Entity_Types', t='input')
    SubElement(search, 'Entity_List',  t='list')

    for n in search:
        annotateWithXmlTypes(n)
    search.attrib[consts.RESERVED_XML_TYPE] = consts.TYPE_SEARCH

    return search,

def getTimestamp(node):
    return Element(
            'Timestamp',
            { consts.RESERVED_XML_TYPE : getType(node) },
            t='input',
            f='readonly nodata'
    ),

def expandCompositeElements(tree):
    # (1) REPLACE ELEMENTS HAVING A CERTAIN T ATTRIBUTE
    for attrib, replacements in table.REPLACEMENTS_BY_T_ATTRIB.iteritems():
        exp     = '//*[@%s]' % consts.RESERVED_XML_TYPE
        cond    = lambda e: guessType(e) == attrib
        matches = tree.xpath(exp)
        matches = filter(cond, matches)

        for m in matches:
            replaceElement(m, replacements, m.tag)

    # (2) REPLACE ELEMENTS HAVING A CERTAIN TAG NAME
    # <autonum> tags get special treatment
    tagMatches  = tree.xpath('//autonum')
    if tagMatches:
        tagMatch = tagMatches[0]

        cond        = lambda e: schema.isFlagged(e, 'autonum')
        exp         = './/*[@%s="%s"]'
        exp        %= consts.RESERVED_XML_TYPE, 'GUI/data element'
        flagMatches = tree.xpath(exp)
        flagMatches = filter(cond, flagMatches)

        replacements = table.REPLACEMENTS_BY_TAG['autonum'] * len(flagMatches)
        replacements = replaceElement(tagMatch, replacements)

        for autonumDest, autonumSrc in zip(flagMatches, replacements):
            needle      = '__REPLACE__'
            haystack    = autonumSrc .tag
            replacement = autonumDest.tag

            autonumSrc.tag = haystack.replace(needle, replacement)

    # Replace non-<autonum> tags similarly to in (1).
    for tag, replacements in table.REPLACEMENTS_BY_TAG.iteritems():
        exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
        matches = tree.xpath(exp)
        for m in matches:
            replaceElement(m, replacements)

def replaceElement(element, replacements, tag='__REPLACE__'):
    replacements = replacements.replace('\n', ' ')
    replacements = replacements.replace('\r', ' ')
    replacements = re.sub('>\s+<', '><', replacements)
    replacements = replacements.replace('__REPLACE__', tag)
    replacements = '<root>%s</root>' % replacements
    replacements = etree.fromstring(replacements)

    originalSourceline = element.sourceline
    xml.setSourceline(replacements, originalSourceline)

    return xml.replaceElement(element, replacements)

def hasAttrib(e, a):
    try:
        if a in e.attrib:
            return True
    except:
        return False

def isValidLink(root, link, linkType):
    if not link:
        return False

    if   linkType == 'tab':
        result  = True
        try:
            result &= bool(root.xpath('/module/' + link))
        except:
            result &= False
        result &= '/'     in link
        result &= '/' != link[ 0]
        result &= '/' != link[-1]
        return result
    elif linkType in ('tabgroup', 'tab group'):
        result  = True
        try:
            result &= bool(root.xpath('/module/' + link))
        except:
            result &= False
        result &= '/' not in link
        return result
    elif linkType == 'all':
        result  = False
        result |= isValidLink(root, link, 'tab'     )
        result |= isValidLink(root, link, 'tabgroup')
        return result
    else:
        return False

def hasReservedName(node):
    return node != None and isReservedName(node.tag)

def isReservedName(name):
    return name in consts.TYPES

def hasUserDefinedName(node):
    return node != None and isUserDefinedName(node.tag)

def isUserDefinedName(name):
    return name != None and name.istitle()

def getType(node):
    '''
    Returns the type assigned during annotation with `annotateWithXmlTypes`.
    '''
    if node == None:
        return ''
    if not consts.RESERVED_XML_TYPE in node.attrib:
        return ''
    return node.attrib[consts.RESERVED_XML_TYPE]

def isTabGroup(node):
    return getType(node) == consts.TYPE_TAB_GROUP

def isTab(node):
    return getType(node) in (consts.TYPE_TAB, consts.TYPE_SEARCH)

def isGuiDataElement(node):
    return getType(node) in (
            consts.TYPE_GUI_DATA,
            consts.TYPE_GROUP,
            consts.TYPE_COLS
    )

def getTabGroups      (node): return xml.getAll(node, isTabGroup)
def getTabs           (node): return xml.getAll(node, isTab)
def getGuiDataElements(node): return xml.getAll(node, isGuiDataElement)
