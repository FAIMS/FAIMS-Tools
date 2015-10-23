import re
from lxml import etree
import sys

def getDuplicates(l):
    '''
    Example:
      input:
        <root>
          <A/>
          <C/>
          <B/>
          <B/>
          <B/>
          <C/>
        </root>
      return value:
      [
        [<C Element>, <C Element>],
        [<B Element>, <B Element>, <B Element>]
      ]
    '''
    tags = set([n.tag for n in l])
    tags = list(tags)

    nodesByTag = {}
    for t in tags:
        nodesByTag[t] = []
    for n in l:
        nodesByTag[n.tag].append(n)

    duplicates = [] # List of lists
    for nodes in nodesByTag.itervalues():
        if len(nodes) >= 2:
            duplicates.append(nodes)

    duplicates.sort(key=lambda listOfDuplicates: listOfDuplicates[0].sourceline)

    return duplicates

def getLower(t):
    nodes = [i for i in t if re.match('^[a-z]+$', i.tag)]
    return nodes

def getNonLower(t):
    #for i in t:
        #print type(i)
    nodes = [i for i in t if re.match('[^a-z]', i.tag)] # Might be failing due to comments
    return nodes

def wMsg(notice, nodes, expected=[]):
    notice = 'WARNING: ' + notice
    printNotice(notice, nodes, expected)

def eMsg(notice, nodes, expected=[]):
    notice = 'ERROR:   ' + notice
    printNotice(notice, nodes, expected)

def printNotice(notice, nodes, expected=[]):
    notice = notice + '.  '

    if   len(expected) == 0:
        expected = ''
    elif len(expected) == 1:
        expected = 'Allowed item is %s.  ' % expected[0]
    else:
        expected = 'Allowed items are:\n  - ' + '\n  - '.join(expected) + '\n'

    if len(nodes) == 0:
        location = ''
    if len(nodes) == 1:
        location = 'Occurs at line ' + str(nodes[0].sourceline) + '.  '
    if len(nodes) >= 2:
        location = 'Occurs at:'
        for node in nodes:
            location += '\n  - Line ' + str(node.sourceline)

    print notice + expected + location
    print


def bye(countWar, countErr, early=True):
    print 'Validation completed with %i error(s) and %i warning(s).' \
            % (countErr, countWar)
    exit()

def parseCommaSeparatedList(list, expansionIndex):
    '''
    Expands ['Element', 'b, c'] into [['Element', 'b'], ['Element', 'c']] when
    expansionIndex is, for instance, 1.
    '''
    separatedList  = [x.strip() for x in list[expansionIndex].split(',')]

    result = []
    for str in separatedList:
        copy = list[:]
        copy[expansionIndex] = str
        result.append(copy)

    return result

def flatten(list, times=1):
    for i in range(times):
        list = [val for sublist in list for val in sublist]
    return list

def expandCommaSeparatedList(list, depth=0, maxDepth=None):
    '''
    Expands list ['x, y', 'b, c'] into
    [['x', 'b'], ['x', 'c'], ['y', 'b'], ['y', 'c']]
    '''
    if list == []:
        return [[]]

    if maxDepth == None:
        length = len(list)
        result = expandCommaSeparatedList(list, depth, length)
        result = flatten(result, length-1)
        return result

    list = parseCommaSeparatedList(list, depth)
    if depth + 1 < maxDepth:
        for i in range(len(list)):
            list[i] = expandCommaSeparatedList(list[i], depth+1, maxDepth)

    return list

def parseTable(table):
    table = table.strip()
    table = table.split('\n')
    table = table[1:]
    table = [re.split(' *\| *', i) for i in table]
    table = [i for i in table if i != ['']]
    for rowIdx in range(len(table)):
        for colIdx in range(len(table[rowIdx])):
            cell = table[rowIdx][colIdx]
            if re.match('.*,', cell):
                table[rowIdx][colIdx] = [x.strip() for x in cell.split(',')]
    return table

def flagAll(nodes, attrib, value):
    for n in nodes:
        n.attrib[attrib] = value

