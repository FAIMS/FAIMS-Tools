#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.gui
import util.arch16n
import util.xml
import util.data
from   util.consts import *

def format(tuples, fmt='%s', indent='', newline='\n'):
    sep = newline + indent
    return sep.join(fmt % tuple for tuple in tuples)

def getUserMenuUiType(tree):
    isFlagged = lambda e: util.schema.isFlagged(e, FLAG_USER)
    nodes = util.xml.getAll(tree, isFlagged)
    if len(nodes) != 1: return None
    node = nodes[0]
    return util.schema.guessType(node)

def isGuiAndData(e):
    return util.gui. isGuiNode    (e) and \
           util.data.isDataElement(e)

def getTabGroups(tree, t):
    nodes = util.schema.getTabGroups(tree)
    refs  = [util.schema.getPathString(tg) for tg in nodes]

    fmt          = 'tabGroups.add("%s");'
    placeholder  = '{{get-tab-groups}}'
    replacement  = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getDropdownValueGetters(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_DROPDOWN)
    refs  = [util.schema.getPathString(n) for n in nodes]
    refs  = zip(refs, refs)

    fmt          = 'addOnEvent("%s", "click", "DROPDOWN_ITEM_VALUE = getFieldValue(\\"%s\\")");'
    placeholder  = '{{dropdown-value-getters}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getGpsDiagUpdate(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_GPSDIAG)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt          = 'addOnEvent("%s", "show", "updateGPSDiagnostics()");'
    placeholder  = '{{gps-diag-update}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getGpsDiagRef(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_GPSDIAG)
    refs  = [util.schema.getPathString(n) for n in nodes]

    placeholder  = '{{gps-diag-ref}}'
    replacement  = format(refs)

    return t.replace(placeholder, replacement)

def getUsers(tree, t):
    isFlagged = lambda e: util.schema.isFlagged(e, FLAG_USER)
    nodes = util.xml.getAll(tree, isFlagged)
    refs  = [util.schema.getPathString(n) for n in nodes]

    placeholder  = '{{user-menu-path}}'
    replacement  = format(refs)

    return t.replace(placeholder, replacement)

def getUsersPopulateCall(tree, t):
    placeholder = '{{users-populate-call}}'

    if   getUserMenuUiType(tree) == UI_TYPE_LIST:
        replacement = 'populateList(userMenuPath, result);'
    elif getUserMenuUiType(tree) == UI_TYPE_DROPDOWN:
        replacement = 'populateDropDown(userMenuPath, result, true);'
    else:
        replacement = 'return;'

    return t.replace(placeholder, replacement)

def getUsersVocabId(tree, t):
    placeholder = '{{users-vocabid}}'

    if   getUserMenuUiType(tree) == UI_TYPE_LIST:
        replacement = 'String userVocabId = getListItemValue();'
    elif getUserMenuUiType(tree) == UI_TYPE_DROPDOWN:
        replacement = 'String userVocabId = getFieldValue(userMenuPath);'
    else:
        replacement = 'return;'

    return t.replace(placeholder, replacement)

def getValidationString(archEntType, fieldPairs):
    fpFmt = 'f.add(fieldPair("%s", "%s"));'
    fpStr = format(fieldPairs, fpFmt, indent='  ')

    s  = \
      'void validate%s() {' \
    '\n  List f = new ArrayList(); // Fields to be validated' \
    '\n  %s' \
    '\n' \
    '\n  String validationMessage = validateFields(f, "PLAINTEXT");' \
    '\n  showWarning("Validation Results", validationMessage);' \
    '\n}' \
    '\n'

    s %= archEntType, fpStr

    return s

def getValidation(tree, t):
    placeholder = '{{validation}}'
    replacement = ''

    # Tab groups which can be validated
    isNotNull = lambda e: util.schema.hasElementFlaggedWith(e, FLAG_NOTNULL)
    tabGroups = util.schema.getTabGroups(tree, isNotNull)
    for n in tabGroups:
        archEntName = util.data.getArchEntName(n)
        #if not archEntName: continue

        # Validate-able nodes
        V = util.xml.getAll(n, lambda n: util.schema.isFlagged(n, FLAG_NOTNULL))
        # Field pairs
        refs   = [util.schema. getPathString(v)                    for v in V]
        labels = [util.arch16n.getArch16nKey(v, doAddCurlies=True) for v in V]
        fieldPairs = zip(refs, labels)

        replacement += getValidationString(archEntName, fieldPairs)

    return t.replace(placeholder, replacement)

