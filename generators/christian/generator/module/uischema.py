#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.ui
import util.xml

# The namespaces uses in the UI schema must be defined here to help us search
# through the uischema-template.xml using xpath.
NS = {'x': 'http://www.w3.org/2002/xforms'}

############################### MODEL GENERATION ###############################

def getModel(node):
    tabGroups      = util.ui.getUiNodes(node, 'tab group')
    modelTabGroups = [getModelTabGroup(n) for n in tabGroups]

    modelContainer = etree.Element('modelContainer')
    for tg in modelTabGroups:
        modelContainer.append(tg)

    return modelContainer

def getModelTabGroup(node):
    tabs      = util.ui.getUiNodes(node, 'tab')
    modelTabs = [getModelTab(n) for n in tabs]

    modelTabGroup = etree.Element(node.tag)
    for t in modelTabs:
        modelTabGroup.append(t)

    return modelTabGroup

def getModelTab(node):
    return etree.Element(node.tag)

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

