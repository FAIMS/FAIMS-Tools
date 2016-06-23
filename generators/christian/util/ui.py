################################################################################
#                                                                              #
# This file contains utility functions related to UI schema generation.        #
#                                                                              #
################################################################################
import arch16n
import schema

def getLabel(node):
    return arch16n.getArch16nVal(node)

def isUiElement(node):
    if     schema.isFlagged(node, 'noui'):                   return False
    if not schema.hasAttrib(node, consts.RESERVED_XML_TYPE): return False
    return node[consts.RESERVED_XML_TYPE] == 'GUI/data element'

