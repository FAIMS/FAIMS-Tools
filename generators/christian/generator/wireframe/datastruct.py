#!/usr/bin/env python

from   lxml import etree
import copy
import sys
import util.schema
import util.gui
from   util.consts import *

def isNoWire(node):
    return util.schema.isFlagged(node, FLAG_NOWIRE)

def isWire(node):
    return not isNoWire(node)

################################################################################

class GraphModule(object):
    def __init__(self, node):
        self.topMatter  = '\n\tgraph ['
        self.topMatter += '\n\t\trankdir="LR"'
        self.topMatter += '\n\t\tfontname="Roboto"'
        self.topMatter += '\n\t\tsplines=ortho'
        self.topMatter += '\n\t\toutputorder="nodesfirst"'
        self.topMatter += '\n\t\tranksep=2'
        self.topMatter += '\n\t];'
        self.topMatter += '\n\tnode ['
        self.topMatter += '\n\t\tfontsize="12"'
        self.topMatter += '\n\t\tshape=plaintext'
        self.topMatter += '\n\t\tfontname="Roboto"'
        self.topMatter += '\n\t\tmargin=0'
        self.topMatter += '\n\t\tshape=none'
        self.topMatter += '\n\t];'
        self.topMatter += '\n'

        self.tabGroups = self.getTabGroups(node)
        self.links     = self.getLinks    (node)

    def getTabGroups(self, node):
        return [GraphTabGroup(n) for n in util.gui.getTabGroups(node, isWire)]

    def getLinks(self, node):
        links  = self.getTabLabelLinks         (node)
        links += self.getGraphConstrainingLinks(node)
        links += self.getUserSpecifiedLinks    (node)
        return links

    def getTabLabelLinks(self, node):
        links = ['/* Intra-tab, label-to-label links */']

        tabGroups = util.gui.getTabGroups(node, isWire)
        for tabGroup in tabGroups:
            tabs = util.gui.getTabs(tabGroup, isWire)
            for i in range(len(tabs) - 1):
                tabFrom = tabs[i  ]; idFrom = GraphTab.nodeId(tabFrom)
                tabTo   = tabs[i+1]; idTo   = GraphTab.nodeId(tabTo  )
                link = '%s -> %s' % (idFrom, idTo)
                links.append(link)

        return links

    def getUserSpecifiedLinks(self, node):
        links = ['/* User-specified links */']

        for n in node.xpath('//*[@l or @lc or @ll]'):
            # Determine `nodeFrom` and `nodeTo`. `nodeTo` is always a tab.
            nodeFrom = n
            nodeTo   = util.schema.getLinkedNode(n)
            if util.schema.isGuiDataElement(nodeTo):
                nodeTo = util.schema.getParentTabGroup(nodeTo)
            if util.schema.isTabGroup(nodeTo):
                nodeTo = util.schema.getTabs(nodeTo)[0]

            if nodeTo == None:
                continue
            if isNoWire(nodeTo):
                continue
            if isNoWire(nodeFrom):
                continue

            # Determine `idFrom` and `idTo`
            idFrom = GuiBlock.nodeId(nodeFrom)
            idTo   = GraphTab.nodeId(nodeTo  )

            # Make the link
            link = '%s -> %s [constraint=false]' % (idFrom, idTo)
            links.append(link)

        return links

    def getGraphConstrainingLinks(self, node):
        links = ['/* Graph-constraining links */']

        for n in node.xpath('//*[@l or @lc or @ll]'):
            # Determine `nodeFrom` and `nodeTo`
            nodeFrom = util.schema.getParentTabGroup(n)
            nodeTo   = util.schema.getLinkedNode(n)
            if not util.schema.isTabGroup(nodeTo):
                nodeTo = util.schema.getParentTabGroup(nodeTo)

            if nodeTo == None:
                continue
            if isNoWire(nodeTo):
                continue
            if isNoWire(nodeFrom):
                continue

            # Determine `idFrom` and `idTo`
            idFrom = GraphTabGroup.nodeIdAnchor(nodeFrom)
            idTo   = GraphTabGroup.nodeIdAnchor(nodeTo  )

            # Make the link
            link = '%s -> %s [style=invis]' % (idFrom, idTo)
            links.append(link)

        return links

    def toString(self):
        tabGroups = [tabGroup.toString() for tabGroup in self.tabGroups]
        tabGroups = ''.join(tabGroups)

        links = ['\n\t' + link for link in self.links] + ['\n']
        links = ''.join(links)

        out  = 'digraph {'
        out += self.topMatter
        out += tabGroups
        out += links
        out += '}'

        return out