def getMakeVocab(tree, t):
    nodes     = util.gui.getAll(tree, MENU_UI_TYPES, util.data.isDataElement)

    types     = []
    attrNames = [util.data.  getAttribName(n) for n in nodes]
    refs      = [util.schema.getPathString(n) for n in nodes]

    # Compute types of nodes
    for n in nodes:
        isHierarchical = util.schema.isHierarchical(n)
        uiType         = util.schema.guessType(n)

        # Determine hierarchical-ness
        if isHierarchical: type = 'Hierarchical'
        else:              type = ''

        # Determine the rest of the type
        if uiType == UI_TYPE_CHECKBOX: type += 'CheckBoxGroup'
        if uiType == UI_TYPE_DROPDOWN: type += 'DropDown'
        if uiType == UI_TYPE_LIST:     type += 'List'
        if uiType == UI_TYPE_PICTURE:  type += 'PictureGallery'
        if uiType == UI_TYPE_RADIO:    type += 'RadioGroup'

        types.append(type)

    fmt         = 'makeVocab("%s", "%s", "%s")'
    placeholder = '{{make-vocab}}'
    replacement = format(zip(types, attrNames, refs), fmt)

    return t.replace(placeholder, replacement)

def getAuthor(tree, t):
    isAuthor      = lambda e: util.schema.getType(e) == TAG_AUTHOR
    authors       = util.xml.getAll(tree, isAuthor)
    tabGroupNames = [util.schema.getParentTabGroup(a).tag for a in authors]
    refs          = [util.schema.getPathString(a)               for a in authors]

    fmt         = 'tabgroupToAuthor.put("%s", "%s");'
    placeholder = '{{author}}'
    replacement = format(zip(tabGroupNames, refs), fmt)

    return t.replace(placeholder, replacement)

def getTimestamp(tree, t):
    isTimestamp   = lambda e: util.schema.getType(e) == TAG_TIMESTAMP
    timestamp     = util.xml.getAll(tree, isTimestamp)
    tabGroupNames = [util.schema.getParentTabGroup(a).tag for a in timestamp]
    refs          = [util.schema.getPathString(a)         for a in timestamp]

    fmt         = 'tabgroupToTimestamp.put("%s", "%s");'
    placeholder = '{{timestamp}}'
    replacement = format(zip(tabGroupNames, refs), fmt)

    return t.replace(placeholder, replacement)

def getOnShowDefs(tree, t):
    tabGroups    = util.schema.getTabGroups(tree, isGuiAndData)
    archEntNames = [util.data.getArchEntName(e)  for e in tabGroups]
    tabGroupRefs = [util.schema.getPathString(e) for e in tabGroups]

    placeholder = '{{defs-on-show}}'
    fmt = \
    'void onShow%s () {\n' \
    '  saveTabGroup("%s");\n' \
    '}\n'
    replacement = format(zip(archEntNames, tabGroupRefs), fmt)

    return t.replace(placeholder, replacement)

def getOnShowBinds(tree, t):
    tabGroups    = util.schema.getTabGroups(tree, isGuiAndData)
    tabGroupRefs = [util.schema.getPathString(e) for e in tabGroups]
    onShowFuns   = [util.data.getAttribName(e)   for e in tabGroups]

    placeholder = '{{binds-on-show}}'
    fmt         = 'addOnEvent("%s", "show", "onShow%s()");'
    replacement = format(zip(tabGroupRefs, onShowFuns), fmt)

    return t.replace(placeholder, replacement)

def getOnClickNodes(tree):
    hasL  = lambda e: util.xml.hasAttrib(e, ATTRIB_L)
    hasLC = lambda e: util.xml.hasAttrib(e, ATTRIB_L)
    return xml.getAll(tree, lambda e: hasL(e) or hasLC(e))

def getXLinksToY(tree, attribVal, noData):
    assert attribVal in (ATTRIB_L, ATTRIB_LC)
    assert type(noData) == bool

    if noData:
        isXLinkToY = lambda e: util.xml.hasAttrib(e, attribVal) and \
                not util.data.isDataElement(util.schema.getLinkedNode(e))
    else:
        isXLinkToY = lambda e: util.xml.hasAttrib(e, attribVal) and \
                util.data.isDataElement(util.schema.getLinkedNode(e))

    return util.xml.getAll(tree, isXLinkToY)

