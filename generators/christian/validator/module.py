#!/usr/bin/env python2

import consts
import helpers
import sys
import tables
import util.xml
import util.schema
import util.arch16n

################################################################################
#                                  PARSE XML                                   #
################################################################################
print 'Parsing XML...'
filenameModule = sys.argv[1]
print 'HERE!', filenameModule
tree = util.xml.parseXml(filenameModule)
print 'Done!'
print

util.schema.normalise(tree)

################################################################################
#                               VALIDATE SCHEMA                                #
################################################################################
print 'Validating schema...'
countWar = 0
countErr = 0

######################### FLAG NODES WITH THEIR TYPES ##########################
util.schema.annotateWithTypes(tree)

# Nodes which didn't end up getting flagged...
exp  = '//*[@%s]/*[not(@%s)]'
exp %= (consts.RESERVED_XML_TYPE, consts.RESERVED_XML_TYPE)
disallowed = tree.xpath(exp)
# ...and aren't in <rels> are disallowed
exp  = './ancestor-or-self::rels'
cond = lambda e: not e.xpath(exp)
disallowed = filter(cond, disallowed)

# Tell the user about the error(s)
for d in disallowed:
    msg           = 'Element `%s` disallowed here' % d.tag
    affectedNodes = [d]
    expectedItems = helpers.getExpectedTypes(tables.TYPES, d, None)
    helpers.eMsg(msg, affectedNodes, expectedItems)

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

exp  = '//*[@%s="%s" and not(@t)]'
exp %= (consts.RESERVED_XML_TYPE, 'GUI/data element')
matches = tree.xpath(exp)
for m in matches:
    m.attrib['t'] = util.schema.guessType(m)

    msg  = 'No value for the attribute t of the element `%s` is present.  '
    msg += 'Assuming a value of `%s`'
    msg %= (m.tag, m.attrib['t'])

    helpers.wMsg(msg, [m])

################ VALIDATE CARDINALITIES FOR COMPOSITE ELEMENTS #################

helpers.expandCompositeElements(tree)

# Check cardinality contraints
el   = 'GUI/data element'
mod  = 'module'
t    = 'tab'
tg   = 'tab group'

data = 'data'
ui   = 'UI'

helpers.checkTagCardinalityConstraints(tree, mod, tg, ui)
helpers.checkTagCardinalityConstraints(tree, tg,  t,  ui)
helpers.checkTagCardinalityConstraints(tree, t,  el,  ui)

helpers.checkTagCardinalityConstraints(tree, mod, tg, data)
helpers.checkTagCardinalityConstraints(tree, mod, el, data)

################################# MISC ERRORS ##################################

################################################################################

msg  = 'Binding in b attribute ignored; use of "autonum" flag forces decimal '
msg += 'binding'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[@b]'
cond = lambda e: util.schema.isFlagged(e, 'autonum')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Style in c attribute not applied; styling conflict exists due to '
msg += '"autonum" flag'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[@c]'
cond = lambda e: util.schema.isFlagged(e, 'autonum')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Style in c attribute not applied; styling conflict exists due to '
msg += '"notnull" flag'

# Select all notnull-flagged elements which also have their b attributes set
exp  = '//*[@c]'
cond = lambda e: util.schema.isFlagged(e, 'notnull')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements whose t attribute is equivalent to "dropdown" or "list" '
msg += 'may have the "user" flag'

