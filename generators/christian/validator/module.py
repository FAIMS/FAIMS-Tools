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
helpers.annotateWithTypes(tree)

# Nodes which didn't end up getting flagged aren't allowed
exp  = '//*[@%s]/*[not(@%s)]'
exp %= (consts.RESERVED_XML_TYPE, consts.RESERVED_XML_TYPE)
disallowed = tree.xpath(exp)

# Tell the user about the error(s)
for d in disallowed:
    msg           = 'Element `%s` disallowed here' % d.tag
    affectedNodes = [d]
    expectedItems = helpers.getExpectedTypes(tables.TYPES, d, None)
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
exp = '//*[@%s]' % (consts.RESERVED_XML_TYPE)
matches = tree.xpath(exp)

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

# Tell user about error(s)
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

################ VALIDATE CARDINALITIES FOR COMPOSITE ELEMENTS #################
ok = True

# "Expand" composite elements into the GUI/Data elements they represent
for attrib, replacements in tables.REPLACEMENTS_BY_T_ATTRIB.iteritems():
    exp = '//*[@%s and @t="%s"]' % (consts.RESERVED_XML_TYPE, attrib)
    matches = tree.xpath(exp)
    for m in matches:
        helpers.replaceElement(m, replacements, m.tag)

for tag, replacements in tables.REPLACEMENTS_BY_TAG.iteritems():
    exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
    matches = tree.xpath(exp)
    for m in matches:
        helpers.replaceElement(m, replacements)

helpers.annotateWithTypes(tree)

# Check cardinality contraints
el   = 'GUI/data element'
mod  = 'module'
t    = 'tab'
tg   = 'tab group'

data = 'data'
ui   = 'UI'

countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, mod, tg, ui)
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, tg,  t,  ui)
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, t,  el,  ui)
countErr += countErr_; ok &= ok_

countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, mod, tg, data)
countErr += countErr_; ok &= ok_
countErr_, ok_ = helpers.checkTagCardinalityConstraints(tree, mod, el, data)
countErr += countErr_; ok &= ok_

################################# MISC ERRORS ##################################

msg  = 'Binding in b attribute ignored; use of "autonum" flag forces decimal '
msg += 'binding'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[@b]'
cond = lambda e: helpers.isFlagged(e, 'autonum')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
for m in matches:
    affectedNodes = [m]
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Property has <str> tags but is not flagged as an identifier'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[str]'
cond = lambda e: not helpers.isFlagged(e, 'id')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
for m in matches:
    affectedNodes = [m]
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Style in c attribute not applied; styling conflict exists due to '
msg += '"autonum" flag'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[@c]'
cond = lambda e: helpers.isFlagged(e, 'autonum')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
for m in matches:
    affectedNodes = [m]
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Style in c attribute not applied; styling conflict exists due to '
msg += '"notnull" flag'

# Select all notnull-flagged elements which also have their b attributes set
exp  = '//*[@c]'
cond = lambda e: helpers.isFlagged(e, 'notnull')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
for m in matches:
    affectedNodes = [m]
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'This module has more than one user login menu'

# Select all user-flagged elements
exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')

cond = lambda e: helpers.isFlagged(e, 'user')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
if len(matches) > 1:
    affectedNodes = matches
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Text must be present in <opt> tags'

# Select all user-flagged elements
exp  = '//opt'
matches = tree.xpath(exp)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
if len(matches) > 1:
    affectedNodes = matches
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'An element cannot have "l" and "lc" attributes simultaneously'

# Select all elements having l and lc attributes
exp  = '//*[@l and @lc]'
matches = tree.xpath(exp)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
if matches:
    affectedNodes = matches
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Elements are flagged with "autonum" but <autonum> tag is not present'

# Select all elements flagged with autonum
exp  = '//*'
cond = lambda e: helpers.isFlagged(e, 'autonum')
matchesFlag = tree.xpath(exp)
matchesFlag = filter(cond, matchesFlag)
matchesFlag = helpers.filterUnannotated(matchesFlag)

# Select all <autonum> tags
exp  = '//autonum'
matchesTag = tree.xpath(exp)
matchesTag = helpers.filterUnannotated(matchesTag)

# Tell the user about the error(s)
if matchesFlag and not matchesTag:
    affectedNodes = matchesFlag
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Elements having a t attribute value of "viewfiles" cannot also have an '
msg += 'lc attribute'

# Select all elements having @lc and @t="viewfiles"
exp  = '//*[@lc and @t="viewfiles"]'
matches = tree.xpath(exp)
matches = helpers.filterUnannotated(matches)

# Tell the user about the error(s)
if matches:
    affectedNodes = matches
    helpers.eMsg(msg, affectedNodes)