def getOnClickDefs(tree, t):
    placeholder = '{{defs-on-click}}'

    # @l link to 'nodata' tab or tab group
    fmtLND = \
      'void onClick%s () {' \
    '\n  newTab("%s", true);' \
    '\n}'

    # @l link to savable tab group
    fmtLD = \
      'void onClick%s () {' \
    '\n  parentTabgroup__ = "%s";' \
    '\n  new%s();' \
    '\n}'

    # @lc link
    fmtLC = \
      'void onClick%s () {' \
    '\n  String tabgroup = "%s";' \
    '\n  if (isNull(getUuid(tabgroup))){' \
    '\n    showToast("{You_must_save_this_tabgroup_first}");' \
    '\n    return;' \
    '\n  }' \
    '\n  parentTabgroup   = tabgroup;' \
    '\n  parentTabgroup__ = tabgroup;' \
    '\n  new%s();' \
    '\n}'

    LNDNodes = getXLinksToY(tree, ATTRIB_L,  noData=True)
    LDNodes  = getXLinksToY(tree, ATTRIB_L,  noData=False)
    LCNodes  = getXLinksToY(tree, ATTRIB_LC, noData=False)

    strLND = format(
            zip(
                [util.schema.getPathString(e, sep='') for e in LNDNodes],
                [util.xml.getAttribVal(e, ATTRIB_L)   for e in LNDNodes]
            ),
            fmtLND,
            newline='\n\n'
    )

    strLD = format(
            zip(
                [util.schema.getPathString(e, sep='') for e in LDNodes],
                [util.schema.getParentTabGroup(e).tag for e in LDNodes],
                [util.xml.getAttribVal(e, ATTRIB_L)   for e in LDNodes]
            ),
            fmtLD,
            newline='\n\n'
    )

    strLC = format(
            zip(
                [util.schema.getPathString(e, sep='') for e in LCNodes],
                [util.schema.getParentTabGroup(e).tag for e in LCNodes],
                [util.xml.getAttribVal(e, ATTRIB_LC)  for e in LCNodes]
            ),
            fmtLC,
            newline='\n\n'
    )

    replacement = '\n\n'.join([strLND, strLD, strLC])

    return t.replace(placeholder, replacement)

def getOnClickBinds(tree, t):
    LNDNodes = getXLinksToY(tree, ATTRIB_L,  noData=True)
    LDNodes  = getXLinksToY(tree, ATTRIB_L,  noData=False)
    LCNodes  = getXLinksToY(tree, ATTRIB_LC, noData=False)

    nodes = LNDNodes + LDNodes + LCNodes
    refs  = [util.schema.getPathString(n)         for n in nodes]
    funs  = [util.schema.getPathString(n, sep='') for n in nodes]

    placeholder = '{{binds-on-click}}'
    fmt         = 'addOnEvent("%s", "click", "onClick%s")'
    replacement = format(zip(refs, funs), fmt)

    return t.replace(placeholder, replacement)

def getMediaBinds(tree, t):
    nodesAudio  = util.gui.getAll(tree, UI_TYPE_AUDIO)
    nodesCamera = util.gui.getAll(tree, UI_TYPE_CAMERA)
    nodesFile   = util.gui.getAll(tree, UI_TYPE_FILE)
    nodesVideo  = util.gui.getAll(tree, UI_TYPE_VIDEO)

    refsAudio  = [util.schema.getPathString(n) for n in nodesAudio]
    refsCamera = [util.schema.getPathString(n) for n in nodesCamera]
    refsFile   = [util.schema.getPathString(n) for n in nodesFile]
    refsVideo  = [util.schema.getPathString(n) for n in nodesVideo]

    btnRefsAudio  = [util.schema.getPathString(n.getnext()) for n in nodesAudio]
    btnRefsCamera = [util.schema.getPathString(n.getnext()) for n in nodesCamera]
    btnRefsFile   = [util.schema.getPathString(n.getnext()) for n in nodesFile]
    btnRefsVideo  = [util.schema.getPathString(n.getnext()) for n in nodesVideo]

    fmtAudio  = 'addOnEvent("%s", "click", "attachAudioTo(\\"%s\\"));'
    fmtCamera = 'addOnEvent("%s", "click", "attachPictureTo(\\"%s\\"));'
    fmtFile   = 'addOnEvent("%s", "click", "attachFileTo(\\"%s\\"));'
    fmtVideo  = 'addOnEvent("%s", "click", "attachVideoTo(\\"%s\\"));'

    replacementAudio  = format(zip(refsAudio,  btnRefsAudio),  fmtAudio)
    replacementCamera = format(zip(refsCamera, btnRefsCamera), fmtCamera)
    replacementFile   = format(zip(refsFile,   btnRefsFile),   fmtFile)
    replacementVideo  = format(zip(refsVideo,  btnRefsVideo),  fmtVideo)

    placeholder = '{{binds-media}}'
    replacement = '\n'.join([
        replacementAudio,
        replacementCamera,
        replacementFile,
        replacementVideo
    ])

    return t.replace(placeholder, replacement)

