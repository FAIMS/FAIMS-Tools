################################################################################
#                                                                              #
# This file contains utility functions related to UI schema generation.        #
#                                                                              #
################################################################################
import arch16n
import consts
import schema
import xml

def getLabel(node):
    return arch16n.getArch16nVal(node)

def isGuiNode(node):
    return not schema.isFlagged(node, 'noui')

def getGuiNodes(node, xmlType):
    exp     = './/*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, xmlType)
    cond    = lambda e: not schema.isFlagged(e, 'noui')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    return matches

def isTabGroup  (node): return isGuiNode(node) and schema.isTabGroup(node)
def isTab       (node): return isGuiNode(node) and schema.isTab(node)
def isGuiElement(node): return isGuiNode(node) and schema.isGuiDataElement(node)

def getTabGroups  (node): return xml.getAll(node, keep=isTabGroup)
def getTabs       (node): return xml.getAll(node, keep=isTab)
def getGuiElements(node): return xml.getAll(node, keep=isGuiElement)
