#! /usr/bin/env python

''' This script was used to fix HTML descriptions when picture galleries(?) were
marked with faims_html_description="true" in the ui_schema'''

import sys
import xmltools
from   lxml import etree
from   copy import deepcopy

# HTML descriptions to be fixed
ENTPROPS = [
        ('Isolated'                , 'Isolated_-_Vulnerability_to_Erosion'),
        ('Isolated'                , 'Isolated_-_Palaeotopographic_Setting'),
        ('Isolated'                , 'Isolated_-_Sediment_Type'),
        ('Isolated'                , 'Isolated_-_Stratigraphic_Unit'),
        ('Isolated'                , 'Isolated_-_Topographic_Setting'),
        ('Hearth'                  , 'Hearth_-_Proportion_of_material_that_remains_in_situ'),
        ('Hearth'                  , 'Hearth_-_Topographic_Setting'),
        ('Hearth'                  , 'Hearth_-_Sediment_Type'),
        ('Hearth'                  , 'Hearth_-_Stratigraphic_Unit'),
        ('Hearth'                  , 'Hearth_-_Vulnerability_To_Erosion'),
        ('Hearth'                  , 'Hearth_-_Palaeotopographic_Setting'),
        ('Shell'                   , 'Shell_-_Topographic_Setting'),
        ('Shell'                   , 'Shell_-_Sediment_Type'),
        ('Shell'                   , 'Shell_-_Stratigraphic_Unit'),
        ('Shell'                   , 'Shell_-_Vulnerability_To_Erosion'),
        ('Shell'                   , 'Shell_-_Palaeotopographic_Setting'),
        ('Stone Artefact Clusters' , 'Stone_-_Topographic_Setting'),
        ('Stone Artefact Clusters' , 'Stone_-_Sediment_Type'),
        ('Stone Artefact Clusters' , 'Stone_-_Stratigraphic_Unit'),
        ('Stone Artefact Clusters' , 'Stone_-_Vulnerability_To_Erosion'),
        ('Stone Artefact Clusters' , 'Stone_-_Palaeotopographic_Setting'),
        ('Bone'                    , 'OldBone_-_Topographic_Setting'),
        ('Bone'                    , 'OldBone_-_Sediment_Type'),
        ('Bone'                    , 'OldBone_-_Stratigraphic_Unit'),
        ('Bone'                    , 'OldBone_-_Vulnerability_To_Erosion'),
        ('Bone'                    , 'OldBone_-_Palaeotopographic_Setting'),
        ('Bone'                    , 'OldBone_-_Proportion_of_material_that_remains_in_situ')
]

def entpropToXpath(ep):
    return '//ArchaeologicalElement[@name="%s"]/property[@name="%s"]' % ep

def getNodeFromEntprop(tree, ep):
    n = tree.xpath(entpropToXpath(ep))
    if len(n) == 1:
        return n[0]
    sys.stderr.write('Not exactly one node matches. Exiting.\n')
    exit()

def fixNode(node):
    fixDescription(node)
    fixLookup     (node)

def fixDescription(node):
    descNode = node.xpath('description')
    if   len(descNode) <  1:
        return
    elif len(descNode) == 1:
        descNode = descNode[0]
    elif len(descNode) >  1:
        sys.stderr.write('More than one node matches. Exiting.\n')
        exit()
    if not descNode.text:
        return

    descText  = '\n'
    descText += '<i>Description:</i>\n'
    descText += '<br>'
    descText += descNode.text

    descNode.text = etree.CDATA(descText)

def fixLookup(node):
    lookupNode = node.xpath('lookup')
    if   len(lookupNode) <  1:
        return
    elif len(lookupNode) == 1:
        lookupNode = lookupNode[0]
    elif len(lookupNode) >  1:
        sys.stderr.write('More than one node matches. Exiting.\n')
        exit()
    if not lookupNode.text:
        return

    for i in range(len(lookupNode)):
        term    = lookupNode[i]
        isFirst = (i == 0)
        fixTerm(term, isFirst)

# WARNING: Doesn't handle nested/hierarchical terms
def fixTerm(term, isFirst):
    termName = term.text
    fixTermDescription(term, termName, isFirst)

def fixTermDescription(term, termName, isFirst):
    descNode = term.xpath('description')
    if   len(descNode) <  1:
        return
    elif len(descNode) == 1:
        descNode = descNode[0]
    elif len(descNode) >  1:
        sys.stderr.write('More than one node matches. Exiting.\n')
        exit()
    if not descNode.text:
        return

    top  = '\n'
    if isFirst:
        top += '<i>Glossary:</i>\n'
        top += '<br>\n'
    top     += '<ul>\n'
    top     += '    <li>\n'
    top     += '        <b>' + termName + '</b>\n'
    bot      = '    </li>\n'
    bot     += '</ul>\n'

    descText = descNode.text
    descText = descText[ 6:  ]                        # Delete opening <div>
    descText = descText[  :-7]                        # Delete closing <div>
    descText = descText.replace('    <', '        <') # Deepen indentation by one level

    descText = top + descText + bot

    descNode.text = etree.CDATA(descText)

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('SYNOPSIS\n')
    sys.stderr.write('       python %s DATASCHEMA\n' % sys.argv[0])
    sys.stderr.write('\n')
    exit()

DATASCHEMA = sys.argv[1]

# Parse DATASCHEMA
parser = etree.XMLParser(strip_cdata=False)
tree = etree.parse(DATASCHEMA, parser)
tree = tree.getroot()

for ep in ENTPROPS:
    n = getNodeFromEntprop(tree, ep)
    fixNode(n)

# Collect your prize
print etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')
