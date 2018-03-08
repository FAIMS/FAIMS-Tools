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
import itertools
import os.path

INVALID_ATTRIB_NAMES_IN_FMT = None

def getPath(node, isInitialCall=True):
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
    if isInitialCall and getXmlType(node) not in nodeTypes:
        return []
    if RESERVED_XML_TYPE not in node.attrib:
        return getPath(node.getparent(), False) + []
    if getXmlType(node) not in nodeTypes:
        return getPath(node.getparent(), False) + []
    else:
        return getPath(node.getparent(), False) + [node.tag]

def getPathString(node, sep='/'):
    return sep.join(getPath(node))

def nodeHash(node, hashLen=10):
    path = getPathString(node)
    hash = hashlib.sha256(path)
    hash = hash.hexdigest()
    hash = hash[:hashLen]
    return hash

def insertIntoInvalidAttribNamesInFmt(attribName):
    global INVALID_ATTRIB_NAMES_IN_FMT

    if INVALID_ATTRIB_NAMES_IN_FMT == None:
        INVALID_ATTRIB_NAMES_IN_FMT = []

    if attribName != None:
        INVALID_ATTRIB_NAMES_IN_FMT.append(attribName)

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
    requiresAncestorCheck = (FLAG_NODATA, FLAG_NOUI, FLAG_NOWIRE)
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

def getSchemaCacheFilename(node):
    return '/tmp/%s.xml' % xml.treeHash(node)

def getCachedSchema(filename):
    if os.path.isfile(filename):
        return xml.parseXml(filename)
    else:
        return None

def cacheSchema(node, filename):
    s = etree.tostring(node)
    with open(filename, 'w') as f:
        f.write(s)

# Warning: Modifies `node` by reference
def parseSchema(node):
    filename = getSchemaCacheFilename(node)
    cachedSchema = getCachedSchema(filename)
    if cachedSchema != None:
        return cachedSchema

    normaliseXml(node)
    annotateWithXmlTypes(node)
    normaliseSchema(node)

    cacheSchema(node, filename)

    return node

def normaliseXml(node):
    normaliseAttributes(node)
    stripComments(node)

def normaliseAttributes(node):
    # Don't normalise stuff in <rels>
    if node.xpath('./ancestor-or-self::rels'):
        return
    # Do normalise everything else
    for key, val in node.attrib.iteritems():
        if key == ATTRIB_P:
            continue
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

def getUiType(node, force=False):
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
    if not force and not gui.isGuiElement(node):
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

def getParent(node, xmlType, orSelf=False):
    if node == None:
        return None

    if orSelf: axis = 'ancestor-or-self'
    else:      axis = 'ancestor'
    exp = './%s::*[@%s="%s"]' % (axis, RESERVED_XML_TYPE, xmlType)

    matches = node.xpath(exp)
    if matches: return matches[0]
    else:       return None

def getParentTabGroup(node, orSelf=False):
    return getParent(node, TYPE_TAB_GROUP, orSelf)

def getParentTab(node, orSelf=False):
    return getParent(node, TYPE_TAB, orSelf)

def getParentGuiDataElement(node, orSelf=False):
    return getParent(node, TYPE_GUI_DATA, orSelf)

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
        elif node.tag == TAG_FMT:         type = TYPE_FMT
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
        elif node.tag == TAG_MARKDOWN:    type = TYPE_MARKDOWN
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
    normaliseImplied(node)
    normaliseProps(node)
    normaliseSchemaRec(node)
    normaliseMap(node)
    normaliseCols(node)
    normaliseMedia(node)
    normaliseSignup(node)

def normaliseProps(node):
    homoProps = data.getHomonymousProps(node)
    homoProps = itertools.chain.from_iterable(homoProps) # Flatten

    for p in homoProps:
        propName = \
                data.getArchEntName(p, True) + \
                SEP_DATA + \
                data.getAttribName(p)
        xml.appendToAttrib(p, RESERVED_PROP_NAME, propName)

    homoProps = data.getHomonymousProps(node)
    homoProps = itertools.chain.from_iterable(homoProps) # Flatten

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
        button.text = arch16n.getArch16nVal(media, force=True)
        xml.insertAfter(media, button)

