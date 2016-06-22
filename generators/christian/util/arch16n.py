################################################################################
#                                                                              #
# This file contains utility functions related to arch16n file generation.     #
#                                                                              #
################################################################################
import util

def getLabelFromTag(node):
    label = node.tag
    label = label.replace('_', ' ')
    label = util.normaliseSpace(label)
    return label

def getLabelFromText(node):
    if node.text == None:  return ''
    if node.text == 'opt': return ''

    label = node.text
    label = util.normaliseSpace(label)
    return label

def getArch16nVal(node):
    if node.xpath('./ancestor-or-self::rels'): return ''
    if isFlagged(node, 'nolabel'):             return ''

    if node.tag == 'autonum':                  return ''
    if node.tag == 'col':                      return ''
    if node.tag == 'cols':                     return ''
    if node.tag == 'desc':                     return ''
    if node.tag == 'logic':                    return ''
    if node.tag == 'module':                   return ''
    if node.tag == 'opts':                     return ''

    if node.tag == 'author':                   return 'Author'
    if node.tag == 'search':                   return 'Search'
    if node.tag == 'timestamp':                return 'Timestamp'

    if getLabelFromText(node):
        return getLabelFromText(node)
    return getLabelFromTag(node)

def getArch16nKey(node):
    return getArch16nVal(node).replace(' ', '_')
