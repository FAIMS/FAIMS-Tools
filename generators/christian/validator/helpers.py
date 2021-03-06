import copy
import re
from   util.consts import *
import util.data
import util.schema
import util.xml
import validator

def wMsg(notice, nodes=None, expected=None, moreLocations=None):
    '''
    Print a warning message (`notice`) about `nodes`.
    '''
    notice = 'WARNING: ' + notice
    if printNotice(notice, nodes, expected, moreLocations): validator.NUM_W += 1

def eMsg(notice, nodes=None, expected=None, moreLocations=None):
    '''
    Print an error message (`notice`) about `nodes`.
    '''
    notice = 'ERROR:   ' + notice
    if printNotice(notice, nodes, expected, moreLocations): validator.NUM_E += 1

def printNotice(notice, nodes=None, expected=None, moreLocations=None):
    '''
    `notice` is a string,
    `nodes` is a list of lxml Elements and `expected` is a list of strings.
    `moreLocations` allows you to override the default locations that are
    printed in the message. If they are given `len(moreLocations)` must equal
    `len(nodes)`.
    '''
    if expected is None: expected = []
    if nodes != None:
        nodes = filter(lambda x: x.sourceline != None, nodes)

    if moreLocations == None:
        pathNodes     = nodes or []
        pathStrings   = [util.schema.getPathString(node) for node in pathNodes]
        moreLocations = [
                ' (%s)' % pathString if pathString else '' \
                for pathString in pathStrings
        ]
    else:
        moreLocations = [' (%s)' % location for location in moreLocations]

    if   nodes      == None:
        location = ''
    elif len(nodes) == 0:
        return False
    elif len(nodes) == 1:
        node         = nodes[0]
        moreLocation = moreLocations[0]
        pathString = util.schema.getPathString(node)

        location  = 'Occurs at line ' + str(node.sourceline)
        location += moreLocation
        location += '.  '
    elif len(nodes) >= 2:
        location = 'Occurs at:'
        for node, moreLocation in zip(nodes, moreLocations):
            pathString = util.schema.getPathString(node)
            location += '\n  - Line ' + str(node.sourceline)
            location += moreLocation

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
    return True

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
            elif rowAttribs[i] == '$link-gui':
                rowAttribs[i] = 'a valid link to a gui/data element'

        if rowXmlType == xmlType:
            return rowAttribs

    return []

def disallowedAttribVals(tree, m, ATTRIB_VALS):
    disallowed = []
    for attrib, oneOf, manyOf in ATTRIB_VALS:
        if attrib not in m.attrib: # Set intersection of attrib and m.attrib
            continue

        # TODO: This code is horrible
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
            if '$link' in manyOf:
                links = m.attrib[attrib].split()
                linkType = manyOf[6:] # 'all', 'tab', or 'tabgroup'
                for link in links:
                    if not util.schema.isValidPath(tree, link, linkType):
                        disallowed.append((attrib, m.attrib[attrib], m))
            else:
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
            (children, RESERVED_XML_TYPE, type)
    )

    if min != None and len(matches) < min: return False
    if max != None and len(matches) > max: return False
    return True

# English is dumb
def childWithGrammaticalNumber(number):
    if number == 1: return 'child'
    else:           return 'children'

def descendantWithGrammaticalNumber(number):
    d = 'descendant'; s = 's'
    if number == 1: return d
    else:           return d + s

def descChildNounPhrase(childDirectness , number):
    if  childDirectness == 'direct':
        childNum = childWithGrammaticalNumber (number)
        return 'direct %s' % childNum
    else:
        return descendantWithGrammaticalNumber(number)

def checkTagCardinalityConstraints(tree, nodeTypeParent, nodeTypeChild):
    elements = tree.xpath(
            '//*[@%s="%s"]' %
            (RESERVED_XML_TYPE, nodeTypeChild)
    )

    for original in elements:
        duplicatesAndSelf = original.xpath(
                './ancestor::*[@%s="%s"]//%s[@%s="%s" and not(@%s="true")]' %
                (
                    RESERVED_XML_TYPE, nodeTypeParent, original.tag,
                    RESERVED_XML_TYPE, nodeTypeChild,
                    RESERVED_IGNORE
                )
        )
        cond = lambda n: not util.schema.isFlagged(n, FLAG_NOUI)
        duplicatesAndSelf = filter(cond, duplicatesAndSelf)

        for original in duplicatesAndSelf: # Make sure not to re-check duplicate
            original.attrib[RESERVED_IGNORE] = "true"
        if len(duplicatesAndSelf) <= 1:
            continue # If this runs, no duplicates were found

        msg  = '%s `%s` is illegally duplicated in its parent %s'
        msg %= (nodeTypeChild.capitalize(), original.tag, nodeTypeParent)
        eMsg(msg, duplicatesAndSelf)

    util.xml.deleteAttribFromTree(elements, RESERVED_IGNORE)

def checkDataSchemaConstraints(node):
    checkDataSchemaConstraintsWarn(node)
    checkDataSchemaConstraintsForType(node, util.data.getProps)
    checkDataSchemaConstraintsForType(node, util.data.getArchEnts)

def checkDataSchemaConstraintsForType(node, getNodesFun):
    homonymousNodes = util.data.getHomonymousNodes(node, getNodesFun)

    for nodeGroup in homonymousNodes:
        if nodeGroup != []:
            msg  = '%s elements share the name `%s` but have different '
            msg += 'representations in the data schema'
            msg %= (
                    util.schema.getXmlType(nodeGroup[0]).capitalize(),
                    nodeGroup[0].tag
            )
            eMsg(msg, nodeGroup)

def checkDataSchemaConstraintsWarn(node):
    wasRenamed = lambda n: util.xml.hasAttrib(n, RESERVED_PROP_NAME)
    nodes = util.xml.getAll(node, wasRenamed)

    msg  = 'Elements which share the same name but have different '
    msg += 'representations in the data schema are present.  These will have '
    msg += 'long-form names when the data schema is produced'
    wMsg(msg, nodes)
