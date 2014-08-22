#!/usr/bin/python
 
import urllib2
import json

arch16n = {}

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

def ui_header(html, format):
    stack = []
    schema = []
    depth = 0
    for entry in html['feed']['entry']:
        row = entry['content']['$t'].encode('utf-8').strip()
        if int(getRowValue(row, format, 'level')) <= int(depth):
            while int(getRowValue(row, format, 'level')) <= int(depth):
                element = stack.pop()
                s = "  " * (int(depth)+4) + "</" + getRowValue(element, format, 'ref') + ">"
                depth = int(depth) - 1
                schema.append(s)
        depth = getRowValue(row, format, 'level')
        stack.append(row)
        s = "  " * (int(depth)+4) + "<" + getRowValue(row, format, 'ref') + ">"
        schema.append(s)

    # close the rest of the stack off
    while len(stack) > 0:
        element = stack.pop()
        s = "  " * (int(getRowValue(element, format, 'level'))+4) + "</" + getRowValue(element, format, 'ref') + ">"
        schema.append(s)
    
    i = 0
    while i < len(schema)-1:
        index = schema[i].index('<')
        if schema[i+1][index+1] == "/" and schema[i][index+1:] == schema[i+1][index+2:]:
            schema.pop(i+1)
            schema[i] = schema[i][:-1] + "/>"
        i += 1
    print "\n".join(schema)

def ui_body(html, format):
    stack = []
    schema = []
    depth = 0
    types = {"dropdown": "select1",
             "radio": "select1",
             "list": "select1",
             "checkbox": "select",
             "input": "input",
             "trigger": "trigger",
             "group": "group",
             "picture": "select1",
             "camera": "select",
             "file": "select"}
    needs_placeholder = ['radio', 'checkbox', 'camera', 'picture', 'list', 'dropdown', 'file']
    for entry in html['feed']['entry']:
        row = entry['content']['$t'].encode('utf-8').strip()
        if int(getRowValue(row, format, 'level')) <= int(depth):
            while int(getRowValue(row, format, 'level')) <= int(depth):
                element = stack.pop()
                s = "  " * int(depth) + "</" + types[getRowValue(element, format, 'type')] + ">"
                depth = int(depth) - 1
                schema.append(s)
        depth = getRowValue(row, format, 'level')
        stack.append(row)
        s = "  " * int(depth) + "<"
        if getRowValue(row, format, 'type') == "radio":
            s = s + types[getRowValue(row, format, 'type')] + " appearance=\"full\""
        elif getRowValue(row, format, 'type') == "list":
            s = s + types[getRowValue(row, format, 'type')] + " appearance=\"compact\""
        elif getRowValue(row, format, 'type') == "picture":
            s = s + types[getRowValue(row, format, 'type')] + " type=\"image\""
        elif getRowValue(row, format, 'type') == "file":
            s = s + types[getRowValue(row, format, 'type')] + " type=\"file\""
        elif getRowValue(row, format, 'type') == "camera":
            s = s + types[getRowValue(row, format, 'type')] + " type=\"camera\" faims_sync=\"true\""
        else:
            s = s + types[getRowValue(row, format, 'type')]
        s = s + " ref=\"" + getRowValue(row, format, 'ref') + "\""
        if getRowValue(row, format, 'faimsattributename') != "":
            s = s + " faims_attribute_name=\"" + getRowValue(row, format, 'faimsattributename') + "\""
        if getRowValue(row, format, 'faimsattributetype') != "":
            s = s + " faims_attribute_type=\"" + getRowValue(row, format, 'faimsattributetype') + "\""
        if getRowValue(row, format, 'certainty') != "":
            s = s + " faims_certainty=\"" + getRowValue(row, format, 'certainty').lower() + "\""
        if getRowValue(row, format, 'annotation') != "":
            s = s + " faims_annotation=\"" + getRowValue(row, format, 'annotation').lower() + "\""
        if getRowValue(row, format, 'readonly') != "":
            s = s + " faims_read_only=\"" + getRowValue(row, format, 'readonly').lower() + "\""
        if getRowValue(row, format, 'hidden') != "":
            s = s + " faims_hidden=\"" + getRowValue(row, format, 'hidden').lower() + "\""
        if getRowValue(row, format, 'faimsarchenttype') != "":
            s = s + " faims_archent_type=\"" + getRowValue(row, format, 'faimsarchenttype').lower() + "\""
        if getRowValue(row, format, 'faimsreltype') != "":
            s = s + " faims_rel_type=\"" + getRowValue(row, format, 'faimsreltype').lower() + "\""
        if getRowValue(row, format, 'faimsstyle') != "":
            s = s + " faims_style=\"" + getRowValue(row, format, 'faimsstyle').lower() + "\""
        if getRowValue(row, format, 'faimsscrollable') != "":
            s = s + " faims_scrollable=\"" + getRowValue(row, format, 'faimsscrollable').lower() + "\""
        s = s + ">"
        schema.append(s)
        s = "  " * (int(depth)+1) + "<label>" 
        if getRowValue(row, format, 'arch16n') != "":
            s = s + "{" + getRowValue(row, format, 'label') + "}</label>"
            arch16n[getRowValue(row, format, 'label')] = getRowValue(row, format, 'arch16n')
        else:
            s = s + getRowValue(row, format, 'label') + "</label>"
        schema.append(s)
        if getRowValue(row, format, 'type') in needs_placeholder:
            s = ""
            s = s + "  " * (int(depth)+1) + "<item>\n"
            s = s + "  " * (int(depth)+3) + "<label>placeholder</label>\n"
            s = s + "  " * (int(depth)+3) + "<value>placeholder</value>\n"
            s = s + "  " * (int(depth)+2) + "</item>"
            schema.append(s)

    # close the rest of the stack off
    while len(stack) > 0:
        element = stack.pop()
        s = "  " * int(getRowValue(element, format, 'level')) + "</" + types[getRowValue(element, format, 'type')] + ">"
        schema.append(s)
    i = 0
    while i < len(schema):
        schema[i] = "  " + schema[i]
        i += 1
    print "\n".join(schema)

url = 'https://spreadsheets.google.com/feeds/list/1ZMVzcvlcWmTthlBZg_sOJmRVGmGQoxboqr4SPYkVat4/od6/public/basic?prettyprint=true&alt=json';
 
response = urllib2.urlopen(url)
html = response.read()

html = json.loads(html)
format = ['level', 'ref', 'type', 'faimsattributename', 'faimsattributetype', 'certainty', 'annotation', 'readonly', 'hidden', 'label', 'faimsarchenttype', 'arch16n', 'faimsstyle','faimsscrollable']
print """<h:html xmlns="http://www.w3.org/2002/xforms" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:h="http://www.w3.org/1999/xhtml" xmlns:jr="http://openrosa.org/javarosa" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <h:head>
    <h:title>hdb FAIMS Community Server</h:title>
    <model>
      <instance>
        <faims id="hdb_FAIMS_Community_Server">
          <style>
            <orientation>
              <orientation/>
            </orientation>
            <even>
              <layout_weight/>
            </even>
            <large>
              <layout_weight/>
            </large>
          </style>
          <user>
            <usertab>
              <Area_Code/>
              <users/>
              <login/>
            </usertab>
          </user>"""
ui_header(html, format)
print """        </faims>
      </instance>
      <!-- Insert nodeset bindings here -->
    </model>
  </h:head>
  <h:body>"""
ui_body(html, format)
print """  </h:body>
</h:html>"""

print "\n\n\n\n\n\n"
for key in arch16n:
    print key + "=" + str(arch16n[key])