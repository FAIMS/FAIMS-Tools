import json
import sys
import urllib2

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
dataSchema = sortTerms(dataSchema)
dataSchema = deleteAttribFromTree('__RESERVED_POS__', dataSchema)

# Gimme dat data schema, blood
print etree.tostring(dataSchema, pretty_print=True, xml_declaration=True, encoding='utf-8')
