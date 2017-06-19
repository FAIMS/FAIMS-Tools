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
import data
import arch16n

def getPath(node):
    nodeTypes = [
            TYPE_GUI_DATA,
            TYPE_SEARCH,
            TYPE_TAB,
            TYPE_TAB_GROUP,
            TYPE_AUTHOR,
            TYPE_TIMESTAMP,
    ]

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

def isAnnotated(node):
    ''' Returns `True` iff `node` was annotated with an XML TYPE from `consts`.
    '''
    try:
        return node.attrib[RESERVED_XML_TYPE] != ''
    except:
        pass
    return False

def getFlags(node, attribName=ATTRIB_F):
    try:
        flags = node.attrib[attribName].split()
        return flags
    except:
        return []

def getFlagsString(node, attribName=ATTRIB_F):
    return ' '.join(getFlags(node, attribName))

def isFlagged(node, flags, checkAncestors=None, attribName=ATTRIB_F):
    if type(flags) is list:
        return isFlaggedList(node, flags, checkAncestors, attribName)
    else:
        return isFlaggedStr (node, flags, checkAncestors, attribName)

def isFlaggedList(node, flags, checkAncestors=True, attribName=ATTRIB_F):
    for flag in flags:
        if isFlaggedStr(node, flag, checkAncestors, attribName):
            return True
    return False

def isFlaggedStr(node, flag, checkAncestors=None, attribName=ATTRIB_F):
    # Set the default value of `checkAncestors` if it hasn't been passed
    requiresAncestorCheck = (FLAG_NODATA, FLAG_NOUI)
    if checkAncestors == None:
        checkAncestors = flag in requiresAncestorCheck

    # Base cases
    if node is None:
        return False
    if flag in getFlags(node, attribName):
        return True

    # Recursive case
    if checkAncestors:
        return isFlagged(node.getparent(), flag, checkAncestors, attribName)

    return False

def nextFreeName(baseName, node):
    parent = node.getparent()
    if parent == None:
        return None

    takenNames = [n.tag for n in parent]
    return util.nextFreeName(baseName, takenNames)

# Warning: Modifies `node` by reference
def parseSchema(node):
    normaliseXml(node)
    annotateWithXmlTypes(node)
    normaliseSchema(node)

def normaliseXml(node):
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

def getUiType(node):
    '''
    Returns the value of the node's `t` attribute if it has been defined.
    Otherwise, a guess of what it might have been intended to be is returned
    instead.
    '''
    # Don't guess the type if it's already there
    try:
        return node.attrib[ATTRIB_T]
    except:
        pass

    # Go ahead and give 'er a guess.
    path = getPath(node)
    if len(path) == 1: return TYPE_TAB_GROUP
    if len(path) == 2: return TYPE_TAB

    # It doesn't have a type
    if not gui.isGuiElement(node):
        return ''

    if isFlagged(node, FLAG_USER):
        return UI_TYPE_LIST
    if hasLink(node):
        return UI_TYPE_BUTTON
    if node.xpath(TAG_OPTS) and     node.xpath('.//opt[@p]'):
        return UI_TYPE_PICTURE
    if node.xpath(TAG_OPTS) and not node.xpath('.//opt[@p]'):
        return UI_TYPE_DROPDOWN
    if ATTRIB_EC in node.attrib:
        return UI_TYPE_LIST
    return UI_TYPE_INPUT

def hasElementFlaggedWith(tabGroup, flag):
    exp  = './/*[@%s="%s"]' % (RESERVED_XML_TYPE, TYPE_GUI_DATA)
    cond = lambda e: isFlagged(e, flag)
    matches = tabGroup.xpath(exp)
    matches = filter(cond, matches)
    return len(matches) > 0

def hasElementFlaggedWithId(tabGroup):
    return hasElementFlaggedWith(tabGroup, 'id')

