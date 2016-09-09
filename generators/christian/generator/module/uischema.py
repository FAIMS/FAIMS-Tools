#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.data
import util.arch16n
import util.ui
import util.xml
import util.consts

# TODO: <cols> need to be expanded into groups

# The namespaces used in the UI schema must be defined here to help us search
# through the uischema-template.xml using xpath.
NS = {'x': 'http://www.w3.org/2002/xforms'}

############################### MODEL GENERATION ###############################

def getModel(node):
    tabGroups = [getModelTabGroup(n) for n in node]
    tabGroups = filter(lambda x: x != None, tabGroups)

    model = etree.Element('MODEL_CONTAINER')
    model.extend(tabGroups)

    return model

def getModelTabGroup(node):
    if not util.schema.isTabGroup(node):
        return None

    tabs = [getModelTab(n) for n in node]
    tabs = filter(lambda x: x != None, tabs)

    tabGroup = etree.Element(node.tag)
    tabGroup.extend(tabs)

    return tabGroup

def getModelTab(node):
    if not util.schema.isTab(node):
        return None

    tabChildren = [getModelTabChildren(n) for n in node]
    tabChildren = filter(lambda x: x != None, tabChildren)

    tab = etree.Element(node.tag)
    tab.extend(tabChildren)

    return tab

def getModelTabChildren(node):
    isGroup = util.schema.guessType(node) == 'group'
    isUi    = util.ui.isUiElement  (node)

    if node == None:             return None
    if node == []:               return None
    if not isUi and not isGroup: return None

    tabGrandChildren = [getModelTabChildren(n) for n in node]
    tabGrandChildren = filter(lambda x: x != None, tabGrandChildren)

    tabChildren = etree.Element(node.tag)
    tabChildren.extend(tabGrandChildren)

    return tabChildren

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
    tabGroup = [getBodyTabGroup(n) for n in node]
    tabGroup = filter(lambda x: x != None, tabGroup)

    body = etree.Element('BODY_CONTAINER')
    body.extend(tabGroup)

    return body

def getBodyTabGroup(node):
    if not util.schema.isTabGroup(node):
        return None

    tabs = [getBodyTab(n) for n in node]
    tabs = filter(lambda x: x != None, tabs)

    # Create `tabGroup`
    tabGroup = etree.Element('group')

    # Add attributes
    archEntName = util.data.getArchEntName(node)
    if archEntName: tabGroup.attrib['faims_archent_type'] = archEntName

    tabGroup.attrib['ref'] = node.tag

    # Add children
    label      = etree.Element('label')
    label.text = util.arch16n.getArch16nKey(node, doAddCurlies=True)

    tabGroup.append(label)
    tabGroup.extend(tabs)

    return tabGroup

def getBodyTab(node):
    if not util.schema.isTab(node):
        return None

    tabChildren = [getBodyTabChildren(n) for n in node]
    tabChildren = filter(lambda x: x != None, tabChildren)

    bodyTab = etree.Element('group', ref=node.tag)
    bodyTab.extend(tabChildren)

    return bodyTab

def getBodyTabChildren(node):
    isGroup = util.schema.guessType(node) == 'group'
    isUi    = util.ui.isUiElement  (node)

    if node == None:             return None
    if node == []:               return None
    if not isUi and not isGroup: return None

    bodyTabGrandChildren = [getBodyTabChildren(n) for n in node]
    bodyTabGrandChildren = filter(lambda x: x != None, bodyTabGrandChildren)

    bodyTabChildren = etree.Element(node.tag)
    bodyTabChildren.extend(bodyTabGrandChildren)

    return bodyTabChildren

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
