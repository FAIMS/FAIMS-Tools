#!/usr/bin/env python2

from   lxml       import etree
from   lxml.etree import Element
import sys
from   util.consts import *
import util.data
import util.schema
import signal

signal.signal(signal.SIGINT, lambda a, b : sys.exit())

def getProperty(node):
    if     util.data.hasFileType(node):               return None
    if not util.data.getAttribName(node):             return None
    if not util.schema.isFlagged(node, FLAG_NOTNULL): return None

    property  = Element('property',  name=util.data.getAttribName(node))
    validator = Element('validator', type='blankchecker')
    param     = Element('param',     value=util.data.getAttribType(node),
                                     type='field'
    )

    property.append(validator)
    validator.append(param)

    return property

def getProperties(node):
    guiDataElements = util.schema.getGuiDataElements(node)

    properties = [getProperty(n) for n in guiDataElements]
    properties = filter(lambda x: x != None, properties)
    return properties

def getArchaeologicalElement(node):
    if not util.schema.hasElementFlaggedWith(node, FLAG_NOTNULL):
        return None
    if not util.data.getArchEntName(node):
        return None

    archaeologicalElement = Element(
            'ArchaeologicalElement',
            name=util.data.getArchEntName(node)
    )

    archaeologicalElement.extend(getProperties(node))
    return archaeologicalElement

def getArchaeologicalElements(node):
    tabGroups = util.schema.getTabGroups(node)

    archaeologicalElements = [getArchaeologicalElement(n) for n in tabGroups]
    archaeologicalElements = filter(lambda x: x != None, archaeologicalElements)
    return archaeologicalElements

def getValidationSchema(node):
    validationSchema = Element('ValidationSchema')
    validationSchema.extend(getArchaeologicalElements(node))
    return validationSchema

if __name__ == '__main__':
    # PARSE XML
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    # GENERATE AND OUTPUT VALIDATION SCHEMA
    validationSchema = getValidationSchema(tree)

    print etree.tostring(
            validationSchema,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8'
    ),
