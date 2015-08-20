#!/usr/bin/python

# Written by Vincent Tran and Brian Ballsun-Stanton

# Scrapes a google spreasheet following the format specified in the README file.
# Generates an appropriate data_schema.xml file, as well as the arch16N translations.

import urllib2, json, sys

arch16n = dict()

#Implementation of perl's autovivification feature.
class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class Term:
    def __init__(self, term, description, parent, index, pictureurl, arch16n):
        self.term = term
        self.description = description
        self.parent = parent
        self.index = index
        self.pictureurl = pictureurl
        self.arch16n = arch16n
        self.children = []

# Do a depth first search to print out hierarchical vocabulary
def dfs(depth, terms, current):
    s = "\n" + '  ' * depth + "<term"
    if current.pictureurl != "":
        s += " pictureURL=\"" + current.pictureurl + "\""
    s += "> "
    if current.arch16n == "":
        s += current.term
    else:
        s += "{" + current.term  + "}"
        arch16n[current.term] = current.arch16n
    if current.description != "":
        s += "\n" + '  ' * (int(depth)+1) +  "<description>" + current.description + "</description>"
    else:
        s += "\n" +'  ' * (int(depth)+1) + "<description/>"
    for child in current.children:
        s += dfs(depth+1, terms, terms[child])
    s += "\n" +'  ' * depth + "</term>"
    return s

def getRowValue(row, column_name):
    return row['gsx$%s' % (column_name)]['$t'].encode('utf-8').strip()

def printArchElement(vocabTable, entity):
    s = "  <ArchaeologicalElement name=\"" + entity + "\""
    if 'type' in vocabTable[entity]:
        s += " type=\"" + vocabTable[entity]['type'] + "\""
    s += ">"
    print s
    printDescription(vocabTable[entity])
    printProperties(vocabTable[entity])
    print "  </ArchaeologicalElement>"

def printRelnElement(vocabTable, entity):
    s = '  ' * depth + "<RelationshipElement name=\"" + entity + "\""
    if 'type' in vocabTable[entity]:
        s += " type=\"" + vocabTable[entity]['type'] + "\""
    s += ">"
    print s
    printDescription(vocabTable[entity])
    if vocabTable[entity]['type'] == "hierarchical":
        if 'parent' in vocabTable[entity]:
            print "    <parent>" + vocabTable[entity]['parent'] + "</parent>"
        if 'child' in vocabTable[entity]:
            print "    <child>" + vocabTable[entity]['child'] + "</child>"
    print "  </RelationshipElement>"

# `source` can either be a vocabTable (dict) or string
def printDescription(source, depth=1):
    # Extract description from source if necessary
    if isinstance(source, basestring):
        desc = source
    else:
        if 'description' in source:
            desc = source['description']
        else:
            desc = ''

    # Print the tag-enclosed description
    if desc == "":
        print '  ' * depth + "<description/>"
    else:
        print '  ' * depth + "<description>" + desc + "</description>"

def printProperties(source):
    depth = 1
    for p in source['properties']:
        s = '  ' * depth + '<property name="' + p['attribute'] + '"'

        if p['type'] == 'hierarchical':
            s += ' type="enum"'
        elif p['type'] == 'file':
            s += ' type="file" file="true" thumbnail="true"'
        elif p['type'] != '':
            s += ' type="' + p['type'] + '"'

        if p['identifier'] != '':
            s += ' isIdentifier="' + p['identifier'].lower() + '"'
        s += '>'
        print s

        depth += 1
        printDescription(p['description'], depth)
        if p['type'] in ('hierarchical', 'enum'):
            s = '  ' * depth + '<lookup>'
            depth += 1
            for term in p['parents']:
                s += dfs(depth, p['terms'], term)
            print s
            depth -= 1
            print '  ' * depth + '</lookup>'
        depth -= 1
        print '  ' * depth + '</property>'

# Program starts here
if len(sys.argv) < 2:
    sys.stderr.write("Specify Google Spreadsheet ID as argument")
    exit()
sheet_id = sys.argv[1]
url      = 'https://spreadsheets.google.com/feeds/list/' + sheet_id + '/1/public/values?prettyprint=true&alt=json';
response = urllib2.urlopen(url)
html     = response.read()
html     = json.loads(html)

vocabTable = AutoVivification()

for row in html['feed']['entry']:
    entity = getRowValue(row, 'entityname')

    if getRowValue(row, 'element') != "":
        vocabTable[entity]['element']     = getRowValue(row, 'element')
        vocabTable[entity]['description'] = getRowValue(row, 'description')
        vocabTable[entity]['properties']  = []
        if getRowValue(row, 'type') != "":
            vocabTable[entity]['type'] = getRowValue(row, 'type')
            if getRowValue(row, 'type') == "hierarchical":
                vocabTable[entity]['parent'] = getRowValue(row, 'parent')
                vocabTable[entity]['child']  = getRowValue(row, 'child')
    else:
        attribute =  getRowValue(row, 'attribute')
        termFound = False
        for attr in vocabTable[entity]['properties']:
            if attr['attribute'] == attribute:
                termFound = True
        if termFound:
            t = Term(
                    getRowValue(row, 'term'),
                    getRowValue(row, 'description'),
                    getRowValue(row, 'parent'),
                    len(p['terms']),
                    getRowValue(row, 'pictureurl'),
                    getRowValue(row, 'arch16n')
            )

            if t.parent == '':
                termIndex = -1
            else:
                termIndex = int(t.parent)
            if termIndex != -1:
                p['terms'][termIndex].children.append(t.index)
            else:
                p['parents'].append(t)
            p['terms'].append(t)
        else:
            p = AutoVivification()
            p['attribute']   = getRowValue(row, 'attribute')
            p['type']        = getRowValue(row, 'type')
            p['identifier']  = getRowValue(row, 'identifier')
            p['description'] = getRowValue(row, 'description')
            p['arch16n']     = getRowValue(row, 'arch16n')
            if p['type'] in ('enum', 'hierarchical'):
                p['terms']   = []
                p['parents'] = []
            if not isinstance(vocabTable[entity]['properties'], list):
                vocabTable[entity]['properties'] = []
            vocabTable[entity]['properties'].append(p)

print """<?xml version="1.0" encoding="UTF-8"?>"""
print """<dataSchema>"""
for entity in vocabTable:
    if   vocabTable[entity]['element'] == 'archent':
        printArchElement(vocabTable, entity)
    elif vocabTable[entity]['element'] == 'relnent':
        printRelnElement(vocabTable, entity)
    else:
        sys.stderr.write('Unexpected element "%s"' % vocabTable[entity]['element'])

    for p in vocabTable[entity]['properties']:
        if p['arch16n'] != '':
            arch16n[p['attribute']] = p['arch16n']
print '</dataSchema>'

print '\n\n\n\n'

for key in arch16n:
    print key + '=' + str(arch16n[key])