# Select all GUI/data elements'
exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
# Select all user-flagged elements from those
cond1 = lambda e: util.schema.isFlagged(e, 'user')
# Select all elements whose type is not dropdown nor list
cond2 = lambda e: util.schema.guessType(e) not in ('dropdown', 'list')
matches = tree.xpath(exp)
matches = filter(cond1, matches)
matches = filter(cond2, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Module contains more than one user login menu'

# Select all GUI/data elements'
exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
# Select all user-flagged elements from those
cond = lambda e: util.schema.isFlagged(e, 'user')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
if len(matches) >= 2:
    affectedNodes = matches
    helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Text not present in <opt> tag'

# Select all user-flagged elements
exp  = '//opt'
cond = lambda e: e.text == None or e.text.strip() == ''
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Elements cannot have "l" and "lc" attributes simultaneously'

# Select all elements having l and lc attributes
exp  = '//*[@l and @lc]'
matches = tree.xpath(exp)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Elements are flagged with "autonum" but <autonum> tag is not present'

# Select all elements flagged with autonum
exp  = '//*'
cond = lambda e: util.schema.isFlagged(e, 'autonum')
matchesFlag = tree.xpath(exp)
matchesFlag = filter(cond, matchesFlag)
matchesFlag = util.schema.filterUnannotated(matchesFlag)

# Select all <autonum> tags
exp  = '//autonum'
matchesTag = tree.xpath(exp)
matchesTag = util.schema.filterUnannotated(matchesTag)

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
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Elements flagged with "noui" or "nodata" cannot possess the "lc" '
msg += 'attribute'

exp  = '//*[@lc]'
cond = lambda e: util.schema.isFlagged(e, ['nodata', 'noui'])
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Tab groups not flagged with "nodata" require at least one identifier'

exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab group')
cond = lambda e: not util.schema.isFlagged(e, 'nodata') and \
                 not util.schema.hasElementFlaggedWithId(e)
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements whose t attribute is equivalent to one of the following '
msg += 'may contain <opts> tags: %s' % ', '.join(tables.MENU_TS)

# Get <opts> tags which are the children of GUI/data elements
exp  = '//*[@%s="%s"]/opts' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
# Filter out <opts> tags whose element's t attrib *is* in DESC_TS
cond = lambda e: not util.schema.guessType(e.getparent()) in tables.MENU_TS
matches = tree.xpath(exp)
matches = filter(cond, matches)
# Effectively, filter out <opts> tags which were already complained about
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements not flagged with "nodata" may contain <desc> tags'

# Get <desc> tags
exp  = '//desc'
# Filter out <desc> tags not flagged with "nodata"
cond = lambda e: util.schema.isFlagged(e, 'nodata')
matches = tree.xpath(exp)
matches = filter(cond, matches)
# Effectively, filter out <desc> tags which were already complained about
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements whose t attribute is equivalent to one of the following '
msg += 'may contain <desc> tags: %s' % ', '.join(tables.DESC_TS)

# Get <desc> tags which are the children of GUI/data elements
exp  = '//*[@%s="%s"]/desc' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
# Filter out <desc> tags whose element's t attrib *is* in DESC_TS
cond = lambda e: not util.schema.guessType(e.getparent()) in tables.DESC_TS
matches = tree.xpath(exp)
matches = filter(cond, matches)
# Effectively, filter out <desc> tags which were already complained about
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'The use of the "lc" attribute generates a relationship `%s` which is a '
msg  += 'duplicate of a user-specified one'

# Get elements which have lc attributes...
exp  = '//*[@lc]'
matches = tree.xpath(exp)
# ...Which also have valid relationships (and therefore valid relNames)...
cond = lambda e: helpers.getRelName(e) != None
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)
# ...And conflict with entries in the <rels> tags
exp = '//rels/*[@name="%s"]'
cond = lambda e: len(tree.xpath(exp % helpers.getRelName(e))) > 0
matches = filter(cond, matches)

for m in matches:
    # Find the entries in <rels> that `m` conflicts with
    relName = helpers.getRelName(m)
    exp = '//rels/*[@name="%s"]' % relName
    conflictingRels = tree.xpath(exp)

    # Notify the user of the conflict
    msg_ = msg % relName
    affectedNodes = conflictingRels + [m]
    helpers.eMsg(msg_, affectedNodes)

################################ MISC WARNINGS #################################

################################################################################

msg  = 'Module is missing a login menu'

# Select all GUI/data elements'
exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
# Select all user-flagged elements from those
cond = lambda e: util.schema.isFlagged(e, 'user')
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
if len(matches) == 0:
    helpers.wMsg(msg)

################################################################################

msg  = 'Text is superfluous here as it can be inferred from its element\'s tag'

# List of types which interpret their text as labels
types = [
        'tab',
        'tab group',
        'GUI/data element',
]
# Make list of nodes whose type is in `types`
matches = []
for t in types:
    exp  = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, t)
    matches += tree.xpath(exp)
# Retain only elements with superfluous text
cond = lambda e: util.arch16n.getLabelFromText(e) == util.arch16n.getLabelFromTag(e)
matches = filter(cond, matches)
# Pretty up the output a little
matches.sort(key=lambda e: e.sourceline)

helpers.wMsg(msg, matches)