def getFileBinds(tree, t):
    nodes  = util.gui.getAll(tree, UI_TYPE_VIEWFILES)
    refs   = [util.schema.getPathString(n)         for n in nodes]
    tgRefs = [util.schema.getParentTabGroup(n).tag for n in nodes]

    placeholder = '{{binds-files}}'
    fmt         = 'addOnEvent("%s", "click", "viewArchEntAttachedFiles(getUuid(\\"%s\\"))");'
    replacement = format(zip(refs, tgRefs), fmt)

    return t.replace(placeholder, replacement)

def getTabGroupsToValidate(tree, t):
    nodes = util.xml.getAll(tree, lambda e: util.schema.isFlagged(e, FLAG_NOTNULL))
    nodes = [util.schema.getParentTabGroup(n) for n in nodes]
    refs  = [util.schema.getPathString(n)     for n in nodes]
    refs  = list(set(refs))

    placeholder = '{{tabgroups-to-validate}}'
    fmt         = 'tabgroupsToValidate.add("%s");'
    replacement = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getNoNextIds(tree):
    # Get the path of the autonum tag's parent
    wasAutoNum  = lambda e: util.xml.getAttribVal(e, ORIGINAL_TAG) == TAG_AUTONUM
    nodes       = util.xml.getAll(tree.getroottree(), wasAutoNum)
    if not len(nodes): return ''
    node        = nodes[0]
    autoNumTab  = util.schema.getParentTab(node)
    autoNumPath = util.schema.getPath(autoNumTab)

    # Get the paths of the autonumed elements in tree
    isAutoNumed    = lambda e: util.schema.isFlagged(e, FLAG_AUTONUM)
    nodes          = util.xml.getAll(tree, isAutoNumed)
    autoNummedPath = [util.schema.getPath(n)[-1] for n in nodes]
    autoNummedPath = [['Next_' + n] for n in autoNummedPath]

    if not len(autoNummedPath): return ''

    refs = [autoNumPath + numed for numed in autoNummedPath]
    refs = ['/'.join(r) for r in refs]

    fmt = \
        'if (isNull("%s")) {' \
    '\n    showWarning("{Alert}", "{A_next_ID_has_not_been_entered_please_provide_one}");' \
    '\n    return;' \
    '\n  }'

    return format(refs, fmt, indent='  ')

def getIncAutoNum(tree):
    # Get refs for nodes flagged with 'autonum'
    isAutoNumed = lambda e: util.schema.isFlagged(e, FLAG_AUTONUM)
    nodes       = util.xml.getAll(tree, isAutoNumed)
    refs        = [util.schema.getPathString(n) for n in nodes]

    fmt = 'incAutoNum("%s");'
    return format(refs, fmt, indent='  ')

def getDefsTabGroupBindsNew(tree):
    nodes        = util.schema.getTabGroups(tree, isGuiAndData)
    refs         = [util.schema.getPathString(n) for n in nodes]
    noNextIds    = [getNoNextIds (n) for n in nodes]
    incAutoNums  = [getIncAutoNum(n) for n in nodes]

    fmt = \
      'void new%s (){' \
    '\n  String tabgroup = "%s";' \
    '\n  %s' \
    '\n' \
    '\n  setUuid(tabgroup, null);' \
    '\n  newTabGroup(tabgroup);' \
    '\n  populateAuthorAndTimestamp(tabgroup);' \
    '\n  populateEntityListsInTabGroup(tabgroup);' \
    '\n  %s' \
    '\n' \
    '\n  onCreate%s__();' \
    '\n}'

    return format(zip(refs, refs, noNextIds, incAutoNums, refs), fmt)

