from   lxml import etree
import json
import sys
import urllib2

def makeTree():
    root = etree.Element('dataSchema')
    return root

def insertIntoTree(row, xmlTree):
    if xmlTree == None:
        xmlTree = makeTree()

    node = rowToNode(row)
    xmlTree = mergeTrees(node, xmlTree)

    return xmlTree

# Parse a string of semicolon-delimited values into a python list
def parseList(listString, delim=';'):
    list = listString.split(delim)
    for i in range(len(list)):# Remove surrounding whitespace for each item
        list[i] = list[i].strip()
    list = filter(None, list) # Remove empty strings

    return list

def rowToNode(row):
    arch16nKey   = getRowValue(row, 'faimsVocab')
    archentNames = getRowValue(row, 'attributeLocation')
    countOrder   = getRowValue(row, 'VocabCountOrder')
    descProp     = getRowValue(row, 'AttributeDescription')
    descVocab    = getRowValue(row, 'VocabDescription')
    infoPictures = getRowValue(row, 'infoFilenames')
    parentVocab  = getRowValue(row, 'parentVocabularyName')
    pictureUrl   = getRowValue(row, 'pictureFilename')
    propertyName = getRowValue(row, 'faimsEntityAttributeName')

    archentNames = parseList(archentNames)
    infoPictures = parseList(infoPictures)

    root = makeTree()
    for n in archentNames:
        # MAKE A NODE

        # Make Arch element
        archEl = etree.SubElement(
                root,
                'ArchaeologicalElement',
                name=n
        )

        # Put property in arch element
        prop   = etree.SubElement(
                archEl,
                'property',
                name=propertyName
        )

        # Put description in property
        descPr = etree.SubElement(
                prop,
                'description'
        )
        s  = '\n'
        s += '<div>\n'
        #s += '    <h1>' + arch16nKey + '</h1>\n'
        s += '    <p>'  + descProp   + '</p>\n'
        s += '    <hr/>\n'
        s += '</div>\n'
        if descProp:
            descPr.text = etree.CDATA(s)

        # Put lookup in property
        lookup = etree.SubElement(
                prop,
                'lookup'
        )

        # Put term in lookup
        term   = etree.SubElement(
                lookup,
                'term',
                __RESERVED_POS__=countOrder,
                __RESERVED_PAR__=parentVocab,
                pictureURL=pictureUrl
        )
        term.text = arch16nKey

        # Put description in term
        descTe = etree.SubElement(
                term,
                'description'
        )
        s  = '\n'
        s += '<div>\n'
        s += '    <h2>' + arch16nKey + '</h2>\n'
        for src in infoPictures:
            s += '    <div>\n'
            s += '        <img style="width:100%" src="' + src + '" alt="' + src + '" />\n'
            s += '    </div>\n'
        s += '<hr/>\n'
        s += '</div>\n'
        if len(infoPictures):
            descTe.text = etree.CDATA(s)

        # DO SOME CLEANUP
        if not pictureUrl:
            del term.attrib['pictureURL']
        if not parentVocab:
            del term.attrib['__RESERVED_PAR__']
        if not arch16nKey:
            lookup.getparent().remove(lookup)
        if not n:
            archEl.getparent().remove(archEl)

    return root

# This thing's time complexity could be better...
# t2 is modified during the call
def mergeTrees(t1, t2):
    if t1 == None:
        return t2
    if t2 == None:
        return t1

    t2NodesToDelete = []
    shallowCopyChildren(t1, t2)
    for i in range(0, len(t2)):
        for j in range(i+1, len(t2)):
            if isEquivalent(t2[i], t2[j]):
                mergeTrees( t2[i], t2[j])
                t2NodesToDelete.append(i)

    t2NodesToDelete.sort(reverse=True) # Needs to be sorted in reverse order to
                                       # prevent elements' indices getting moved
                                       # after each `del`.
    for index in t2NodesToDelete:
        del t2[index]

    return t2

# Returns true iff the roots of the trees share the same names and attributes.
def isEquivalent(t1, t2):
    return t1.tag == t2.tag and t1.attrib == t2.attrib

def shallowCopyChildren(src, dest):
    for child in src:
        dest.append(child)
    return dest

def sortTerms(t):
    t[:] = sorted(t, key=lambda n: getPositionOfTerm(n))
    for e in t:
        e = sortTerms(e)
    return t

def deleteAttribFromTree(attrib, t):
    if t == None:
        return t
    if attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(attrib, e)
    return t

def getPositionOfTerm(n):
    positionAttribute = '__RESERVED_POS__'
    if positionAttribute in n.attrib:
        return n.attrib[positionAttribute]
    else:
        return sys.maxint

# Nests the hierarchical vocab entries appropriately
def arrangeTerms(t):
    positionAttribute = '__RESERVED_PAR__'

    # If there aren't an elements with a `positionAttribute`, there's nothing to
    # do.
    source = t.xpath('(//*[@%s])[1]' % positionAttribute)
    if len(source) == 0:
        return t
    source = source[0]

    # The desired parent node
    dest = t.xpath('//ArchaeologicalElement[@name="%s"]/property[@name="%s"]//term[text()="%s"]' % arrangeTermsHelper(source))
    dest = dest[0]

    dest.append(source) # Move (not copy) source to dest
    source = deleteAttribFromTree(positionAttribute, source)
    return arrangeTerms(t)

# Returns a tuple containing entries used to uniquely identify a child term's
# proper parent.
def arrangeTermsHelper(t):
    positionAttribute = '__RESERVED_PAR__'

    archentName  = t.xpath('ancestor::ArchaeologicalElement')[0].attrib['name']
    propertyName = t.xpath('ancestor::property')[0].attrib['name']
    text         = t.attrib[positionAttribute]
    return archentName, propertyName, text

def getRowValue(row, columnName):
    columnName = columnName.lower()
    columnName = 'gsx$%s' % columnName
    if columnName in row:
        return row[columnName]['$t'].encode('utf-8').strip()
    return ''

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify Google Spreadsheet ID as argument')
    exit()

# Download the spreadsheet and interpret as JSON object
sheet_id = sys.argv[1]
url      = 'https://spreadsheets.google.com/feeds/list/' + sheet_id + '/1/public/values?prettyprint=true&alt=json';
response = urllib2.urlopen(url)
html     = response.read()
html     = json.loads(html)

# Read each row into an XML tree which represents the data schema
dataSchema = makeTree()
for row in html['feed']['entry']:
    dataSchema = insertIntoTree(row, dataSchema)

# Make terms hierarchical where needed and remove temporary attribute
dataSchema = arrangeTerms(dataSchema)

# Sort entries and remove the attribute used to temporarily store ordering
dataSchema = sortTerms(dataSchema)
dataSchema = deleteAttribFromTree('__RESERVED_POS__', dataSchema)

# Gimme dat data schema, blood
print etree.tostring(dataSchema, pretty_print=True)