FAIMS-Tools
===========
These are a collection of tools designed to help with developing modules faster. These scripts are not designed to output a working module in one go. They are designed to speed up the process of developing modules so that you can focus on the details.

The scripts are written in a variety of languages, mostly which ever language is most convenient for the job. I encourage you to do the same.
## Basics
### Permissions
To run them, you need to give executable permissions by doing:
```bash
$ chmod +x <script_name>
$ ./<script_name> <args>
```
### Google spreadsheets
Some of the scripts scrape data and generate code based on google spreadsheets. To do this, you must create a google spreadsheet with the specific format which will be specified in the script description. Next, you will need to publish the script to make it accessible to the Google Spreadsheet API. You can do this by going to ```File > Publish to the web...``` and click on ```Publish```.

This will generate a link which you can use for API calls. For simplicities sake, you should only need to find the Google Spreadsheet ID. For example:

```
https://docs.google.com/spreadsheets/d/1urureOuCdRKoiwmAU9WDH0wcgGEpHh2R0vJdR6bTc_0/pubhtml
```

The Google Spreadsheet ID for this spreadsheet is ```1urureOuCdRKoiwmAU9WDH0wcgGEpHh2R0vJdR6bTc_0```

## data_schema_generator.py
To run:
```bash
$ ./data_schema.py <google_spreadsheet_id>
```
Supply the Google Spreadsheet ID and it will generates an appropriate data_schema.xml file, as well as the arch16N translations.

### Spreadsheet Format
Scrapes a google spreasheet in the following the format:

| DUMMY | entity_name | element | attribute | type | identifier | term | arch16n | pictureurl | description | parent | child |
| ----- | ----------- | ------- | --------- | ---- | ---------- | ---- | ------- | ---------- | ----------- | ------ | ----- |
|       | Value       | Value   | Value     | Value| Value      | Value| Value   | Value      | Value       | Value  | Value |

**DUMMY:** Leave this column completely blank

**entity_name:** Name of the Archaeological Entity or Relationship Entity

**element:** Specify whether or not it is a Archaeological Entity (**archent**) or Relationship Entity (**relnent**). You should put this beside the first declaration

**attribute:** Name of the attribute.

**type:** Type of the attribute. Use **file** for any thing that needs to sync with server, i.e. Photos and Attachments. Use enum for any vocabulary. Use freetext for everything else.

**identifier:** Put **true** in this field if this attribute is an identifier.

**term:** Specifies the name of a term in a vocabulary lookup.

**arch16n:** Specifies the arch16N translation of a term. Do not put {} in this field.

**pictureurl:** URL to the a picture for picture galleries

**description:** A description of the field

**parent:** Used for determining hierarchical terms. See Hierarchical Terms below.

**child:** Used for determining hierarchical relationship elements. May have been made redundant in FAIMS 2.0

### An example

| DUMMY    | entity_name | element | attribute   | type         | identifier | term    | arch16n | pictureurl                  | description       | parent     | child    |
| -------- | ----------- | ------- | ----------- | ------------ | ---------- | ------- | ------- | --------------------------- | ----------------- | ---------- | -------- |
|          | Building    | archent |             |              |            |         |         |                             | Historic building |            |          |
|          | Building    |         | Cornerstone | freetext     | TRUE       |         |         |                             | Bii's             |            |          |
|          | Building    |         | Roof        |              |            |         |         |                             | Fum, hahaha       |            |          |
|          | Building    |         | Roof Height |              |            |         |         |                             | gum               |            |          |
|          | Building    |         | Roof form   | enum         |            |         |         |                             | Roof form!        |            |          |
|          | Building    |         | Roof form   | enum         |            | term1   | term2   | files/data/gallery/test.png | asd               | -1         |          |
|          | Building    |         | Roof form   | enum         |            | term2   | term5   |                             | asd               | -1         |          |
|          | Building    |         | Roof form   | enum         |            | term3   | term4   |                             | asd               | -1         |          |
|          | Building    |         | Roof form   | enum         |            | term4   | term3   |                             | asd               | -1         |          |
|          | Building    |         | Roof form   | enum         |            | term5   | term1   |                             | asd               | -1         |          |
|          | Building    |         | Verandah    | enum         | FALSE      |         |         |                             | Verandah!         |            |          |
|          | Building    |         | Verandah    | enum         |            | term1   |         |                             | jkl               | -1         |          |
|          | Building    |         | Verandah    | enum         |            | term11  |         |                             | jkl               | 0          |          |
|          | Building    |         | Verandah    | enum         |            | term12  |         |                             | jkl               | 0          |          |
|          | Building    |         | Verandah    | enum         |            | term2   |         |                             | jkl               | -1         |          |
|          | Building    |         | Verandah    | enum         |            | term21  |         |                             | jkl               | 3          |          |
|          | Building    |         | Verandah    | enum         |            | term211 |         |                             | jkl               | 3          |          |
|          | Building    |         | Verandah    | enum         |            | term3   |         |                             | jkl               |-1          |          |
|          | Date        | relnent |             | hierarchical |            |         |         |                             | Related date      | start date | end date |