def getDefsTabGroupBindsEvents(tree, funName, evtName):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]
    funNames = [funName]*len(nodes)
    evtNames = [evtName]*len(nodes)

    fmt =  \
      'void %s%s__(){' \
    '\n  String ref      = "";' \
    '\n  String event    = "%s";' \
    '\n  String stmtsStr = getStatementsString(ref, event);' \
    '\n  execute(stmtsStr);' \
    '\n}'

    return format(zip(funNames, refs, evtNames), fmt)

# Media list population calls
def getDefsTabGroupBindsDuplicateMP_(nodes):
    type2Fun = {
            UI_TYPE_AUDIO  : 'populateFileList',
            UI_TYPE_CAMERA : 'populateCameraPictureGallery',
            UI_TYPE_FILE   : 'populateFileList',
            UI_TYPE_VIDEO  : 'populateVideoGallery',
    }
    isMediaType = lambda e: util.schema.guessType(e) in type2Fun
    nodes = util.xml.getAll(nodes, isMediaType)

    funs  = [type2Fun[util.schema.guessType(n)] for n in nodes]
    refs  = [util.schema.getPathString(n)       for n in nodes]

    fmt = '%s("%s", new ArrayList());'
    return format(zip(funs, refs), fmt, indent='  ')

def getDefsTabGroupBindsDuplicateMP(nodes):
    return [getDefsTabGroupBindsDuplicateMP_(n) for n in nodes]

def getDefsTabGroupBindsDuplicateME_(nodes):
    isMediaType = lambda e: util.schema.guessType(e) in MEDIA_UI_TYPES
    nodes       = util.xml.getAll(nodes, isMediaType)
    attribNames = [util.data.getAttribName(n) for n in nodes]

    fmt = 'excludeAttributes.add("%s");'

    return format(zip(attribNames), fmt, indent='      ')

def getDefsTabGroupBindsDuplicateME(nodes):
    return [getDefsTabGroupBindsDuplicateME_(n) for n in nodes]

def getDefsTabGroupBindsDuplicate(tree):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]
    incAutoNums  = [getIncAutoNum(n) for n in nodes]
    mediaPopulate = getDefsTabGroupBindsDuplicateMP(nodes)
    mediaExcludes = getDefsTabGroupBindsDuplicateME(nodes)

    fmt = \
      'void duplicate%s(){' \
    '\n  String tabgroup = "%s";' \
    '\n  String uuidOld = getUuid(tabgroup);' \
    '\n  setUuid(tabgroup, "");' \
    '\n  disableAutoSave(tabgroup);' \
    '\n  %s' \
    '\n  clearGpsInTabGroup(tabgroup);' \
    '\n  populateAuthorAndTimestamp(tabgroup);' \
    '\n  populateEntityListsInTabGroup(tabgroup);' \
    '\n  %s' \
    '\n  onCopy%s__();' \
    '\n' \
    '\n  saveCallback = new SaveCallback() {' \
    '\n    onSave(uuid, newRecord) {' \
    '\n      setUuid(tabgroup, uuid);' \
    '\n' \
    '\n      fetchAll(getDuplicateRelnQuery(uuidOld), new FetchCallback(){' \
    '\n        onFetch(result) {' \
    '\n          Log.e("Module", result.toString());' \
    '\n' \
    '\n          if (result != null &amp;&amp; result.size() &gt;= 1) {' \
    '\n            parentTabgroup__ = result.get(0).get(4);' \
    '\n            parentTabgroup__ = parentTabgroup__.replaceAll(" ", "_");' \
    '\n          }' \
    '\n' \
    '\n          makeDuplicateRelationships(result, getUuid(tabgroup));' \
    '\n' \
    '\n          showToast("{Duplicated_record}");' \
    '\n          dialog.dismiss();' \
    '\n        }' \
    '\n      });' \
    '\n' \
    '\n      saveTabGroup(tabgroup);' \
    '\n    }' \
    '\n  };' \
    '\n' \
    '\n  String extraDupeAttributes = "";' \
    '\n  fetchAll(getDuplicateAttributeQuery(uuidOld, extraDupeAttributes), new FetchCallback(){' \
    '\n    onFetch(result) {' \
    '\n      excludeAttributes = new ArrayList();' \
    '\n' \
    '\n      %s' \
    '\n' \
    '\n      duplicateTabGroup(tabgroup, null, getExtraAttributes(result), excludeAttributes, saveCallback);' \
    '\n    }' \
    '\n  });' \
    '\n}'

    return format(
            zip(refs, refs, incAutoNums, mediaPopulate, refs, mediaExcludes),
            fmt
    )

