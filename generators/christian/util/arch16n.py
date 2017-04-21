################################################################################
#                                                                              #
# This file contains utility functions related to arch16n file generation.     #
#                                                                              #
################################################################################
import hashlib
import schema
import util
import xml
from  consts import *
import re

def getLabelFromTag(node):
    if node.tag == TAG_OPT:
        return ''

    if node.tag == TAG_AUTHOR:     return 'Author'
    if node.tag == TAG_SEARCH:     return 'Search'
    if node.tag == TAG_TIMESTAMP:  return 'Timestamp'

    label = node.tag
    label = label.replace('_', ' ')
    label = util.normaliseSpace(label)
    return label

def getLabelFromText(node):
    if node.text == None:
        return ''

    label = node.text
    label = util.normaliseSpace(label)
    return label

def hasArch16Entry(node):
    if node.xpath('./ancestor-or-self::rels'):  return False
    if schema.isFlagged(node, FLAG_NOLABEL):    return False

    if schema.getType(node)   == TYPE_COLS:     return False
    if schema.getType(node)   == TYPE_COL:      return False
    if schema.guessType(node) == UI_TYPE_GROUP: return False

    if node.tag == TAG_COL:                     return False
    if node.tag == TAG_COLS:                    return False
    if node.tag == TAG_DESC:                    return False
    if node.tag == TAG_FMT:                     return False
    if node.tag == TAG_GROUP:                   return False
    if node.tag == TAG_LOGIC:                   return False
    if node.tag == TAG_MODULE:                  return False
    if node.tag == TAG_OPTS:                    return False
    if node.tag == TAG_POS:                     return False
    if node.tag == TAG_STR:                     return False

    return True

def getArch16nVal(node):
    if not hasArch16Entry(node): return ''

    return getLabelFromText(node) or getLabelFromTag(node)

def getArch16nKey(node, doAddCurlies=True):
    if not hasArch16Entry(node): return ''

    key = getArch16nVal(node)
    key = key.strip()
    key = re.sub('[^0-9a-zA-Z]', '_', key)

    if doAddCurlies:
        key = '{' + key + '}'

    return key
