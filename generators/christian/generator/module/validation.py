#!/usr/bin/env python2

from   lxml import etree
import helpers
import sys
import consts

def addEnts(source, target):
    exp     = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab group')
    cond1   = lambda e: not helpers.isFlagged(e, 'nodata')
    cond2   = lambda e: helpers.hasElementFlaggedWith(e, 'notnull')
    matches = source.xpath(exp)
    matches = filter(cond1, matches)
    matches = filter(cond2, matches)

    for m in matches:
        addEnt(m, target)

def addEnt(entNode, target):
    a                = etree.Element('ArchaeologicalElement')
    a.attrib['name'] = entNode.tag.replace('_', ' ')

    target.append(a)

def addProps(source, target):
    # Get data elements
    exp     = '//*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    matches = source.xpath(exp)
    matches = filter(helpers.isDataElement, matches)

    for m in matches:
        addProp(m, target)

def addProp(dataElement, target):
    prp                = etree.Element('property')
    prp.attrib['name'] = dataElement.tag.replace('_', ' ')

    vdr                = etree.Element('validator')
    vdr.attrib['type'] = 'blankchecker'

    prm                 = etree.Element('param')
    prm.attrib['value'] = helpers.getPropType(dataElement)
    prm.attrib['type']  = 'field'

    vdr   .append(prm)
    prp   .append(vdr)
    target.append(prp)

def getValidationSchema(node):
    validationSchema = etree.Element('ValidationSchema')

    exp     = './*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'tab group')
    cond1   = lambda e: not helpers.isFlagged(e, 'nodata')
    cond2   = lambda e: helpers.hasElementFlaggedWith(e, 'notnull')
    matches = node.xpath(exp)
    matches = filter(cond1, matches)
    matches = filter(cond2, matches)

    archaeologicalElements = [getArchaeologicalElement(m) for m in matches]
    validationSchema.extend(archaeologicalElements)

    return validationSchema

def getArchaeologicalElement(node):
    archaeologicalElement = etree.Element('ArchaeologicalElement')

    exp     = './/*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, 'GUI/data element')
    cond    = lambda e: helpers.isFlagged(e, 'notnull')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    matches = filter(helpers.isDataElement, matches)

    properties = [getProperty(m) for m in matches]
    archaeologicalElement.extend(properties)

    return archaeologicalElement

def getProperty(node):
    return etree.Element('property')

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
dataSchema = etree.Element('ValidationSchema')
addEnts (tree, dataSchema)
addProps(tree, dataSchema)

print etree.tostring(
        dataSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
