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
    for i in t:
        print type(i)
    nodes = [i for i in t if re.match('[^a-z]', i.tag)] # Might be failing due to comments
    return nodes

def wMsg(notice, nodes, expected=None):
    notice = "WARNING: " + notice
    printNotice(notice, nodes, expected)

def eMsg(notice, nodes, expected=None):
    notice = "ERROR:   " + notice
    printNotice(notice, nodes, expected)

def printNotice(notice, nodes, expected=None):
    notice = notice + "."

    if   expected == None:
        pass
    elif len(expected) == 1:
        expected = 'Expected ' + expected[0] + '.'
    else:
        expected = 'Expected one of:\n  - ' + '\n  - '.join(expected)

    if len(nodes) == 0:
        print notice + "."
    if len(nodes) == 1:
        print notice + ". Occurs at line " + str(node.sourceline) + "."
    if len(nodes) >= 2:
        print notice + ". Occurs at:"
        for node in nodes:
            print "    - Line " + str(node.sourceline)
    print

    if len(nodes) == 0:
        print notice + "."
    if len(nodes) == 1:
        print notice + ". Occurs at line " + str(node.sourceline) + "."
    if len(nodes) >= 2:
        print notice + ". Occurs at:"
        for node in nodes:
            print "    - Line " + str(node.sourceline)
    print


def bye(countWar, countErr, early=True):
    print "Validation completed with %i error(s) and %i warning(s)." \
            % (countErr, countWar)
    exit()

def parseTable(table):
    table = table.strip()
    table = table.split('\n')
    table = table[1:]
    table = [re.split(' *\| *', i) for i in table]
    table = [i for i in table if i != ['']]
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
        parentType = t[0]
        pattern    = t[1]
        matchType  = t[2]

        if parent.attrib[attribType] != parentType:
            continue

        if reserved:
            regex = '[^a-z]'
        else:
            regex = '^[a-z]+$'

        if re.match(regex, matchType):
            expected.append(matchType)

    return expected

################################################################################
#                                     MAIN                                     #
################################################################################

filenameModule = sys.argv[1]

################################## PARSE XML ###################################
print "Parsing XML..."
parser = etree.XMLParser(strip_cdata=False)
try:
    tree = etree.parse(filenameModule, parser)
except etree.XMLSyntaxError as e:
    print e
    exit()
tree = tree.getroot()
print "Done!"
print

############################### VALIDATE SCHEMA ################################
print "Validating schema..."
countWar = 0
countErr = 0

TYPES = '''
PARENT XML TYPE | PATTERN     | MATCH XML TYPE
Document        | /           | Module

Module          | /[^a-z]/    | Tabgroup
Module          | logic       | Logic
Module          | rels        | Rels

Tabgroup        | /[^a-z]/    | Tab
Tabgroup        | desc        | Desc
Tabgroup        | search      | Search

Tab             | /[^a-z]/    | Element
Tab             | autonum     | Autonum
Tab             | cols        | Cols
Tab             | gps         | GPS
Tab             | author      | Author
Tab             | timestamp   | Timestamp

Element         | desc        | Desc
Element         | opts        | Opts
Element         | str         | Str

Cols            | /[^a-z]/    | Element
Cols            | col         | Col

Opts            | opt         | Opt

Str             | app         | App
Str             | fmt         | Fmt
Str             | pos         | Pos

Col             | /[^a-z]/    | Element

Opt             | opt         | Opt
'''

TYPES = parseTable(TYPES)
attribType = '__RESERVED_XML_TYPE__'
for t in TYPES:
    parentType = t[0]
    pattern      = t[1]
    matchType  = t[2]

    if   pattern == '/':
        matches = tree.xpath('/*')
        flagAll(matches, attribType, matchType)
    elif pattern == '/[^a-z]/':
        matches = tree.xpath(
                '//*[@%s="%s"]/*' %
                (attribType, parentType)
        )
        matches = getNonLower(matches)
        flagAll(matches, attribType, matchType)
    else:
        matches = tree.xpath(
                '//*[@%s="%s"]/%s' %
                (attribType, parentType, pattern)
        )
        flagAll(matches, attribType, matchType)

print(etree.tostring(tree, pretty_print=True))

disallowed = tree.xpath('//*[@%s]/*[not(@%s)]' % (attribType, attribType))
disallowedLowers = getLower(disallowed)
disallowedUppers = getNonLower(disallowed)
for d in disallowedLowers:
    eMsg(
            'Not a valid reserved tag',
            [d]
    )
    countErr += 1; ok &= False
for d in disallowedUppers:

    eMsg(
            "Not a valid %s tag" % expectedType,
            [tree]
    )
    countErr += 1; ok &= False



print(etree.tostring(tree, pretty_print=True))
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
