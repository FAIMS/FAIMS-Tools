from   lxml import etree
import consts
import helpers
import sys
import tables

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
parser = etree.XMLParser(strip_cdata=False)
try:
    print 'Parsing XML...'
    tree = etree.parse(filenameModule, parser)
except etree.XMLSyntaxError as e:
    print e
    exit()
print 'Done!'
print
tree = tree.getroot()
helpers.normaliseAttributes(tree)

################################################################################
#                               VALIDATE SCHEMA                                #
################################################################################
print 'Validating schema...'
countWar = 0
countErr = 0

######################### FLAG NODES WITH THEIR TYPES ##########################
ok = True
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
        matches = helpers.getNonLower(matches)
    else:
        exp  = '//*[@%s="%s"]/%s'
        exp %= (consts.RESERVED_XML_TYPE, parentType, pattern)
        matches = tree.xpath(exp)
    helpers.flagAll(matches, consts.RESERVED_XML_TYPE, matchType)

# Nodes which didn't end up getting flagged aren't allowed
exp  = '//*[@%s]/*[not(@%s)]'
exp %= (consts.RESERVED_XML_TYPE, consts.RESERVED_XML_TYPE)
disallowed = tree.xpath(exp)

# Tell the user about the error(s)
for d in disallowed:
    msg           = 'Element `%s` disallowed here' % d.tag
    affectedNodes = [d]
    expectedItems = getExpectedTypes(TYPES, d, None)
    helpers.eMsg(msg, affectedNodes, expectedItems)

    countErr += 1; ok &= False



############# COARSE-GRAINED VALIDATION OF ATTRIBUTES OF ELEMENTS ##############
# Only consider nodes flagged with `consts.RESERVED_XML_TYPE`
exp  = '//*[@%s]'
exp %= (consts.RESERVED_XML_TYPE)
matches = tree.xpath(exp)
# Determine if nodes contain an attribute disallowed according to tables.ATTRIBS
disallowed = []
for m in matches:
    mAttribs     = dict(m.attrib)
    mXmlType     = mAttribs[consts.RESERVED_XML_TYPE]
    mAttribNames = mAttribs
    mAttribNames.pop(consts.RESERVED_XML_TYPE, None)

    for mAttribName in mAttribNames:
        if not mAttribName in helpers.getAttributes(tables.ATTRIBS, mXmlType):
            disallowed.append((mAttribName, m))
# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib   = d[0]
    disallowedNode     = d[1]
    disallowedNodeType = d[1].attrib[consts.RESERVED_XML_TYPE]

    msg           = 'Attribute `%s` disallowed here' % disallowedAttrib
    affectedNodes = [disallowedNode]
    expectedItems = helpers.getAttributes(tables.ATTRIBS, disallowedNodeType)
    helpers.eMsg(msg, affectedNodes, expectedItems)

    countErr += 1; ok &= False




############## COARSE-GRAINED VALIDATION OF VALUES OF ATTRIBUTES ###############
# Only consider nodes flagged with `consts.RESERVED_XML_TYPE`
matches = tree.xpath(
        '//*[@%s]' %
        (consts.RESERVED_XML_TYPE)
)
# Determine if attributes contain allowed values according to tables.ATTRIB_VALS
disallowed = []
for m in matches:
    disallowed.extend(helpers.disallowedAttribVals(tree, m, tables.ATTRIB_VALS))

# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib    = d[0]
    disallowedAttribVal = d[1]
    disallowedNode      = d[2]

    ATTRIB_VALS = tables.ATTRIB_VALS
    allowedOneOf  = helpers.getAttributes(ATTRIB_VALS, disallowedAttrib, 1)
    allowedManyOf = helpers.getAttributes(ATTRIB_VALS, disallowedAttrib, 2)
    allowed       = allowedOneOf + allowedManyOf

    if   allowedOneOf:
        msg  = 'Item `%s` in attribute %s is disallowed.  Exactly one item is '
        msg += 'expected'
    elif allowedManyOf:
        msg  = 'Item `%s` in attribute %s is disallowed.  One or more items '
        msg += 'are expected'
    else:
        sys.stderr.write('Oops!')
        exit()
    msg %= (disallowedAttribVal, disallowedAttrib)
    affectedNodes = [disallowedNode]
    expectedItems = allowed
    helpers.eMsg(msg, affectedNodes, expectedItems)

    countErr += 1; ok &= False




