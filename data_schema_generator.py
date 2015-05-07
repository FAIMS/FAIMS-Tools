#!/usr/bin/python

# Written by Vincent Tran and Brian Ballsun-Stanton

# Scrapes a google spreasheet following the format specified in the README file.
# Generates an appropriate data_schema.xml file, as well as the arch16N translations.

import urllib2, json, sys

arch16n = dict()

def getRowValue(row, format, column_name):    
    if str(column_name) == '':
        raise ValueError('column_name must not empty')
    begin = row.find('%s:' % column_name)       
    if begin == -1:
        return ''
    begin = begin + len(column_name) + 1
    end = -1
    found_begin = False
    
    for entity in format:
        if found_begin and row.find(entity) != -1:
            end = row.find(entity)
            break
        
        if entity == column_name:
            found_begin = True
    
    #check if last element
    if format[len(format) -1 ] == column_name:
        end = len(row)
    else:
        if end == -1:
            end = len(row)
        else:
            end = end - 2
    value = row[begin: end].strip()
    return value

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
        s = s + " pictureURL=\"" + current.pictureurl + "\""
    s = s + "> "
    if current.arch16n == "":
        s = s + current.term
    else:
        s = s + "{" + current.term  + "}"
        arch16n[current.term] = current.arch16n
    if current.description != "":
        s += "\n" + '  ' * (int(depth)+1) +  "<description>" + current.description + "</description>"
    else:
        s += "\n" +'  ' * (int(depth)+1) + "<description/>"
    for child in current.children:
        s = s + dfs(depth+1, terms, terms[child])
    s += "\n" +'  ' * depth + "</term>"
    return s

# Program starts here

if len(sys.argv) < 2:
    sys.stderr.write("Specify Google Spreadsheet ID as argument")
    exit()
sheet_id = sys.argv[1]
url = 'https://spreadsheets.google.com/feeds/list/' + sheet_id + '/od6/public/basic?prettyprint=true&alt=json';
response = urllib2.urlopen(url)
html = response.read()

html = json.loads(html)

format = ['entityname', 'element', 'attribute', 'type', 'identifier', 'term', 'arch16n', 'pictureurl', 'description', 'depth', 'parent', 'child']

vocabTable = AutoVivification()

for entry in html['feed']['entry']:
    row = entry['content']['$t'].encode('utf-8').strip()
    entity = getRowValue(row, format, 'entityname')
    if getRowValue(row, format, 'element') != "":
        vocabTable[entity]['enttype'] = getRowValue(row, format, 'element')
        vocabTable[entity]['description'] = getRowValue(row, format, 'description')
        vocabTable[entity]['properties'] = []
        if getRowValue(row, format, 'type') != "":
            vocabTable[entity]['type'] = getRowValue(row, format, 'type')
            if getRowValue(row, format, 'type') == "hierarchical":
                vocabTable[entity]['parent'] = getRowValue(row, format, 'parent')
                vocabTable[entity]['child'] = getRowValue(row, format, 'child')
    else:
        attribute =  getRowValue(row, format, 'attribute')
        # print attribute
        found = False
        for attr in vocabTable[entity]['properties']:
            if attr['attribute'] == attribute:
                found = True
        if found:
            t = Term(getRowValue(row, format, 'term'), getRowValue(row, format, 'description'), getRowValue(row, format, 'parent'), len(p['terms']), getRowValue(row, format, 'pictureurl'), getRowValue(row, format, 'arch16n'))
            
            if int(t.parent) != -1:
                p['terms'][int(t.parent)].children.append(t.index)
            else:
                p['parents'].append(t)
            p['terms'].append(t)
        else:
            p = AutoVivification()
            p['attribute'] = getRowValue(row, format, 'attribute')
            p['type'] = getRowValue(row, format, 'type')
            p['identifier'] = getRowValue(row, format, 'identifier')
            p['description'] = getRowValue(row, format, 'description')
            p['arch16n'] = getRowValue(row, format, 'arch16n')
            if p['type'] == "enum" or p['type'] == "hierarchical":
                p['terms'] = []
                p['parents'] = []
            vocabTable[entity]['properties'].append(p)

print """<?xml version="1.0" encoding="UTF-8"?>
<dataSchema>"""
depth = 1
for entity in vocabTable:
    # print out ArchElement or RelnElement
    if vocabTable[entity]['enttype'] == "archent":
        s = '  ' * depth + "<ArchaeologicalElement name=\"" + entity + "\""
        if 'type' in vocabTable[entity]:
            s += " type=\"" + vocabTable[entity]['type'] + "\""

        s += ">"
        print s
    else:
        s = '  ' * depth + "<RelationshipElement name=\"" + entity + "\""
        if 'type' in vocabTable[entity]:
            s += " type=\"" + vocabTable[entity]['type'] + "\""

        s += ">"
        print s
    depth += 1
    #print description
    if 'description' in vocabTable[entity]:
        print '  ' * depth + "<description>" + vocabTable[entity]["description"] + "</description>"
    else:
        print '  ' * depth + "<description/>"
    #if its a hierarchical relationship, print the parent/child
    if vocabTable[entity]['enttype'] == "relnent" and vocabTable[entity]['type'] == "hierarchical":
        if 'parent' in vocabTable[entity]:
            print '  ' * depth + "<parent>" + vocabTable[entity]['parent'] + "</parent>"
        if 'child' in vocabTable[entity]:
            print '  ' * depth + "<child>" + vocabTable[entity]['child'] + "</child>"

    #print the properties
    for p in vocabTable[entity]['properties']:
        s = '  ' * depth + "<property name=\"" + p['attribute'] + "\""
        if p['type'] != "":
            if p['type'] == "hierarchical":
                s = s + " type=\"enum\""
            elif p['type'] == "file":
                s = s + " type=\"file\" file=\"true\" thumbnail=\"true\""
            else:
                s = s + " type=\"" + p['type'] + "\""
        if p['identifier'] != "":
            s = s + " isIdentifier=\"" + p['identifier'].lower() + "\""
        s = s + ">"
        if p['arch16n'] != "":
            arch16n[p['attribute']] = p['arch16n']
        print s
        depth += 1
        if p['description'] != "":
            s = '  ' * depth + "<description>" + p['description'] + "</description>"
        else:
            s = '  ' * depth + "<description/>"
        print s
        if p['type'] == "hierarchical" or p['type'] == "enum":
            s = '  ' * depth + "<lookup>"
            depth += 1
            for term in p['parents']: 
                s = s + dfs(depth, p['terms'], term)
            print s    
            depth -= 1
            print '  ' * depth + "</lookup>"
        depth -= 1
        print '  ' * depth + "</property>"

    depth -= 1
    if vocabTable[entity]['enttype'] == "archent":
        print '  ' * depth + "</ArchaeologicalElement>"

    else:
        print '  ' * depth + "</RelationshipElement>"
print "</dataSchema>"

print "\n\n\n\n"
for key in arch16n:
    print key + "=" + str(arch16n[key])