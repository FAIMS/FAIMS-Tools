#!/usr/bin/env python2

import helpers
import sys
import util.arch16n
from   util.consts import *
import util.data
import util.schema
import util.xml
import itertools
import validator

################################################################################
#                                  PARSE XML                                   #
################################################################################
print 'Parsing XML...'
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
print 'Parsing XML completed'
print

util.schema.normaliseXml(tree)

################################################################################
#                               VALIDATE SCHEMA                                #
################################################################################
print 'Validating schema...'
print

######################### FLAG NODES WITH THEIR TYPES ##########################
util.schema.annotateWithXmlTypes(tree)

# Nodes which didn't end up getting flagged...
exp  = '//*[@%s]/*[not(@%s)]'
exp %= (RESERVED_XML_TYPE, RESERVED_XML_TYPE)
disallowed = tree.xpath(exp)
# ...and aren't in <rels> are disallowed
exp  = './ancestor-or-self::rels'
cond = lambda e: not e.xpath(exp)
disallowed = filter(cond, disallowed)

# Tell the user about the error(s)
for d in disallowed:
    msg           = 'Element `%s` disallowed here' % d.tag
    affectedNodes = [d]
    expectedItems = helpers.getExpectedTypes(util.table.TYPES, d, None)
    helpers.eMsg(msg, affectedNodes, expectedItems)

############# COARSE-GRAINED VALIDATION OF ATTRIBUTES OF ELEMENTS ##############
# Only consider nodes flagged with `RESERVED_XML_TYPE`
exp  = '//*[@%s]'
exp %= (RESERVED_XML_TYPE)
matches = tree.xpath(exp)

# Determine if nodes contain an attribute disallowed according to util.table.ATTRIBS
disallowed = []
for m in matches:
    mAttribs     = dict(m.attrib)
    mXmlType     = mAttribs[RESERVED_XML_TYPE]
    mAttribNames = mAttribs
    mAttribNames.pop(RESERVED_XML_TYPE, None)

    for mAttribName in mAttribNames:
        if not mAttribName in helpers.getAttributes(util.table.ATTRIBS, mXmlType):
            disallowed.append((mAttribName, m))

# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib   = d[0]
    disallowedNode     = d[1]
    disallowedNodeType = d[1].attrib[RESERVED_XML_TYPE]

    msg           = 'Attribute `%s` disallowed here' % disallowedAttrib
    affectedNodes = [disallowedNode]
    expectedItems = helpers.getAttributes(util.table.ATTRIBS, disallowedNodeType)
    helpers.eMsg(msg, affectedNodes, expectedItems)

############## COARSE-GRAINED VALIDATION OF VALUES OF ATTRIBUTES ###############
# Only consider nodes flagged with `RESERVED_XML_TYPE`
exp = '//*[@%s]' % (RESERVED_XML_TYPE)
matches = tree.xpath(exp)

# Determine if attributes contain allowed values according to util.table.ATTRIB_VALS
disallowed = []
for m in matches:
    disallowed.extend(helpers.disallowedAttribVals(tree, m, util.table.ATTRIB_VALS))

# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib    = d[0]
    disallowedAttribVal = d[1]
    disallowedNode      = d[2]

    ATTRIB_VALS = util.table.ATTRIB_VALS
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
# Only consider nodes flagged with `RESERVED_XML_TYPE`
disallowed = []
for c in util.table.CARDINALITIES:
    parentTypeName        = c[0]
    directChildContraints = c[1]
    descendantContraints  = c[2]

    exp = '//*[@%s="%s"]' % (RESERVED_XML_TYPE, parentTypeName)
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

################ VALIDATE CARDINALITIES FOR COMPOSITE ELEMENTS #################

util.schema.normaliseSchema(tree)

# Check cardinality contraints
el  = TYPE_GUI_DATA
mod = TYPE_MODULE
t   = TYPE_TAB
tg  = TYPE_TAB_GROUP

helpers.checkTagCardinalityConstraints(tree, TYPE_MODULE,    TYPE_TAB_GROUP)
helpers.checkTagCardinalityConstraints(tree, TYPE_TAB_GROUP, TYPE_TAB)
helpers.checkTagCardinalityConstraints(tree, TYPE_TAB,       TYPE_GUI_DATA)

helpers.checkDataSchemaConstraints(tree)

################################# MISC ERRORS ##################################

################################################################################

msg  = 'Binding in b attribute ignored; use of "autonum" flag forces decimal '
msg += 'binding'