def normaliseMap(node):
    mapList = xml.getAll(node, keep=lambda e: getUiType(e) == UI_TYPE_MAP)

    for map in mapList:
        # Make 'Center Me' button
        btnCenter = Element(
                nextFreeName('Center_Me', map),
                { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                t=UI_TYPE_BUTTON
        )
        btnCenter.text = 'Center Me'

        # Make 'Save Map Settings' button
        btnSave = Element(
                nextFreeName('Save_Map_Settings', map),
                { RESERVED_XML_TYPE : TYPE_GUI_DATA },
                t=UI_TYPE_BUTTON
        )
        btnSave.text = 'Save Map Settings'

        # Make cols
        cols = Element(TAG_COLS, { RESERVED_XML_TYPE : TYPE_COLS })
        cols.append(btnCenter)
        cols.append(btnSave)

        # Add cols below map
        xml.insertAfter(map, cols)

def normaliseImplied(node):
    normaliseImpliedCss(node)
    #normaliseImpliedFlags(node)
    normaliseImpliedFmt(node)

def normaliseImpliedCss(node):
    # f="notnull" implies c="required"
    isNotNull = lambda e: isFlagged(
            e,
            FLAG_NOTNULL,
            checkAncestors=False,
    )
    notNull = xml.getAll(node, keep=isNotNull);

    for n in notNull:
        xml.appendToAttrib(n, ATTRIB_C, CSS_REQUIRED)

def normaliseImpliedFlags(node):
    isList = lambda n: getUiType(n) == UI_TYPE_LIST
    lists = util.xml.getAll(node, isList)

    tabs = [getParentTab(l) for l in lists]
    for t in tabs:
        xml.appendToAttrib(t, ATTRIB_F, FLAG_NOSCROLL)

def normaliseImpliedFmt(node):
    # <fmt>{{Attrib_Name}}</fmt> implies <Attrib_Name f="id>...
    nodes = util.schema.getTabGroups(node)
    for n in nodes:
        normaliseImpliedFmtInTabGroup(n)

def normaliseImpliedFmtInTabGroup(schemaTabGroup):
    ''' Converts the `<fmt>` tags which are direct children of tab groups into
        `<fmt>` tags which are direct children of GUI/Data elements.

        Returns the curly brace-enclosed components of the tab group's `<fmt>`
        text which did not refer to a GUI/Data element.
    '''
    newFmtStrNodes = schemaTabGroup.xpath('./fmt')
    if len(newFmtStrNodes) == 0:
        insertIntoInvalidAttribNamesInFmt(None)
        return

    newFmtStrNode = newFmtStrNodes[0]
    if not newFmtStrNode.text:
        insertIntoInvalidAttribNamesInFmt(None)
        return
    newFmtStr = newFmtStrNode.text
    newFmtStr = newFmtStr.strip()

    reChunk   = '((?!}}).)+((?!{{).)+'
    reCurlies = '({{((?!}}).)+}})'
    reAttrib  = '{{(((?!(}})|\s).)+)(((?!}}).)*)}}' # attrib    = group 1,
                                                    # condition = group 4

    # Chunk the fmt string. Each chunk corresponds to an old-style format
    # string, for individual properties
    split = re.split(reCurlies, newFmtStr)
    chunks = []
    while len(split) >= 2:
        chunk  = split.pop(0)
        chunk += split.pop(0)
        split.pop(0)

        chunks.append(chunk)
    while len(split) > 0:
        if len(chunks) == 0: chunks     += [split.pop(0)]
        else:                chunks[-1] +=  split.pop(0)

    # Get fmt strings
    # Replaces "my{{Identifer}}isgreat" with "my$0isgreat" in each chunk and
    # replaces "my{{Identifer if $0 then "$0" }}isgreat" with "my{{ if $0 then
    # "$0" }}isgreat"
    fmtStrs = [re.sub(reAttrib, '{{\\4}}', chunk) for chunk in chunks]
    fmtStrs = [fmtStr.replace('{{}}', '$0') for fmtStr in fmtStrs]

    # Get fmt attrib names
    attribNames = [awc.group(1) for awc in re.finditer(reAttrib, newFmtStr)]
    if len(attribNames) == 0:
        isId = lambda e: util.schema.isFlagged(e, FLAG_ID)
        idNodes = util.xml.getAll(schemaTabGroup, isId)
        attribNames = [n.tag for n in idNodes]

    # Convert attrib names to nodes
    attribNodes = []
    for aName in attribNames:
        getByTag = lambda n: n.tag == aName
        nodes = util.data.getProps(schemaTabGroup, keep=getByTag)

        if len(nodes) == 0:
            insertIntoInvalidAttribNamesInFmt(
                    (aName, schemaTabGroup.tag, newFmtStrNode)
            )

        if len(nodes) > 0:
            node = nodes[0]
            attribNodes.append(node)

    # Get fmt positions (i.e. the positions they should take in the data schema)
    fmtPoss = [str(i) for i in range(len(fmtStrs))]

    # Add str tags to the affected attribNodes if they don't exist
    for aNode in attribNodes:
        strNodes = aNode.xpath('./str')
        if len(strNodes) == 0:
            etree.SubElement(aNode, TAG_STR)

    # Flag affected attribNodes with f="id"
    for aNode in attribNodes:
        xml.appendToAttrib(aNode, ATTRIB_F, FLAG_ID)

    # Make and append fmt tags to attribNodes
    for aNode, fmtStr, fmtPos in zip(attribNodes, fmtStrs, fmtPoss):
        strNodes = aNode.xpath('./str')
        strNode = strNodes[0]
        fmtNode = etree.SubElement(strNode, TAG_FMT); fmtNode.text = fmtStr
        posNode = etree.SubElement(strNode, TAG_POS); posNode.text = fmtPos

        aNode.append(strNode)

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
    textMd += '* Bond@007\n'
    textMd += '* Dig.123\n'

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

def getNodeAtPath(tree, pathString):
    pathString = pathString.replace('!', '')

    root  = tree.getroottree().getroot()
    nodes = xml.getAll(root, lambda n: getPathString(n) == pathString)

    if len(nodes): return nodes[0]
    else:          return None

def getLinkedNode(node):
    return getNodeAtPath(node, getLink(node))

def getLinkedNodes(node, attribName=None):
    root = node.getroottree().getroot()
    return [getNodeAtPath(root, path) for path in getLinks(node, attribName)]

def isValidPath(root, path, pathType):
    if not path:
        return False

    if   pathType in ('gui', TYPE_GUI_DATA):
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

def isGuiDataElement(node, includeCols=False):
    if includeCols: return getXmlType(node) in GUI_DATA_UI_TYPES + [TYPE_COLS]
    else:           return getXmlType(node) in GUI_DATA_UI_TYPES

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
