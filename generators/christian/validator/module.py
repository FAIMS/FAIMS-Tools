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

#def parseCommaSeparatedList(list, expansionIndex):
    #'''
    #Expands ['Element', 'b, c'] into [['Element', 'b'], ['Element', 'c']] when
    #expansionIndex is, for instance, 1.
    #'''
    #separatedList  = [x.strip() for x in list[expansionIndex].split(',')]

    #result = []
    #for str in separatedList:
        #copy = list[:]
        #copy[expansionIndex] = str
        #result.append(copy)

    #return result

#def flatten(list, times=1):
    #for i in range(times):
        #list = [val for sublist in list for val in sublist]
    #return list

#def expandCommaSeparatedList(list, depth=0, maxDepth=None):
    #'''
    #Expands list ['x, y', 'b, c'] into
    #[['x', 'b'], ['x', 'c'], ['y', 'b'], ['y', 'c']]
    #'''
    #if list == []:
        #return [[]]

    #if maxDepth == None:
        #length = len(list)
        #result = expandCommaSeparatedList(list, depth, length)
        #result = flatten(result, length-1)
        #return result

    #list = parseCommaSeparatedList(list, depth)
    #if depth + 1 < maxDepth:
        #for i in range(len(list)):
            #list[i] = expandCommaSeparatedList(list[i], depth+1, maxDepth)

    #return list

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

    # Special treatment of tables with cardinalities
    hasCardinalities = False
    for i in range(len(table)):
        for j in range(1, len(table[i])):
            if '<=' in table[i][j]:
                hasCardinalities |= True
    if hasCardinalities:
        for i in range(len(table)):
            for j in range(1, len(table[i])):
                regMin  = '(([0-9]+)\s+<=\s+)?'
                regType = '(\<?[a-zA-Z][a-zA-Z ]*[a-zA-Z]\>?)'
                regMax  = '(\s+<=\s+([0-9]+))?'
                reg     = regMin + regType + regMax
                m = re.search(reg, table[i][j])

                if m:
                    min  = m.group(2)
                    type = m.group(3)
                    max  = m.group(5)

                    if min:
                        min = int(min)
                    if max:
                        max = int(max)

                    lim = [min,  type, max]
                else:
                    lim = [None, None, None]

                table[i][j] = lim
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

def getAttributes(table, xmlType, rowAttribsIndex=1):
    for row in table:
        rowXmlType = row[0]
        rowAttribs = row[rowAttribsIndex]

        if type(rowAttribs) is not list:
            if not rowAttribs:
                rowAttribs = []
            else:
                rowAttribs = [rowAttribs]

        for i in range(len(rowAttribs)):
            if   rowAttribs[i] == '$link-all':
                rowAttribs[i] = 'a valid link to a tab or tab group'
            elif rowAttribs[i] == '$link-tabgroup':
                rowAttribs[i] = 'a valid link to a tab group'
            elif rowAttribs[i] == '$link-tab':
                rowAttribs[i] = 'a valid link to a tab'

        if rowXmlType == xmlType:
            return rowAttribs

def isValidLink(root, link, linkType):
    if not link:
        return False

    if   linkType == 'tab':
        result  = True
        try:
            result &= bool(root.xpath('/module/' + link))
        except:
            result &= False
        result &= '/'     in link
        result &= '/' != link[ 0]
        result &= '/' != link[-1]
        return result
    elif linkType == 'tabgroup':
        result  = True
        try:
            result &= bool(root.xpath('/module/' + link))
        except:
            result &= False
        result &= '/' not in link
        return result
    elif linkType == 'all':
        result  = False
        result |= isValidLink(root, link, 'tab'     )
        result |= isValidLink(root, link, 'tabgroup')
        return result
    else:
        return False

def disallowedAttribVals(m, ATTRIB_VALS):
    disallowed = []
    for attrib, oneOf, manyOf in ATTRIB_VALS:
        if attrib not in m.attrib: # Set intersection of attrib and m.attrib
            continue

        if oneOf:
            if '$link' in oneOf:
                link = m.attrib[attrib]
                linkType = oneOf[6:] # 'all', 'tab', or 'tabgroup'
                if not isValidLink(tree, link, linkType):
                    disallowed.append((attrib, m.attrib[attrib], m))
            else:
                if m.attrib[attrib] not in oneOf:
                    disallowed.append((attrib, m.attrib[attrib], m))
        if manyOf:
            for flag in m.attrib[attrib].split():
                if flag not in manyOf:
                    disallowed.append((attrib, flag,             m))
    return disallowed