data_schema.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<dataSchema>
  <ArchaeologicalElement name="Building">
    <description>Historic building</description>
    <property name="Cornerstone" type="freetext" isIdentifier="true">
      <description>Bii’s</description>
    </property>
    <property name="Roof">
      <description>Fum, hahaha</description>
    </property>
    <property name="Roof Height">
      <description>gum</description>
    </property>
    <property name="Roof form" type="enum">
      <description>Roof form!</description>
      <lookup>
        <term pictureURL="files/data/gallery/test.png"> {term1}
          <description>asd</description>
        </term>
        <term> {term2}
          <description>asd</description>
        </term>
        <term> {term3}
          <description>asd</description>
        </term>
        <term> {term4}
          <description>asd</description>
        </term>
        <term> {term5}
          <description>asd</description>
        </term>
      </lookup>
    </property>
    <property name="Verandah" type="enum" isIdentifier="false">
      <description>Verandah!</description>
      <lookup>
        <term> term1
          <description>jkl</description>
          <term> term11
            <description>jkl</description>
          </term>
          <term> term12
            <description>jkl</description>
          </term>
        </term>
        <term> term2
          <description>jkl</description>
          <term> term21
            <description>jkl</description>
          </term>
          <term> term211
            <description>jkl</description>
          </term>
        </term>
        <term> term3
          <description>jkl</description>
        </term>
      </lookup>
    </property>
  </ArchaeologicalElement>
  <RelationshipElement name="Date" type="hierarchical">
    <description>Related date</description>
    <parent>start date</parent>
    <child>end date</child>
  </RelationshipElement>
</dataSchema>
```

arch16N.properties
```Java
term5=term5
term4=term4
term3=term3
term2=term2
term1=term1
```

### Hierarchical Terms

Hierarchical terms are a little bit complicated to express on a spreadsheet, so a key-index array scheme is implemented to handle this. Suppose we enter the following data:

| DUMMY | entity_name | element | attribute | type | identifier | term | arch16n | pictureurl | description | parent | child |
| ----- | ----------- | ------- | --------- | ---- | ---------- | ---- | ------- | ---------- | ----------- | ------ | ----- |
|       | Example     | archent |           |      |            |      |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            |      |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T1   |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T2   |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T3   |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T4   |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T5   |         |            |             |        |       |

And we want the following hierarchy:

```
T1:
  T2
T5:
  T3
  T4
```

What happens is we place T1 through to T5 in an array

| 0   | 1   | 2   | 3   | 4   |
| --- | --- | --- | --- | --- |
| T1  | T2  | T3  | T4  | T5  |

In the parent field, we specify which element in the array is the parent of that term. If the term is in the top level, the parent is -1. So to get this heirarchy, we want to have:

| DUMMY | entity_name | element | attribute | type | identifier | term | arch16n | pictureurl | description | parent | child |
| ----- | ----------- | ------- | --------- | ---- | ---------- | ---- | ------- | ---------- | ----------- | ------ | ----- |
|       | Example     | archent |           |      |            |      |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            |      |         |            |             |        |       |
|       | Example     |         | Hier-Attr | enum |            | T1   |         |            |             |  -1    |       |
|       | Example     |         | Hier-Attr | enum |            | T2   |         |            |             |   0    |       |
|       | Example     |         | Hier-Attr | enum |            | T3   |         |            |             |   4    |       |
|       | Example     |         | Hier-Attr | enum |            | T4   |         |            |             |   4    |       |
|       | Example     |         | Hier-Attr | enum |            | T5   |         |            |             |  -1    |       |

So the parent of T1 and T5 is -1 because they are at the top level. The parent of T2 is T1, so we put 0 because the index of T1 is 0. The parent of T3 and T4 is T5, so we put 4.

## ui_schema_generator.py
To run:
```bash
$ ./data_schema.py <google_spreadsheet_id>
```
Supply the Google Spreadsheet ID and it will generates an appropriate data_schema.xml file, as well as the arch16N translations.

| DUMMY | level | ref   | type  | faims_attribute_name | faims_attribute_type | certainty | annotation | read_only | hidden | label | arch16n | faims_archent_type | faims_rel_type | faims_style | faims_sync | faims_style_class |
| ----- | ----- | ----- | ----- | -------------------- | -------------------- | --------- | ---------- | --------- | ------ | ----- | ------- | ------------------ | -------------- | ----------- | ----- | ----------------- |
|       | Value | Value | Value | Value                | Value                | Value     | Value      | Value     | Value  | Value | Value   | Value              | Value          | Value       | Value | Value             |

Most of this should be self explanatory. For all the fields except for level and type, it will simply put an equals sign between the column name and column value. For example:

| DUMMY | level | ref   | type  | faims_attribute_name | faims_attribute_type | certainty | annotation | read_only | hidden | label | arch16n | faims_archent_type | faims_rel_type | faims_style | faims_sync | faims_style_class |
| ----- | ----- | ----- | ----- | -------------------- | -------------------- | --------- | ---------- | --------- | ------ | ----- | ------- | ------------------ | -------------- | ----------- | ----- | ----------------- |
|       |       | test  | input | Test                 | Test                 | TRUE      | TRUE       |           |        | Test  |         |                    |                |             |       |                   |

will output:
```
<input ref="test" faims_attribute_name="Test" faims_attribute_type="Test" faims_certainty="true" faims_annotation="true">
  <label>Test</label>