################################################################################

class GraphTabGroup(object):
    prefix       = 'cluster_'
    prefix_anchor = 'cluster_anchor_'

    def __init__(self, node):
        self.node = node

        self.topMatter  = '\n\t\tlabel="%s"'
        self.topMatter %= util.gui.getLabel(node)
        self.topMatter += '\n\t\tbgcolor="lightblue"'
        self.topMatter += '\n'
        self.topMatter += '\n\t\t%s [label="" fixedsize=shape width=0 height=0]'
        self.topMatter %= self.nodeIdAnchor(node)
        self.topMatter += '\n'

        self.tabs = self.getTabs(node)

    @classmethod
    def nodeIdAnchor(cls, node):
        return "%s%s" % (cls.prefix_anchor, util.xml.nodeHash(node))

    @classmethod
    def nodeId(cls, node):
        return "%s%s" % (cls.prefix, util.xml.nodeHash(node))

    def getTabs(self, node):
        return [GraphTab(n) for n in util.gui.getTabs(node, isWire)]

    def toString(self):
        tabs = ''
        for i, tab in enumerate(self.tabs):
            hasPrecedingTab = i > 0
            hasFollowingTab = i < len(self.tabs) - 1
            tabs += tab.toString(hasPrecedingTab, hasFollowingTab)

        out  = '\n\tsubgraph %s {' % self.nodeId(self.node)
        out += self.topMatter
        out += tabs
        out += '\n\t}'
        out += '\n'

        return out

################################################################################

class GraphTab(object):
    prefix       = 'cluster_'
    prefix_label = 'struct_Label_'

    def __init__(self, node):
        self.node  = node

        self.label = util.gui.getLabel(node)

        self.topMatter  = '\n\t\t\tlabel=""'
        self.topMatter += '\n\t\t\tbgcolor="white"'
        self.topMatter += '\n'

        self.guiBlocks = self.getGuiBlocks(node)

    @classmethod
    def nodeId(cls, node):
        return cls.nodeIdLabel(node)

    @classmethod
    def nodeIdLabel(cls, node):
        return "%s%s" % (cls.prefix_label, util.xml.nodeHash(node))

    @classmethod
    def nodeIdElem (cls, node):
        return "%s%s" % (cls.prefix,       util.xml.nodeHash(node))

    def getGuiBlocks(self, node):
        isWireIsGui = lambda n: isWire(n) and util.gui.isGuiElement(n)
        return [GuiBlock(n) for n in node if isWireIsGui(n)]

    def getTabBarStructString(self, hasPrecedingTab, hasFollowingTab):
        out  = '\n\t\t\t%s [' % self.nodeIdLabel(self.node)
        out += '\n\t\t\tlabel=<'
        out += '\n\t\t\t\t<TABLE BORDER="1" CELLBORDER="3" CELLSPACING="0" CELLPADDING="5" WIDTH="150" HEIGHT="10">'
        out += '\n\t\t\t\t\t<TR>'
        out += '\n\t\t\t\t\t\t<TD SIDES="b" BORDER="1">...</TD>' if hasPrecedingTab else ''
        out += '\n\t\t\t\t\t\t<TD SIDES="b" ALIGN="TEXT">%s</TD>' % self.label
        out += '\n\t\t\t\t\t\t<TD SIDES="b" BORDER="1">...</TD>' if hasFollowingTab else ''
        out += '\n\t\t\t\t\t</TR>'
        out += '\n\t\t\t\t</TABLE>'
        out += '\n\t\t\t>];'
        out += '\n'

        return out

    def getGuiBlocksString(self):
        guiBlocks = [guiBlock.toString() for guiBlock in self.guiBlocks]
        guiBlocks = ''.join(guiBlocks)
        return guiBlocks

    def toString(self, hasPrecedingTab=False, hasFollowingTab=False):
        out  = '\n\t\tsubgraph %s {' % self.nodeIdElem(self.node)
        out += self.topMatter
        out += self.getTabBarStructString(hasPrecedingTab, hasFollowingTab)
        out += self.getGuiBlocksString()
        out += '\n\t\t}'
        out += '\n'

        return out

