#!/usr/bin/env python2
from   lxml       import etree
from   lxml.etree import Element, SubElement
import sys
import util.schema
import util.data
import util.arch16n
import util.ui
import util.xml
import util.consts

# The namespaces used in the UI schema must be defined here to help us search
# through the uischema-template.xml using xpath.
NS = {'x': 'http://www.w3.org/2002/xforms'}

CONTAINER = 'CONTAINER'

############################### MODEL GENERATION ###############################
def getModel(node):
    body = getBody(node)
    return getModelFromBody(body)

def getModelFromBody(node):
    # Make a `modelNode`
    modelNode = None
    if   'ref' in node.attrib:  modelNode = Element(node.attrib['ref'])
    elif node.tag == CONTAINER: modelNode = Element(CONTAINER)

    # Add children to the `modelNode`
    if modelNode is not None:
        modelChildNodes = [getModelFromBody(n) for n in node]
        modelChildNodes = filter(lambda x: x != None, modelChildNodes)
        modelNode.extend(modelChildNodes)

    return modelNode

############################## BINDING GENERATION ##############################
def getBindings(node):
    bindings = Element(CONTAINER)
    bindings.extend([getBinding(n) for n in node.xpath('//*[@b]')])

    return bindings

def getBinding(node):
    type    = node.attrib['b']
    nodeset = '/faims/' + util.xml.getPathString(node)

    return Element('bind', type=type, nodeset=nodeset)

############################### BODY GENERATION ################################
def getBody(node):
    tabGroup = [getBodyTabGroup(n) for n in node]
    tabGroup = filter(lambda x: x != None, tabGroup)

    body = Element(CONTAINER)
    body.extend(tabGroup)

    return body

def getBodyTabGroup(node):
    if not util.schema.isTabGroup(node):
        return None

    # Create `tabGroup`
    tabGroup = getBodyLabelled(node, 'group')

    # Add faims_archent_type
    archEntName = util.data.getArchEntName(node)
    if archEntName: tabGroup.attrib['faims_archent_type'] = archEntName

    # Add child elements (`tabs`)
    tabs = [getBodyTab(n) for n in node]
    tabs = filter(lambda x: x != None, tabs)
    tabGroup.extend(tabs)

    return tabGroup

def getBodyTab(node):
    if not util.schema.isTab(node):
        return None

    # Create `tab`
    tab = getBodyLabelled(node, 'group')

    # Add child elements (GUI elements, etc)
    tabChildren = [getBodyTabChildren(n) for n in node]
    tabChildren = filter(lambda x: x != None, tabChildren)
    util.xml.extendFlatly(tab, tabChildren)
    #tab.extend(tabChildren)

    return tab

def getBodyTabChildren(node):
    type    = util.schema.guessType(node)
    hasType = bool(type)

    if node == None: return None
    if node == []:   return None
    if not hasType:  return None

    bodyTabGrandChildren = [getBodyTabChildren(n) for n in node]
    bodyTabGrandChildren = filter(lambda x: x != None, bodyTabGrandChildren)

    if type == util.consts.UI_TYPE_AUDIO:     return getBodyAudio    (node)
    if type == util.consts.UI_TYPE_BUTTON:    return getBodyButton   (node)
    if type == util.consts.UI_TYPE_CAMERA:    return getBodyCamera   (node)
    if type == util.consts.UI_TYPE_CHECKBOX:  return getBodyCheckbox (node)
    if type == util.consts.UI_TYPE_DROPDOWN:  return getBodyDropdown (node)
    if type == util.consts.UI_TYPE_FILE:      return getBodyFile     (node)
    if type == util.consts.UI_TYPE_GPSDIAG:   return getBodyGpsDiag  (node)
    if type == util.consts.UI_TYPE_GROUP:     return getBodyGroup    (node)
    if type == util.consts.UI_TYPE_INPUT:     return getBodyInput    (node)
    if type == util.consts.UI_TYPE_LIST:      return getBodyList     (node)
    if type == util.consts.UI_TYPE_MAP:       return getBodyMap      (node)
    if type == util.consts.UI_TYPE_PICTURE:   return getBodyPicture  (node)
    if type == util.consts.UI_TYPE_RADIO:     return getBodyRadio    (node)
    if type == util.consts.UI_TYPE_VIDEO:     return getBodyVideo    (node)
    if type == util.consts.UI_TYPE_VIEWFILES: return getBodyViewfiles(node)
    if type == util.consts.UI_TYPE_WEB:       return getBodyWebview  (node)
    if type == util.consts.UI_TYPE_WEBVIEW:   return getBodyWebview  (node)
    return None

def getBodyAudio(node):
    return getBodySelect(node, faims_sync='true', type='file')

def getBodyButton(node):
    button = getBodyLabelled(node, 'trigger')
    return button

def getBodyCamera(node):
    return getBodySelect(node, faims_sync='true')

def getBodyCheckbox(node):
    return getBodySelect(node)

def getBodyDropdown(node):
    return getBodySelect1(node)

def getBodyFile(node):
    return getBodySelect(node, type='file', faims_sync='true')

def getBodyGpsDiag(node):
    return Element('input', faims_read_only='true', ref=node.tag)

def getBodyGroup(node):
    children = [getBodyTabChildren(n) for n in node]
    children = filter(lambda x: x != None, children)


    group = Element('group', ref=node.tag)
    group.append(Element('label'))
    group.extend(children)

    faimsStyle = util.xml.getAttribVal(node, 's')
    if faimsStyle: group.attrib['faims_style'] = faimsStyle

    return group

def getBodyInput(node, **kwargs):
    return getBodyLabelled(node, 'input', **kwargs)

def getBodyList(node):
    return getBodySelect1(node, appearance='compact')

def getBodyMap(node):
    map = getBodyInput(node, faims_map='true')
    return map

def getBodyPicture(node):
    return getBodySelect(node, type='image')

def getBodyRadio(node):
    return getBodySelect(node, appearance='full')

def getBodyVideo(node):
    return getBodySelect(node, type='video', faims_sync='true')

def getBodyViewfiles(node):
    return getBodyButton(node)

def getBodyWebview(node):
    webview = getBodyInput(node, faims_web='true')
    return webview

def getBodySelect(node, **kwargs):
    select = getBodyLabelled(node, 'select', **kwargs)

    item  = SubElement(select, 'item')
    label = SubElement(item,   'label'); label.text = 'Options not loaded'
    value = SubElement(item,   'value'); value.text = '0'

    return select

def getBodySelect1(node, **kwargs):
    select1 = getBodySelect(node, **kwargs)
    select1.tag = 'select1'
    return select1

def getBodyLabelled(node, name, **kwargs):
    isBlank = util.schema.isFlagged(node, 'nolabel', checkAncestors=False)

    labelled = Element(name, **kwargs)
    labelled.append(getBodyLabel(node, isBlank))

    attribName = util.data.getAttribName(node)
    attribType = util.data.getAttribType(node)
    ref        = node.tag
    styleClass = util.xml.getAttribVal(node, util.consts.ATTRIB_C)
    if attribName: labelled.attrib['faims_attribute_name'] = attribName
    if attribType: labelled.attrib['faims_attribute_type'] = attribType
    if ref:        labelled.attrib['ref']                  = ref
    if styleClass: labelled.attrib['faims_style_class']    = styleClass

    return labelled

def getBodyLabel(node, isBlank=False):
    label = Element('label')
    if isBlank:
        return label

    label.text = util.arch16n.getArch16nKey(node, doAddCurlies=True)

    return label

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
util.schema.canonicalise(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
uiSchema = getUiSchema(tree)

print etree.tostring(
        uiSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