def getParent(node, xmlType):
    if node == None:
        return None

    exp = './ancestor::*[@%s="%s"]' % (RESERVED_XML_TYPE, xmlType)
    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentTabGroup(node):
    return getParent(node, TYPE_TAB_GROUP)

def getParentTab(node):
    return getParent(node, TYPE_TAB)

def getParentGuiDataElement(node):
    return getParent(node, TYPE_GUI_DATA)

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
    guessedType = schema.getUiType(node)

    # Determine XML type
    type = ''
    if   parent == None:
        type = TYPE_MODULE
    elif parentType == TAG_MODULE:
        if   util.isNonLower(node.tag):   type = TYPE_TAB_GROUP
        elif node.tag == TAG_LOGIC:       type = TYPE_LOGIC
        elif node.tag == TAG_RELS:        type = TYPE_RELS
    elif parentType == TYPE_TAB_GROUP:
        if   util.isNonLower(node.tag):   type = TYPE_TAB
        elif node.tag == TAG_DESC:        type = TYPE_DESC
        elif node.tag == TAG_SEARCH:      type = TYPE_SEARCH
    elif parentType == TYPE_TAB:
        if   guessedType == TAG_GROUP:    type = TYPE_GROUP
        elif util.isNonLower(node.tag):   type = TYPE_GUI_DATA
        elif node.tag == TAG_AUTHOR:      type = TYPE_AUTHOR
        elif node.tag == TAG_AUTONUM:     type = TYPE_AUTONUM
        elif node.tag == TAG_COLS:        type = TYPE_COLS
        elif node.tag == TAG_GPS:         type = TYPE_GPS
        elif node.tag == TAG_TIMESTAMP:   type = TYPE_TIMESTAMP
    elif parentType == TYPE_GROUP:
        if   guessedType == TAG_GROUP:    type = TYPE_GROUP
        elif util.isNonLower(node.tag):   type = TYPE_GUI_DATA
    elif parentType == TYPE_COLS:
        if   util.isNonLower(node.tag):   type = TYPE_GUI_DATA
        elif node.tag == TAG_COL:         type = TYPE_COL
        elif node.tag == TAG_AUTHOR:      type = TYPE_AUTHOR
        elif node.tag == TAG_TIMESTAMP:   type = TYPE_TIMESTAMP
    elif parentType == TYPE_COL:
        if   util.isNonLower(node.tag):   type = TYPE_GUI_DATA
    elif parentType in (TYPE_GUI_DATA, TAG_TIMESTAMP, TAG_AUTHOR):
        if   node.tag == TAG_DESC:        type = TYPE_DESC
        elif node.tag == TAG_OPTS:        type = TYPE_OPTS
        elif node.tag == TAG_STR:         type = TYPE_STR
    elif parentType == TYPE_STR:
        if   node.tag == TAG_APP:         type = TYPE_APP
        elif node.tag == TAG_FMT:         type = TYPE_FMT
        elif node.tag == TAG_POS:         type = TYPE_POS
    elif parentType == TYPE_OPTS:
        if   node.tag == TAG_OPT:         type = TYPE_OPT
    elif parentType == TYPE_OPT:
        if   node.tag == TAG_OPT:         type = TYPE_OPT
        elif node.tag == TAG_DESC:        type = TYPE_DESC

    # Annotate current node
    if type:
        if not xml.hasAttrib(node, RESERVED_XML_TYPE):
            node.attrib[RESERVED_XML_TYPE] = type

        # Annotate child nodes
        for child in node:
            annotateWithXmlTypes(child)

def normaliseSchema(node):
    normaliseSchemaRec(node)
    normaliseCols(node)
    normaliseMedia(node)
    normaliseImplied(node)
    normaliseSignup(node)