def getExpectedTypes(table, node, reserved=False):
    attribType = '__RESERVED_XML_TYPE__'

    parent = node.getparent()

    # Get expected type(s)
    expected = []
    for row in table:
        parentType = row[0]
        pattern    = row[1]
        matchType  = row[2]

        if parent.attrib[attribType] != parentType:
            continue

        if   reserved == True:
            regex = '[^a-z]'
        elif reserved == False:
            regex = '^[a-z]+$'
        elif reserved == None:
            regex = '.*'
        else:
            continue

        if re.match(regex, matchType):
            expected.append(matchType)

    return expected

def getAttributes(table, xmlType):
    for row in table:
        rowXmlType = row[0]
        rowAttribs = row[1]

        if type(rowAttribs) is not list:
            if not rowAttribs:
                rowAttribs = []
            else:
                rowAttribs = [rowAttribs]

        if rowXmlType == xmlType:
            return rowAttribs

################################################################################
#                                     MAIN                                     #
################################################################################

filenameModule = sys.argv[1]

################################## PARSE XML ###################################
print 'Parsing XML...'
parser = etree.XMLParser(strip_cdata=False)
try:
    tree = etree.parse(filenameModule, parser)
except etree.XMLSyntaxError as e:
    print e
    exit()
tree = tree.getroot()
print 'Done!'
print

############################### VALIDATE SCHEMA ################################
print 'Validating schema...'
countWar = 0
countErr = 0

TYPES = '''
PARENT XML TYPE | PATTERN     | MATCH XML TYPE
document        | /           | module

module          | /[^a-z]/    | tabgroup
module          | logic       | <logic>
module          | rels        | <rels>

tabgroup        | /[^a-z]/    | tab
tabgroup        | desc        | <desc>
tabgroup        | search      | <search>

tab             | /[^a-z]/    | GUI element
tab             | author      | <author>
tab             | autonum     | <autonum>
tab             | cols        | <cols>
tab             | gps         | <gps>
tab             | timestamp   | <timestamp>

GUI element     | desc        | <desc>
GUI element     | opts        | <opts>
GUI element     | str         | <str>

<cols>          | /[^a-z]/    | GUI Element
<cols>          | col         | <col>

<opts>          | opt         | <opt>

<str>           | app         | <app>
<str>           | fmt         | <fmt>
<str>           | pos         | <pos>

<col>           | /[^a-z]/    | <element>

<opt>           | opt         | <opt>
'''

TYPES = parseTable(TYPES)
typeAttribName = '__RESERVED_XML_TYPE__'

ok = True
for t in TYPES:
    parentType = t[0]
    pattern    = t[1]
    matchType  = t[2]

    if   pattern == '/':
        matches = tree.xpath('/*')
        flagAll(matches, typeAttribName, matchType)
    elif pattern == '/[^a-z]/':
        matches = tree.xpath(
                '//*[@%s="%s"]/*' %
                (typeAttribName, parentType)
        )
        matches = getNonLower(matches)
        flagAll(matches, typeAttribName, matchType)
    else:
        matches = tree.xpath(
                '//*[@%s="%s"]/%s' %
                (typeAttribName, parentType, pattern)
        )
        flagAll(matches, typeAttribName, matchType)

disallowed = tree.xpath(
        '//*[@%s]/*[not(@%s)]' %
        (typeAttribName, typeAttribName)
)
for d in disallowed:
    eMsg(
            'Element `%s` disallowed here' % d.tag,
            [d],
            getExpectedTypes(TYPES, d, None)
    )
    countErr += 1; ok &= False




ATTRIBS = '''
XML TYPE      | ATTRIBUTES ALLOWED
module        |
tabgroup      | f
tab           | f
GUI element   | b, c, ec, f, l, lc, t
<cols>        | f
<opts>        |
<str>         |
<col>         | f
<opt>         | p
<app>         |
<author>      |
<autonum>     |
<desc>        |
<fmt>         |
<gps>         |
<logic>       |
<pos>         |
<rels>        |
<search>      |
<timestamp>   |
'''
ATTRIBS = parseTable(ATTRIBS)

matches = tree.xpath(
        '//*[@%s]' %
        (typeAttribName)
)