######################## VALIDATE CARDINALITIES BY TYPE ########################
# Only consider nodes flagged with `consts.RESERVED_XML_TYPE`
disallowed = []
for c in tables.CARDINALITIES:
    parentTypeName        = c[0]
    directChildContraints = c[1]
    descendantContraints  = c[2]

    exp = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, parentTypeName)
    matches = tree.xpath(exp)

    for m in matches:
        sat = helpers.satisfiesTypeCardinalityConstraint
        dir = (m, parentTypeName, directChildContraints, 'direct')
        des = (m, parentTypeName, descendantContraints , 'descendant')
        if not sat(m, directChildContraints, 'direct'    ): disallowed += [dir]
        if not sat(m, descendantContraints , 'descendant'): disallowed += [des]

for d in disallowed:
    node                = d[0]
    name                = node.tag
    typeParent          = d[1]
    min, typeChild, max = d[2]
    childDirectness     = d[3]

    if   min == None:
        nounPhrase = helpers.descChildNounPhrase(childDirectness, max)
        msg  = 'Element `%s` of type %s requires at most %s %s of type %s'
        msg %= (name, typeParent,      max, nounPhrase, typeChild)
    elif max == None:
        nounPhrase = helpers.descChildNounPhrase(childDirectness, min)
        msg  = 'Element `%s` of type %s requires at least %s %s of type %s'
        msg %= (name, typeParent, min,      nounPhrase, typeChild)
    else:
        pluralNumber = 2
        nounPhrase = helpers.descChildNounPhrase(childDirectness, pluralNumber)
        msg  = 'Element `%s` of type %s requires between %s and %s %s '
        msg += '(inclusive) of type %s'
        msg %= (name, typeParent, min, max, nounPhrase, typeChild)
    helpers.eMsg(msg, [node])

    countErr += 1; ok &= False

exp  = '//*[@%s="%s" and not(@t)]'
exp %= (consts.RESERVED_XML_TYPE, 'GUI/data element')
matches = tree.xpath(exp)
for m in matches:
    m.attrib['t'] = helpers.guessType(m)

    msg  = 'No value for the attribute t of the element `%s` is present.  '
    msg += 'Assuming a value of `%s`'
    msg %= (m.tag, m.attrib['t'])

    helpers.wMsg(msg, [m])
    countWar += 1; ok &= True



######################## VALIDATE CARDINALITIES BY TAG #########################
# Transform XML such that cardinalities of UI and data schema elements
# represented by "composite" XML elements are preserved.  For "composite" XML
# elements, this makes some checks easier to perform.

for attrib, replacement in tables.REPLACEMENTS_BY_T_ATTRIB.iteritems():
    exp = '//*[@%s and @t="%s"]' % (consts.RESERVED_XML_TYPE, attrib)
    matches = tree.xpath(exp)
    for m in matches:
        helpers.replaceElement(m, replacements, m.tag)

for tag, replacements in tables.REPLACEMENTS_BY_TAG.iteritems():
    exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
    matches = tree.xpath(exp)
    for m in matches:
        helpers.replaceElement(m, replacements)

# Check cardinality contraints
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'module',    'tab group',   'UI')
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'tab group', 'tab',         'UI')
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'tab',       'GUI/data element', 'UI')
countErr += countErr_; ok &= ok_

countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'module',    'tab group',   'data')
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'tab group', 'GUI/data element', 'data')
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, 'module',    'GUI/data element', 'data')
countErr += countErr_; ok &= ok_


exit()