# Select all autonum-flagged elements which also have their b attributes set
exp  = '//*[@b]'
cond = lambda e: util.schema.isFlagged(e, FLAG_AUTONUM);
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
exp  = '//*[@c != "required"]'
cond = lambda e: util.schema.isFlagged(e, FLAG_AUTONUM)
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
exp  = '//*[@c != "required"]'
cond = lambda e: util.schema.isFlagged(e, FLAG_NOTNULL)
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
exp  = '//*[@%s="%s"]' % (RESERVED_XML_TYPE, TYPE_GUI_DATA)
# Select all user-flagged elements from those
cond1 = lambda e: util.schema.isFlagged(e, FLAG_USER)
# Select all elements whose type is not dropdown nor list
cond2 = lambda e: util.schema.getUiType(e) not in (UI_TYPE_DROPDOWN, UI_TYPE_LIST)
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
exp  = '//*[@%s="%s"]' % (RESERVED_XML_TYPE, TYPE_GUI_DATA)
# Select all user-flagged elements from those
cond = lambda e: util.schema.isFlagged(e, FLAG_USER)
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
exp  = '//*[@%s="%s"]' % (RESERVED_XML_TYPE, TYPE_AUTONUM)
cond = lambda e: util.schema.isFlagged(e, FLAG_AUTONUM)
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
cond = lambda e: util.schema.isFlagged(e, [FLAG_NODATA, FLAG_NOUI])
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Tab groups not flagged with "nodata" require at least one identifier'

exp  = '//*[@%s="%s"]' % (RESERVED_XML_TYPE, TYPE_TAB_GROUP)
cond = lambda e: not util.schema.isFlagged(e, FLAG_NODATA) and \
                 not util.schema.hasElementFlaggedWithId(e)
matches = tree.xpath(exp)
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements whose t attribute is equivalent to one of the following '
msg += 'may contain <opts> tags: %s' % ', '.join(util.table.MENU_TS)

# Get <opts> tags which are the children of GUI/data elements
exp  = '//*[@%s="%s"]/opts' % (RESERVED_XML_TYPE, TYPE_GUI_DATA)
# Filter out <opts> tags whose element's t attrib *is* in DESC_TS
cond = lambda e: not util.schema.getUiType(e.getparent()) in util.table.MENU_TS
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
cond = lambda e: util.schema.isFlagged(e, FLAG_NODATA)
matches = tree.xpath(exp)
matches = filter(cond, matches)
# Effectively, filter out <desc> tags which were already complained about
matches = util.schema.filterUnannotated(matches)

affectedNodes = matches
helpers.eMsg(msg, affectedNodes)

################################################################################

msg  = 'Only elements whose t attribute is equivalent to one of the following '
msg += 'may contain <desc> tags: %s' % ', '.join(util.table.DESC_TS)

# Get <desc> tags which are the children of GUI/data elements
exp  = '//*[@%s="%s"]/desc' % (RESERVED_XML_TYPE, TYPE_GUI_DATA)
# Filter out <desc> tags whose element's t attrib *is* in DESC_TS
cond = lambda e: not util.schema.getUiType(e.getparent()) in util.table.DESC_TS
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
cond = lambda e: bool(util.data.getRelName(e))
matches = filter(cond, matches)
matches = util.schema.filterUnannotated(matches)
# ...And conflict with entries in the <rels> tags
exp = '//rels/*[@name="%s"]'
cond = lambda e: len(tree.xpath(exp % util.data.getRelName(e))) > 0
matches = filter(cond, matches)

for m in matches:
    # Find the entries in <rels> that `m` conflicts with
    relName = util.data.getRelName(m)
    exp = '//rels/*[@name="%s"]' % relName
    conflictingRels = tree.xpath(exp)

    # Notify the user of the conflict
    msg_ = msg % relName
    affectedNodes = conflictingRels + [m]
    helpers.eMsg(msg_, affectedNodes)

################################ MISC WARNINGS #################################

################################################################################

msg  = 'Module is missing a login menu'

cond = lambda e: util.schema.isFlagged(e, FLAG_USER)
matches = util.schema.getGuiDataElements(tree, cond)
matches = util.schema.filterUnannotated(matches)

# Tell the user about the error(s)
if len(matches) == 0:
    helpers.wMsg(msg)

################################################################################

msg  = 'Text is superfluous here as it can be inferred from its element\'s tag'

matches = util.schema.getTabGroups      (tree) + \
          util.schema.getTabs           (tree) + \
          util.schema.getGuiDataElements(tree)
# Retain only elements with superfluous text
cond = lambda e: util.arch16n.getLabelFromText(e) == util.arch16n.getLabelFromTag(e)
matches = filter(cond, matches)
# Pretty up the output a little
matches.sort(key=lambda e: e.sourceline)

