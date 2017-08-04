################################################################################
#                                                                              #
# This file contains utility functions related to UI schema generation.        #
#                                                                              #
################################################################################
import arch16n
from   consts import *
import schema
import xml

def getLabel(node):
    return arch16n.getArch16nVal(node)

def isGuiNode(node):
    return not schema.isFlagged(node, FLAG_NOUI)

def getGuiNodes(node, xmlType):
    exp     = './/*[@%s="%s"]' % (RESERVED_XML_TYPE, xmlType)
    cond    = lambda e: not schema.isFlagged(e, FLAG_NOUI)
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    return matches

def getAll(node, uiType, keep=None):
    if type(uiType) == str:
        uiType = [uiType]

    if keep:
        l = lambda n: isGuiNode(n) and schema.getUiType(n) in uiType and keep(n)
    else:
        l = lambda n: isGuiNode(n) and schema.getUiType(n) in uiType

    return xml.getAll(node, l)

def isTabGroup  (node): return isGuiNode(node) and schema.isTabGroup(node)
def isTab       (node): return isGuiNode(node) and schema.isTab(node)
def isGuiElement(node): return isGuiNode(node) and schema.isGuiDataElement(
        node, includeCols=True)

def getTabGroups  (node, keep=None): return schema.getByType(node, isTabGroup, keep, True)
def getTabs       (node, keep=None): return schema.getByType(node, isTab, keep, True)
def getGuiElements(node, keep=None): return schema.getByType(node, isGuiElement, keep, True)
