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

        self.tabGroups = self.getTabGroups(node)
        self.links     = self.getLinks    (node)

    def getTabGroups(self, node):
        return [GraphTabGroup(n) for n in getUiNodes(node, 'tab group')]

    def getLinks(self, node):
        links  = self.getTabLabelLinks     (node)
        links += self.getUserSpecifiedLinks(node)
        return links

    def getTabLabelLinks(self, node):
        links = ['/* Tab label links */']

        tabGroups = getUiNodes(node, 'tab group')
        for tabGroup in tabGroups:
            tabs = getUiNodes(tabGroup, 'tab')
            for i in range(len(tabs) - 1):
                tabFrom = tabs[i  ]; idFrom = GraphTab.nodeId(tabFrom)
                tabTo   = tabs[i+1]; idTo   = GraphTab.nodeId(tabTo  )
                link = '%s -> %s' % (idFrom, idTo)
                links.append(link)

        return links

    def getUserSpecifiedLinks(self, node):
        links = ['/* User-specified links */']

        for n in node.xpath('//*[@l or @lc]'):
            # Does `n` have an 'l' attribute, or an 'lc' attribute?
            if helpers.hasAttrib(n, 'l' ): attrib = 'l'
            if helpers.hasAttrib(n, 'lc'): attrib = 'lc'

            # Determine `nodeFrom` and `nodeTo`
            nodeFrom = n; parFrom = n.getparent()
            if helpers.isValidLink(n, n.attrib[attrib], 'tab group'):
                exp     = '/module/%s/*[@%s="%s"][1]'
            if helpers.isValidLink(n, n.attrib[attrib], 'tab'):
                exp     = '/module/%s[@%s="%s"]'
            exp    %= n.attrib[attrib], consts.RESERVED_XML_TYPE, 'tab'
            matches = n.xpath(exp)
            nodeTo  = matches[0]

            # Determine `idFrom` and `idTo`
            idFrom = GuiBlock.nodeId(nodeFrom)
            idTo   = GraphTab.nodeId(nodeTo  )

            # Make the link
            link = '%s -> %s' % (idFrom, idTo)
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
    prefix = 'cluster_'

    def __init__(self, node):
        self.node = node

        self.topMatter  = '\n\t\tlabel="%s"' % helpers.getLabel(node)
        self.topMatter += '\n\t\tbgcolor="lightblue"'
        self.topMatter += '\n'

        self.tabs = self.getTabs(node)

    @classmethod
    def nodeId(cls, node):
        return "%s%s" % (cls.prefix, helpers.nodeHash(node))

    def getTabs(self, node):
        return [GraphTab(n) for n in getUiNodes(node, 'tab')]

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

        self.label = helpers.getLabel(node)

        self.topMatter  = '\n\t\t\tlabel=""'
        self.topMatter += '\n\t\t\tbgcolor="white"'
        self.topMatter += '\n'

        self.guiBlocks = self.getGuiBlocks(node)

    @classmethod
    def nodeId(cls, node):
        return cls.nodeIdLabel(node)

    @classmethod
    def nodeIdLabel(cls, node):
        return "%s%s" % (cls.prefix_label, helpers.nodeHash(node))

    @classmethod
    def nodeIdElem (cls, node):
        return "%s%s" % (cls.prefix,       helpers.nodeHash(node))

    def getGuiBlocks(self, node):
        matches  = getUiNodes(node, 'GUI/data element')
        matches += getUiNodes(node, '<cols>')
        matches  = sorted(matches, key=lambda e: e.getparent().index(e))
        return [GuiBlock(n) for n in matches]

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
        exp     = './descendant-or-self::*[@%s="%s"][1]'
        exp    %= consts.RESERVED_XML_TYPE, 'GUI/data element'
        matches = node.xpath(exp)
        match   = matches[0]
        return "%s%s" % (cls.prefix_block, helpers.nodeHash(match))

    @classmethod
    def nodeIdElem (cls, node):
        return "%s%s" % (cls.prefix_elem , helpers.nodeHash(node))

    def getBlock(self, node):
        head  = '\n\t\t\t%s [' % GuiBlock.nodeIdBlock(node)
        head += '\n\t\t\tlabel=<'
        head += '\n\t\t\t\t<TABLE BORDER="0" CELLSPACING="0" WIDTH="150">'

        tail  = '\n\t\t\t\t</TABLE>'
        tail += '\n\t\t\t>];'
        tail += '\n'

        if node.attrib[consts.RESERVED_XML_TYPE] == 'GUI/data element':
            return head + self.getElementBlock(node) + tail
        if node.attrib[consts.RESERVED_XML_TYPE] == '<cols>':
            return head + self.getColsBlock   (node) + tail

        msg  = 'An unexpected %s value was encountered'
        msg %= consts.RESERVED_XML_TYPE
        raise ValueError(msg)

    def getElementBlock(self, node):
        guiBlock  = '\n\t\t\t\t\t<TR><TD PORT="%s"><IMG SRC="%s.svg"/></TD></TR>'
        guiBlock %= GuiBlock.nodeIdElem(node), helpers.getPathString(node, '_')
        return guiBlock

    def getColsBlock(self, node):
        # What we're about to do will probably modify `node` if we don't copy
        # it.
        nodeCopy = copy.deepcopy(node)

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
        guiBlock = ''
        for row in table:
            tdElms = ''
            for elm in row:
                if   elm == None:
                    tdElms += '\n\t\t\t\t\t\t<TD></TD>'
                else:
                    tdElms += '\n\t\t\t\t\t\t<TD PORT="%s"><IMG SRC="%s.svg"></IMG></TD>'
                    tdElms %= GuiBlock.nodeIdElem(node), helpers.getPathString(elm, '_')

            guiBlock += '\n\t\t\t\t\t<TR>'
            guiBlock += tdElms
            guiBlock += '\n\t\t\t\t\t</TR>'

        node[:] = nodeCopy
        return guiBlock

    def toString(self):
        return self.guiBlock

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
