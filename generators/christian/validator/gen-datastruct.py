#!/usr/bin/env python

from   lxml import etree
import consts
import copy
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
        self.addLinks    (node)

    def addTabGroups(self, node):
        matches = getUiNodes(node, 'tab group')
        for m in matches:
            graphTabGroup = GraphTabGroup(m)
            self.tabGroups.append(graphTabGroup)

    def addLinks(self, node):
        self.addTabLabelLinks     (node)
        self.addUserSpecifiedLinks(node)

    def addTabLabelLinks(self, node):
        links = []

        tabGroups = getUiNodes(node, 'tab group')
        for tabGroup in tabGroups:
            tabs = getUiNodes(tabGroup, 'tab')
            for i in range(len(tabs) - 1):
                tabFrom = tabs[i  ]; idFrom = GraphTab.nodeId(tabFrom)
                tabTo   = tabs[i+1]; idTo   = GraphTab.nodeId(tabTo  )
                link = '%s -> %s' % (idFrom, idTo)
                links.append(link)

        self.links.append('/* Tab label links */')
        self.links += links

    def addUserSpecifiedLinks(self, node):
        links = []

        for n in node.xpath('//*[@l or @lc]'):
            # Does `n` have an 'l' attribute, or an 'lc' attribute?
            if helpers.hasAttrib(n, 'l' ): attrib = 'l'
            if helpers.hasAttrib(n, 'lc'): attrib = 'lc'

            # Determine `nodeFrom` and `nodeTo`
            nodeFrom = n; parFrom = n.getparent()
            if   helpers.isValidLink(n, n.attrib[attrib], 'tab'):
                nodeTo = n.xpath('/module/%s' % n.attrib[attrib])[0]
            else:
                nodeTo = n.xpath('/module/%s/*[1]' % n.attrib[attrib])[0]

            # Determine `idFrom` and `idTo`
            idFrom  = '%s:%s'
            idFrom %= (GraphTab.nodeId(parFrom), GuiBlock.nodeId(nodeFrom))
            idTo    =  GraphTab.nodeId(nodeTo )

            # Make the link
            link = '%s -> %s' % (idFrom, idTo)
            links.append(link)

        self.links.append('/* User-specified links */')
        self.links += links

    def toString(self):
        tabGroups = ''
        links     = ''
        for tabGroup in self.tabGroups: tabGroups += tabGroup.toString()
        for link     in self.links:     links     += '\n\t' + link
        links += '\n'

        out  = 'digraph {'
        out += self.topMatter
        out += tabGroups
        out += links
        out += '}'

        return out

################################################################################

class GraphTabGroup(object):
    prefix = 'cluster_'

    def __init__(self, node):
        self.name  = helpers.nodeHash(node)
        self.label = helpers.getLabel(node)

        self.topMatter  = '\n\t\tlabel="%s"' % self.label
        self.topMatter += '\n\t\tbgcolor="lightblue"'
        self.topMatter += '\n'

        self.tabs = []

        self.addTabs(node)

    @classmethod
    def nodeId(cls, node):
        return "%s%s" % (GraphTabGroup.prefix, helpers.nodeHash(node))

    def addTabs(self, node):
        matches = getUiNodes(node, 'tab')
        for m in matches:
            graphTab = GraphTab(m)
            self.tabs.append(graphTab)

    def toString(self):
        tabs = ''
        for i, tab in enumerate(self.tabs):
            hasPrecedingTab = i > 0
            hasFollowingTab = i < len(self.tabs) - 1
            tabs += tab.toString(hasPrecedingTab, hasFollowingTab)

        out  = '\n\tsubgraph %s%s {' % (GraphTabGroup.prefix, self.name)
        out += self.topMatter
        out += tabs
        out += '\n\t}'
        out += '\n'

        return out

################################################################################

