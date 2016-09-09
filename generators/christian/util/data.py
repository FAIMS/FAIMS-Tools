################################################################################
#                                                                              #
# This file contains utility functions related to data schema generation.      #
#                                                                              #
################################################################################
import schema
import xml

def isDataElement(guiDataElement):
    if schema.isFlagged(guiDataElement, 'nodata'):      return False
    if schema.isFlagged(guiDataElement, 'user'):        return False
    if schema.hasAttrib(guiDataElement, 'e'):           return False
    if schema.hasAttrib(guiDataElement, 'ec'):          return False
    if schema.guessType(guiDataElement) == 'button':    return False
    if schema.guessType(guiDataElement) == 'gpsdiag':   return False
    if schema.guessType(guiDataElement) == 'group':     return False
    if schema.guessType(guiDataElement) == 'map':       return False
    if schema.guessType(guiDataElement) == 'table':     return False
    if schema.guessType(guiDataElement) == 'viewfiles': return False
    return True

def getArchEntName(node, doRecurse=False):
    if node is None:
        return ''
    if schema.isTabGroup(node) and isDataElement(node):
        return node.tag.replace('_', ' ')
    if doRecurse:
        return getArchEntName(node.getparent())

def getAttribName(node, doRecurse=False):
    if node is None:
        return ''
    if isDataElement(node):
        return node.tag.replace('_', ' ')
    if doRecurse:
        return getArchEntName(node.getparent())

def getPropType(node):
    if hasMeasureType(node): return 'measure'
    if hasFileType   (node): return 'file'
    if hasVocabType  (node): return 'vocab'

    print node
    print schema.getPathString(node)
    raise ValueError('An unexpected t value was encountered')

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
    if not schema.hasAttrib(node, 'lc'):       return None
    if schema.getParentTabGroup(node) == None: return None

    parentName = schema.getParentTabGroup(node)
    parentName = parentName.tag
    parentName = parentName.replace('_', ' ')

    childName = node.attrib['lc']
    childName = childName.replace('_', ' ')

    relName = '%s - %s' % (parentName, childName)
    return relName

    # Replace non-<autonum> tags similarly to in (1).
    for tag, replacements in table.REPLACEMENTS_BY_TAG.iteritems():
        exp = '//%s[@%s]' % (tag, consts.RESERVED_XML_TYPE)
        matches = tree.xpath(exp)
        for m in matches:
            replaceElement(m, replacements)

    schema.annotateWithXmlTypes(tree)
