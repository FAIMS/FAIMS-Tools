FAIMS-Tools
===========
These are a collection of tools designed to help with developing modules faster. They are written in a variety of languages, mostly which ever language is most convenient for the job. 
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
T1:

>T2

T5:

>T3

>T4

What happens is we place T1 through to T5 in an array

| 0  | 1  | 2  | 3  | 4  |
| -- | -- | -- | -- | -- |
| T1 | T2 | T3 | T4 | T5 |

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
## arch16N_cleaner.py
## convertVocab.pl
## populations.pl
## ui_logic_generator.py
