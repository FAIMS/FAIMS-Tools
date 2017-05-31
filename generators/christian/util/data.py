################################################################################
#                                                                              #
# This file contains utility functions related to data schema generation.      #
#                                                                              #
################################################################################
import util
import schema
import xml
from   consts import *

def isDataElement(node):
    if node is None:                        return False
    if schema.isFlagged(node, FLAG_NODATA): return False
    if schema.isFlagged(node, FLAG_USER):   return False
    if    xml.hasAttrib(node, ATTRIB_E):    return False
    if    xml.hasAttrib(node, ATTRIB_EC):   return False

    dataTypes = [
        UI_TYPE_AUDIO,
        UI_TYPE_CAMERA,
        UI_TYPE_CHECKBOX,
        UI_TYPE_DROPDOWN,
        UI_TYPE_FILE,
        UI_TYPE_INPUT,
        UI_TYPE_LIST,
        UI_TYPE_PICTURE,
        UI_TYPE_RADIO,
        UI_TYPE_VIDEO,
    ]
    return schema.isTabGroup(node) or schema.guessType(node) in dataTypes

def formsArchEnt(node):
    return bool(getArchEntName(node))

def formsProp(node):
    return bool(getAttribName(node))

def getDataElements(node):
    return xml.getAll(node, isDataElement)

# Gets the elements in the schema which can be made into arch ents
def getArchEnts(node):
    return xml.getAll(node, formsArchEnt)

def getProps(node):
    return xml.getAll(node, formsProp)

def getArchEntName(node, doRecurse=False):
    if node is None:
        return ''
    if schema.isTabGroup(node) and isDataElement(node):
        return node.tag.replace('_', ' ')
    if doRecurse:
        return getArchEntName(node.getparent(), doRecurse)
    return ''

def getAttribName(node):
    if isDataElement(node) and schema.isGuiDataElement(node):
        return node.tag.replace('_', ' ')
    else:
        return ''

def getName(node):
    return util.data.getAttribName(node) or \
           util.data.getArchEntName(node)

def getAttribType(node, isSpecific=False):
    if not isDataElement(node): return ''

    typesSpecific    = ('measure', 'file',    'vocab')
    typesNonSpecific = ('measure', 'measure', 'vocab')

    if isSpecific: types = typesSpecific
    else:          types = typesNonSpecific

    if hasMeasureType(node): return types[0]
    if hasFileType   (node): return types[1]
    if hasVocabType  (node): return types[2]

    return ''

def hasMeasureType(node):
    return schema.guessType(node) in MEASURE_UI_TYPES

def hasFileType(node):
    return schema.guessType(node) in FILE_UI_TYPES

def hasVocabType(node):
    return schema.guessType(node) in MENU_UI_TYPES

def getRelName(node):
    if not xml.hasAttrib(node, ATTRIB_LC):     return ''
    if schema.getParentTabGroup(node) == None: return ''

    parentNode = schema.getParentTabGroup(node)
    childNode  = schema.getLinkedNode(node)
    if schema.getType(childNode) != TYPE_TAB_GROUP:
        childNode = schema.getParentTabGroup(childNode)

    parentName = parentNode.tag
    parentName = parentName.replace('_', ' ')

    childName = childNode.tag
    childName = childName.replace('_', ' ')

    return '%s - %s' % (parentName, childName)

    # Replace non-<autonum> tags similarly to in (1).
    for tag, replacements in table.REPLACEMENTS_BY_TAG.iteritems():
        exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
        matches = tree.xpath(exp)
        for m in matches:
            replaceElement(m, replacements)

    schema.annotateWithXmlTypes(tree)

# Gets the relationship name implied by a node having an ec attribute
def getRelNameEntityList(node):
    ecVal = xml.getAttribVal(node, ATTRIB_EC)
    if not ecVal:
        return ''

    parentName = getArchEntName(node, doRecurse=True)
    childName  = node.attrib[ATTRIB_EC]
    childName = childName.replace('_', ' ')

    return '%s - %s' % (parentName, childName)

def getHierarchy(node):
    topLevelNodes = getTopLevelArchEntNodes(node)
    hier = util.Tree(
            None,
            [getHierarchyForTopLevelNode(n) for n in topLevelNodes]
    )

    def nodesToNames(n): n.data = getArchEntName(n.data)
    hier.apply(nodesToNames)
    return hier

def getHierarchyForTopLevelNode(node, seenLinks=None):
    seenLinks = seenLinks or []

    # Handles qr links
    gui2tg = lambda n : schema.getParentTabGroup(n) \
            if schema.getType(n) == TYPE_GUI_DATA \
            else n

    link         = lambda n : (node.tag, n.tag)
    linkedNodes  = schema.getLinkedNodes(node, ATTRIB_LC)
    linkedNodes  = [gui2tg(n) for n in linkedNodes]
    linkedNodes  = filter(isDataElement, linkedNodes)
    linkedNodes  = filter(schema.isTabGroup, linkedNodes)
    unseenNodes  = [n for n in linkedNodes if link(n) not in seenLinks]
    seenLinks   += [link(n) for n in unseenNodes]

    return util.Tree(
            node,
            [getHierarchyForTopLevelNode(n, seenLinks) for n in unseenNodes]
    )

def getTopLevelArchEntNodes(node, parentNode=None):
    if schema.getType(node) == TYPE_MODULE:
        return list(set(getTopLevelArchEntNodes(schema.getEntryPoint(node))))
    if node == None:
        return []

    linkedNodes = schema.getLinkedNodes(node)
    top = sum([getTopLevelArchEntNodes(n, node) for n in linkedNodes], [])
    if isTopLevelArchEntNode(node, parentNode):
        return [node] + top
    else:
        return top

def isTopLevelArchEntNode(node, parentNode):
    return node != None and parentNode != None and \
            schema.isTabGroup(node) and \
            isDataElement(node) and \
            not isDataElement(parentNode)
