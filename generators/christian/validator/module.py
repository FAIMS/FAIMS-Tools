import helpers
import sys
from lxml import etree
import tables
import consts

################################################################################
#                                     MAIN                                     #
################################################################################

filenameModule = sys.argv[1]

################################## PARSE XML ###################################
print 'Parsing XML...'
parser = etree.XMLParser(strip_cdata=False)
try:
    tree = etree.parse(filenameModule, parser)
except etree.XMLSyntaxError as e:
    print e
    exit()
tree = tree.getroot()
helpers.normaliseAttributes(tree)
print 'Done!'
print

############################### VALIDATE SCHEMA ################################
print 'Validating schema...'
countWar = 0
countErr = 0

ok = True
# Flag nodes with their TYPEs
for t in tables.TYPES:
    parentType = t[0]
    pattern    = t[1]
    matchType  = t[2]

    if   pattern == '/':
        matches = tree.xpath('/*')
        helpers.flagAll(matches, consts.RESERVED_XML_TYPE, matchType)
    elif pattern == '/[^a-z]/':
        matches = tree.xpath(
                '//*[@%s="%s"]/*' %
                (consts.RESERVED_XML_TYPE, parentType)
        )
        matches = helpers.getNonLower(matches)
        helpers.flagAll(matches, consts.RESERVED_XML_TYPE, matchType)
    else:
        matches = tree.xpath(
                '//*[@%s="%s"]/%s' %
                (consts.RESERVED_XML_TYPE, parentType, pattern)
        )
        helpers.flagAll(matches, consts.RESERVED_XML_TYPE, matchType)
matches = tree.xpath(
        '//*[@%s="%s"]/*' %
        (consts.RESERVED_XML_TYPE, '<cols>')
)

# Nodes which didn't end up getting flagged aren't allowed
disallowed = tree.xpath(
        '//*[@%s]/*[not(@%s)]' %
        (consts.RESERVED_XML_TYPE, consts.RESERVED_XML_TYPE)
)
# Tell the user about the error(s)
for d in disallowed:
    helpers.eMsg(
            'Element `%s` disallowed here' % d.tag,
            [d],
            getExpectedTypes(TYPES, d, None)
    )
    countErr += 1; ok &= False




# Only consider nodes flagged with `consts.RESERVED_XML_TYPE`
matches = tree.xpath(
        '//*[@%s]' %
        (consts.RESERVED_XML_TYPE)
)
# Determine if nodes contain an attibute not allowed according to tables.ATTRIBS
disallowed = []
for m in matches:
    mAttribs     = dict(m.attrib)
    mXmlType     = mAttribs[consts.RESERVED_XML_TYPE]
    mAttribs.pop(consts.RESERVED_XML_TYPE, None)
    mAttribNames = mAttribs

    for mAttribName in mAttribNames:
        if not mAttribName in helpers.getAttributes(tables.ATTRIBS, mXmlType):
            disallowed.append((mAttribName, m))
# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib = d[0]
    disallowedNode   = d[1]
    helpers.eMsg(
            'Attribute `%s` disallowed here' % disallowedAttrib,
            [disallowedNode],
            helpers.getAttributes(tables.ATTRIBS, disallowedNode.attrib[consts.RESERVED_XML_TYPE])
    )
    countErr += 1; ok &= False




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

    allowedOneOf  = helpers.getAttributes(tables.ATTRIB_VALS, disallowedAttrib, 1)
    allowedManyOf = helpers.getAttributes(tables.ATTRIB_VALS, disallowedAttrib, 2)
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

    helpers.eMsg(
            msg % (disallowedAttribVal, disallowedAttrib),
            [disallowedNode],
            allowed
    )
    countErr += 1; ok &= False





