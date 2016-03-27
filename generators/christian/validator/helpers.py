from   lxml import etree
import consts
import copy
import hashlib
import re
import tables

def isDataElement(guiDataElement):
    if isFlagged(guiDataElement, 'nodata'):      return False
    if isFlagged(guiDataElement, 'user'):        return False
    if hasAttrib(guiDataElement, 'e'):           return False
    if hasAttrib(guiDataElement, 'ec'):          return False
    if guessType(guiDataElement) == 'button':    return False
    if guessType(guiDataElement) == 'gpsdiag':   return False
    if guessType(guiDataElement) == 'group':     return False
    if guessType(guiDataElement) == 'map':       return False
    if guessType(guiDataElement) == 'table':     return False
    if guessType(guiDataElement) == 'viewfiles': return False
    return True

def getPropType(node):
    if hasMeasureType(node): return 'measure'
    if hasFileType   (node): return 'file'
    if hasVocabType  (node): return 'vocab'

    raise ValueError('An unexpected t value was encountered')

def hasMeasureType(node):
    measureTypes = (
            'input',
    )
    return guessType(node) in measureTypes

def hasFileType(node):
    fileTypes    = (
            'audio',
            'camera',
            'file',
            'video',
    )
    return guessType(node) in fileTypes

def hasVocabType(node):
    vocabTypes   = (
            'checkbox',
            'dropdown',
            'list',
            'picture',
            'radio',
    )
    return guessType(node) in vocabTypes

################################################################################

def appendNotNone(src, dst):
    if src == None:
        return
    dst.append(src)

def normaliseSpace(str):
    str = str.split()
    str = ' '.join(str)
    return str

def parseXml(filename):
    parser = etree.XMLParser(strip_cdata=False)
    try:
        tree = etree.parse(filename, parser)
    except etree.XMLSyntaxError as e:
        print e
        exit()
    tree = tree.getroot()
    return tree

def filterUnannotated(nodes):
    cond = lambda e: isAnnotated(e)
    return filter(cond, nodes)

def isAnnotated(e):
    try:
        return e.attrib[consts.RESERVED_XML_TYPE] != ''
    except:
        pass
    return False

def deleteAttribFromTree(t, attrib):
    if t == None:
        return
    if hasattr(t, 'attrib') and attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(e, attrib)

def annotateWithTypes(tree):
    for t in tables.TYPES:
        parentType = t[0]
        pattern    = t[1]
        matchType  = t[2]

        if   pattern == '/':
            exp = '/*'
            matches = tree.xpath(exp)
        elif pattern == '/[^a-z]/':
            exp = '//*[@%s="%s"]/*' % (consts.RESERVED_XML_TYPE, parentType)
            matches = tree.xpath(exp)
            matches = getNonLower(matches)
        else:
            exp  = '//*[@%s="%s"]/%s'
            exp %= (consts.RESERVED_XML_TYPE, parentType, pattern)
            matches = tree.xpath(exp)
        flagAll(matches, consts.RESERVED_XML_TYPE, matchType)


def replaceElement(element, replacements, tag='__REPLACE__'):
    replacements = replacements.replace('\n', ' ')
    replacements = replacements.replace('\r', ' ')
    replacements = re.sub('>\s+<', '><', replacements)
    replacements = replacements.replace('__REPLACE__', tag)
    replacements = '<root>%s</root>' % replacements
    replacements = etree.fromstring(replacements)

    originalSourceline = element.sourceline
    setSourceline(replacements, originalSourceline)

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

def setSourceline(t, sourceline):
    if t == None:
        return

    t.sourceline = sourceline
    for e in t:
        setSourceline(e, sourceline)

def getNonLower(t):
    nodes = [i for i in t if re.search('[^a-z]', i.tag)] # TODO: Might be failing due to comments
    return nodes

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

def wMsg(notice, nodes=None, expected=[]):
    notice = 'WARNING: ' + notice
    printNotice(notice, nodes, expected)

def eMsg(notice, nodes=None, expected=[]):
    notice = 'ERROR:   ' + notice
    printNotice(notice, nodes, expected)