def satisfiesCardinalityConstraint(parent, constraint, children='direct'):
    min, type, max = constraint
    if type == None:
        return True

    if children == 'direct':
        children = ''
    else:
        children = './/'
    matches = parent.xpath(
            '%s*[@%s="%s"]' %
            (children, typeAttribName, type)
    )

    if min != None and len(matches) < min: return False
    if max != None and len(matches) > max: return False
    return True

# English is dumb
def childWithGrammaticalNumber(number):
    if number == 1:
        return 'child'
    return 'children'
def descendantWithGrammaticalNumber(number):
    d = 'descendant'; s = 's'
    if number == 1:
        return d
    return  d + s
def descChildNounPhrase(child, number):
    if  childDirectness == 'direct':
        childNum = childWithGrammaticalNumber (number)
        return 'direct %s' % childNum
    else:
        return descendantWithGrammaticalNumber(number)

def guessType(node):
    isUser = 'f' in node.attrib and 'user' in node.attrib['f'].split()

    if isUser:
        return 'list'
    if node.xpath('opts') and     node.xpath('.//opt[@p]'):
        return 'picture'
    if node.xpath('opts') and not node.xpath('.//opt[@p]'):
        return 'dropdown'
    return 'input'

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

<cols>          | /[^a-z]/    | GUI element
<cols>          | col         | <col>

<col>           | /[^a-z]/    | GUI element

GUI element     | desc        | <desc>
GUI element     | opts        | <opts>
GUI element     | str         | <str>

<str>           | app         | <app>
<str>           | fmt         | <fmt>
<str>           | pos         | <pos>

<opts>          | opt         | <opt>

<opt>           | opt         | <opt>
'''

TYPES = parseTable(TYPES)
typeAttribName = '__RESERVED_XML_TYPE__'

ok = True
# Flag nodes with their TYPEs
for t in TYPES:
    parentType = t[0]
    pattern    = t[1]
    matchType  = t[2]
    print t

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
matches = tree.xpath(
        '//*[@%s="%s"]/*' %
        (typeAttribName, '<cols>')
)

# Nodes which didn't end up getting flagged aren't allowed
disallowed = tree.xpath(
        '//*[@%s]/*[not(@%s)]' %
        (typeAttribName, typeAttribName)
)
# Tell the user about the error(s)
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

# Only consider nodes flagged with `typeAttribName`
matches = tree.xpath(
        '//*[@%s]' %
        (typeAttribName)
)
# Determine if nodes contain an attibute not allowed according to ATTRIBS
disallowed = []
for m in matches:
    mAttribs     = dict(m.attrib)
    mXmlType     = mAttribs[typeAttribName]
    mAttribs.pop(typeAttribName, None)
    mAttribNames = mAttribs

    for mAttribName in mAttribNames:
        if not mAttribName in getAttributes(ATTRIBS, mXmlType):
            disallowed.append((mAttribName, m))
# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib = d[0]
    disallowedNode   = d[1]
    eMsg(
            'Attribute `%s` disallowed here' % disallowedAttrib,
            [disallowedNode],
            getAttributes(ATTRIBS, disallowedNode.attrib[typeAttribName])
    )
    countErr += 1; ok &= False

ATTRIB_VALS = '''
ATTRIBUTE    | ALLOWED VALUES (ONE-OF)     | ALLOWED VALUES (MANY-OF)
b            | date, decimal, string, time |
c            |                             |
f            |                             | autonum, hidden, id, noannotation, nocertainty, nodata, nolabel, noscroll, nosync, nothumb, nothumbnail, notnull, noui, readonly, user
l            | $link-all                   |
ec           | $link-tabgroup              |
lc           | $link-tabgroup              |
t            | audio, button, camera, checkbox, dropdown, file, gpsdiag, group, input, list, map, picture, radio, table, video, viewfiles, web, webview |
p            |                             |
'''
ATTRIB_VALS = parseTable(ATTRIB_VALS)

# Only consider nodes flagged with `typeAttribName`
matches = tree.xpath(
        '//*[@%s]' %
        (typeAttribName)
)
# Determine if attributes contain allowed values according to ATTRIB_VALS
disallowed = []
for m in matches:
    disallowed.extend(disallowedAttribVals(m, ATTRIB_VALS))

# Tell the user about the error(s)
for d in disallowed:
    disallowedAttrib    = d[0]
    disallowedAttribVal = d[1]
    disallowedNode      = d[2]

    allowedOneOf  = getAttributes(ATTRIB_VALS, disallowedAttrib, 1)
    allowedManyOf = getAttributes(ATTRIB_VALS, disallowedAttrib, 2)
    allowed       = allowedOneOf + allowedManyOf

    if   allowedOneOf:
        msg = 'Item `%s` in attribute %s is disallowed.  Exactly one item is expected'
    elif allowedManyOf:
        msg = 'Item `%s` in attribute %s is disallowed.  One or more items are expected'
    else:
        sys.stderr.write('Oops!')
        exit()

    eMsg(
            msg % (disallowedAttribVal, disallowedAttrib),
            [disallowedNode],
            allowed
    )
    countErr += 1; ok &= False

CARDINALITIES = '''
PARENT XML TYPE | DIRECT CHILD COUNT    | DESCENDANT COUNT
document        | 1 <= module <= 1      |

