#!/usr/bin/env python

from   lxml import etree
import consts
import helpers
import sys
import tables

def addRels(source, target):
    copyRels(source, target)
    genRels (source, target)

def copyRels(source, target):
    exp = '//rels/*'
    matches = source.xpath(exp)
    for m in matches:
        target.append(m)

def genRels(source, target):
    exp = '//*[@lc]'
    matches = source.xpath(exp)
    for m in matches:
        r                = etree.Element('RelationshipElement')
        r.attrib['name'] = helpers.getRelName(m)
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

def isDataElement(guiDataElement):
    if helpers.isFlagged(guiDataElement, 'nodata'):      return False
    if helpers.isFlagged(guiDataElement, 'user'):        return False
    if helpers.hasAttrib(guiDataElement, 'e'):           return False
    if helpers.hasAttrib(guiDataElement, 'ec'):          return False
    if helpers.guessType(guiDataElement) == 'button':    return False
    if helpers.guessType(guiDataElement) == 'gpsdiag':   return False
    if helpers.guessType(guiDataElement) == 'group':     return False
    if helpers.guessType(guiDataElement) == 'map':       return False
    if helpers.guessType(guiDataElement) == 'table':     return False
    if helpers.guessType(guiDataElement) == 'viewfiles': return False
    return True

def addEnts(source, target):
    exp     = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab group')
    cond    = lambda e: not helpers.isFlagged(e, 'nodata')
    matches = tree.xpath(exp)
    matches = filter(cond, matches)

    for m in matches:
        addEnt(m, target)

def addEnt(entNode, target):
    exp = './desc'
    matches = tree.xpath(exp)
    if    matches: descText = matches[0].text
    else:          descText = ''

    a                = etree.Element('ArchaeologicalElement')
    a.attrib['name'] = entNode.tag.replace('_', ' ')

    d      = etree.Element('description')
    d.text = descText

    a.append(d)
    target.append(a)


def addProps(source, target):
    # Get data elements
    exp     = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    matches = tree.xpath(exp)
    matches = filter(isDataElement, matches)

    for m in matches:
        addProp(m, target)
    sortPropsByFmtStr(target)

def addProp(dataElement, target):
    pass

def sortPropsByFmtStr(dataSchema):
    pass

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = helpers.parseXml(filenameModule)
helpers.normaliseAttributes(tree)
helpers.annotateWithTypes(tree)
helpers.expandCompositeElements(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
dataSchema = etree.Element("dataSchema")
addRels (tree, dataSchema)
addEnts (tree, dataSchema)
#addProps(tree, dataSchema)

print etree.tostring(
        dataSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