def printNotice(notice, nodes=None, expected=[]):
    if   nodes      == None:
        location = ''
    elif len(nodes) == 0:
        return
    elif len(nodes) == 1:
        location = 'Occurs at line ' + str(nodes[0].sourceline) + '.  '
    elif len(nodes) >= 2:
        location = 'Occurs at:'
        for node in nodes:
            location += '\n  - Line ' + str(node.sourceline)

    if   len(expected) == 0:
        expected = ''
    elif len(expected) == 1:
        expected = 'Allowed item is %s.  ' % expected[0]
    else:
        expected = '\n  - '.join(expected)
        expected = 'Allowed items may include:\n  - %s\n' % expected

    notice = notice + '.  '

    print notice + expected + location
    print

def flagAll(nodes, attrib, value):
    for n in nodes:
        n.attrib[attrib] = value

def getExpectedTypes(table, node, reserved=False):
    attribType = '__RESERVED_XML_TYPE__'

    parent = node.getparent()

    # Get expected type(s)
    expected = []
    for row in table:
        parentType = row[0]
        pattern    = row[1]
        matchType  = row[2]

        if parent.attrib[attribType] != parentType:
            continue

        if   reserved == True:
            regex = '[^a-z]'
        elif reserved == False:
            regex = '^[a-z]+$'
        elif reserved == None:
            regex = '.*'
        else:
            continue

        if re.match(regex, matchType):
            expected.append(matchType)

    return expected

def getAttributes(table, xmlType, rowIndex=1):
    for row in table:
        rowXmlType = row[0]
        rowAttribs = row[rowIndex]

        if type(rowAttribs) is not list:
            if not rowAttribs:
                rowAttribs = []
            else:
                rowAttribs = [rowAttribs]

        for i in range(len(rowAttribs)):
            if   rowAttribs[i] == '$link-all':
                rowAttribs[i] = 'a valid link to a tab or tab group'
            elif rowAttribs[i] == '$link-tabgroup':
                rowAttribs[i] = 'a valid link to a tab group'
            elif rowAttribs[i] == '$link-tab':
                rowAttribs[i] = 'a valid link to a tab'

        if rowXmlType == xmlType:
            return rowAttribs

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

def disallowedAttribVals(tree, m, ATTRIB_VALS):
    disallowed = []
    for attrib, oneOf, manyOf in ATTRIB_VALS:
        if attrib not in m.attrib: # Set intersection of attrib and m.attrib
            continue

        if oneOf:
            if '$link' in oneOf:
                link = m.attrib[attrib]
                linkType = oneOf[6:] # 'all', 'tab', or 'tabgroup'
                if not isValidLink(tree, link, linkType):
                    disallowed.append((attrib, m.attrib[attrib], m))
            else:
                if m.attrib[attrib] not in oneOf:
                    disallowed.append((attrib, m.attrib[attrib], m))
        if manyOf:
            for flag in m.attrib[attrib].split():
                if flag not in manyOf:
                    disallowed.append((attrib, flag,             m))
    return disallowed

def satisfiesTypeCardinalityConstraint(parent, constraint, children='direct'):
    min, type, max = constraint
    if type == None:
        return True

    if children == 'direct':
        children = ''
    else:
        children = './/'
    matches = parent.xpath(
            '%s*[@%s="%s"]' %
            (children, consts.RESERVED_XML_TYPE, type)
    )

    if min != None and len(matches) < min: return False
    if max != None and len(matches) > max: return False
    return True

# English is dumb
def childWithGrammaticalNumber(number):
    if number == 1:
        return 'child'
    return 'children'
def descendantWithGrammaticalNumber(number):
    d = 'descendant'; s = 's'
    if number == 1:
        return d
    return  d + s
def descChildNounPhrase(childDirectness , number):
    if  childDirectness == 'direct':
        childNum = childWithGrammaticalNumber (number)
        return 'direct %s' % childNum
    else:
        return descendantWithGrammaticalNumber(number)

def guessType(node):
    # Don't guess the type if it's already there
    try:
        return node.attrib['t']
    except:
        pass

    # Okay, fine. Go ahead and give 'er a guess.
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

