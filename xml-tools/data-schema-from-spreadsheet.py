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

def normaliseUrls(urls):
    if not urls:
        return ''

    prefix = 'files/data/gallery/'

    if   isinstance(urls, str):
        urls = urls.replace('&', '_')
        urls = urls.replace(' ', '_')
        return prefix + urls
    elif isinstance(urls, list):
        for i in range(len(urls)):
            urls[i] = normaliseUrls(urls[i])
        return urls
    else:
        return ''

def parseDesc(desc, delim='_x000D_'):
    if not desc:
        return ''
    paragraphs = desc.split(delim)
    for i in range(len(paragraphs)):
        paragraphs[i] = '<p>' + paragraphs[i] + '</p>\n'
    parsed = ''.join(paragraphs)
    return parsed

# Parse a string of semicolon-delimited values into a python list
def parseList(listString, delim=';'):
    list = listString.split(delim)
    for i in range(len(list)):# Remove surrounding whitespace for each item
        list[i] = list[i].strip()
    list = filter(None, list) # Remove empty strings

    return parseListAttributeCountOrderNormaliser(list)

def parseListAttributeCountOrderNormaliser(parsedList):
    containsOnlyDigits = True
    for e in parsedList:
        if not e.isdigit():
            containsOnlyDigits = False

    elementsAreEqual = len(set(parsedList)) <= 1
    if containsOnlyDigits and not elementsAreEqual:
        sys.stderr('attributeCountOrder contains semi-colon delimited list whose elements differ.\n')

    if   containsOnlyDigits and len(parsedList) == 0:
        return ''
    elif containsOnlyDigits and len(parsedList) >  0:
        return parsedList[0]
    else:
        return parsedList


def rowToNode(row):
    arch16nKey   = getRowValue(row, 'faimsVocab')
    archentNames = getRowValue(row, 'attributeLocation')
    attribOrder  = getRowValue(row, 'attributeorder')
    countOrder   = getRowValue(row, 'VocabCountOrder')
    desc         = getRowValue(row, 'VocabDescription', 'AttributeDescription')
    infoPictures = getRowValue(row, 'infoFilenames')
    parentVocab  = getRowValue(row, 'parentVocabularyName')
    pictureUrl   = getRowValue(row, 'pictureFilename')
    propertyName = getRowValue(row, 'faimsEntityAttributeName')

    desc         = parseDesc(desc)
    archentNames = parseList(archentNames)
    countOrder   = parseList(countOrder)
    infoPictures = parseList(infoPictures)

    infoPictures = normaliseUrls(infoPictures)
    pictureUrl   = normaliseUrls(pictureUrl)

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
                name=propertyName,
                __RESERVED_ATTR_ORDER__=attribOrder
        )

        # Put description in property
        descPr = etree.SubElement(
                prop,
                'description'
        )
        s  = '\n'
        s += '<div>\n'
        #s += '    <h1>' + arch16nKey + '</h1>\n'
        s += '    '     + desc
        s += '    <hr/>\n'
        s += '</div>\n'
        if desc and not arch16nKey: # if this row is a property (instead of term)
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
        s  =     '\n'
        s +=     '<div>\n'
        s +=     '    <h2>' + arch16nKey + '</h2>\n'
        for src in infoPictures:
            s += '    <div>\n'
            s += '        <img style="width:100%" src="' + src + '" alt="' + src + '" />\n'
            s += '    </div>\n'
        s +=     '    <div>\n'
        s +=     '        ' + desc
        s +=     '    </div>\n'
        s +=     '    <hr/>\n'
        s +=     '</div>\n'
        if desc and arch16nKey and len(infoPictures):
            descTe.text = etree.CDATA(s)

        # DO SOME CLEANUP
        if not pictureUrl:
            del term.attrib['pictureURL']
        if not parentVocab:
            del term.attrib['__RESERVED_PAR__']
        if not descTe.text:
            descTe.getparent().remove(descTe)
        if not arch16nKey:
            lookup.getparent().remove(lookup)
        if not descPr.text:
            descPr.getparent().remove(descPr)
        if not attribOrder:
            del prop.attrib['__RESERVED_ATTR_ORDER__']
        if not propertyName or len(prop) == 0:
            prop.getparent().remove(prop)
        if not n            or len(archEl) == 0:
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
            if isEquivalent(t2[j], t2[i]):
                mergeTrees( t2[j], t2[i])
                t2NodesToDelete.append(j)

    t2NodesToDelete.sort(reverse=True) # Needs to be sorted in reverse order to
                                       # prevent elements' indices getting moved
                                       # after each `del`.
    for index in t2NodesToDelete:
        del t2[index]

    return t2

# Returns true iff the roots of the trees share the same names and attributes.
def isEquivalent(t1, t2):
    if t1 == None or t2 == None:
        return t1 == t2

    # Ignore reserved attributes when checking equivalence of attributes
    reserved = []
    reserved.append('__RESERVED_ATTR_ORDER__')
    reserved.append('__RESERVED_CP__')
    reserved.append('__RESERVED_PAR__')

    attribT1 = dict(t1.attrib)
    attribT2 = dict(t2.attrib)
    for r in reserved:
        attribT1.pop(r, None)
        attribT2.pop(r, None)

    t1Text = t1.text
    t2Text = t2.text
    if not t1Text:
        t1Text = ''
    if not t2Text:
        t2Text = ''
    t1Text = t1Text.strip()
    t2Text = t2Text.strip()

    return t1.tag == t2.tag and attribT1 == attribT2 and t1Text == t2Text

# Copies each child from `src` to within `dest`. I.e. makes the children of
# `src` into the children of `dest`.
def shallowCopyChildren(src, dest):
    for child in src:
        dest.append(child)
    return dest

def sortSiblings(t, attrib):
    t[:] = sorted(t, key=lambda n: getPositionOfNode(n, attrib))
    for e in t:
        e = sortSiblings(e, attrib)
    return t

def deleteAttribFromTree(attrib, t):
    if t == None:
        return t
    if attrib in t.attrib:
        del t.attrib[attrib]

    for e in t:
        deleteAttribFromTree(attrib, e)
    return t

def getPositionOfNode(n, attrib):
    attrib = '__RESERVED_POS__'
    if attrib in n.attrib:
        return n.attrib[attrib]
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
    destPath = '//ArchaeologicalElement[@name="%s"]/property[@name="%s"]//term[text()="%s"]' % arrangeTermsHelper(source)
    dest = t.xpath(destPath)
    if len(dest) < 1:
        return t
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

def getRowValue(row, *columnNames):
    for n in columnNames:
        val = getRowValue_(row, n)
        if val:
            return val
    return ''

def getRowValue_(row, columnName):
    columnName = columnName.lower()
    columnName = 'gsx$%s' % columnName
    if columnName in row:
        return row[columnName]['$t'].encode('utf-8').strip()
    return ''

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify Google Spreadsheet ID as argument\n')
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
sortBy = []
sortBy.append('__RESERVED_POS__')
sortBy.append('__RESERVED_ATTR_ORDER__')
for s in sortBy:
    dataSchema = sortSiblings(dataSchema, s)
    dataSchema = deleteAttribFromTree(s, dataSchema)

# Gimme dat data schema, blood
print etree.tostring(dataSchema, pretty_print=True, xml_declaration=True, encoding='utf-8')
