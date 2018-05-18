#!/usr/bin/python

# Written by Vincent Tran

# Given an arch16N.properties, ui_schema.xml and data_schema.xml file,
# go through all the arch16N values and strip out the ones that aren't mentioned
# in any of the files.

import sys, re

class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

if len(sys.argv) < 4:
    sys.stderr.write("Please specify an arch16N.properties file, ui_schema.xml and a data_schema.xml file")
    exit()

arch16N = sys.argv[1]
ui_schema = sys.argv[2]
data_schema = sys.argv[3]

original_properties = AutoVivification()
for line in open(arch16N, 'r'):
    line = line.rstrip()
    line = re.split('=', line)
    original_properties[line[0]] = line[1]

new_properties = AutoVivification()

for line in open(ui_schema, 'r'):
    if '{' in line:
        m = re.search('{.*}', line)
        term = m.group(0)[1:-1]
        if term in original_properties:
            new_properties[term] = original_properties[term]

for line in open(data_schema, 'r'):
    if '{' in line:
        m = re.search('{.*}', line)
        term = m.group(0)[1:-1]
        if term in original_properties:
            new_properties[term] = original_properties[term]

sorted_properties = []

for term in new_properties:
    term = term + "=" + new_properties[term]
    sorted_properties.append(term)

sorted_properties.sort(key=lambda a: a.lower())
for term in sorted_properties:
    print term
print ""