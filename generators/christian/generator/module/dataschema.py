#!/usr/bin/env python2
from   lxml import etree
import sys
import util.arch16n
import util.consts
import util.data
import util.schema
import util.xml

def addRels(source, target):
    copyRels(source, target)
    genRels (source, target)

def copyRels(source, target):
    exp     = '//rels/*'
    matches = source.xpath(exp)
    for m in matches:
        target.append(m)

def genRels(source, target):
    exp     = '//*[@lc]'
    matches = source.xpath(exp)
    for m in matches:
        r                = etree.Element('RelationshipElement')
        r.attrib['name'] = util.data.getRelName(m)
        r.attrib['type'] = 'hierarchical'

        d       = etree.Element('description')
        d.text  = 'A 1-to-n relationship between the parent and its children, '
        d.text += 'respectively.'

        p       = etree.Element('parent')
        p.text  = 'Parent Of'

        c       = etree.Element('child')
        c.text  = 'Child Of'

        r.append(d)
        r.append(p)
        r.append(c)

        target.append(r)

def addEnts(source, target):
    exp     = '//*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'tab group')
    cond    = lambda e: not util.schema.isFlagged(e, 'nodata')
    matches = source.xpath(exp)
    matches = filter(cond, matches)

    for m in matches:
        addEnt(m, target)

def addEnt(entNode, target):
    a                = etree.Element('ArchaeologicalElement')
    a.attrib['name'] = util.data.getArchEntName(entNode)

    d      = etree.Element('description')
    d.text = getDescriptionText(entNode)

    a.append(d)
    target.append(a)

def addProps(source, target):
    # Get data elements
    exp     = '//*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'GUI/data element')
    matches = source.xpath(exp)
    matches = filter(util.data.isDataElement, matches)

    for m in matches:
        addProp(m, target)
    sortPropsByPos(target)
    delPosNodes   (target)

def addProp(dataElement, target):
    # make prop
    prp                = etree.Element('property')
    prp.attrib['name'] = util.data.getAttribName(dataElement)
    prp.attrib['type'] = util.data.getAttribType(dataElement)
    if util.schema.isFlagged(dataElement, 'id'):
        prp.attrib['isIdentifier'] = 'true'
    if util.data.hasFileType(dataElement):
        prp.attrib['file']         = 'true'
    # TODO:
    #if util.data.hasFileType(dataElement) and not util.schema.isFlagged(dataElement):
        #prp.attrib['thumbnail']    = 'true'

    # make description
    dsc      = etree.Element('description')
    dsc.text = getDescriptionText(dataElement)

    # make (1) format and (2) append character strings.
    # (3) make <lookup> nodes
    # (4) make <pos> nodes
    fmtDefault  = '{{if $1 then $1}}{{if and($1, $2) then " " }}'
    fmtDefault += '{{if $2 then $2}}{{if $3 then " ($3)"}}'
    fmtDefault += '{{if between($4,0,0.49) then "??"'
    fmtDefault += ' elsif lessThan($4,1) then "?" }}'
    appDefault  = ' - '

    # (1) format string
    exp     = './str/fmt'
    matches = dataElement.xpath(exp)
    fmtText = ''
    if matches:
        fmtText = matches[0].text
    if not fmtText:
        fmtText = fmtDefault

    fmt      = etree.Element('formatString')
    fmt.text = fmtText

    # (2) append character string
    exp     = './str/app'
    matches = dataElement.xpath(exp)
    appText = ''
    if matches:
        appText = matches[0].text
    if not appText:
        appText = appDefault

    app      = etree.Element('appendCharacterString')
    app.text = appText

    # (3) lookup nodes
    lup = makeLookup(dataElement)

    # (4) pos nodes
    exp     = './str/pos'
    matches = dataElement.xpath(exp)
    posText = ''
    if matches:
        posText = matches[0].text

    pos      = etree.Element('pos')
    pos.text = posText

    # find correct parent arch ent
    archName = util.schema.getParentTabGroup(dataElement)
    archName = archName.tag
    archName = archName.replace('_', ' ')

    exp     = './ArchaeologicalElement[@%s="%s"]' % ('name', archName)
    matches = target.xpath(exp)
    archEnt = matches[0]

    # append prp's (property's) children to it
    util.xml.appendNotNone(dsc, prp)
    util.xml.appendNotNone(fmt, prp)
    util.xml.appendNotNone(app, prp)
    util.xml.appendNotNone(lup, prp)
    util.xml.appendNotNone(pos, prp)
    # append prp to parent archent
    archEnt.append(prp)

def makeLookup(dataElement):
    exp     = './opts'
    matches = dataElement.xpath(exp)
    if not matches:
        return None

    lookup  = etree.Element('lookup')

    exp     = './opts/opt'
    matches = dataElement.xpath(exp)
    for m in matches:
        addTerm(m, lookup)

    return lookup

def getDescText(node):
    exp     = './desc'
    matches = node.xpath(exp)
    if matches:
        return matches[0].text
    else:
        return ''

# `source` is an <opt> element. `target` is a <lookup> or <term> element which
# an option (<opt>) should be added to as a child.
def addTerm(source, target):
    term = etree.Element('term')

    if 'p' in source.attrib:
        term.attrib['pictureURL'] = 'files/data/' + source.attrib['p']

    dsc      = etree.Element('description')
    dsc.text = getDescText(source)

    term.text = util.arch16n.getArch16nKey(source)
    term.text = '{%s}\n' % term.text

    term  .append(dsc)
    target.append(term)

    exp     = './opt'
    matches = source.xpath(exp)
    for m in matches:
        addTerm(m, term)

# Returns a key for sorted() such that <description> elements appear at the
# start of their parent <ArchaeologicalElement>, elements not having (text in)
# <pos> tags appear at the end of their parent <ArchaeologicalElement>, and all
# other elements are sorted in ascending order of the text in their <pos> tags.
# The text is interpreted as an integer.
def propKey(prop):
    startPos = - sys.maxint - 1  # sys.minint isn't defined, so we make our own
    endPos   =   sys.maxint

    # Effectively, leave <descriptions> at the start
    if prop.tag != 'property': return startPos

    exp     = './pos'
    matches = prop.xpath(exp)
    if not matches:            return endPos
    pos     = matches[0]
    key     = pos.text
    if not key:                return endPos
    else:                      return int(key)

def sortPropsByPos(dataSchema):
    exp      = './ArchaeologicalElement'
    archEnts = dataSchema.xpath(exp)
    for archEnt in archEnts:
        archEnt[:] = sorted(archEnt, key=propKey)

def delPosNodes(dataSchema):
    for pos in dataSchema.xpath('//pos'):
        pos.getparent().remove(pos)

def getDescriptionText(node):
    exp     = './desc'
    matches = node.xpath(exp)
    if   matches: return matches[0].text
    else        : return ''

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithXmlTypes(tree)
util.schema.expandCompositeElements(tree)
util.schema.annotateWithXmlTypes(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
dataSchema = etree.Element('dataSchema')
addRels (tree, dataSchema)
addEnts (tree, dataSchema)
addProps(tree, dataSchema)

print etree.tostring(
        dataSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
