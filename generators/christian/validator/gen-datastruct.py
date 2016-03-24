#!/usr/bin/env python

from   lxml import etree
import consts
import helpers
import sys
import tables

def getUiNodes(node, xmlType):
    exp     = './*[@%s="%s"]' % (consts.RESERVED_XML_TYPE, xmlType)
    cond    = lambda e: not helpers.isFlagged(e, 'noui')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    return matches

################################################################################

class GraphModule(object):
    def __init__(self, node):
        self.topMatter  = '\n\tgraph ['
        self.topMatter += '\n\t\trankdir="LR"'
        self.topMatter += '\n\t\tfontname="Roboto"'
        self.topMatter += '\n\t];'
        self.topMatter += '\n\tnode ['
        self.topMatter += '\n\t\tfontsize="12"'
        self.topMatter += '\n\t\tshape=plaintext'
        self.topMatter += '\n\t\tfontname="Roboto"'
        self.topMatter += '\n\t\tmargin=0'
        self.topMatter += '\n\t\tshape=none'
        self.topMatter += '\n\t];'
        self.topMatter += '\n'

        self.tabGroups = []

        self.links     = []

        self.addTabGroups(node)

    def addTabGroups(self, node):
        matches = getUiNodes(node, 'tab group')
        for m in matches:
            graphTabGroup = GraphTabGroup(m)
            self.tabGroups.append(graphTabGroup)

    def toString(self):
        out  = 'digraph g {'
        out += self.topMatter
        for tabGroup in self.tabGroups: out += tabGroup.toString()
        for link     in self.links:     out += link
        out += '}'
        out += '\n'

        return out

################################################################################

class GraphTabGroup(object):
    def __init__(self, node):
        self.name  = node.tag
        self.label = helpers.getLabel(node)

        self.topMatter  = '\n\t\tlabel="%s"' % self.label
        self.topMatter += '\n\t\tbgcolor="lightblue"'
        self.topMatter += '\n'

        self.tabs = []

        self.addTabs(node)

    def addTabs(self, node):
        matches = getUiNodes(node, 'tab')
        for m in matches:
            graphTab = GraphTab(m)
            self.tabs.append(graphTab)

    def toString(self):
        out  = '\tsubgraph cluster_%s {' % self.name
        out += self.topMatter
        for tab in self.tabs: out += tab.toString()
        out += '\t}'
        out += '\n'

        return out

################################################################################

class GraphTab(object):
    def __init__(self, node):
        self.name  = node.tag
        self.label = helpers.getLabel(node)

        self.topMatter  = '\n\t\t\tlabel=""'
        self.topMatter += '\n\t\t\tbgcolor="white"'
        self.topMatter += '\n'

        self.guiRows = []

    def getTabBarStructString(self, hasPrecedingTab, hasFollowingTab):
        out  = '\n\t\t\tstructLabel%sTab [' % self.name
        out += '\n\t\t\tlabel=<'
        out += '\n\t\t\t\t<TABLE BORDER="1" CELLBORDER="3" CELLSPACING="0" CELLPADDING="5" WIDTH="150" HEIGHT="10">'
        out += '\n\t\t\t\t\t<TR>'
        out += '\n\t\t\t\t\t\t<TD SIDES="b" BORDER="1">...</TD>' if hasPrecedingTab else ''
        out += '\n\t\t\t\t\t\t<TD PORT="search" ALIGN="TEXT" SIDES="b">%s</TD>' % self.label
        out += '\n\t\t\t\t\t\t<TD SIDES="b" BORDER="1">...</TD>' if hasFollowingTab else ''
        out += '\n\t\t\t\t\t</TR>'
        out += '\n\t\t\t\t</TABLE>'
        out += '\n\t\t\t>];'
        out += '\n'

        return out

    def getGuiRowsString(self):
        out  = '\n\t\t\tstructBurialGeneral ['
        out += '\n\t\t\tlabel=<'
        out += '\n\t\t\t\t<TABLE BORDER="0" CELLSPACING="0" WIDTH="150">'
        out += '\n\t\t\t\t\t<TR>'
        out += '\n\t\t\t\t\t\t<TD PORT="search" ALIGN="TEXT" SIDES="b">%s</TD>' % self.label
        out += '\n\t\t\t\t\t</TR>'
        for guiRow in self.guiRows:
            out += guiRow.toString()
        out += '\n\t\t\t\t</TABLE>'
        out += '\n\t\t\t>];'
        out += '\n'

        return out

    def toString(self, hasPrecedingTab=False, hasFollowingTab=False):
        out  = '\t\tsubgraph cluster_%s {' % self.name
        out += self.topMatter
        out += self.getTabBarStructString(hasPrecedingTab, hasFollowingTab)
        out += self.getGuiRowsString()
        out += '\t\t}'
        out += '\n'

        return out

################################################################################

class GuiRow(object):
    def __init__(self):
        self.guiCols = []

    def toString(self):
        out  = ''
        for guiCol in self.guiCols:
            out += '\n\t\t\t\t\t\t<TD><IMG SRC="%s.svg"/></TD>' % guiCol

        return out

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = helpers.parseXml(filenameModule)
helpers.normaliseAttributes(tree)
helpers.expandCompositeElements(tree)

################################################################################
#                        GENERATE AND OUTPUT DATASTRUCT                        #
################################################################################
gm = GraphModule(tree)
print gm.toString()
