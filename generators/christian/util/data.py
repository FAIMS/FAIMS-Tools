################################################################################
#                                                                              #
# This file contains utility functions related to data schema generation.      #
#                                                                              #
################################################################################

def isDataElement(guiDataElement):
    if isFlagged(guiDataElement, 'nodata'):      return False
    if isFlagged(guiDataElement, 'user'):        return False
    if hasAttrib(guiDataElement, 'e'):           return False
    if hasAttrib(guiDataElement, 'ec'):          return False
    if guessType(guiDataElement) == 'button':    return False
    if guessType(guiDataElement) == 'gpsdiag':   return False
    if guessType(guiDataElement) == 'group':     return False
    if guessType(guiDataElement) == 'map':       return False
    if guessType(guiDataElement) == 'table':     return False
    if guessType(guiDataElement) == 'viewfiles': return False
    return True

def getPropType(node):
    if hasMeasureType(node): return 'measure'
    if hasFileType   (node): return 'file'
    if hasVocabType  (node): return 'vocab'

    raise ValueError('An unexpected t value was encountered')

def hasMeasureType(node):
    measureTypes = (
            'input',
    )
    return guessType(node) in measureTypes

def hasFileType(node):
    fileTypes    = (
            'audio',
            'camera',
            'file',
            'video',
    )
    return guessType(node) in fileTypes

def hasVocabType(node):
    vocabTypes   = (
            'checkbox',
            'dropdown',
            'list',
            'picture',
            'radio',
    )
    return guessType(node) in vocabTypes
