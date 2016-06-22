from   lxml import etree
import copy
import hashlib
import re
import util.schema
import util.xml
import util.consts

def replaceElement(element, replacements, tag='__REPLACE__'):
    replacements = replacements.replace('\n', ' ')
    replacements = replacements.replace('\r', ' ')
    replacements = re.sub('>\s+<', '><', replacements)
    replacements = replacements.replace('__REPLACE__', tag)
    replacements = '<root>%s</root>' % replacements
    replacements = etree.fromstring(replacements)

    originalSourceline = element.sourceline
    util.xml.setSourceline(replacements, originalSourceline)

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
            (children, util.consts.RESERVED_XML_TYPE, type)
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

def checkTagCardinalityConstraints(tree, nodeTypeParent, nodeTypeChild, schemaType):
    assert schemaType in ['UI', 'data']

    elements = tree.xpath(
            '//*[@%s="%s"]' %
            (util.consts.RESERVED_XML_TYPE, nodeTypeChild)
    )

    for original in elements:
        duplicatesAndSelf = original.xpath(
                './ancestor::*[@%s="%s"]//%s[@%s="%s" and not(@%s="true")]' %
                (
                    util.consts.RESERVED_XML_TYPE, nodeTypeParent, original.tag,
                    util.consts.RESERVED_XML_TYPE, nodeTypeChild,
                    util.consts.RESERVED_IGNORE
                )
        )
        if schemaType == 'UI'  : cond = lambda n: not util.schema.isFlagged(n, 'noui')
        if schemaType == 'data': cond = lambda n: not util.schema.isFlagged(n, 'nodata')
        duplicatesAndSelf = filter(cond, duplicatesAndSelf)

        for original in duplicatesAndSelf: # Make sure not to re-check duplicate
            original.attrib[util.consts.RESERVED_IGNORE] = "true"
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

    util.xml.deleteAttribFromTree(elements, util.consts.RESERVED_IGNORE)

def getRelName(node):
    if not util.xml.hasAttrib(node, 'lc'):
        return None
    if util.schema.getParentTabGroup(node) == None:
        return None

    parentName = util.schema.getParentTabGroup(node)
    parentName = parentName.tag
    parentName = parentName.replace('_', ' ')

    childName = node.attrib['lc']
    childName = childName.replace('_', ' ')

    relName = '%s - %s' % (parentName, childName)
    return relName

def expandCompositeElements(tree):
    # (1) REPLACE ELEMENTS HAVING A CERTAIN T ATTRIBUTE
    for attrib, replacements in util.table.REPLACEMENTS_BY_T_ATTRIB.iteritems():
        exp     = '//*[@%s]' % util.consts.RESERVED_XML_TYPE
        cond    = lambda e: util.schema.guessType(e) == attrib
        matches = tree.xpath(exp)
        matches = filter(cond, matches)

        for m in matches:
            replaceElement(m, replacements, m.tag)

    # (2) REPLACE ELEMENTS HAVING A CERTAIN TAG NAME
    # <autonum> tags get special treatment
    tagMatches  = tree.xpath('//autonum')
    if tagMatches:
        tagMatch = tagMatches[0]

        cond        = lambda e: util.schema.isFlagged(e, 'autonum')
        exp         = './/*[@%s="%s"]'
        exp        %= util.consts.RESERVED_XML_TYPE, 'GUI/data element'
        flagMatches = tree.xpath(exp)
        flagMatches = filter(cond, flagMatches)

        replacements = util.table.REPLACEMENTS_BY_TAG['autonum'] * len(flagMatches)
        replacements = replaceElement(tagMatch, replacements)

        for autonumDest, autonumSrc in zip(flagMatches, replacements):
            needle      = '__REPLACE__'
            haystack    = autonumSrc .tag
            replacement = autonumDest.tag

            autonumSrc.tag = haystack.replace(needle, replacement)

    # Replace non-<autonum> tags similarly to in (1).
    for tag, replacements in util.table.REPLACEMENTS_BY_TAG.iteritems():
        exp = '//%s[@%s]' % (tag, util.consts.RESERVED_XML_TYPE)
        matches = tree.xpath(exp)
        for m in matches:
            replaceElement(m, replacements)

    util.schema.annotateWithTypes(tree)