def getDefsTabGroupBindsDelete(tree):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt = \
      'void delete%s(){' \
    '\n  String tabgroup = "%s";' \
    '\n  if (isNull(getUuid(tabgroup))) {' \
    '\n    cancelTabGroup(tabgroup, true);' \
    '\n  } else {' \
    '\n    showAlert("{Confirm_Deletion}", "{Press_OK_to_Delete_this_Record}", "reallyDelete%s()", "doNotDelete()");' \
    '\n  }' \
    '\n}'

    return format(zip(refs, refs, refs), fmt)

def getDefsTabGroupBindsReallyDelete(tree):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt = \
      'void reallyDelete%s (){' \
    '\n  String tabgroup = "%s";' \
    '\n' \
    '\n  deleteArchEnt(getUuid(tabgroup));' \
    '\n  cancelTabGroup(tabgroup, false);' \
    '\n  populateEntityListsOfArchEnt(tabgroup);' \
    '\n  onDelete%s__();' \
    '\n}' \

    return format(zip(refs, refs, refs), fmt)

def getDefsTabGroupBinds(tree, t):
    placeholder = '{{defs-tabgroup-binds}}'
    replacement = '\n'.join([
        getDefsTabGroupBindsNew         (tree),
        getDefsTabGroupBindsEvents      (tree, 'onCreate', 'create'),
        getDefsTabGroupBindsEvents      (tree, 'onFetch',  'fetch'),
        getDefsTabGroupBindsEvents      (tree, 'onSave',   'save'),
        getDefsTabGroupBindsEvents      (tree, 'onCopy',   'copy'),
        getDefsTabGroupBindsEvents      (tree, 'onDelete', 'delete'),
        getDefsTabGroupBindsDuplicate   (tree),
        getDefsTabGroupBindsDelete      (tree),
        getDefsTabGroupBindsReallyDelete(tree),
    ])

    return t.replace(placeholder, replacement)

def getNavButtonBinds(tree, t):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt  = 'addOnEvent("%s", "show", "removeNavigationButtons()");\n'
    fmt += 'addOnEvent("%s", "show", "addNavigationButtons(\\"%s\\")");'
    placeholder = '{{binds-nav-buttons}}'
    replacement = format(zip(refs, refs, refs), fmt)

    return t.replace(placeholder, replacement)

def getSearchTabGroupString(tree):
    hasSearchType = lambda e: util.schema.getType(e) == TYPE_SEARCH
    nodes = util.xml.getAll(tree, hasSearchType)
    if not len(nodes): return ''
    search = nodes[0]
    searchTG = util.schema.getParentTabGroup(search)
    return util.schema.getPathString(searchTG)

def getSearchBinds(tree, t):
    placeholder = '{{binds-search}}'
    tgStr = getSearchTabGroupString(tree)
    if not tgStr:
        return t.replace(placeholder, '')

    replacement = \
      'addOnEvent("{{tab-group-search}}/Search"               , "show"  , "search();");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Entity_List"   , "click" , "loadEntity();");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Search_Button" , "click" , "search()");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Search_Term"   , "click" , "clearSearch()");' \

    return t.replace(placeholder, replacement)

def getSearchTabGroup(tree, t):
    placeholder = '{{tab-group-search}}'
    replacement = getSearchTabGroupString(tree)

    return t.replace(placeholder, replacement)

def getSearchEntities(tree, t):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    arch16nKeys  = [util.arch16n.getArch16nKey(n) for n in nodes]
    archEntNames = [util.data.getArchEntName  (n) for n in nodes]

    placeholder = '{{search-entities}}'
    fmt         = 'entityTypes.add(new NameValuePair("%s", "%s"));'
    replacement = \
      'addOnEvent("{{tab-group-search}}/Search/Entity_Types"  , "click" , "search()");' \
    '\nentityTypes = new ArrayList();' \
    '\nentityTypes.add(new NameValuePair("{All}", ""));' + \
    '\n' + format(zip(arch16nKeys, archEntNames), fmt) + \
    '\npopulateDropDown("{{tab-group-search}}/Search/Entity_Types", entityTypes);'
    if len(nodes) <= 1:
        replacement = ''

    return t.replace(placeholder, replacement)

