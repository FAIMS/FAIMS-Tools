################################################################################
#                                                                              #
# This file contains utility functions related to arch16n file generation.     #
#                                                                              #
################################################################################
import hashlib
import schema
import util
import xml

def getLabelFromTag(node):
    if node.text == 'opt':
        return ''

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
    if node.xpath('./ancestor-or-self::rels'): return False
    if schema.isFlagged(node, 'nolabel'):      return False

    if node.tag == 'autonum':                  return False
    if node.tag == 'col':                      return False
    if node.tag == 'cols':                     return False
    if node.tag == 'desc':                     return False
    if node.tag == 'logic':                    return False
    if node.tag == 'module':                   return False
    if node.tag == 'opts':                     return False

    return True

def getArch16nVal(node):
    if not hasArch16Entry(node): return ''

    if node.tag == 'author':     return 'Author'
    if node.tag == 'search':     return 'Search'
    if node.tag == 'timestamp':  return 'Timestamp'

    return getLabelFromText(node) or getLabelFromTag(node)

def getArch16nKey(node, keyLen=10, doAddCurlies=False):
    if node.tag == 'opt': lastSegment = [node.text]
    else:                 lastSegment = []

    path = schema.getPath(node) + lastSegment
    path = '/'.join(path)

    hash = hashlib.sha256(path)
    hash = hash.hexdigest()
    hash = hash[:keyLen]

    if doAddCurlies:
        hash = '{' + hash + '}'

    return hash
