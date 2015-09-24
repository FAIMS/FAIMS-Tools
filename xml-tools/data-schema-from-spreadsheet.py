#! /usr/bin/env python

from   lxml import etree
import re
import os
import glob
import urllib           as urllib
import xml.sax.saxutils as saxutils
import spreadsheettools as sheets
import sys
import xmltools

def getImageNamesOnDisk():
    filenames = glob.glob(IMAGE_DIR_ON_DISK + '*.*')

    # Consider only the basenames
    for i in range(len(filenames)):
        filenames[i] = os.path.basename(filenames[i])

    return filenames

def makeTree():
    root = etree.Element('dataSchema')
    return root

def insertIntoTree(row, xmlTree):
    if xmlTree == None:
        xmlTree = makeTree()

    node = rowToNode(row)
    xmlTree = xmltools.mergeTrees(node, xmlTree)

    return xmlTree

def computeMostSimilar(word, candidates):
    if len(candidates) == 0:
        return word

    min = sys.maxint
    minIdx = -1
    for i in range(len(candidates)):
        d = minEditDist(word, candidates[i])
        if d < min:
            min    = d
            minIdx = i
    mostSimilar = candidates[minIdx]

    if min >= 1:
        formatStr = 'Edit dist:{0: >2}    Given word: {1: <50} Closest candidate: {2: <50}\n'
        sys.stderr.write(formatStr.format(min, word, mostSimilar))
    return mostSimilar

# Minimum edit distance. Source:
# http://www.cs.colorado.edu/~martin/csci5832/edit-dist-blurb.html
def  minEditDist(target, source):
    ''' Computes the min edit distance from target to source. Figure 3.25 '''

    n = len(target)
    m = len(source)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + 1

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + 1

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j  ]+1,
                                distance[i  ][j-1]+1,
                                distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def substCost(s1, s2):
    if s1 == s2:
        return 0
    return 1

def correctUrls(urls):
    if   isinstance(urls, str):
        return correctUrl(urls)
    elif isinstance(urls, list):
        for i in range(len(urls)):
            urls[i] = correctUrl(urls[i])
        return urls
    else:
        return ''

def correctUrl(url):
    if not url:
        return ''

    urlDir  = os.path.dirname(url)
    urlBase = os.path.basename(url)
    correctUrlBase = computeMostSimilar(urlBase, IMAGE_NAMES_ON_DISK)
    correctedUrl   = urlDir + correctUrlBase
    return correctedUrl

def correctCountOrder():
    pass

def normaliseUrls(urls, doPercentEncode=True):
    if not urls:
        return ''

    prefix = 'files/data/gallery/'

    if   isinstance(urls, str):
        if doPercentEncode:
            urls = urllib.quote(urls)
        urls = saxutils.escape(urls)
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
        sys.stderr.write('attributeCountOrder contains semi-colon delimited list whose elements differ.\n')

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

    infoPictures = correctUrls(infoPictures)
    pictureUrl   = correctUrls(pictureUrl)

    infoPictures = normaliseUrls(infoPictures)
    pictureUrl   = normaliseUrls(pictureUrl, False)

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
        #s +=     '    <h2>' + arch16nKey + '</h2>\n'
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

# Just numbers the vocab entries according to their row number
def normaliseHtml(html):
    for i in range(len(html['feed']['entry'])):
        row = html['feed']['entry'][i]
        if sheets.getRowValue(row, 'faimsVocab'):
            sheets.setRowValue(row, 'VocabCountOrder', i)
    return html

#def normaliseHtml(html):
    #lastCountOrder   = ''
    #lastPropertyName = ''
    #for i in range(len(html['feed']['entry'])):
        #row = html['feed']['entry'][i]

        #thisCountOrder   = sheets.getRowValue(row, 'VocabCountOrder')
        #thisPropertyName = sheets.getRowValue(row, 'faimsEntityAttributeName')

        ## Skip rows with VocabCountOrder already provided
        #if thisCountOrder:
            #lastCountOrder   = thisCountOrder
            #lastPropertyName = thisPropertyName
            #continue

        ## Set VocabCountOrder to 1 for first entry in each vocab
        #if thisPropertyName != lastPropertyName:
            #thisCountOrder   = '1'
            #lastCountOrder   = thisCountOrder
            #lastPropertyName = thisPropertyName

        #sheets.setRowValue(row, 'VocabCountOrder', lastCountOrder)
    #return html

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify Google Spreadsheet ID as argument\n')
    exit()

# If I just use these two itty-bitty globals, I can improve performance a lot
IMAGE_DIR_ON_DISK   = 'images/all photos 1-542 for all modules/'
IMAGE_NAMES_ON_DISK = getImageNamesOnDisk()

# Download the spreadsheet and interpret as JSON object
sheetId = sys.argv[1]
html = sheets.id2Html(sheetId)
html = normaliseHtml(html)

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