def normaliseSchemaRec(node):
    newNodes = None
    if getXmlType(node) == TYPE_AUTHOR:    newNodes = getAuthor   (node)
    if getXmlType(node) == TYPE_AUTONUM:   newNodes = getAutonum  (node)
    if getXmlType(node) == TYPE_GPS:       newNodes = getGps      (node)
    if getXmlType(node) == TYPE_SEARCH:    newNodes = getSearch   (node)
    if getXmlType(node) == TYPE_TIMESTAMP: newNodes = getTimestamp(node)
    newNodes = xml.replaceElement(node, newNodes)

    for n in node:
        normaliseSchemaRec(n)

def normaliseCols(node):
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
            if getXmlType(child) in (TYPE_GUI_DATA, TYPE_AUTHOR, TYPE_TIMESTAMP):
                newCol = Element(
                        'col',
                        { RESERVED_XML_TYPE : TYPE_COL }
                )

                xml.insertAfter(child, nodeToInsert=newCol)
                newCol.append(child) # Moves `child` into `newCol`

    # 2. Re-write the cols as t="group" elements.
    for cols in colsList:
        cols.tag = nextFreeName('Colgroup', cols)
        cols.attrib[ATTRIB_T] = 'group'
        cols.attrib[ATTRIB_S] = 'orientation'
        for col in cols:
            col.tag = nextFreeName('Col', col)
            col.attrib[ATTRIB_T] = 'group'
            col.attrib[ATTRIB_S] = 'even'

def normaliseMedia(node):
    mediaList = xml.getAll(node, keep=lambda e: getUiType(e) in MEDIA_UI_TYPES)

    for media in mediaList:
        button = Element(
                nextFreeName(media.tag + '_Button', media),
                { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                t=UI_TYPE_BUTTON
        )
        button.text = arch16n.getArch16nVal(media)
        xml.insertAfter(media, button)

def normaliseImplied(node):
    # f="notnull" implies c="required"
    isNotNull = lambda e: isFlagged(
            e,
            FLAG_NOTNULL,
            checkAncestors=False,
    )
    notNull = xml.getAll(node, keep=isNotNull);

    for n in notNull:
        xml.appendToAttrib(n, ATTRIB_C, CSS_REQUIRED)

def normaliseSignup(node):
    isSignup = lambda e: getLink(e) == LINK_SIGNUP
    signupNodes = getGuiDataElements(node, isSignup)

    for n in signupNodes:
        xml.insertBefore(n, getSignupGuide(n)[0])

def getSignupGuide(node):
    tagGuide     = nextFreeName('Signup_Guide', node)
    attribsGuide = {
        RESERVED_XML_TYPE : TYPE_GUI_DATA,
        ATTRIB_F          : FLAG_NOLABEL,
        ATTRIB_T          : UI_TYPE_WEBVIEW,
    }

    tagMd  = TAG_MARKDOWN
    textMd  = '---\n'
    textMd += 'In order to sign up, please ensure:\n'
    textMd += '\n'
    textMd += '1. Your device is online\n'
    textMd += '2. FAIMS is connected to the correct server\n'
    textMd += '3. You have choosen a strong password\n'
    textMd += '\n'
    textMd += 'A strong password has at least 6 characters, 1 uppercase letter,'
    textMd += ' 1 lowercase letter, 1 digit and 1 symbol. Examples of strong '
    textMd += 'passwords:\n'
    textMd += '\n'
    textMd += '* D!gging4bi0facts\n'
    textMd += '* 2_artif&ctS\n'

    g = Element   (   tagGuide, attribsGuide)
    m = SubElement(g, tagMd                 ); m.text = textMd

    return g,

def getAuthor(node):
    flags = getFlagsString(node)

    e = Element(
            schema.getParentTabGroup(node).tag + '_author',
            { RESERVED_XML_TYPE : getXmlType(node) },
            t=UI_TYPE_INPUT,
            f=FLAG_READONLY + SEP_FLAGS + flags,
    )

    e.extend(node.getchildren())

    if node.text: e.text = node.text
    else:         e.text = 'Author'

    return e,

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
                { RESERVED_XML_TYPE : TYPE_GUI_DATA,
                  ORIGINAL_TAG      : node.tag,
                  AUTONUM_DEST      : getPathString(n) },
                b=BIND_DECIMAL,
                f=FLAG_NOTNULL,
                c=CSS_REQUIRED,
                t=UI_TYPE_INPUT,
        )
        e.text = n.text

        autonum.append(e)

    return tuple(autonum)

