#! /usr/bin/env python

from   lxml import etree
import spreadsheettools as sheets
import sys
import xmltools

def makeTree():
    root = etree.Element('dataSchema')
    return root

def insertIntoTree(row, xmlTree):
    if xmlTree == None:
        xmlTree = makeTree()

    node = rowToNode(row)
    xmlTree = xmltools.mergeTrees(node, xmlTree)

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
    arch16nKey   = sheets.getRowValue(row, 'faimsVocab')
    archentNames = sheets.getRowValue(row, 'attributeLocation')
    attribOrder  = sheets.getRowValue(row, 'attributeorder')
    countOrder   = sheets.getRowValue(row, 'VocabCountOrder')
    desc         = sheets.getRowValue(row, 'VocabDescription', 'AttributeDescription')
    infoPictures = sheets.getRowValue(row, 'infoFilenames')
    parentVocab  = sheets.getRowValue(row, 'parentVocabularyName')
    pictureUrl   = sheets.getRowValue(row, 'pictureFilename')
    propertyName = sheets.getRowValue(row, 'faimsEntityAttributeName')

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

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify Google Spreadsheet ID as argument\n')
    exit()

# Download the spreadsheet and interpret as JSON object
sheetId = sys.argv[1]
html = sheets.id2Html(sheetId)

# Read each row into an XML tree which represents the data schema
dataSchema = makeTree()
for row in html['feed']['entry']:
    dataSchema = insertIntoTree(row, dataSchema)

# Make terms hierarchical where needed and remove temporary attribute
dataSchema = xmltools.nestTerms(dataSchema)

# Sort entries and remove the attribute used to temporarily store ordering
sortBy = []
sortBy.append('__RESERVED_POS__')
sortBy.append('__RESERVED_ATTR_ORDER__')
for s in sortBy:
    dataSchema = xmltools.sortSiblings(dataSchema, s)
    dataSchema = xmltools.deleteAttribFromTree(s, dataSchema)

# Gimme dat data schema, blood
print etree.tostring(dataSchema, pretty_print=True, xml_declaration=True, encoding='utf-8')
