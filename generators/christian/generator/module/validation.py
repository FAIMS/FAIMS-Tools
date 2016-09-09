#!/usr/bin/env python2

from   lxml import etree
import sys
import util.consts
import util.data
import util.schema

def addEnts(source, target):
    exp     = '//*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'tab group')
    cond1   = lambda e: not util.schema.isFlagged(e, 'nodata')
    cond2   = lambda e:     util.schema.isFlagged(e, 'notnull')
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
    exp     = '//*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'GUI/data element')
    matches = source.xpath(exp)
    matches = filter(util.data.isDataElement, matches)

    for m in matches:
        addProp(m, target)

def addProp(dataElement, target):
    prp                = etree.Element('property')
    prp.attrib['name'] = dataElement.tag.replace('_', ' ')

    vdr                = etree.Element('validator')
    vdr.attrib['type'] = 'blankchecker'

    prm                 = etree.Element('param')
    prm.attrib['value'] = util.data.getPropType(dataElement)
    prm.attrib['type']  = 'field'

    vdr   .append(prm)
    prp   .append(vdr)
    target.append(prp)

def getValidationSchema(node):
    validationSchema = etree.Element('ValidationSchema')

    exp     = './*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'tab group')
    cond1   = lambda e: not util.schema.isFlagged(e, 'nodata')
    cond2   = lambda e:     util.schema.isFlagged(e, 'notnull')
    matches = node.xpath(exp)
    matches = filter(cond1, matches)
    matches = filter(cond2, matches)

    archaeologicalElements = [getArchaeologicalElement(m) for m in matches]
    validationSchema.extend(archaeologicalElements)

    return validationSchema

def getArchaeologicalElement(node):
    archaeologicalElement = etree.Element('ArchaeologicalElement')

    exp     = './/*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, 'GUI/data element')
    cond    = lambda e: util.schema.isFlagged(e, 'notnull')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    matches = filter(util.data.isDataElement, matches)

    properties = [getProperty(m) for m in matches]
    archaeologicalElement.extend(properties)

    return archaeologicalElement

def getProperty(node):
    return etree.Element('property')

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
dataSchema = etree.Element('ValidationSchema')
addEnts (tree, dataSchema)
addProps(tree, dataSchema)

print etree.tostring(
        dataSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
