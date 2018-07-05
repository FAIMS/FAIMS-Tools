# Adding a Novel Feature to The Autogen

This file describes how to implement the autogen's built-in search tab.

## Setting up

Let's say that we want to implement the search tab as if it was the first time
doing so. Let's also say that we wanted to denote it by writing
`<tutorialsearch/>` instead of `<search/>`. To test our work as we go, we'll use
the [ES-Fish-Module](https://github.com/FAIMS/ES-Fish-Module) because it's
fairly simple while still being complicated enough to test our work.

## Extending The Validator

We'll start off by replacing the `search` element with the element that we want
to make work, `<tutorialsearch/>`. After doing that and running the validator,
you should see the following:

```
Applying @SOURCE directives...

Parsing XML...
Parsing XML completed

Validating schema...

ERROR:   Element `tutorialsearch` disallowed here.  Allowed items may include:
  - tab
  - <desc>
  - <search>
  - <fmt>
Occurs at line 15.  

Validation completed with 1 error(s) and 0 warning(s).
```

To make the validator work, we need to make small changes to three different
files in the autogen:

- `util/table.py`
- `util/consts.py`
- `util/schema.py`

### util/table.py

The diff is as follows (it may be easier to view in your terminal if it supports
colour, or on Github):

```
diff --git a/generators/christian/util/table.py b/generators/christian/util/table.py
index 195c75e..4de9d10 100644
--- a/generators/christian/util/table.py
+++ b/generators/christian/util/table.py
@@ -29,6 +29,7 @@ logic              |
 pos                |
 rels               |
 search             |
+tutorialsearch     |
 timestamp          | f
 '''
 
@@ -63,6 +64,7 @@ module          | 0 <= css     <= 1     |
 tab group       | 1 <= tab              |
 tab group       | 0 <= desc     <= 1    |
 tab group       | 0 <= search   <= 1    |
+tab group       | 0 <= tutorialsearch <= 1 |
 tab group       | 0 <= fmt      <= 1    |
 
 tab             | 0 <= autonum     <= 1 |
@@ -101,6 +103,7 @@ module               | css         | <css>
 tab group            | /[^a-z]/    | tab
 tab group            | desc        | <desc>
 tab group            | search      | <search>
+tab group            | tutorialsearch | <tutorialsearch>
 tab group            | fmt         | <fmt>
 
 tab                  | /[^a-z]/    | GUI/data element
```

The change in range `@@ -29,6 +29,7 @@` adds permitted XML attributes for the
new element. In this case, no attributes are allowed. So, for example, if your
`module.xml` file contained `<tutorialsearch f="notnull"`, an error would be
produced by the validator.

The next change (range `@@ -63,6 +64,7 @@`) tells the validator that between 0
and 1 (inclusive) `<tutorialsearch/>` elements are allowed in each tab. (You
might notice that there should be further constraints on this element. For
example, the module itself should contain no more than one `<tutorialsearch/>`
element. These can easily be added using the `DESCENDANT COUNT` column in the
`CARDINALITIES` string.)

The final change (range `@@ -101,6 +103,7 @@`) allows the validator to provide
a list of "Allowed items" if the `module.xml` file is invalid.

### util/consts.py

The diff is as follows:

```
diff --git a/generators/christian/util/consts.py b/generators/christian/util/consts.py
index 1e1a408..eb0af1a 100644
--- a/generators/christian/util/consts.py
+++ b/generators/christian/util/consts.py
@@ -96,6 +96,7 @@ TAG_OPTS      = 'opts'
 TAG_POS       = 'pos'
 TAG_RELS      = 'rels'
 TAG_SEARCH    = 'search'
+TAG_TUTORIALSEARCH = 'tutorialsearch'
 TAG_STR       = 'str'
 TAG_TIMESTAMP = 'timestamp'
 TAGS = [
@@ -151,6 +152,7 @@ TYPE_OPTS      = 'opts'
 TYPE_POS       = 'pos'
 TYPE_RELS      = 'rels'
 TYPE_SEARCH    = 'search'
+TYPE_TUTORIALSEARCH = 'tutorialsearch'
 TYPE_STR       = 'str'
 TYPE_TAB       = 'tab'
 TYPE_TAB_GROUP = 'tab group'
```

These added variables will be used in `util/schema.py`.
`TAG_TUTORIALSEARCH` refers to our new element's XML tag name (i.e.
"tutorialsearch", whereas `TYPE_TUTORIALSEARCH` refers to its "XML type".
(Search for "XML Types" in `util/consts.py` for an explanation of XML types.)

### util/schema.py

```
@@ -393,6 +393,7 @@ def annotateWithXmlTypes(node):
         if   util.isNonLower(node.tag):   type = TYPE_TAB
         elif node.tag == TAG_DESC:        type = TYPE_DESC
         elif node.tag == TAG_SEARCH:      type = TYPE_SEARCH
+        elif node.tag == TAG_TUTORIALSEARCH:   type = TYPE_TUTORIALSEARCH
         elif node.tag == TAG_FMT:         type = TYPE_FMT
     elif parentType == TYPE_TAB:
         if   guessedType == TAG_GROUP:    type = TYPE_GROUP
```

This change allows the new element's XML type to be inferred. It says that
anything inside a tab group whose tag is `TAG_TUTORIALSEARCH` should be given
the XML type `TYPE_TUTORIALSEARCH`.

### Testing The Changes

Now when we run the validator again, we should see the following:

```
Applying @SOURCE directives...

Parsing XML...
Parsing XML completed

Validating schema...

Validation completed with 0 error(s) and 0 warning(s).
```

## Extending The Generator

### Re-writing `module.xml`

(The changes described in this section occur in `util/schema.py`.)

The generator produces some elements by first re-writing them in a more verbose
form. We'll implment the `<tutorialsearch/>` element so that it'll be expanded
into the following 11 lines:

```
<Tutorial_Search f="nodata noscroll">
  <Colgroup_0 s="orientation" t="group">
    <Col_0 s="even" t="group">
      <Search_Term t="input"/>
    </Col_0>
    <Col_1 s="large" t="group">
      <Search_Button t="button">Search</Search_Button>
    </Col_1>
  </Colgroup_0>
  <Entity_List t="list"/>
</Tutorial_Search>
```

Note that this is a valid snippet of `module.xml`. Even without modifying the
autogen, you can write this to produce a search tab. (The only problem is that
it wouldn't have any logic to make it do something.)

The way the expansion happens in the autogen is complicated somewhat by the
fact that you need to do as `util.schema.annotateWithXmlTypes` would and
annotate each element with an appropriate `__RESERVED_XML_TYPE__`. (Ideally,
this necessity would be refactored away from the autogen.) What this entails is
that we actually want to re-write `<tutorialsearch/>` as the following:

```
<Tutorial_Search f="nodata noscroll" __RESERVED_XML_TYPE__="tutorialsearch">
   <Colgroup_0 s="orientation" t="group" __RESERVED_XML_TYPE__="cols">
      <Col_0 s="even" t="group" __RESERVED_XML_TYPE__="col">
         <Search_Term t="input" __RESERVED_XML_TYPE__="GUI/data element"/>
      </Col_0>
      <Col_1 s="large" t="group" __RESERVED_XML_TYPE__="col">
         <Search_Button t="button" __RESERVED_XML_TYPE__="GUI/data element">Search</Search_Button>
      </Col_1>
   </Colgroup_0>
   <Entity_List t="list" __RESERVED_XML_TYPE__="GUI/data element"/>
</Tutorial_Search>
```

This is the expanded form we'd like to produce as the autogen runs. To make this
expansion take place, we modify the `normaliseSchemaRec` by calling a function
`getTutorialSearch` which will produce the expanded form of `<tutorialsearch/>`.
We haven't written this function yet, but its argument will be the
`<tutorialsearch/>` node as an `lxml.etree._Element`:

```
@@ -494,6 +496,7 @@ def normaliseSchemaRec(node):
     if getXmlType(node) == TYPE_AUTONUM:   newNodes = getAutonum  (node)
     if getXmlType(node) == TYPE_GPS:       newNodes = getGps      (node)
     if getXmlType(node) == TYPE_SEARCH:    newNodes = getSearch   (node)
+    if getXmlType(node) == TYPE_TUTORIALSEARCH: newNodes = getTutorialSearch(node)
     if getXmlType(node) == TYPE_TIMESTAMP: newNodes = getTimestamp(node)
     newNodes = xml.replaceElement(node, newNodes)
```

Now we'll implement the `getTutorialSearch` function. This returns a tuple of
`lxml.etree._Element`s which represents the expanded, annotated `module.xml`
code that we saw above. (Actually, `getTutorialSearch(node)` also includes an
'Entity List' dropdown if the module has more than one archent.) The code is as
follows:

```
@@ -840,6 +843,36 @@ def getSearch(node):
 
     return search,
 
+def getTutorialSearch(node):
+    search = Element(
+            'Tutorial_Search',
+            { RESERVED_XML_TYPE : TYPE_TAB },
+            f='nodata noscroll'
+    )
+    cols = SubElement(search, 'Colgroup_0', { RESERVED_XML_TYPE : TYPE_COLS }, t=UI_TYPE_GROUP, s='orientation')
+    lCol = SubElement(cols,   'Col_0',      { RESERVED_XML_TYPE : TYPE_COL  }, t=UI_TYPE_GROUP, s='even')
+    rCol = SubElement(cols,   'Col_1',      { RESERVED_XML_TYPE : TYPE_COL  }, t=UI_TYPE_GROUP, s='large')
+
+    term = SubElement(lCol,   'Search_Term',   t=UI_TYPE_INPUT)
+    btn  = SubElement(rCol,   'Search_Button', t=UI_TYPE_BUTTON)
+
+    # Add 'Entity Types' dropdown if there's more than one entity to choose from
+    isGuiAndData = lambda e: util.gui. isGuiNode    (e) and \
+                             util.data.isDataElement(e)
+    nodes = getTabGroups(node, isGuiAndData, descendantOrSelf=False)
+    if len(nodes) > 1:
+        SubElement(search, 'Entity_Types', t=UI_TYPE_DROPDOWN)
+
+    SubElement(search, 'Entity_List',  t=UI_TYPE_LIST)
+
+    for n in search:
+        annotateWithXmlTypes(n)
+    search.attrib[RESERVED_XML_TYPE] = TYPE_TUTORIALSEARCH
+
+    btn.text = 'Search'
+
+    return search,
+
```

We also need to modify the `isTab` function so that it recognises the
`__RESERVED_XML_TYPE__="tutorialsearch"` element as a tab:

@@ -1007,7 +1039,7 @@ def isTabGroup(node):
     return getXmlType(node) == TYPE_TAB_GROUP
 
 def isTab(node):
-    return getXmlType(node) in (TYPE_TAB, TYPE_SEARCH)
+    return getXmlType(node) in (TYPE_TAB, TYPE_SEARCH, TYPE_TUTORIALSEARCH)

Additionally, we need to modify the `getPath` function:

```
@@ -44,6 +44,7 @@ def getPath(node, isInitialCall=True):
     nodeTypes = [
             TYPE_GUI_DATA,
             TYPE_SEARCH,
+            TYPE_TUTORIALSEARCH,
             TYPE_TAB,
             TYPE_TAB_GROUP,
             TYPE_AUTHOR,
```

This change allows the autogen to use XML elements having
`__RESERVED_XML_TYPE__="tutorialsearch"` in refs in the `ui_logic.bsh` file. If
we didn't include it, instead of getting paths like
`"Control/Tutorial_Search/Entity_List"` or
`"Control/Tutorial_Search/Search_Term"`, when we called `util.schema.getPath`,
we'd get `"Control/Entity_List"` or `"Control/Search_Term"` instead.

The autogen should now treat `<tutorialsearch/>` as if it was the 11 lines of
XML mentioned at the start of this section. This can be verified by running
`./generate.sh -w` and checking the `ui_logic.bsh`, `ui_schema.xml` and
`english.0.properties` files. The 'Tutorial Search' tab should also be rendered
in the wireframe.

### Generating Logic

To make the new `<tutorialsearch/>` element do something, the autogen needs to
produce logic for it. In this case, we'll acheive this using a combination of
the `generator/module/uilogic-template.bsh` file and
`generator/module/uilogic.py`. `uilogic.py` modifies `uilogic-template.bsh` to
produce the `ui_logic.bsh` file. By convention these modifications are
predominantly the replacement of things in `{{double-curly-braces}}` however,
arbitrary modifications are possible.

The change we need to make to `uilogic-template.bsh` is as follows:

```
@@ -3597,6 +3597,48 @@ void search(){
 {{defs-load-entity}}
 
 /******************************************************************************/
+/*                              TUTORIAL SEARCH                               */
+/******************************************************************************/
+{{binds-tutorial-search}}
+
+{{tutorial-search-entities}}
+
+void clearSearch(){
+  setFieldValue("{{tab-group-tutorial-search}}/Tutorial_Search/Search_Term","");
+}
+
+void tutorialSearch(){
+  String refEntityList  = "{{tab-group-tutorial-search}}/Tutorial_Search/Entity_List";
+  String refSearchTerm  = "{{tab-group-tutorial-search}}/Tutorial_Search/Search_Term";
+  String refEntityTypes = "{{tab-group-tutorial-search}}/Tutorial_Search/Entity_Types";
+
+  {{type-tutorial-search}}
+  String term = getFieldValue(refSearchTerm);
+  String searchQuery = "SELECT uuid, response "+
+                       "  FROM latestNonDeletedArchEntFormattedIdentifiers  "+
+                       " WHERE uuid in (SELECT uuid "+
+                       "                  FROM latestNonDeletedArchEntIdentifiers "+
+                       "                 WHERE measure LIKE {term}||'%'  "+
+                       "                   AND ( aenttypename = {type} OR '' = {type} ) "+
+                       "                )  "+
+                       " ORDER BY substr(uuid, 7, 13) desc, response " +
+                       " LIMIT ? "+
+                       "OFFSET ? ";
+  searchQuery = dbReplaceFirst(searchQuery, "{term}", term);
+  searchQuery = dbReplaceFirst(searchQuery, "{type}", type);
+  searchQuery = dbReplaceFirst(searchQuery, "{type}", type);
+
+  populateMenu(refEntityList, MSG_LOADING);
+  populateCursorList(refEntityList, searchQuery, 25);
+  refreshTabgroupCSS("{{tab-group-tutorial-search}}");
+
+  Log.d("Module", "Search query: " + searchQuery);
+}
+
+{{tutorial-defs-load-entity}}
+
+
+/******************************************************************************/
 /*                          TAKE FROM GPS BUTTON(S)                           */
 /******************************************************************************/
 {{binds-take-from-gps}}
```

The parts in double curly braces will be replaced as follows:

* {{binds-tutorial-search}} -- Calls to `addOnEvent` which allow the newly defined functions (e.g. `clearSearch`, `tutorialSearch`, etc) to be triggered.
* {{tutorial-search-entities}} -- Code allowing the 'Entity Types' dropdown to work. If the 'entity types' dropdown isn't needed, the generated code will be the empty string.
* {{type-tutorial-search}} -- The definition of the `type` variable which will be used in the `searchQuery`.
* {{tutorial-defs-load-entity}} -- Defines the `load*From(String)` functions. For the ES-Fish-Module, only `loadFishFrom(String)` will be produced.

To replace the parts of the template with curly braces, we will define the following
functions in `uilogic.py`:

```
@@ -838,6 +838,92 @@ def getNavButtonBindsAdd(tree, t):
 
     return t.replace(placeholder, replacement)
 
+def getTutorialSearchTabGroupString(tree):
+    hasSearchType = lambda e: util.schema.getXmlType(e) == TYPE_TUTORIALSEARCH
+    nodes = util.xml.getAll(tree, hasSearchType)
+    if not len(nodes): return ''
+    search = nodes[0]
+    searchTG = util.schema.getParentTabGroup(search)
+    return util.schema.getPathString(searchTG)
+
+def getTutorialSearchBinds(tree, t):
+    placeholder = '{{binds-tutorial-search}}'
+    tgStr = getTutorialSearchTabGroupString(tree)
+    if not tgStr:
+        return t.replace(placeholder, '')
+
+    replacement = \
+      'addOnEvent("{{tab-group-tutorial-search}}/Tutorial_Search"               , "show"  , "tutorialSearch()");' \
+    '\naddOnEvent("{{tab-group-tutorial-search}}/Tutorial_Search/Entity_List"   , "click" , "loadEntity();");' \
+    '\naddOnEvent("{{tab-group-tutorial-search}}/Tutorial_Search/Search_Button" , "click" , "tutorialSearch()");' \
+    '\naddOnEvent("{{tab-group-tutorial-search}}/Tutorial_Search/Search_Term"   , "click" , "clearSearch()");' \
+
+    return t.replace(placeholder, replacement)
+
+def getTutorialSearchTabGroup(tree, t):
+    placeholder = '{{tab-group-tutorial-search}}'
+    replacement = getTutorialSearchTabGroupString(tree)
+
+    return t.replace(placeholder, replacement)
+
+def getTutorialSearchEntities(tree, t):
+    hasSearchType = lambda e: util.schema.getXmlType(e) == TYPE_TUTORIALSEARCH
+    searchNodes = util.xml.getAll(tree, hasSearchType)
+
+    nodes = util.schema.getTabGroups(tree, isGuiAndData)
+    arch16nKeys  = [util.arch16n.getArch16nKey(n) for n in nodes]
+    archEntNames = [util.data.getArchEntName  (n) for n in nodes]
+
+    placeholder = '{{tutorial-search-entities}}'
+    fmt         = 'entityTypes.add(new NameValuePair("%s", "%s"));'
+    replacement = \
+      'addOnEvent("{{tab-group-tutorial-search}}/Tutorial_Search/Entity_Types"  , "click" , "tutorialSearch()");' \
+    '\nentityTypes = new ArrayList();' \
+    '\nentityTypes.add(new NameValuePair("{All}", ""));' + \
+    '\n' + format(zip(arch16nKeys, archEntNames), fmt) + \
+    '\npopulateDropDown("{{tab-group-tutorial-search}}/Tutorial_Search/Entity_Types", entityTypes);'
+    if len(nodes) <= 1 or len(searchNodes) < 1:
+        replacement = ''
+
+    return t.replace(placeholder, replacement)
+
+def getTutorialSearchType(tree, t):
+    nodes = util.schema.getTabGroups(tree, isGuiAndData)
+
+    placeholder = '{{type-tutorial-search}}'
+    if len(nodes) <= 1:
+        replacement = 'String type = "";'
+    else:
+        replacement = 'String type = getFieldValue(refEntityTypes);'
+
+    return t.replace(placeholder, replacement)
+
+def getTutorialLoadEntityDefs(tree, t):
+    nodes    = util.schema.getTabGroups(tree, isGuiAndData)
+    refs     = [util.schema.getPathString(n) for n in nodes]
+    funNames = [getFunName(n) for n in nodes]
+
+    placeholder = '{{tutorial-defs-load-entity}}'
+    fmt = \
+      'void load%sFrom(String uuid) {' \
+    '\n  String tabgroup = "%s";' \
+    '\n  setUuid(tabgroup, uuid);' \
+    '\n  if (isNull(uuid)) return;' \
+    '\n' \
+    '\n  FetchCallback cb = new FetchCallback() {' \
+    '\n    onFetch(result) {' \
+    '\n      populateEntityListsInTabGroup(tabgroup);' \
+    '\n      executeOnEvent(tabgroup, "fetch");' \
+    '\n    }' \
+    '\n  };' \
+    '\n' \
+    '\n  executeOnEvent(tabgroup, "prefetch");' \
+    '\n  showTabGroup(tabgroup, uuid, cb);' \
+    '\n}'
+    replacement = format(zip(funNames, refs), fmt)
+
+    return t.replace(placeholder, replacement)
+
```

Notice that the defined functions take up to two arguments:

* `tree` -- An `lxml.etree._Element` object which represents the processed `module.xml` file. You can view `tree` as human-readable XML by looking for an .xml file in your `/tmp` directory. It'll be named something like `222603639f82cc84c55be011fb262a987aa8f3618a449da93e95b75414e8a8de.xml`.
* `t` -- A string containging the UI logic template.

To use the newly defined functions, we call them from within `getUiLogic`:

```
@@ -1122,6 +1212,11 @@ def getUiLogic(tree):
     t = getDefsTabGroupBinds(tree, t)
     t = getNavButtonBindsDel(tree, t)
     t = getNavButtonBindsAdd(tree, t)
+    t = getTutorialSearchBinds(tree, t)
+    t = getTutorialSearchEntities(tree, t)
+    t = getTutorialSearchType(tree, t)
+    t = getTutorialSearchTabGroup(tree, t)
+    t = getTutorialLoadEntityDefs(tree, t)
     t = getSearchBinds(tree, t)
     t = getSearchEntities(tree, t)
     t = getSearchType(tree, t)
```

This completes the needed changes. Run `./generate.sh` and check the
`ui_logic.bsh`. It should contain the following:

```
/******************************************************************************/
/*                              TUTORIAL SEARCH                               */
/******************************************************************************/
addOnEvent("Control/Tutorial_Search"               , "show"  , "tutorialSearch()");
addOnEvent("Control/Tutorial_Search/Entity_List"   , "click" , "loadEntity();");
addOnEvent("Control/Tutorial_Search/Search_Button" , "click" , "tutorialSearch()");
addOnEvent("Control/Tutorial_Search/Search_Term"   , "click" , "clearSearch()");



void clearSearch(){
  setFieldValue("Control/Tutorial_Search/Search_Term","");
}

void tutorialSearch(){
  String refEntityList  = "Control/Tutorial_Search/Entity_List";
  String refSearchTerm  = "Control/Tutorial_Search/Search_Term";
  String refEntityTypes = "Control/Tutorial_Search/Entity_Types";

  String type = "";
  String term = getFieldValue(refSearchTerm);
  String searchQuery = "SELECT uuid, response "+
                       "  FROM latestNonDeletedArchEntFormattedIdentifiers  "+
                       " WHERE uuid in (SELECT uuid "+
                       "                  FROM latestNonDeletedArchEntIdentifiers "+
                       "                 WHERE measure LIKE {term}||'%'  "+
                       "                   AND ( aenttypename = {type} OR '' = {type} ) "+
                       "                )  "+
                       " ORDER BY substr(uuid, 7, 13) desc, response " +
                       " LIMIT ? "+
                       "OFFSET ? ";
  searchQuery = dbReplaceFirst(searchQuery, "{term}", term);
  searchQuery = dbReplaceFirst(searchQuery, "{type}", type);
  searchQuery = dbReplaceFirst(searchQuery, "{type}", type);

  populateMenu(refEntityList, MSG_LOADING);
  populateCursorList(refEntityList, searchQuery, 25);
  refreshTabgroupCSS("Control");

  Log.d("Module", "Search query: " + searchQuery);
}

void loadFishFrom(String uuid) {
  String tabgroup = "Fish";
  setUuid(tabgroup, uuid);
  if (isNull(uuid)) return;

  FetchCallback cb = new FetchCallback() {
    onFetch(result) {
      populateEntityListsInTabGroup(tabgroup);
      executeOnEvent(tabgroup, "fetch");
    }
  };

  executeOnEvent(tabgroup, "prefetch");
  showTabGroup(tabgroup, uuid, cb);
}
```
