################################################################################
#                                                                              #
# This file contains utility functions which are used with the module.xml      #
# schema but are, as much as possible, agnostic of any output format such as   #
# the so called data and UI "schemas".                                         #
#                                                                              #
################################################################################
from   lxml       import etree
from   lxml.etree import Element, SubElement
from   consts import *
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
    if RESERVED_XML_TYPE not in node.attrib:
        return getPath(node.getparent()) + []
    if node.attrib[RESERVED_XML_TYPE] not in nodeTypes:
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
        return e.attrib[RESERVED_XML_TYPE] != ''
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

def nextFreeName(baseName, node):
    parent     = node.getparent()
    if parent == None:
        return None

    takenNames = [n.tag for n in parent]
    return util.nextFreeName(baseName, takenNames)

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
    if len(path) == 1: return TYPE_TAB_GROUP
    if len(path) == 2: return TYPE_TAB

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
    exp  = './/*[@%s="%s"]' % (RESERVED_XML_TYPE, 'GUI/data element')
    cond = lambda e: isFlagged(e, flag)
    matches = tabGroup.xpath(exp)
    matches = filter(cond, matches)
    return len(matches) > 0

def hasElementFlaggedWithId(tabGroup):
    return hasElementFlaggedWith(tabGroup, 'id')

def getParentTabGroup(node):
    exp = './ancestor::*[@%s="%s"]' % (RESERVED_XML_TYPE, 'tab group')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentTab(node):
    exp = './ancestor::*[@%s="%s"]' % (RESERVED_XML_TYPE, 'tab')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentGuiDataElement(node):
    exp = './ancestor::*[@%s="%s"]' % (RESERVED_XML_TYPE, 'GUI/data element')
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def annotateWithXmlTypes(node):
    if node == []:   return
    if node == None: return

    # Determine parent and its type
    parent = node.getparent()
    if parent != None and RESERVED_XML_TYPE in parent.attrib:
        parentType = parent.attrib[RESERVED_XML_TYPE]
    else:
        parentType = ''

    # Guess UI type
    guessedType = schema.guessType(node)

    # Determine XML type
    type = ''
    if   parent == None:
        type = TYPE_MODULE
    elif parentType == TYPE_MODULE:
        if   util.isNonLower(node.tag):   type = TYPE_TAB_GROUP
        elif node.tag == TYPE_LOGIC:      type = TYPE_LOGIC
        elif node.tag == TYPE_RELS:       type = TYPE_RELS
    elif parentType == TYPE_TAB_GROUP:
        if   util.isNonLower(node.tag):   type = TYPE_TAB
        elif node.tag == TYPE_LOGIC:      type = TYPE_DESC
        elif node.tag == TYPE_SEARCH:     type = TYPE_SEARCH
    elif parentType == TYPE_TAB:
        if   guessedType == TYPE_GROUP:   type = TYPE_GROUP
        elif util.isNonLower(node.tag):   type = TYPE_GUI_DATA
        elif node.tag == TYPE_AUTHOR:     type = TYPE_AUTHOR
        elif node.tag == TYPE_AUTONUM:    type = TYPE_AUTONUM
        elif node.tag == TYPE_COLS:       type = TYPE_COLS
        elif node.tag == TYPE_GPS:        type = TYPE_GPS
        elif node.tag == TYPE_TIMESTAMP:  type = TYPE_TIMESTAMP
    elif parentType == TYPE_GROUP:
        if   guessedType == TYPE_GROUP:   type = TYPE_GROUP
        elif util.isNonLower(node.tag):   type = TYPE_GUI_DATA
    elif parentType == TYPE_COLS:
        if   util.isNonLower(node.tag):   type = TYPE_GUI_DATA
        elif node.tag == TYPE_COL:        type = TYPE_COL
    elif parentType == TYPE_COL:
        if   util.isNonLower(node.tag):   type = TYPE_GUI_DATA
    elif parentType == TYPE_GUI_DATA:
        if   node.tag == TYPE_DESC:       type = TYPE_DESC
        elif node.tag == TYPE_OPTS:       type = TYPE_OPTS
        elif node.tag == TYPE_STR:        type = TYPE_STR
    elif parentType == TYPE_STR:
        if   node.tag == TYPE_APP:        type = TYPE_APP
        elif node.tag == TYPE_FMT:        type = TYPE_FMT
        elif node.tag == TYPE_STR:        type = TYPE_STR
    elif parentType == TYPE_OPTS:
        if   node.tag == TYPE_OPT:        type = TYPE_OPT
    elif parentType == TYPE_OPT:
        if   node.tag == TYPE_OPT:        type = TYPE_OPT
        elif node.tag == TYPE_DESC:       type = TYPE_DESC

    # Annotate current node
    if type:
        node.attrib[RESERVED_XML_TYPE] = type

        # Annotate child nodes
        for child in node:
            annotateWithXmlTypes(child)

# TODO: The roles of this and `schema.normalise` are easily confused
def canonicalise(node):
    canonicaliseRec(node)
    canonicaliseCols(node)
    canonicaliseMedia(node)
    canonicaliseImplied(node)

def canonicaliseRec(node):
    newNodes = None
    if getType(node) == TYPE_AUTHOR:    newNodes = getAuthor   (node)
    if getType(node) == TYPE_AUTONUM:   newNodes = getAutonum  (node)
    if getType(node) == TYPE_GPS:       newNodes = getGps      (node)
    if getType(node) == TYPE_SEARCH:    newNodes = getSearch   (node)
    if getType(node) == TYPE_TIMESTAMP: newNodes = getTimestamp(node)
    newNodes = xml.replaceElement(node, newNodes)

    for n in node:
        canonicaliseRec(n)