helpers.wMsg(msg, matches)

################################################################################

msg  = 'Elements having certain types (i.e. %s) may render incorrectly unless '
msg += 'their parent tab is flagged with `f="noscroll"`'
msg %= ', '.join(NO_SCROLL_UI_TYPES)

cond = lambda e: util.schema.getUiType(e) in NO_SCROLL_UI_TYPES and \
        not util.schema.isFlagged(util.schema.getParentTab(e), FLAG_NOSCROLL)
matches = util.xml.getAll(tree, cond)
helpers.wMsg(msg, matches)

################################################################################

msg  = 'The `ll` attribute might be more appropriate than `l` for one or more '
msg += 'elements'

# By the end of this, `linkerNodes` should contain the elements that:
#   1) Share a tab group with an element that has f="user"; and
#   2) Link to a tab group other than that mentioned in 1).
cond = lambda e: e != None
userNodes = util.xml.getAll(tree, lambda e: util.schema.isFlagged(e, FLAG_USER))
parentTabGroups = [util.schema.getParentTabGroup(n) for n in userNodes]
parentTabGroups = filter(cond, parentTabGroups)

cond = lambda n: util.schema.getParentTabGroup(
                util.schema.getLinkedNode(n), True
        ) not in (None, util.schema.getParentTabGroup(n))
linkerNodes = [util.xml.getAll(n, util.schema.hasLink) for n in parentTabGroups]
linkerNodes = itertools.chain.from_iterable(linkerNodes) # Flatten
linkerNodes = filter(lambda n: not util.xml.hasAttrib(n, ATTRIB_LL), linkerNodes)
linkerNodes = filter(cond, linkerNodes)

helpers.wMsg(msg, linkerNodes)

################################################################################

msg  = 'The `makeVocab` function is being called in <logic>.  Consider using'
msg += ' the `vp` attribute instead.  If this cannot be done, ensure that '
msg += 'handwritten calls to `makeVocab` occur upon module load by using '
msg += '`addOnEvent("module", "load", ...)`'

logicText = util.schema.getLogic(tree)
if 'makeVocab' in logicText:
    helpers.wMsg(msg)

################################################################################

msg  = 'The `createdat` column is being used in <logic>.  It might be more '
msg += 'appropriate to write `parentchild.createdat` instead'

logicText = util.schema.getLogic(tree)
if ' createdat' in logicText:
    helpers.wMsg(msg)

################################################################################

msg  = 'Only tabs may be flagged with `noscroll`'

cond = lambda n: not util.schema.isTab(n) and \
        util.schema.isFlagged(n, FLAG_NOSCROLL)
matches = util.xml.getAll(tree, cond)
helpers.eMsg(msg, matches)

################################################################################

msg  = 'Only inputs may have the `b` attribute'

cond = lambda n: util.xml.hasAttrib(n, ATTRIB_B) and \
             not util.schema.getUiType(n) == UI_TYPE_INPUT
matches = util.xml.getAll(tree, cond)
helpers.eMsg(msg, matches)

################################################################################

msg  = 'GUI/Data elements referenced in <fmt> elements do not exist in their '
msg += 'parent tab groups'

matches = util.schema.INVALID_ATTRIB_NAMES_IN_FMT
if matches: attribs, tabGroups, nodes = zip(*matches)
else:       attribs, tabGroups, nodes = [], [], []

locations = [
        'Referenced element "%s" in tab group "%s"' % (a, t) \
        for a, t in zip(attribs, tabGroups)
]

helpers.eMsg(msg, nodes, moreLocations=locations)

################################################################################

msg  = 'Elements whose `%s` attribute is `%s` are not generated such that they '
msg += 'can be used to collect data.  Consider using a different kind of menu '
msg += '(e.g. %s) or flagging the affected element(s) with `%s` (e.g `%s="%s"`)'

menuTypesNoList = list(MENU_UI_TYPES)
menuTypesNoList.remove(UI_TYPE_LIST)
menuTypesNoList = ', '.join(menuTypesNoList)

msg %= (
        ATTRIB_T,
        UI_TYPE_LIST,
        menuTypesNoList,
        FLAG_NODATA,
        ATTRIB_F,
        FLAG_NODATA,
)

cond1 = lambda e: util.schema.getUiType(e) == UI_TYPE_LIST
cond2 = lambda e: util.data.formsProp(e)
cond  = lambda e: cond1(e) and cond2(e)
matches = util.xml.getAll(tree, cond)

helpers.wMsg(msg, matches)

################################################################################

print 'Validation completed with %s error(s) and %s warning(s).' % (
        validator.NUM_E,
        validator.NUM_W
)