</input>
```

The *level* and *type* column are less self explanatory

### level
The level field is a number that specifies the depth of the element. In a standard UI schema, you have something like:

```
<tabgroup>
  <tab>
    <field/>
  </tab>
</tabgroup>
```

To create this, you would specify something like:


| DUMMY | level | ref      | type    | faims_attribute_name | faims_attribute_type | certainty | annotation | read_only | hidden | label | arch16n | faims_archent_type | faims_rel_type | faims_style | faims_sync | faims_style_class |
| ----- | ----- | -------- | ------- | -------------------- | -------------------- | --------- | ---------- | --------- | ------ | ----- | ------- | ------------------ | -------------- | ----------- | ----- | ----------------- |
|       | 1     | tabgroup | group   |                      |                      |           |            |           |        |       |         |                    |                |             |       |                   |
|       | 2     | tab      | group   |                      |                      |           |            |           |        |       |         |                    |                |             |       |                   |
|       | 3     | field    | trigger |                      |                      |           |            |           |        |       |         |                    |                |             |       |                   |

Of course if you want something like containers you can go as many levels deep as you want. The underlying implementation is a stack, so when you specify levels, make sure that it only increments by 1 and a time. It can decrement by as many as you want however (it just keeps popping off the stack).

### type
The *type* column is where you specify what kind of element you want. The following options are:

| type     | output                                         |
| -------- | ---------------------------------------------- |
| dropdown | &lt;select1&gt;                                |
| radio    | &lt;select1 appearance="full"&gt;              |
| list     | &lt;select1 appearance="compact"&gt;           |
| checkbox | &lt;select&gt;                                 |
| input    | &lt;input&gt;                                  |
| trigger  | &lt;trigger&gt;                                |
| group    | &lt;group&gt;                                  |
| picture  | &lt;select1 type="image"&gt;                   |
| camera   | &lt;select type="camera" faims_sync="true"&gt; |
| file     | &lt;select type="file"&gt;                     |

## arch16N_cleaner.py
To run:

```
./arch16N_cleaner.py <arch16n.properties> <ui_schema.xml> <data_schema.xml>
```

The script goes through the arch16.properties files and records all the properties. It then goes through ui_schema.xml and data_schema.xml and looks at which of the arch16N values have actually been used. It then prints out a sorted arch16N.properties file for you to use.

## convertVocab.pl
To run:

```
./convertVocab.pl <ui_logic.bsh>
```

This script is used to upgrade vocabulary populations from the FAIMS 1.3 format to the FAIMS 2.0 format. Will be redundant once all FAIMS 1.3 modules have been upgraded.

## populations.pl
To run:

```
./populations.pl <ui_schema.xml>
```

This script goes through the ui_schema.xml file and generates all the vocabulary population statements that you need in the ui_logic.bsh. Note that it cannot differentiate between a heirarchical and non-hierarchical drop down and picture gallery, so it's up to you to remember to change them to hierarchical.

## ui_logic_generator.py
To run:

```
./ui_logic_generator.py
```

Reads in arch entity names from STDIN and generates some basic methods for those arch_ents. For example:

```
echo "Water Sample" | ./ui_logic_generator.py
```