#!/usr/bin/env python2
from   lxml import etree
import sys

def getModel(node):
    pass

def getBindings(node):
    pass

def getBody(node):
    pass

def getUiSchema(node):
    pass

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithTypes(tree)
util.schema.expandCompositeElements(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
uiSchema = getUiSchema(tree)

print etree.tostring(
        uiSchema
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