disallowed = []
for m in matches:
    mAttribs     = dict(m.attrib)
    mXmlType     = mAttribs[typeAttribName]
    mAttribs.pop(typeAttribName, None)
    mAttribNames = mAttribs

    for mAttribName in mAttribNames:
        if not mAttribName in getAttributes(ATTRIBS, mXmlType):
            disallowed.append((mAttribName, m))

for d in disallowed:
    disallowedAttrib = d[0]
    disallowedNode   = d[1]
    eMsg(
            'Attribute `%s` disallowed here' % disallowedAttrib,
            [disallowedNode],
            getAttributes(ATTRIBS, disallowedNode.attrib[typeAttribName])
    )
    countErr += 1; ok &= False

if not ok:
    bye(countWar, countErr)
exit()















ok = True
allowedLowers = ['logic', 'rels']

tgs = getNonLower(tree)
if not tgs:
    eMsg(
            "Module must contain at least one tabgroup",
            [tree]
    )
    countErr += 1; ok &= False

ds = getDuplicates(tgs)
for d in ds:
    tag = d[0].tag
    eMsg(
            "Tabgroup element name `%s` cannot be duplicated in module" % tag,
            d
    )
    countErr += 1; ok &= False

ns = getLower(tree)
for n in ns:
    if n.tag in allowedLowers: continue
    eMsg(
            "Element `%s` not allowed here" % n.tag,
            [n]
    )
    countErr += 1; ok &= False

ds = getDuplicates(ns)
for d in ds:
    tag = d[0].tag
    eMsg(
            "Reserved element name `%s` cannot be duplicated here" % tag,
            d
    )
    countErr += 1; ok &= False

# "BLOCKING POINT" - CANNOT CONTINUE VALIDATION UNLESS ok==TRUE
if not ok:
    bye(countWar, countErr)
ok = True
allowedLowers = ['desc', 'search']

tgs = getNonLower(tree)
for tg in tgs:
    ts = getNonLower(tg)
    if not ts:
        eMsg(
                "Tabgroup `%s` must contain at least one tab" % tg.tag,
                [tg]
        )
        countErr += 1; ok &= False

    ds = getDuplicates(ts)
    for d in ds:
        tag = d[0].tag
        eMsg(
                "Tab element name `%s` cannot be duplicated in tabgroup" % tag,
                d
        )
        countErr += 1; ok &= False

    ns = getLower(tg)
    for n in ns:
        if n.tag in allowedLowers: continue
        eMsg(
                "Element `%s` not allowed here" % n.tag,
                [n]
        )
        countErr += 1; ok &= False

    ds = getDuplicates(ns)
    for d in ds:
        tag = d[0].tag
        eMsg(
                "Reserved element `%s` cannot be duplicated here" % tag,
                d
        )
        countErr += 1; ok &= False

# "BLOCKING POINT" - CANNOT CONTINUE VALIDATION UNLESS ok==TRUE
if not ok:
    bye(countWar, countErr)
ok = True
allowedLowers = ['author', 'autonum', 'cols', 'gps', 'timestamp']

tgs = getNonLower(tree)
ts = []
for tg in tgs:
    ts += getNonLower(tg)
for t in ts:
    print t.tag
    gs = getNonLower(t)
    #if not gs:
        #eMsg(
                #"Tab `%s` must contain at least one GUI element" % t.tag
                #[t]
        #)
        #countErr += 1; ok &= False

    #ds = getDuplicates(gs)
    #for d in ds:
        #tag = d[0].tag
        #eMsg(
                #"GUI element name `%s` cannot be duplicated in tab" % tag,
                #d
        #)
        #countErr += 1; ok &= False

    #ns = getLower(t)
    #for n in ns:
        #tag = n.tag
        #if tag in allowedLowers: continue
        #eMsg(
                #"Element `%s` not allowed here" % tag,
                #[n]
        #)
        #countErr += 1; ok &= False

    #ds = getDuplicates(ns)
    #for d in ds:
        #tag = d[0].tag
        #eMsg(
                #"Reserved element `%s` cannot be duplicated here" % tag,
                #d
        #)
        #countErr += 1; ok &= False

bye(countWar, countErr)