class GraphTab(object):
    prefix       = 'cluster_'
    prefix_label = 'struct_Label_'
    prefix_elems = 'struct_Elems_'

    def __init__(self, node):
        self.name  = helpers.nodeHash(node)
        self.label = helpers.getLabel(node)

        self.topMatter  = '\n\t\t\tlabel=""'
        self.topMatter += '\n\t\t\tbgcolor="white"'
        self.topMatter += '\n'

        self.guiBlocks = []

        self.addGuiBlocks(node)

    @classmethod
    def nodeId(cls, node):
        return "%s%s" % (GraphTab.prefix_label, helpers.nodeHash(node))

    def addGuiBlocks(self, node):
        matches  = getUiNodes(node, 'GUI/data element')
        matches += getUiNodes(node, '<cols>')
        matches  = sorted(matches, key=lambda e: e.getparent().index(e))
        for m in matches:
            guiBlock = GuiBlock(m)
            self.guiBlocks.append(guiBlock)

    def getTabBarStructString(self, hasPrecedingTab, hasFollowingTab):
        out  = '\n\t\t\t%s%s [' % (GraphTab.prefix_label, self.name)
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
        if not self.guiBlocks:
            return ''

        guiBlocks = ''
        for guiBlock in self.guiBlocks:
            guiBlocks += guiBlock.toString()

        out  = '\n\t\t\t%s%s [' % (GraphTab.prefix_elems, self.name)
        out += '\n\t\t\tlabel=<'
        out += '\n\t\t\t\t<TABLE BORDER="0" CELLSPACING="0" WIDTH="150">'
        out += guiBlocks
        out += '\n\t\t\t\t</TABLE>'
        out += '\n\t\t\t>];'
        out += '\n'

        return out

    def toString(self, hasPrecedingTab=False, hasFollowingTab=False):
        out  = '\n\t\tsubgraph %s%s {' % (GraphTab.prefix, self.name)
        out += self.topMatter
        out += self.getTabBarStructString(hasPrecedingTab, hasFollowingTab)
        out += self.getGuiBlocksString()
        out += '\n\t\t}'
        out += '\n'

        return out

################################################################################

class GuiBlock(object):
    prefix = '_'

    def __init__(self, node):
        self.block = ''

        self.addBlock(node)

    @classmethod
    def nodeId(cls, node):
        return "%s%s" % (GuiBlock.prefix, helpers.nodeHash(node))

    def addBlock(self, node):
        if   node.attrib[consts.RESERVED_XML_TYPE] == 'GUI/data element':
            self.addElement(node)
        elif node.attrib[consts.RESERVED_XML_TYPE] == '<cols>':
            self.addCols(node)
        else:
            msg  = 'An unexpected %s value was encountered'
            msg %= consts.RESERVED_XML_TYPE
            raise ValueError(msg)

    def addElement(self, node):
        self.block  = '\n\t\t\t\t\t<TR><TD><IMG PORT="%s%s" SRC="%s.svg"/></TD></TR>'
        self.block %= GuiBlock.prefix, helpers.nodeHash(node), node.tag

    def addCols(self, node):
        # What we're about to do will probably modify `node` if we don't copy it
        node = copy.deepcopy(node)

        # NORMALISATION: Take GUI/data elements which are direct descendants of
        # <cols> and put them in <col> tags.
        for i, child in enumerate(node):
            if child.attrib[consts.RESERVED_XML_TYPE] == 'GUI/data element':
                node[i] = etree.Element('col')
                node[i].append(child)

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
        self.block = ''
        for row in table:
            tdElms = ''
            for elm in row:
                if   elm == None:
                    tdElms += '\n\t\t\t\t\t\t<TD></TD>'
                else:
                    tdElms += '\n\t\t\t\t\t\t<TD><IMG PORT="%s%s" SRC="%s.svg"></IMG></TD>'
                    tdElms %= (GuiBlock.prefix, helpers.nodeHash(elm), elm.tag)

            self.block += '\n\t\t\t\t\t<TR>'
            self.block += tdElms
            self.block += '\n\t\t\t\t\t</TR>'

    def toString(self):
        return self.block

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = helpers.parseXml(filenameModule)
helpers.normaliseAttributes(tree)
helpers.annotateWithTypes(tree)
helpers.expandCompositeElements(tree)

################################################################################
#                        GENERATE AND OUTPUT DATASTRUCT                        #
################################################################################
gm = GraphModule(tree)
print gm.toString()