# Only consider nodes flagged with `consts.RESERVED_XML_TYPE`
disallowed = []
for c in tables.CARDINALITIES:
    parentTypeName        = c[0]
    directChildContraints = c[1]
    descendantContraints  = c[2]

    matches = tree.xpath(
            '//*[@%s="%s"]' %
            (consts.RESERVED_XML_TYPE, parentTypeName)
    )

    for m in matches:
        if not helpers.satisfiesTypeCardinalityConstraint(m,  directChildContraints, 'direct'):
            disallowed.append((m, parentTypeName, directChildContraints, 'direct'))
        if not helpers.satisfiesTypeCardinalityConstraint(m,  descendantContraints, 'descendant'):
            disallowed.append((m, parentTypeName, descendantContraints, 'descendant'))

for d in disallowed:
    node                = d[0]
    name                = node.tag
    typeParent          = d[1]
    min, typeChild, max = d[2]
    childDirectness     = d[3]

    if   min == None:
        nounPhrase = descChildNounPhrase(childDirectness, max)
        msg = 'Element `%s` of type %s requires at most %s %s of type %s' % \
        (name, typeParent,      max, nounPhrase, typeChild)
    elif max == None:
        nounPhrase = descChildNounPhrase(childDirectness, min)
        msg = 'Element `%s` of type %s requires at least %s %s of type %s' % \
        (name, typeParent, min,      nounPhrase, typeChild)
    else:
        pluralNumber = 2
        nounPhrase = descChildNounPhrase(childDirectness, pluralNumber)
        msg  = 'Element `%s` of type %s requires between %s and %s %s '
        msg += '(inclusive) of type %s'
        msg % \
        (name, typeParent, min, max, nounPhrase, typeChild)
    helpers.eMsg(
            msg,
            [node]
    )
    countErr += 1; ok &= False

matches = tree.xpath(
        '//*[@%s="%s" and not(@t)]' %
        (consts.RESERVED_XML_TYPE, 'GUI/data element')
)
for m in matches:
    m.attrib['t'] = helpers.guessType(m)
    helpers.wMsg(
            'No value for the attribute t of the element `%s` is present.  Assuming a value of `%s`' %
            (m.tag, m.attrib['t']),
            [m]
    )
    countWar += 1; ok &= True



# Transform XML such that cardinalities of UI and data schema elements
# represented by "composite" XML elements are preserved.  For "composite" XML
# elements, this makes some checks easier to perform.

replacementsByTAttrib = {
        'audio'  : '<%s t="dropdown"/><Button_%s t="button"/>',
        'camera' : '<%s t="dropdown"/><Button_%s t="button"/>',
        'file'   : '<%s t="dropdown"/><Button_%s t="button"/>',
        'video'  : '<%s t="dropdown"/><Button_%s t="button"/>',
}
replacementsByTag = {
        'gps'       : '<Colgroup_GPS t="group"/>              \
                       <Latitude     t="input" f="readonly"/> \
                       <Longitude    t="input" f="readonly"/> \
                       <Northing     t="input" f="readonly"/> \
                       <Easting      t="input" f="readonly"/>',
        'search'    : '<Search f="readonly">           \
                         <cols>                        \
                           <Search_Term t="input"/>    \
                           <Search_Button t="button"/> \
                         </cols>                       \
                         <Entity_Types t="input"/>     \
                         <Entity_List t="list"/>       \
                       </Search>',
        'timestamp' : '<Timestamp t="input" f="readonly nodata"/>'
}
for k, v in replacementsByTAttrib.iteritems():
    # Valid XML has only one root element
    replacementsByTAttrib[k] = '<root>%s</root>' % v
for k, v in replacementsByTag.iteritems():
    replacementsByTag[k] = '<root>%s</root>' % v

for attrib, replacement in replacementsByTAttrib.iteritems():
    matches = tree.xpath(
            '//*[@%s and @t="%s"]' %
            (consts.RESERVED_XML_TYPE, attrib)
    )
    for m in matches:
        t = m.tag
        n = m.sourceline

        replacement.replace('%s', t)
        replacements = etree.fromstring(replacements)
        helpers.setSourceline(replacements, n)
        replaceElement(m, replacements)

for tag, replacements in replacementsByTag.iteritems():
    matches = tree.xpath(
            '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
    )
    for m in matches:
        n = m.sourceline

        replacements = etree.fromstring(replacements)
        helpers.setSourceline(replacements, n)
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
