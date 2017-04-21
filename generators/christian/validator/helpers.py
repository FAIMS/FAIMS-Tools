from   lxml import etree
import copy
import re
import util.consts
import util.schema
import util.xml

def wMsg(notice, nodes=None, expected=None):
    if expected is None: expected = []

    notice = 'WARNING: ' + notice
    printNotice(notice, nodes, expected)

def eMsg(notice, nodes=None, expected=None):
    if expected is None: expected = []

    notice = 'ERROR:   ' + notice
    printNotice(notice, nodes, expected)

def printNotice(notice, nodes=None, expected=None):
    if expected is None: expected = []

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

    return []

def disallowedAttribVals(tree, m, ATTRIB_VALS):
    disallowed = []
    for attrib, oneOf, manyOf in ATTRIB_VALS:
        if attrib not in m.attrib: # Set intersection of attrib and m.attrib
            continue

        if oneOf:
            if '$link' in oneOf:
                link = m.attrib[attrib]
                linkType = oneOf[6:] # 'all', 'tab', or 'tabgroup'
                if not util.schema.isValidPath(tree, link, linkType):
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