def getGps(node):
    btnName = nextFreeName('Take_From_GPS', node)

    colsTop = Element(TAG_COLS, { RESERVED_XML_TYPE : TYPE_COLS })
    colsBot = Element(TAG_COLS, { RESERVED_XML_TYPE : TYPE_COLS })
    btn     = Element(btnName,  { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                t=UI_TYPE_BUTTON
    )

    colsTop.append(Element('Latitude',  t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsTop.append(Element('Longitude', t=UI_TYPE_INPUT, f=FLAG_READONLY))

    colsBot.append(Element('Northing',  t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsBot.append(Element('Easting',   t=UI_TYPE_INPUT, f=FLAG_READONLY))
    colsBot.append(Element('Accuracy',  t=UI_TYPE_INPUT, f=FLAG_READONLY))

    for n in colsTop: annotateWithXmlTypes(n)
    for n in colsBot: annotateWithXmlTypes(n)
    colsTop.attrib[RESERVED_XML_TYPE] = TYPE_GPS

    btn.text = 'Take From GPS'

    return colsTop, colsBot, btn

def getSearch(node):
    search = Element(
            'Search',
            { RESERVED_XML_TYPE : TYPE_TAB },
            f='nodata noscroll'
    )
    cols = SubElement(search, 'Colgroup_0', { RESERVED_XML_TYPE : TYPE_COLS }, t=UI_TYPE_GROUP, s='orientation')
    lCol = SubElement(cols,   'Col_0',      { RESERVED_XML_TYPE : TYPE_COL  }, t=UI_TYPE_GROUP, s='even')
    rCol = SubElement(cols,   'Col_1',      { RESERVED_XML_TYPE : TYPE_COL  }, t=UI_TYPE_GROUP, s='large')

    term = SubElement(lCol,   'Search_Term',   t=UI_TYPE_INPUT)
    btn  = SubElement(rCol,   'Search_Button', t=UI_TYPE_BUTTON)

    # Add 'Entity Types' dropdown if there's more than one entity to choose from
    isGuiAndData = lambda e: util.gui. isGuiNode    (e) and \
                             util.data.isDataElement(e)
    nodes = getTabGroups(node, isGuiAndData, descendantOrSelf=False)
    if len(nodes) > 1:
        SubElement(search, 'Entity_Types', t=UI_TYPE_DROPDOWN)

    SubElement(search, 'Entity_List',  t=UI_TYPE_LIST)

    for n in search:
        annotateWithXmlTypes(n)
    search.attrib[RESERVED_XML_TYPE] = TYPE_SEARCH

    btn.text = 'Search'

    return search,

def getTimestamp(node):
    flags = getFlagsString(node)

    e = Element(
            schema.getParentTabGroup(node).tag + '_timestamp',
            { RESERVED_XML_TYPE : getXmlType(node) },
            t=UI_TYPE_INPUT,
            f=FLAG_READONLY + SEP_FLAGS + flags,
    )

    e.extend(node.getchildren())

    if node.text: e.text = node.text
    else:         e.text = 'Timestamp'

    return e,

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

def isInTestTime(node):
    aVal = util.xml.getAttribVal(node, ATTRIB_TEST_MODE)

    return str(aVal).lower() == \
           str(True).lower()

def getLink(node, attribName=None):
    if attribName != None:
        return util.xml.getAttribVal(node, attribName)

    for linkAttrib in LINK_ATTRIBS:
        link = util.xml.getAttribVal(node, linkAttrib)
        if link:
            return link

    return None

# Recursive version of `getLink`
def getLinks(node, attribName=None):
    if node == None:
        return []
    if hasLink(node, attribName):
        return [getLink(node, attribName)]

    return sum([getLinks(n, attribName) for n in node], [])

def hasLink(node, attribName=None):
    return bool(getLink(node, attribName))

def hasValidLink(node):
    return getLinkedNode(node) != None

def getEntity(node):
    link = util.xml.getAttribVal(node, ATTRIB_E)
    if link:
        return link.replace('_', ' ')

    link = util.xml.getAttribVal(node, ATTRIB_EC)
    if link:
        return link.replace('_', ' ')

    return None

def hasEntity(node):
    return bool(getEntity(node))

def getNodeAtPath(tree, path):
    if not path:
        return None

    nodes = tree.xpath('/module/' + path)
    if len(nodes) != 1:
        return None

    return nodes[0]

def getLinkedNode(node):
    return getNodeAtPath(node, getLink(node))

def getLinkedNodes(node, attribName=None):
    root = node.getroottree().getroot()
    return [getNodeAtPath(root, path) for path in getLinks(node, attribName)]

def isValidPath(root, path, pathType):
    if not path:
        return False

    if   pathType == TYPE_GUI_DATA:
        return getXmlType(getNodeAtPath(root, path)) == TYPE_GUI_DATA
    elif pathType in ('tab', TYPE_TAB):
        return getXmlType(getNodeAtPath(root, path)) == TYPE_TAB
    elif pathType in ('tabgroup', TYPE_TAB_GROUP):
        return getXmlType(getNodeAtPath(root, path)) == TYPE_TAB_GROUP
    elif pathType == 'all':
        result  = False
        result |= isValidPath(root, path, TYPE_GUI_DATA)
        result |= isValidPath(root, path, TYPE_TAB)
        result |= isValidPath(root, path, TYPE_TAB_GROUP)
        result |= isValidPath(root, path, LINK_SIGNUP)
        return result
    elif pathType == LINK_SIGNUP:
        return path == LINK_SIGNUP
    else:
        return False

def getEntryPoint(node):
    tabGroups = getTabGroups(node)

    if len(tabGroups) >= 1:
        return tabGroups[0]
    return None

def hasReservedName(node):
    return node != None and isReservedName(node.tag)

def isReservedName(name):
    return name in TYPES

def hasUserDefinedName(node):
    return node != None and isUserDefinedName(node.tag)

def isUserDefinedName(name):
    return name != None and name.istitle()

def isHierarchical(node):
    return getUiType(node) in MENU_UI_TYPES \
            and bool(node.xpath('.//opt/opt'))

def getXmlType(node):
    '''
    Returns the type assigned during annotation with `annotateWithXmlTypes`.
    '''
    if node == None:
        return ''
    if not RESERVED_XML_TYPE in node.attrib:
        return ''
    return node.attrib[RESERVED_XML_TYPE]

def getLogic(node):
    nodes = xml.getAll(node, lambda e: getXmlType(e) == TYPE_LOGIC)
    if len(nodes) < 1:
        return ''
    else:
        return nodes[0].text

def isTabGroup(node):
    return getXmlType(node) == TYPE_TAB_GROUP

def isTab(node):
    return getXmlType(node) in (TYPE_TAB, TYPE_SEARCH)

def isGuiDataElement(node):
    return getXmlType(node) in GUI_DATA_UI_TYPES

def getByType(node, typeFun, keep, descendantOrSelf):
    if keep: everythingToKeep = lambda e : typeFun(e) and keep(e)
    else:    everythingToKeep = lambda e : typeFun(e)

    return xml.getAll(node, everythingToKeep, descendantOrSelf)

def getTabGroups(node, keep=None, descendantOrSelf=True):
    return getByType(node, isTabGroup, keep, descendantOrSelf)

def getTabs(node, keep=None, descendantOrSelf=True):
    return getByType(node, isTab, keep, descendantOrSelf)

def getGuiDataElements(node, keep=None, descendantOrSelf=True):
    return getByType(node, isGuiDataElement, keep, descendantOrSelf)
