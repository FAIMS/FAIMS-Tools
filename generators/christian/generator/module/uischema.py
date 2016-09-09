#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.ui
import util.xml

# The namespaces used in the UI schema must be defined here to help us search
# through the uischema-template.xml using xpath.
NS = {'x': 'http://www.w3.org/2002/xforms'}

############################### MODEL GENERATION ###############################

def getModel(node):
    modelTabGroups = [getModelTabGroup(n) for n in node]
    modelTabGroups = filter(lambda x: x != None, modelTabGroups)

    model = etree.Element('modelContainer')
    model.extend(modelTabGroups)

    return model

def getModelTabGroup(node):
    isTabGroup = util.schema.hasUserDefinedName(node)

    if not isTabGroup:
        return None

    modelTabs = [getModelTab(n) for n in node]
    modelTabs = filter(lambda x: x != None, modelTabs)

    modelTabGroup = etree.Element(node.tag)
    modelTabGroup.extend(modelTabs)

    return modelTabGroup

def getModelTab(node):
    isTab = util.schema.hasUserDefinedName(node)

    if not isTab:
        return None

    modelTabChildren = [getModelTabChildren(n) for n in node]
    modelTabChildren = filter(lambda x: x != None, modelTabChildren)

    modelTab = etree.Element(node.tag)
    modelTab.extend(modelTabChildren)

    return modelTab

def getModelTabChildren(node):
    isGroup = util.schema.guessType(node) == 'group'
    pass

############################## BINDING GENERATION ##############################

def getBindings(node):
    return etree.Element('Bindings')

############################### BODY GENERATION ################################

def getBody(node):
    return etree.Element('Body')

################################################################################

def getUiSchema(node):
    # Parse XML template
    filename = 'generator/module/uischema-template.xml'
    parser = etree.XMLParser(strip_cdata=False, remove_blank_text=True)
    try:
        tree = etree.parse(filename, parser)
    except etree.XMLSyntaxError as e:
        print e
        exit()
    uiSchema = tree.getroot()

    # Locate places in template which will be filled in
    anchorModel   = uiSchema.xpath('//x:MODEL_ANCHOR'  , namespaces=NS)[0]
    anchorBinding = uiSchema.xpath('//x:BINDING_ANCHOR', namespaces=NS)[0]
    anchorBody    = uiSchema.xpath('//x:BODY_ANCHOR'   , namespaces=NS)[0]

    # Generate XML to insert into template
    nodeModel   = getModel   (node)
    nodeBinding = getBindings(node)
    nodeBody    = getBody    (node)

    # Replace anchors with generated XML
    util.xml.replaceElement(anchorModel,   nodeModel  )
    util.xml.replaceElement(anchorBinding, nodeBinding)
    util.xml.replaceElement(anchorBody,    nodeBody   )

    return uiSchema

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithTypes(tree)
util.schema.expandCompositeElements(tree)
util.schema.annotateWithTypes(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
uiSchema = getUiSchema(tree)

print etree.tostring(
        tree,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)

print etree.tostring(
        uiSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)