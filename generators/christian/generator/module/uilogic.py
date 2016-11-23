#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.gui
import util.xml
from   util.consts import *

def format(tuples, fmt='%s', indent='', newline='\n'):
    sep = newline + indent
    return sep.join(fmt % tuple for tuple in tuples)

def getUserMenuUiType(tree):
    isFlagged = lambda e: util.schema.isFlagged(e, FLAG_USER)
    nodes = util.xml.getAll(tree, isFlagged)
    if len(nodes) != 1: return None
    node = nodes[0]
    return util.schema.guessType(node)

def getTabGroups(tree, t):
    nodes = util.schema.getTabGroups(tree)
    refs  = [util.schema.getPathString(tg) for tg in nodes]

    fmt          = 'tabGroups.add("%s");'
    placeholder  = '{{get-tab-groups}}'
    replacement  = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getDropdownValueGetters(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_DROPDOWN)
    refs  = [util.schema.getPathString(n) for n in nodes]
    refs  = zip(refs, refs)

    fmt          = 'addOnEvent("%s", "click", "DROPDOWN_ITEM_VALUE = getFieldValue(\\"%s\\")");'
    placeholder  = '{{dropdown-value-getters}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getGpsDiagUpdate(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_GPSDIAG)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt          = 'addOnEvent("%s", "show", "updateGPSDiagnostics()");'
    placeholder  = '{{gps-diag-update}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getGpsDiagRef(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_GPSDIAG)
    refs  = [util.schema.getPathString(n) for n in nodes]

    placeholder  = '{{gps-diag-ref}}'
    replacement  = format(refs)

    return t.replace(placeholder, replacement)

def getUsers(tree, t):
    isFlagged = lambda e: util.schema.isFlagged(e, FLAG_USER)
    nodes = util.xml.getAll(tree, isFlagged)
    refs  = [util.schema.getPathString(n) for n in nodes]

    placeholder  = '{{user-menu-path}}'
    replacement  = format(refs)

    return t.replace(placeholder, replacement)

def getUsersPopulateCall(tree, t):
    placeholder = '{{users-populate-call}}'

    if   getUserMenuUiType(tree) == UI_TYPE_LIST:
        replacement = 'populateList(userMenuPath, result);'
    elif getUserMenuUiType(tree) == UI_TYPE_DROPDOWN:
        replacement = 'populateDropDown(userMenuPath, result, true);'
    else:
        replacement = 'return;'

    return t.replace(placeholder, replacement)

def getUsersVocabId(tree, t):
    placeholder = '{{users-vocabid}}'

    if   getUserMenuUiType(tree) == UI_TYPE_LIST:
        replacement = 'String userVocabId = getListItemValue();'
    elif getUserMenuUiType(tree) == UI_TYPE_DROPDOWN:
        replacement = 'String userVocabId = getFieldValue(userMenuPath);'
    else:
        replacement = 'return;'

    return t.replace(placeholder, replacement)

def getMakeVocab(tree, t):

    # TODO: Rewrite ui-logic.xml:950 and onwards
    # Protip: use util.schema.isHierarchical
    return t

def getUiLogic(tree):
    templateFileName = 'generator/module/uilogic-template.bsh'

    # Load template, `t`
    t = None
    with open(templateFileName, 'r') as tFile:
        t = tFile.read()
    if not t:
        raise Exception('"%s" could not be loaded' % templateFileName)

    t = getTabGroups(tree, t)
    t = getDropdownValueGetters(tree, t)
    t = getGpsDiagUpdate(tree, t)
    t = getGpsDiagRef(tree, t)
    t = getUsers(tree, t)
    t = getUsersPopulateCall(tree, t)
    t = getUsersVocabId(tree, t)
    t = getMakeVocab(tree, t)

    return t

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithXmlTypes(tree)
util.schema.canonicalise(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################

#print etree.tostring(
        #tree,
        #pretty_print=True,
        #xml_declaration=True,
        #encoding='utf-8'
#)

print getUiLogic(tree),