def checkTagCardinalityConstraints(tree, nodeTypeParent, nodeTypeChild, schemaType):
    assert schemaType in ['UI', 'data']

    elements = tree.xpath(
            '//*[@%s="%s"]' %
            (consts.RESERVED_XML_TYPE, nodeTypeChild)
    )

    for original in elements:
        duplicatesAndSelf = original.xpath(
                './ancestor::*[@%s="%s"]//%s[@%s="%s" and not(@%s="true")]' %
                (
                    consts.RESERVED_XML_TYPE, nodeTypeParent, original.tag,
                    consts.RESERVED_XML_TYPE, nodeTypeChild,
                    consts.RESERVED_IGNORE
                )
        )
        if schemaType == 'UI'  : cond = lambda n: not isFlagged(n, 'noui')
        if schemaType == 'data': cond = lambda n: not isFlagged(n, 'nodata')
        duplicatesAndSelf = filter(cond, duplicatesAndSelf)

        for original in duplicatesAndSelf: # Make sure not to re-check duplicate
            original.attrib[consts.RESERVED_IGNORE] = "true"
        if len(duplicatesAndSelf) <= 1:
            continue # If this runs, no duplicates were found

        capitalisedType = nodeTypeChild[0].upper() + nodeTypeChild[1:]

        msg  = '%s `%s` is illegally duplicated in its parent %s when the %s '
        msg += 'schema is generated.  (Note that some reserved elements are '
        msg += 'shorthand for sets of elements)'
        msg  = msg % \
                (
                        capitalisedType,
                        original.tag,
                        nodeTypeParent,
                        schemaType
                )
        eMsg(
                msg,
                duplicatesAndSelf
        )

    deleteAttribFromTree(elements, consts.RESERVED_IGNORE)

def hasAttrib(e, a):
    try:
        if a in e.attrib:
            return True
    except:
        return False

def hasElementFlaggedWith(tabGroup, flag):
    exp  = './/*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    cond = lambda e: isFlagged(e, flag)
    matches = tabGroup.xpath(exp)
    matches = filter(cond, matches)
    return len(matches) > 0

def hasElementFlaggedWithId(tabGroup):
    return hasElementFlaggedWith(tabGroup, 'id')

def getParentTabGroup(node):
    exp = './ancestor::*[last()-1]'
    matches = node.xpath(exp)
    if matches:
        return matches[0]
    return None

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

def getRelName(node):
    if not hasAttrib(node, 'lc'):
        return None
    if getParentTabGroup(node) == None:
        return None

    parentName = getParentTabGroup(node)
    parentName = parentName.tag
    parentName = parentName.replace('_', ' ')

    childName = node.attrib['lc']
    childName = childName.replace('_', ' ')

    relName = '%s - %s' % (parentName, childName)
    return relName

def getLabelFromTag(node):
    label = node.tag
    label = label.replace('_', ' ')
    label = normaliseSpace(label)
    return label

def getLabelFromText(node):
    if node.text == None:  return ''
    if node.text == 'opt': return ''

    label = node.text
    label = normaliseSpace(label)
    return label

def getArch16nVal(node):
    if node.xpath('./ancestor-or-self::rels'): return ''
    if isFlagged(node, 'nolabel'):             return ''

    if node.tag == 'autonum':                  return ''
    if node.tag == 'col':                      return ''
    if node.tag == 'cols':                     return ''
    if node.tag == 'desc':                     return ''
    if node.tag == 'logic':                    return ''
    if node.tag == 'module':                   return ''
    if node.tag == 'opts':                     return ''

    if node.tag == 'author':                   return 'Author'
    if node.tag == 'search':                   return 'Search'
    if node.tag == 'timestamp':                return 'Timestamp'

    if getLabelFromText(node):
        return getLabelFromText(node)
    return getLabelFromTag(node)

def getLabel(node):
    return getArch16nVal(node)

def getArch16nKey(node):
    return getArch16nVal(node).replace(' ', '_')

def expandCompositeElements(tree):
    # (1) REPLACE ELEMENTS HAVING A CERTAIN T ATTRIBUTE
    for attrib, replacements in tables.REPLACEMENTS_BY_T_ATTRIB.iteritems():
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

        cond        = lambda e: isFlagged(e, 'autonum')
        flagMatches = tree.xpath('//*')
        flagMatches = filter(cond, flagMatches)

        replacements = tables.REPLACEMENTS_BY_TAG['autonum'] * len(flagMatches)
        replacements = replaceElement(tagMatch, replacements)

        for autonumDest, autonumSrc in zip(flagMatches, replacements):
            needle      = '__REPLACE__'
            haystack    = autonumSrc .tag
            replacement = autonumDest.tag

            autonumSrc.tag = haystack.replace(needle, replacement)

    # Replace non-<autonum> tags similarly to in (1).
    for tag, replacements in tables.REPLACEMENTS_BY_TAG.iteritems():
        exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
        matches = tree.xpath(exp)
        for m in matches:
            replaceElement(m, replacements)

    annotateWithTypes(tree)
