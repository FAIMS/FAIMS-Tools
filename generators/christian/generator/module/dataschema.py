#!/usr/bin/env python2
from   lxml import etree
import sys
import util.arch16n
from   util.consts import *
import util.data
import util.schema
import util.xml
import re

def getDefaultDollarFmtStr(node):
    if util.data.hasVocabType  (node): return '$1'
    if util.data.hasMeasureType(node): return '$2'
    return '$0'

def convertDefaultDollar(dataElement, fmtStr):
    return fmtStr.replace('$0', getDefaultDollarFmtStr(dataElement))

def getDataElement(node):
    if util.data.formsProp(node):    return getProp(node)
    if util.data.formsArchEnt(node): return getArchEnt(node)
    return None

def getRels(node):
    # This function returns the children of <rels> elements (plus a few other
    # elements). `relsNodes` stores the found <rels> elements (not their
    # children!)
    relsNodes = util.xml.getAll(node, lambda n: n.tag == TAG_RELS)
    relsNode = []
    if len(relsNodes) > 0:
        relsNode = relsNodes[0]
    for n in relsNode:
        n.tail = None

    rels  = []
    rels += relsNode
    rels += getGennedRels(node)

    return rels

def getGennedRels(node):
    gennedRels = []

    matches = util.xml.getAll(node, lambda n: util.xml.hasAttrib(n, ATTRIB_LC))
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

        gennedRels.append(r)

    return gennedRels

def getArchEnts(node):
    return [getArchEnt(m) for m in util.data.getArchEnts(node)]

def getArchEnt(node):
    a                = etree.Element('ArchaeologicalElement')
    a.attrib['name'] = util.data.getArchEntName(node)

    d      = etree.Element('description')
    d.text = getDescriptionText(node)

    a.append(d)
    a.extend(getProps(node))

    return a

def getProps(node):
    # Get data elements
    return [getProp(m) for m in util.data.getProps(node)]

def getProp(node):
    # make prop
    prp                = etree.Element('property')
    prp.attrib['name'] = util.data.getAttribName(node)
    prp.attrib['type'] = util.data.getAttribType(node, True)
    if util.schema.isFlagged(node, FLAG_ID):
        prp.attrib['isIdentifier'] = 'true'
    if util.data.hasFileType(node):
        prp.attrib['file']         = 'true'
    if util.data.hasFileType(node) and not util.schema.isFlagged(node, [FLAG_NOTHUMB, FLAG_NOTHUMBNAIL]):
        prp.attrib['thumbnail']    = 'true'

    if ATTRIB_SP in node.attrib:
        prp.attrib['SemanticMapPredicate'] = node.attrib[ATTRIB_SP]

    if ATTRIB_SU in node.attrib:
        prp.attrib['SemanticMapURL'] = node.attrib[ATTRIB_SU]

    # make description
    dsc      = etree.Element('description')
    dsc.text = getDescriptionText(node)

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
    matches = node.xpath(exp)
    fmtText = ''
    if matches:
        fmtText = matches[0].text
        fmtText = convertDefaultDollar(node, fmtText)
    if not fmtText:
        fmtText = fmtDefault

    fmt      = etree.Element('formatString')
    fmt.text = fmtText

    # (2) append character string
    exp     = './str/app'
    matches = node.xpath(exp)
    appText = ''
    if matches:
        appText = matches[0].text
    if not appText:
        appText = appDefault

    app      = etree.Element('appendCharacterString')
    app.text = appText

    # (3) lookup nodes
    lup = makeLookup(node)

    # (4) pos nodes
    exp     = './str/pos'
    matches = node.xpath(exp)
    posText = ''
    if matches:
        posText = matches[0].text

    pos      = etree.Element(TAG_POS)
    pos.text = posText

    # append prp's (property's) children to it
    util.xml.appendNotNone(dsc, prp)
    util.xml.appendNotNone(fmt, prp)
    util.xml.appendNotNone(app, prp)
    util.xml.appendNotNone(lup, prp)
    util.xml.appendNotNone(pos, prp)

    return prp

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

    if ATTRIB_P in source.attrib:
        term.attrib['pictureURL'] = 'files/data/' + source.attrib['p']

    if ATTRIB_SP in source.attrib:
        term.attrib['SemanticMapPredicate'] = source.attrib[ATTRIB_SP]

    if ATTRIB_SU in source.attrib:
        term.attrib['SemanticMapURL'] = source.attrib[ATTRIB_SU]

    dsc      = etree.Element('description')
    dsc.text = getDescText(source)
    if dsc.text == '': # Workaround for a bug in FAIMS where infoboxes can
        dsc.text = ' ' # contain 'null'

    term.text = util.arch16n.getArch16nKey(source) + '\n'

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

def getDataSchema(node):
    children  = getRels(node)
    children += getArchEnts(node)

    dataSchema = etree.Element('dataSchema')
    dataSchema.extend(children)

    sortPropsByPos(dataSchema)
    delPosNodes   (dataSchema)

    return dataSchema

if __name__ == '__main__':
    # PARSE XML
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    #GENERATE AND OUTPUT DATA SCHEMA
    dataSchema = getDataSchema(tree)
    print etree.tostring(
            dataSchema,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8'
    ),