def getSearchType(tree, t):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)

    placeholder = '{{type-search}}'
    if len(nodes) <= 1:
        replacement = 'String type = "";'
    else:
        replacement = 'String type = getFieldValue(refEntityTypes);'

    return t.replace(placeholder, replacement)

def getLoadEntityDefs(tree, t):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]

    placeholder = '{{defs-load-entity}}'
    fmt = \
      'void load%sFrom(String uuid) {' \
    '\n  String tabgroup = "%s";' \
    '\n  setUuid(tabgroup, uuid);' \
    '\n  if (isNull(uuid)) return;' \
    '\n' \
    '\n  FetchCallback cb = new FetchCallback() {' \
    '\n    onFetch(result) {' \
    '\n      populateEntityListsInTabGroup(tabgroup);' \
    '\n      onFetch%s__();' \
    '\n    }' \
    '\n  };' \
    '\n' \
    '\n  showTabGroup(tabgroup, uuid, cb);' \
    '\n}'
    replacement = format(zip(refs, refs, refs), fmt)

    return t.replace(placeholder, replacement)

def getTakeFromGpsBinds(tree, t):
    placeholder = '{{binds-take-from-gps}}'
    return t

def getTakeFromGpsMappings(tree, t):
    placeholder = '{{take-from-gps-mappings}}'
    return t

def getControlStartingIdPaths(tree, t):
    placeholder = '{{control-starting-id-paths}}'
    return t

def getAutonumParent(tree, t):
    placeholder = '{{autonum-parent}}'
    return t

def getIncAutonumMap(tree, t):
    placeholder = '{{incautonum-map}}'
    return t

def getEntityMenus(tree, t):
    placeholder = '{{entity-menus}}'
    return t

def getEntityLoading(tree, t):
    placeholder = '{{entity-loading}}'
    return t

def getHandWrittenLogic(tree, t):
    placeholder = '{{hand-written-logic}}'
    return t

def getUiLogic(tree):
    templateFileName = 'generator/module/uilogic-template.bsh'

    # Load template, `t`
    t = None
    with open(templateFileName, 'r') as tFile:
        t = tFile.read()
    if not t:
        raise Exception('"%s" could not be loaded' % templateFileName)

    t = getTabGroups(tree, t)
    t = getDropdownValueGetters(tree, t)
    t = getGpsDiagUpdate(tree, t)
    t = getGpsDiagRef(tree, t)
    t = getUsers(tree, t)
    t = getUsersPopulateCall(tree, t)
    t = getUsersVocabId(tree, t)
    t = getMakeVocab(tree, t)
    t = getValidation(tree, t)
    t = getAuthor(tree, t)
    t = getTimestamp(tree, t)
    t = getOnShowDefs(tree, t)
    t = getOnShowBinds(tree, t)
    t = getOnClickDefs(tree, t)
    t = getOnClickBinds(tree, t)
    t = getMediaBinds(tree, t)
    t = getFileBinds(tree, t)
    t = getTabGroupsToValidate(tree, t)
    t = getDefsTabGroupBinds(tree, t)
    t = getNavButtonBinds(tree, t)
    t = getSearchBinds(tree, t)
    t = getSearchEntities(tree, t)
    t = getSearchType(tree, t)
    t = getSearchTabGroup(tree, t)
    t = getLoadEntityDefs(tree, t)

    # TODO:
    t = getTakeFromGpsBinds(tree, t)
    t = getTakeFromGpsMappings(tree, t)
    t = getControlStartingIdPaths(tree, t)
    t = getAutonumParent(tree, t)
    t = getIncAutonumMap(tree, t)
    t = getEntityMenus(tree, t)
    t = getEntityLoading(tree, t)
    t = getHandWrittenLogic(tree, t)

    return t

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithXmlTypes(tree)
util.schema.canonicalise(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################

print etree.tostring(
        tree,
        pretty_print=True,
        xml_declaration=True,
        encoding='utf-8'
)

print getUiLogic(tree),