################################################################################

class GuiBlock(object):
    prefix_elem  = '_'
    prefix_block = 'struct_Elems_'

    def __init__(self, node):
        self.guiBlock = self.getBlock(node)

    @classmethod
    def nodeId(cls, node):
        return '%s:%s' % (cls.nodeIdBlock(node), cls.nodeIdElem(node))

    @classmethod
    def nodeIdBlock(cls, node):
        path = util.xml.getPath(node)
        path = path[:3]

        pathString = '/'.join(path)

        exp  = '/module/' + pathString
        matches = node.xpath(exp)
        if matches: match = matches[0]
        else:       match = None
        return "%s%s" % (cls.prefix_block, util.xml.nodeHash(match))

    @classmethod
    def nodeIdElem (cls, node):
        return "%s%s" % (cls.prefix_elem, util.xml.nodeHash(node))

    def getBlock(self, node):
        head  = '\n\t\t\t%s [' % GuiBlock.nodeIdBlock(node)
        head += '\n\t\t\tlabel=<'
        head += '\n\t\t\t\t<TABLE BORDER="0" CELLSPACING="0" WIDTH="150">'

        tail  = '\n\t\t\t\t</TABLE>'
        tail += '\n\t\t\t>];'
        tail += '\n'

        if node.attrib[RESERVED_XML_TYPE] in (TYPE_GUI_DATA, TYPE_AUTHOR, TYPE_TIMESTAMP):
            return head + self.getElementBlock(node) + tail
        if node.attrib[RESERVED_XML_TYPE] in (TYPE_COLS, TYPE_GPS):
            return head + self.getColsBlock   (node) + tail
        if node.attrib[RESERVED_XML_TYPE] == TYPE_GROUP:
            return ''

        msg  = 'An unexpected %s value was encountered: %s'
        msg %= (
                RESERVED_XML_TYPE,
                node.attrib[RESERVED_XML_TYPE]
        )
        raise ValueError(msg)

    def getElementBlock(self, node):
        guiBlock  = '\n\t\t\t\t\t<TR><TD PORT="%s"><IMG SRC="%s.svg"/></TD></TR>'
        guiBlock %= GuiBlock.nodeIdElem(node), util.schema.getPathString(node, '_')
        return guiBlock

    def getColsBlock(self, node):
        # TRANSFORMATION 1 (PREPARATION): Make a 2D array with the dimensions of
        # the desired table.
        numCols = len(node)
        numRows = max(node, key=lambda col: len(col)) # Get tallest column
        numRows = len(numRows)

        table   = [[None for i in range(numCols)] for j in range(numRows)]

        # TRANSFORMATION 1 (EXECUTION): Populate the table.
        for     i, col in enumerate(node):
            for j, elm in enumerate(col):
                table[j][i] = elm

        # TRANSFORMATION 2: Convert `table` to markup code.
        cellEmpty = '\n\t\t\t\t\t\t<TD></TD>'
        cellFull  = '\n\t\t\t\t\t\t<TD PORT="%s"><IMG SRC="%s.svg"></IMG></TD>'

        guiBlock = ''
        for row in table:
            tdElms = ''
            for elm in row:
                if   elm == None:
                    tdElms += cellEmpty
                elif util.schema.getUiType(elm) == UI_TYPE_GROUP:
                    tdElms += cellEmpty
                else:
                    id   = GuiBlock.nodeIdElem(elm)
                    path = util.schema.getPathString(elm, '_')

                    tdElms += cellFull % (id, path)

            guiBlock += '\n\t\t\t\t\t<TR>'
            guiBlock += tdElms
            guiBlock += '\n\t\t\t\t\t</TR>'

        return guiBlock

    def toString(self):
        return self.guiBlock

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
tree = util.schema.parseSchema(tree)

################################################################################
#                        GENERATE AND OUTPUT DATASTRUCT                        #
################################################################################
#print etree.tostring(
        #tree,
        #pretty_print=True,
        #xml_declaration=True,
        #encoding='utf-8'
#)

gm = GraphModule(tree)
print gm.toString()
