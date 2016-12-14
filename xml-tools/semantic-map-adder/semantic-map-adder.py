#!/usr/bin/env python2

from   lxml import etree
import csv
import os
import sys
import urllib

################################### GLOBALS ####################################

FLAG_OVERWRITE = '--overwrite'
DO_OVERWRITE = False

URL_FMT = 'https://docs.google.com/a/fedarch.org/spreadsheets/d/1JWnps7UEDLIvrP7okYeaVLdgDVd499NrY7CWIf3OUoo/export?format=csv&id=1JWnps7UEDLIvrP7okYeaVLdgDVd499NrY7CWIf3OUoo&gid=%s'

ARCHS   = 'archs.csv'
RELS    = 'rels.csv'
ATTRIBS = 'attribs.csv'
VOCABS  = 'vocabs.csv'

SHEET_GIDS = {
        ARCHS   : '0',
        RELS    : '858928007',
        ATTRIBS : '1883249420',
        VOCABS  : '615757782',
}

################################################################################

def readCsv(filename):
    with open(filename, 'rb') as csvfile:
        # Figure out how the CSV file is formatted and start reading it
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        # Read file into list
        csvData = []
        for readerRow in reader:
            # Convert readerRow to dataRow (i.e. strip whitespace)
            dataRow = [cell.strip() for cell in readerRow]
            csvData.append(dataRow)

        return csvData

def strippedEquals(str1, str2):
    if not type(str1) == str: return False
    if not type(str2) == str: return False

    return str1.strip() == str2.strip()

def addAttribToElement(
        dataSchema,
        srcAttribs,        # Dictionary in this format: {attribName : attribVal}
        dstTag=None,
        dstText=None,
        dstAttribName=None,
        dstAttribVal=None
):
    if not type(srcAttribs) == dict:
        return
    if '' in srcAttribs:
        del srcAttribs['']
    if not srcAttribs:
        return

    # Normalise white space of arguments
    if dstTag:        dstTag        = dstTag       .strip()
    if dstText:       dstText       = dstText      .strip()
    if dstAttribName: dstAttribName = dstAttribName.strip()
    if dstAttribVal:  dstAttribVal  = dstAttribVal .strip()

    # Find the elements to annotate
    matches = dataSchema.xpath('//*')
    if dstTag:
        matches = filter(lambda n: strippedEquals(n.tag, dstTag), matches)
    if dstText:
        matches = filter(lambda n: strippedEquals(n.text, dstText), matches)
    if dstAttribName:
        matches = filter(lambda n: dstAttribName in n.attrib, matches)
    if dstAttribVal:
        matches = filter(
                lambda n: strippedEquals(n.attrib[dstAttribName], dstAttribVal),
                matches
        )

    # Annotate the elements in `dataSchema`
    for n in matches:
        n.attrib.update(srcAttribs)

def addAttribsToArchs(dataSchema):
    csv = readCsv(ARCHS)

    for archentName, semanticMapPredicate, semanticMapObjectURI, _ in csv:
        addAttribToElement(
                dataSchema,
                {
                    'SemanticMapPredicate' : semanticMapPredicate,
                    'SemanticMapObjectURI' : semanticMapObjectURI
                },
                dstTag='ArchaeologicalElement',
                dstAttribName='name',
                dstAttribVal=archentName
        )

def addAttribsToRels(dataSchema):
    csv = readCsv(RELS)

    for relnName, semanticMapPredicate, semanticMapObjectURI, _ in csv:
        addAttribToElement(
                dataSchema,
                {
                    'SemanticMapPredicate' : semanticMapPredicate,
                    'SemanticMapObjectURI' : semanticMapObjectURI
                },
                dstTag='RelationshipElement',
                dstAttribName='name',
                dstAttribVal=relnName
        )

def addAttribsToAttribs(dataSchema):
    csv = readCsv(ATTRIBS)

    for attribute, semanticMapPredicate, semanticMapObjectURI, _ in csv:
        addAttribToElement(
                dataSchema,
                {
                    'SemanticMapPredicate' : semanticMapPredicate,
                    'SemanticMapObjectURI' : semanticMapObjectURI
                },
                dstTag='property',
                dstAttribName='name',
                dstAttribVal=attribute
        )

def addAttribsToVocabs(dataSchema):
    csv = readCsv(VOCABS)

    for controlledVocab, semanticMapPredicate, semanticMapObjectURI, _ in csv:
        addAttribToElement(
                dataSchema,
                {
                    'SemanticMapPredicate' : semanticMapPredicate,
                    'SemanticMapObjectURI' : semanticMapObjectURI
                },
                dstTag='term',
                dstText=controlledVocab
        )

def bye():
    msg  = 'Usage: %s input_schema [%s] > output_schema\n\n' % \
            (sys.argv[0], FLAG_OVERWRITE)
    msg += '  input_schema: The data schema whose elements are to be \n'
    msg += '      annotated. This is read into a buffer so that it is valid \n'
    msg += '      read from and write to the same file simultaneously.\n'
    msg += '  %s: Whether to overwrite previously downloaded CSV files.\n' % \
            FLAG_OVERWRITE
    msg += '  output_schema: The annotated data schema, printed to stdout.\n\n'
    msg += '  The URL of the CSV files is hard-coded.\n'

    sys.stderr.write(msg)
    exit()

##################################### MAIN #####################################

# Argument cardinality check
if not 2 <= len(sys.argv) <= 3:
    bye()

# Argument semantics check -- First arg
if not os.path.exists(sys.argv[1]):
    sys.stderr.write('Data schema "%s" not found\n\n' % sys.argv[1])
    bye()

# Argument semantics check -- Second arg
if len(sys.argv) == 3 and sys.argv[2] != FLAG_OVERWRITE:
    bye()

# Interpret flag(s) passed to the program
DO_OVERWRITE = len(sys.argv) == 3 and sys.argv[2] == FLAG_OVERWRITE

# Download sheets
for filename, sheetGid in SHEET_GIDS.iteritems():
    if os.path.exists(filename) and not DO_OVERWRITE:
        msg = 'Not downloading %s. File already exists.\n' % filename
        sys.stderr.write(msg)
    else:
        msg = 'Downloading %s...\n' % filename
        sys.stderr.write(msg)
        urllib.urlretrieve(URL_FMT % sheetGid, filename)

# Load data schema
filename = sys.argv[1]
parser = etree.XMLParser(strip_cdata=False)
dataSchema = etree.parse(filename, parser)
dataSchema = dataSchema.getroot()

# Annotate dataSchema
addAttribsToArchs  (dataSchema)
addAttribsToRels   (dataSchema)
addAttribsToAttribs(dataSchema)
addAttribsToVocabs (dataSchema)

# Print annotated data schema
print etree.tostring(
        dataSchema,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)