module          | 1 <= tabgroup         |
module          | 0 <= <logic> <= 1     |
module          | 0 <= <rels>  <= 1     |

tabgroup        | 1 <= tab              |
tabgroup        | 0 <= <desc>   <= 1    |
tabgroup        | 0 <= <search> <= 1    |

tab             |                       | 1 <= GUI element
tab             | 0 <= <autonum>   <= 1 |
tab             | 0 <= <cols>           |
tab             | 0 <= <gps>       <= 1 |
tab             | 0 <= <author>    <= 1 |
tab             | 0 <= <timestamp> <= 1 |

GUI element     | 0 <= <desc> <= 1      |
GUI element     | 0 <= <opts> <= 1      |
GUI element     | 0 <= <str>  <= 1      |

<cols>          |                       | 1 <= GUI element
<cols>          | 1 <= <col>            |

<opts>          | 1 <= <opt>            |

<str>           | 0 <= app <= 1         |
<str>           | 0 <= fmt <= 1         |
<str>           | 0 <= pos <= 1         |

<col>           | 1 <= GUI element      |

<opt>           | 0 <= <opt>            |
'''
CARDINALITIES = parseTable(CARDINALITIES)

# Only consider nodes flagged with `typeAttribName`
disallowed = []
for c in CARDINALITIES:
    parentTypeName        = c[0]
    directChildContraints = c[1]
    descendantContraints  = c[2]

    matches = tree.xpath(
            '//*[@%s="%s"]' %
            (typeAttribName, parentTypeName)
    )

    for m in matches:
        if not satisfiesCardinalityConstraint(m,  directChildContraints, 'direct'):
            disallowed.append((m, parentTypeName, directChildContraints, 'direct'))
        if not satisfiesCardinalityConstraint(m,  descendantContraints, 'descendant'):
            disallowed.append((m, parentTypeName, descendantContraints, 'descendant'))

for d in disallowed:
    node                = d[0]
    name                = node.tag
    typeParent          = d[1]
    min, typeChild, max = d[2]
    childDirectness     = d[3]

    if   min == None:
        nounPhrase = descChildNounPhrase(childDirectness, max)
        msg = 'Element `%s` of type %s requires at most %s %s of type %s' % \
        (name, typeParent,      max, nounPhrase, typeChild)
    elif max == None:
        nounPhrase = descChildNounPhrase(childDirectness, min)
        msg = 'Element `%s` of type %s requires at least %s %s of type %s' % \
        (name, typeParent, min,      nounPhrase, typeChild)
    else:
        pluralNumber = 2
        nounPhrase = descChildNounPhrase(childDirectness, pluralNumber)
        msg = 'Element `%s` of type %s requires between %s and %s %s (inclusive) of type %s' % \
        (name, typeParent, min, max, nounPhrase, typeChild)
    eMsg(
            msg,
            [node]
    )
    countErr += 1; ok &= False

matches = tree.xpath(
        '//*[@%s="%s" and not(@t)]' %
        (typeAttribName, 'GUI element')
)
for m in matches:
    m.attrib['t'] = guessType(m)
    wMsg(
            'No value for the attribute t of the element `%s` is present.  Assuming a value of `%s`' %
            (m.tag, m.attrib['t']),
            [m]
    )
    countWar += 1; ok &= True


exit()

# TODO
for d in disallowed:
    'Element `%s` is duplicated or results in duplicate properties when the data schema is generated' % d.tag
    'Element `%s` is duplicated or results in duplicate GUI elements when the UI schema is generated' % d.tag
    eMsg(
            'Element `%s` is duplicated or results in duplicate GUI elements when the UI schema is generated' % d.tag
            [disallowedNode],
            allowed
    )
    countErr += 1; ok &= False

if not ok:
    bye(countWar, countErr)
exit()















ds = getDuplicates(tgs)
for d in ds:
    tag = d[0].tag
    eMsg(
            "Tabgroup element name `%s` cannot be duplicated in module" % tag,
            d
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
    ds = getDuplicates(ts)
    for d in ds:
        tag = d[0].tag
        eMsg(
                "Tab element name `%s` cannot be duplicated in tabgroup" % tag,
                d
        )
        countErr += 1; ok &= False

bye(countWar, countErr)
