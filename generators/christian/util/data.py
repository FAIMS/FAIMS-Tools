################################################################################
#                                                                              #
# This file contains utility functions related to data schema generation.      #
#                                                                              #
################################################################################
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

def getAttribType(node):
    if not isDataElement(node): return ''

    if hasMeasureType(node): return 'measure'
    if hasFileType   (node): return 'measure'
    if hasVocabType  (node): return 'vocab'

    return ''

def hasMeasureType(node):
    measureTypes = (
            'input',
    )
    return schema.guessType(node) in measureTypes

def hasFileType(node):
    fileTypes    = (
            'audio',
            'camera',
            'file',
            'video',
    )
    return schema.guessType(node) in fileTypes

def hasVocabType(node):
    vocabTypes   = (
            'checkbox',
            'dropdown',
            'list',
            'picture',
            'radio',
    )
    return schema.guessType(node) in vocabTypes

def getRelName(node):
    if not xml.hasAttrib(node, 'lc'):          return ''
    if schema.getParentTabGroup(node) == None: return ''

    parentName = schema.getParentTabGroup(node)
    parentName = parentName.tag
    parentName = parentName.replace('_', ' ')

    childName = node.attrib['lc']
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