def canonicaliseCols(node):
    colsList = xml.getAll(node, keep=lambda e: e.tag == TAG_COLS)

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
            if getType(child) == TYPE_GUI_DATA:
                newCol = Element(
                        'col',
                        { RESERVED_XML_TYPE : TYPE_COL }
                )

                xml.insertAfter(child, nodeToInsert=newCol)
                newCol.append(child) # Moves `child` into `newCol`

    # 2. Re-write the cols as t="group" elements.
    for cols in colsList:
        cols.tag = nextFreeName('Colgroup', cols)
        cols.attrib['t'] = 'group'
        cols.attrib['s'] = 'orientation'
        for col in cols:
            col.tag = nextFreeName('Col', col)
            col.attrib['t'] = 'group'
            col.attrib['s'] = 'even'

def canonicaliseMedia(node):
    mediaTypes = (
            UI_TYPE_AUDIO,
            UI_TYPE_VIDEO,
            UI_TYPE_CAMERA,
            UI_TYPE_FILE,
    )
    mediaList = xml.getAll(node, keep=lambda e: guessType(e) in mediaTypes)

    for media in mediaList:
        button = Element(
                nextFreeName(media.tag + '_Button', media),
                { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                t='button'
        )
        xml.insertAfter(media, button)

def canonicaliseImplied(node):
    # f="notnull" implies c="required"
    isNotNull = lambda e: isFlagged(
            e,
            FLAG_NOTNULL,
            checkAncestors=False,
    )
    notNull = xml.getAll(node, keep=isNotNull);

    for n in notNull:
        xml.appendToAttrib(n, ATTRIB_C, 'required')

def getAuthor(node):
    return Element(
            'Author',
            { RESERVED_XML_TYPE : getType(node) },
            t=UI_TYPE_INPUT,
            f='readonly nodata',
    ),

def getAutonum(node):
    # Get the nodes flagged with f="notnull"
    isAutonumbered = lambda e: isFlagged(
            e,
            FLAG_AUTONUM,
            checkAncestors=False
    )
    autonumbered = xml.getAll(
            node,
            keep=isAutonumbered,
            descendantOrSelf=False
    )

    # Generate some 'Next_XYZ' fields to replace the <autonum/> tag with
    autonum = []
    for n in autonumbered:
        e = Element(
                'Next_' + n.tag,
                { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                b=BIND_DECIMAL,
                f=FLAG_NOTNULL,
                c='required',
                t=UI_TYPE_INPUT,
        )
        e.text = n.text

        autonum.append(e)

    return tuple(autonum)

def getGps(node):
    colsTop = Element(TAG_COLS, { RESERVED_XML_TYPE : TYPE_COLS })
    colsBot = Element(TAG_COLS, { RESERVED_XML_TYPE : TYPE_COLS })

    colsTop.append(Element('Latitude',  t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsTop.append(Element('Longitude', t=UI_TYPE_INPUT, f=FLAG_READONLY))

    colsBot.append(Element('Northing',  t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsBot.append(Element('Easting',   t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsBot.append(Element('Accuracy',  t=UI_TYPE_INPUT, f=FLAG_READONLY))

    for n in colsTop: annotateWithXmlTypes(n)
    for n in colsBot: annotateWithXmlTypes(n)
    colsTop.attrib[RESERVED_XML_TYPE] = TYPE_GPS

    return colsTop, colsBot

def getSearch(node):
    search = Element(
            'Search',
            { RESERVED_XML_TYPE : TYPE_TAB },
            f='readonly nodata noscroll'
    )
    cols = SubElement(search, 'Colgroup_0', t='group', s='orientation')
    lCol = SubElement(cols,   'Col_0',      t='group', s='even')
    rCol = SubElement(cols,   'Col_1',      t='group', s='large')

    term = SubElement(lCol,   'Search_Term',   t=UI_TYPE_INPUT)
    btn  = SubElement(rCol,   'Search_Button', t='button')

    SubElement(search, 'Entity_Types', t=UI_TYPE_INPUT)
    SubElement(search, 'Entity_List',  t='list')

    for n in search:
        annotateWithXmlTypes(n)
    search.attrib[RESERVED_XML_TYPE] = TYPE_SEARCH

    return search,

def getTimestamp(node):
    return Element(
            'Timestamp',
            { RESERVED_XML_TYPE : getType(node) },
            t=UI_TYPE_INPUT,
            f='readonly nodata'
    ),

def expandCompositeElements(tree):
    # (1) REPLACE ELEMENTS HAVING A CERTAIN T ATTRIBUTE
    for attrib, replacements in table.REPLACEMENTS_BY_T_ATTRIB.iteritems():
        exp     = '//*[@%s]' % RESERVED_XML_TYPE
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
        exp        %= RESERVED_XML_TYPE, 'GUI/data element'
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
        exp = '//%s[@%s]' % (tag, RESERVED_XML_TYPE)
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
    return name in TYPES

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
    if not RESERVED_XML_TYPE in node.attrib:
        return ''
    return node.attrib[RESERVED_XML_TYPE]

def isTabGroup(node):
    return getType(node) == TYPE_TAB_GROUP

def isTab(node):
    return getType(node) in (TYPE_TAB, TYPE_SEARCH)

def isGuiDataElement(node):
    return getType(node) in (
            TYPE_GUI_DATA,
            TYPE_GROUP,
            TYPE_COLS
    )

def getTabGroups      (node): return xml.getAll(node, isTabGroup)
def getTabs           (node): return xml.getAll(node, isTab)
def getGuiDataElements(node): return xml.getAll(node, isGuiDataElement)
