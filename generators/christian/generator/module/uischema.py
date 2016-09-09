#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.ui
import util.xml
import util.consts

# TODO: <cols> need to be expanded into groups

# The namespaces used in the UI schema must be defined here to help us search
# through the uischema-template.xml using xpath.
NS = {'x': 'http://www.w3.org/2002/xforms'}

############################### MODEL GENERATION ###############################

def getModel(node):
    modelTabGroups = [getModelTabGroup(n) for n in node]
    modelTabGroups = filter(lambda x: x != None, modelTabGroups)

    model = etree.Element('MODEL_CONTAINER')
    model.extend(modelTabGroups)

    return model

def getModelTabGroup(node):
    isTabGroup = util.xml.getType(node) == util.consts.TYPE_TAB_GROUP

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
    isUi    = util.ui.isUiElement  (node)

    if node == None:             return None
    if node == []:               return None
    if not isUi and not isGroup: return None

    modelTabGrandChildren = [getModelTabChildren(n) for n in node]
    modelTabGrandChildren = filter(lambda x: x != None, modelTabGrandChildren)

    modelTabChildren = etree.Element(node.tag)
    modelTabChildren.extend(modelTabGrandChildren)

    return modelTabChildren

############################## BINDING GENERATION ##############################

def getBindings(node):
    bindings = etree.Element('BINDINGS_CONTAINER')
    bindings.extend([getBinding(n) for n in node.xpath('//*[@b]')])

    return bindings

def getBinding(node):
    type    = node.attrib['b']
    nodeset = '/faims/' + util.xml.getPathString(node)

    return etree.Element('bind', type=type, nodeset=nodeset)

############################### BODY GENERATION ################################

def getBody(node):
    bodyTabGroups = [getBodyTabGroup(n) for n in node]
    bodyTabGroups = filter(lambda x: x != None, bodyTabGroups)

    body = etree.Element('BODY_CONTAINER')
    body.extend(bodyTabGroups)

    return body

def getBodyTabGroup(node):
    return None

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
util.schema.annotateWithXmlTypes(tree)
util.schema.expandCompositeElements(tree)
util.schema.annotateWithXmlTypes(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
uiSchema = getUiSchema(tree)

#print etree.tostring(
        #tree,
        #pretty_print=True,
        #xml_declaration=True,
        #encoding='utf-8'
#)

print etree.tostring(
        uiSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
