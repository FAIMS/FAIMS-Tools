################################################################################
#                                                                              #
# This file contains utility functions related to UI schema generation.        #
#                                                                              #
################################################################################
import arch16n
import consts
import schema

def getLabel(node):
    return arch16n.getArch16nVal(node)

def isUiElement(node):
    if     schema.isFlagged(node, 'noui'): return False
    if not schema.isGuiDataElement(node):  return False
    return node.attrib[consts.RESERVED_XML_TYPE] == 'GUI/data element'

def getUiNodes(node, xmlType):
    exp     = './/*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, xmlType)
    cond    = lambda e: not schema.isFlagged(e, 'noui')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    return matches
