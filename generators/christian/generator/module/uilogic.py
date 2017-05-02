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

def getFunName(node, prefix='', pathLen=3):
    if type(node) == etree._Element:
        path = util.schema.getPath(node)
    elif type(node) == str:
        path = [node]
    else:
        raise TypeError(
                'Argument `node` has type %s. ' \
                'Expected `lxml.etree._Element` or `str`.' % type(node)
        )

    pathSep = ''
    path = path[:pathLen]

    return prefix + pathSep.join(path).replace('_', '')

def getMakeVocabType(node):
    isHierarchical = util.schema.isHierarchical(node)
    uiType         = util.schema.guessType(node)

    # Determine hierarchical-ness
    if isHierarchical: type = 'Hierarchical'
    else:              type = ''

    # Determine the rest of the type
    if uiType == UI_TYPE_CHECKBOX: type += 'CheckBoxGroup'
    if uiType == UI_TYPE_DROPDOWN: type += 'DropDown'
    if uiType == UI_TYPE_LIST:     type += 'List'
    if uiType == UI_TYPE_PICTURE:  type += 'PictureGallery'
    if uiType == UI_TYPE_RADIO:    type += 'RadioGroup'

    return type

def getRefsToTypes(tree, t):
    nodes = util.schema.getGuiDataElements(tree)
    refs  = [util.schema.getPathString(n) for n in nodes]
    types = [util.schema.guessType(n)     for n in nodes]

    fmt         = 'REF_TO_TYPE.put("%s", "%s");'
    placeholder = '{{refs-to-types}}'
    replacement = format(zip(refs, types), fmt)

    return t.replace(placeholder, replacement)

def getDataRefs(tree, t):
    nodes = util.schema.getGuiDataElements(tree, util.data.isDataElement)
    refs  = [util.schema.getPathString(n) for n in nodes]
    types = [util.schema.guessType(n)     for n in nodes]

    fmt         = 'DATA_REFS.add("%s");'
    placeholder = '{{data-refs}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getTabGroups(tree, t):
    nodes = util.schema.getTabGroups(tree)
    refs  = [util.schema.getPathString(tg) for tg in nodes]

    fmt          = 'tabGroups.add("%s");'
    placeholder  = '{{get-tab-groups}}'
    replacement  = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getMenuTypes(tree, t):
    fmt          = 'menuTypes.add("%s");'
    placeholder  = '{{menu-ui-types}}'
    replacement  = format(MENU_UI_TYPES, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getMediaTypes(tree, t):
    fmt          = 'mediaTypes.add("%s");'
    placeholder  = '{{media-ui-types}}'
    replacement  = format(MEDIA_UI_TYPES, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getNodataTabGroups(tree, t):
    isNodata = lambda e : util.schema.isFlagged(e, FLAG_NODATA)

    nodes = util.schema.getTabGroups(tree, keep=isNodata)
    refs  = [util.schema.getPathString(tg) for tg in nodes]

    fmt          = 'flaggedTabGroups.add("%s");'
    placeholder  = '{{is-flagged-nodata}}'
    replacement  = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getPersistBinds(tree, t):
    isPersist = lambda e: util.schema.isFlagged(e, FLAG_PERSIST) or \
                          util.schema.isFlagged(e, FLAG_PERSIST_OW)

    nodes = util.gui.getGuiElements(tree)
    nodes = filter(isPersist, nodes)
    refs  = [util.schema.getPathString(tg                 ) for tg in nodes]
    ow    = [util.schema.isFlagged    (tg, FLAG_PERSIST_OW) for tg in nodes]
    ow    = [str(x).lower()                                 for x  in ow]

    fmt          = 'persistOverSessions("%s", %s);'
    placeholder  = '{{binds-persist}}'
    replacement  = format(zip(refs, ow), fmt)

    return t.replace(placeholder, replacement)

def getInheritanceBinds(tree, t):
    hasI  = lambda e: util.xml.hasAttrib(e, ATTRIB_I)
    nodes = util.xml.getAll(tree, hasI)

    refsSrc  = [util.xml.getAttribVal(n, ATTRIB_I) for n in nodes]
    refsDst  = [util.schema.getPathString(n)       for n in nodes]
    checkPar = []

    # Deal with the case where i="the/1st/path the/2nd/path"
    refsSrc_ = []
    refsDst_ = []
    for refSrc, refDst in zip(refsSrc, refsDst):
        splitSrcRefs = refSrc.split()

        refsSrc_ += splitSrcRefs
        refsDst_ += [refDst] * len(splitSrcRefs)
    refsSrc = refsSrc_
    refsDst = refsDst_

    # Figure out whether to check parents (and normalise refs)
    checkPar = [str('!' not in refSrc).lower() for refSrc in refsSrc]
    refsSrc  = [refSrc.replace('!', '')        for refSrc in refsSrc]

    fmt          = 'inheritFieldValue("%s", "%s", %s);'
    placeholder  = '{{binds-inheritance}}'
    replacement  = format(zip(refsSrc, refsDst, checkPar), fmt)

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

def getValidationString(node, fieldPairs):
    fpFmt = 'f.add(fieldPair("%s", "%s"));'
    fpStr = format(fieldPairs, fpFmt, indent='  ')

    funName = getFunName(node)
    funFmt  = \
      'void validate%s() {' \
    '\n  List f = new ArrayList(); // Fields to be validated' \
    '\n  %s' \
    '\n' \
    '\n  String validationMessage = validateFields(f, "PLAINTEXT");' \
    '\n  showWarning("{validation_results}", validationMessage);' \
    '\n}' \
    '\n'

    return funFmt % (funName, fpStr)

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
        refs   = [util.schema. getPathString(v) for v in V]
        labels = [util.arch16n.getArch16nKey(v) for v in V]
        fieldPairs = zip(refs, labels)

        replacement += getValidationString(n, fieldPairs)

    return t.replace(placeholder, replacement)

def getMakeVocab(tree, t):
    nodes     = util.gui.getAll(tree, MENU_UI_TYPES, isGuiAndData)

    types     = [getMakeVocabType(n)          for n in nodes]
    refs      = [util.schema.getPathString(n) for n in nodes]
    attrNames = [util.data.  getAttribName(n) for n in nodes]

    fmt         = 'makeVocab("%s", "%s", "%s");'
    placeholder = '{{make-vocab}}'
    replacement = format(zip(types, refs, attrNames), fmt)

    return t.replace(placeholder, replacement)

def getMakeVocabVp(tree, t):
    hasVp       = lambda e: util.xml.hasAttrib(e, ATTRIB_VP)
    nodes       = util.xml.getAll(tree, hasVp)
    linkedRefs  = [util.xml.getAttribVal(n, ATTRIB_VP)  for n   in nodes]
    linkedNodes = [util.schema.getNodeAtPath(tree, ref) for ref in linkedRefs]

    types     = [getMakeVocabType(n)          for n in nodes]
    refs      = [util.schema.getPathString(n) for n in nodes]
    attrNames = [util.data.  getAttribName(n) for n in linkedNodes]

    fmt         = 'makeVocab("%s", "%s", "%s");'
    placeholder = '{{make-vocab-vp}}'
    replacement = format(zip(types, refs, attrNames), fmt)

    return t.replace(placeholder, replacement)

def getAuthor(tree, t):
    isAuthor      = lambda e: util.schema.getType(e) == TAG_AUTHOR
    authors       = util.xml.getAll(tree, isAuthor)
    tabGroupNames = [util.schema.getParentTabGroup(a).tag for a in authors]
    refs          = [util.schema.getPathString(a)         for a in authors]

    fmt         = 'tabgroupToAuthor.put("%s", "%s");'
    placeholder = '{{author}}'
    replacement = format(zip(tabGroupNames, refs), fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getTimestamp(tree, t):
    isTimestamp   = lambda e: util.schema.getType(e) == TAG_TIMESTAMP
    timestamp     = util.xml.getAll(tree, isTimestamp)
    tabGroupNames = [util.schema.getParentTabGroup(a).tag for a in timestamp]
    refs          = [util.schema.getPathString(a)         for a in timestamp]

    fmt         = 'tabgroupToTimestamp.put("%s", "%s");'
    placeholder = '{{timestamp}}'
    replacement = format(zip(tabGroupNames, refs), fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getOnShowDefs(tree, t):
    tabGroups    = util.schema.getTabGroups(tree, isGuiAndData)
    funNames     = [getFunName(n)                for n in tabGroups]
    tabGroupRefs = [util.schema.getPathString(n) for n in tabGroups]

    placeholder = '{{defs-on-show}}'
    fmt = \
    'void onShow%s () {\n' \
    '  saveTabGroup("%s");\n' \
    '}\n'
    replacement = format(zip(funNames, tabGroupRefs), fmt)

    return t.replace(placeholder, replacement)

def getOnShowBinds(tree, t):
    tabGroups    = util.schema.getTabGroups(tree, isGuiAndData)
    tabGroupRefs = [util.schema.getPathString(n) for n in tabGroups]
    funNames     = [getFunName(n)                for n in tabGroups]

    placeholder = '{{binds-on-show}}'
    fmt         = 'addOnEvent("%s", "show", "onShow%s()");'
    replacement = format(zip(tabGroupRefs, funNames), fmt)

    return t.replace(placeholder, replacement)

def getXLinksToY(tree, attribVal, noData):
    assert attribVal in (ATTRIB_L, ATTRIB_LC, ATTRIB_LQ)
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
    '\n  triggerAutoSave();' \
    '\n  parentTabgroup   = tabgroup;' \
    '\n  parentTabgroup__ = tabgroup;' \
    '\n  new%s();' \
    '\n}'

    LNDNodes = getXLinksToY(tree, ATTRIB_L,  noData=True)
    LDNodes  = getXLinksToY(tree, ATTRIB_L,  noData=False)
    LCNodes  = getXLinksToY(tree, ATTRIB_LC, noData=False)

    strLND = format(
            zip(
                [getFunName(e)          for e in LNDNodes],
                [util.schema.getLink(e) for e in LNDNodes]
            ),
            fmtLND,
            newline='\n\n'
    )

    strLD = format(
            zip(
                [getFunName(e)                        for e in LDNodes],
                [util.schema.getParentTabGroup(e).tag for e in LDNodes],
                [getFunName(util.schema.getLink(e))   for e in LDNodes]
            ),
            fmtLD,
            newline='\n\n'
    )

    strLC = format(
            zip(
                [getFunName(e)                        for e in LCNodes],
                [util.schema.getParentTabGroup(e).tag for e in LCNodes],
                [getFunName(util.schema.getLink(e))   for e in LCNodes]
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
    refs     = [util.schema.getPathString(n) for n in nodes]
    funNames = [getFunName(n)                for n in nodes]

    placeholder = '{{binds-on-click}}'
    fmt         = 'addOnEvent("%s", "click", "onClick%s()");'
    replacement = format(zip(refs, funNames), fmt)

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

    fmtAudio  = 'addOnEvent("%s", "click", "attachAudioTo(\\"%s\\")");'
    fmtCamera = 'addOnEvent("%s", "click", "attachPictureTo(\\"%s\\")");'
    fmtFile   = 'addOnEvent("%s", "click", "attachFileTo(\\"%s\\")");'
    fmtVideo  = 'addOnEvent("%s", "click", "attachVideoTo(\\"%s\\")");'

    replacementAudio  = format(zip(btnRefsAudio , refsAudio ),  fmtAudio)
    replacementCamera = format(zip(btnRefsCamera, refsCamera), fmtCamera)
    replacementFile   = format(zip(btnRefsFile  , refsFile  ),   fmtFile)
    replacementVideo  = format(zip(btnRefsVideo , refsVideo ),  fmtVideo)

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
    nodes          = util.schema.getTabGroups(tree, isGuiAndData)
    newFunNames    = [getFunName(n) for n in nodes]
    refs           = [util.schema.getPathString(n) for n in nodes]
    noNextIds      = [getNoNextIds (n) for n in nodes]
    incAutoNums    = [getIncAutoNum(n) for n in nodes]
    createFunNames = [getFunName(n) for n in nodes]

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

    return format(
            zip(newFunNames, refs, noNextIds, incAutoNums, createFunNames),
            fmt
    )

def getDefsTabGroupBindsEvents(tree, funPrefix, evtName):
    ''' Get function definitions ("defs") for triggering events bound to tab
        groups.
    '''
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    funNames = [getFunName(n, funPrefix)     for n in nodes]
    refs     = [util.schema.getPathString(n) for n in nodes]
    evtNames = [evtName]*len(nodes)

    fmt =  \
      'void %s__(){' \
    '\n  String ref      = "%s";' \
    '\n  String event    = "%s";' \
    '\n  String stmtsStr = getStatementsString(ref, event);' \
    '\n  execute(stmtsStr);' \
    '\n}'

    return format(zip(funNames, refs, evtNames), fmt)

# TODO: Check that I'm right
def getOnSaveBinds(tree, t):
    tabGroups    = util.schema.getTabGroups(tree, isGuiAndData)
    tabGroupRefs = [util.schema.getPathString(n) for n in tabGroups]

    placeholder = '{{binds-onsave}}'
    fmt         = 'addOnEvent("%s", "save", "populateEntityListsOfArchEnt(\\"%s\\")");'
    replacement = format(zip(tabGroupRefs, tabGroupRefs), fmt)

    return t.replace(placeholder, replacement)

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
    nodes         = util.schema.getTabGroups(tree, isGuiAndData)
    dupFunNames   = [getFunName(n) for n in nodes]
    refs          = [util.schema.getPathString(n) for n in nodes]
    incAutoNums   = [getIncAutoNum(n) for n in nodes]
    mediaPopulate = getDefsTabGroupBindsDuplicateMP(nodes)
    cpyFunNames   = [getFunName(n) for n in nodes]
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
    '\n          if (result != null && result.size() >= 1) {' \
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
            zip(
                dupFunNames,
                refs,
                incAutoNums,
                mediaPopulate,
                cpyFunNames,
                mediaExcludes
            ),
            fmt
    )

def getDefsTabGroupBindsDelete(tree):
    nodes   = util.schema.getTabGroups(tree, isGuiAndData)
    refs    = [util.schema.getPathString(n) for n in nodes]
    funName = [getFunName(n)                   for n in nodes]

    fmt = \
      'void delete%s(){' \
    '\n  String tabgroup = "%s";' \
    '\n  if (isNull(getUuid(tabgroup))) {' \
    '\n    cancelTabGroup(tabgroup, true);' \
    '\n  } else {' \
    '\n    showAlert("{Confirm_Deletion}", "{Press_OK_to_Delete_this_Record}", "reallyDelete%s()", "doNotDelete()");' \
    '\n  }' \
    '\n}'

    return format(zip(funName, refs, funName), fmt)

def getDefsTabGroupBindsReallyDelete(tree):
    nodes   = util.schema.getTabGroups(tree, isGuiAndData)
    refs    = [util.schema.getPathString(n) for n in nodes]
    funName = [getFunName(n)                   for n in nodes]

    fmt = \
      'void reallyDelete%s (){' \
    '\n  String tabgroup = "%s";' \
    '\n' \
    '\n  deleteArchEnt(getUuid(tabgroup));' \
    '\n  cancelTabGroup(tabgroup, false);' \
    '\n  populateEntityListsOfArchEnt(tabgroup);' \
    '\n  onDelete%s__();' \
    '\n}' \

    return format(zip(funName, refs, funName), fmt)

def getDefsTabGroupBinds(tree, t):
    placeholder = '{{defs-tabgroup-binds}}'
    replacement = '\n'.join([
        getDefsTabGroupBindsNew         (tree),
        getDefsTabGroupBindsEvents      (tree, 'onCreate',   'create'),
        getDefsTabGroupBindsEvents      (tree, 'onPrefetch', 'prefetch'),
        getDefsTabGroupBindsEvents      (tree, 'onFetch',    'fetch'),
        getDefsTabGroupBindsEvents      (tree, 'onSave',     'save'),
        getDefsTabGroupBindsEvents      (tree, 'onCopy',     'copy'),
        getDefsTabGroupBindsEvents      (tree, 'onDelete',   'delete'),
        getDefsTabGroupBindsDuplicate   (tree),
        getDefsTabGroupBindsDelete      (tree),
        getDefsTabGroupBindsReallyDelete(tree),
    ])

    return t.replace(placeholder, replacement)

def getNavButtonBindsDel(tree, t):
    nodes = util.schema.getTabGroups(tree, util.gui.isGuiNode)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt = 'addOnEvent("%s", "show", "removeNavigationButtons()");'
    placeholder = '{{binds-nav-buttons-del}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getNavButtonBindsAdd(tree, t):
    nodes = util.schema.getTabGroups(tree, isGuiAndData)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt = 'addOnEvent("%s", "show", "addNavigationButtons(\\"%s\\")");'
    placeholder = '{{binds-nav-buttons-add}}'
    replacement = format(zip(refs, refs), fmt)

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
      'addOnEvent("{{tab-group-search}}/Search"               , "show"  , "search()");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Entity_List"   , "click" , "loadEntity();");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Search_Button" , "click" , "search()");' \
    '\naddOnEvent("{{tab-group-search}}/Search/Search_Term"   , "click" , "clearSearch()");' \

    return t.replace(placeholder, replacement)

def getSearchTabGroup(tree, t):
    placeholder = '{{tab-group-search}}'
    replacement = getSearchTabGroupString(tree)

    return t.replace(placeholder, replacement)

def getSearchEntities(tree, t):
    hasSearchType = lambda e: util.schema.getType(e) == TYPE_SEARCH
    searchNodes = util.xml.getAll(tree, hasSearchType)

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
    if len(nodes) <= 1 or len(searchNodes) < 1:
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
    nodes    = util.schema.getTabGroups(tree, isGuiAndData)
    refs     = [util.schema.getPathString(n) for n in nodes]
    funNames = [getFunName(n) for n in nodes]

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
    '\n  onPrefetch%s__();' \
    '\n  showTabGroup(tabgroup, uuid, cb);' \
    '\n}'
    replacement = format(zip(funNames, refs, funNames, funNames), fmt)

    return t.replace(placeholder, replacement)

def getTakeFromGpsBinds(tree, t):
    isGps  = lambda e: util.schema.getType(e) == TYPE_GPS
    nodes  = util.xml.getAll(tree, isGps)
    btns   = [n.getnext().getnext() for n in nodes] # Take from GPS buttons
    parTgs = [util.schema.getParentTabGroup(n) for n in nodes]

    btnRefs   = [util.schema.getPathString(n) for n in btns]
    parTgRefs = [util.schema.getPathString(n) for n in parTgs]

    fmt         = 'addOnEvent("%s", "click", "takePoint(\\"%s\\")");'
    placeholder = '{{binds-take-from-gps}}'
    replacement = format(zip(btnRefs, parTgRefs), fmt)

    return t.replace(placeholder, replacement)

def getTakeFromGpsMappings(tree, t):
    isGps  = lambda e: util.schema.getType(e) == TYPE_GPS
    nodes  = util.xml.getAll(tree, isGps)

    tabs      = [util.schema.getParentTab     (n) for n in nodes]
    tabGroups = [util.schema.getParentTabGroup(n) for n in nodes]

    tabRefs      = [util.schema.getPathString(n) for n in tabs]
    tabGroupRefs = [util.schema.getPathString(n) for n in tabGroups]

    fmt         = 'tabgroupToTabRef.put("%s", "%s");'
    placeholder = '{{take-from-gps-mappings}}'
    replacement = format(zip(tabGroupRefs, tabRefs), fmt)

    return t.replace(placeholder, replacement)

def getControlStartingIdPaths(tree, t):
    wasAutoNum = lambda e: util.xml.getAttribVal(e, ORIGINAL_TAG) == TAG_AUTONUM
    nodes      = util.xml.getAll(tree, wasAutoNum)
    refs       = [util.schema.getPathString(n) for n in nodes]

    fmt         = 'l.add("%s");'
    placeholder = '{{control-starting-id-paths}}'
    replacement = format(refs, fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getQrBinds(tree, t):
    nodes      = getXLinksToY(tree, ATTRIB_LQ, noData=False)
    buttonRefs = [util.schema.getPathString(n) for n in nodes]
    fieldRefs  = [util.schema.getLink(n)       for n in nodes]

    fmt         = 'bindQrScanning("%s", "%s");'
    placeholder = '{{binds-qr}}'
    replacement = format(zip(buttonRefs, fieldRefs), fmt);

    return t.replace(placeholder, replacement)

def getAutonumBinds(tree, t):
    wasAutoNum = lambda e: util.xml.getAttribVal(e, ORIGINAL_TAG) == TAG_AUTONUM
    nodes      = util.xml.getAll(tree, wasAutoNum)
    parTabs    = [util.schema.getParentTabGroup(n) for n in nodes]
    refs       = [util.schema.getPathString    (n) for n in parTabs]
    refs       = list(set(refs))

    fmt         = 'addOnEvent("%s", "show", "loadStartingIds()");'
    placeholder = '{{binds-autonum}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getIncAutonumMap(tree, t):
    wasAutoNum = lambda e: util.xml.getAttribVal(e, ORIGINAL_TAG) == TAG_AUTONUM
    nodes      = util.xml.getAll(tree, wasAutoNum)
    srcRefs    = [util.schema.getPathString(n)           for n in nodes]
    dstRefs    = [util.xml.getAttribVal(n, AUTONUM_DEST) for n in nodes]

    fmt         = 'destToSource.put("%s", "%s");'
    placeholder = '{{incautonum-map}}'
    replacement = format(zip(dstRefs, srcRefs), fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getEntityMenus(tree, t):
    isEntList    = lambda e: util.xml.hasAttrib(e, ATTRIB_E ) or \
                             util.xml.hasAttrib(e, ATTRIB_EC)
    type2TypeArg = { UI_TYPE_DROPDOWN : "DropDown", UI_TYPE_LIST : "List" }

    nodes    = util.xml.getAll(tree, isEntList)
    types    = [util.schema.guessType(n) for n in nodes]
    parTgs   = [util.schema.getParentTabGroup(n) for n in nodes]

    typeArgs     = [type2TypeArg                  [t_] for t_ in types]
    refs         = [util.schema.getPathString     (n)  for n  in nodes]
    parTgRefs    = [util.schema.getPathString     (n)  for n  in parTgs]
    archEntNames = [util.schema.getEntity         (n)  for n  in nodes]
    relNames     = [util.data.getRelNameEntityList(n)  for n  in nodes]

    fmt = \
        'ENTITY_MENUS.add(new String[] {' \
      '\n    "%s",' \
      '\n    "%s",' \
      '\n    "getUuid(\\"%s\\")",' \
      '\n    "%s",' \
      '\n    "%s"' \
      '\n});'
    placeholder = '{{entity-menus}}'
    replacement = format(
            zip(typeArgs, refs, parTgRefs, archEntNames, relNames),
            fmt
    )

    return t.replace(placeholder, replacement)

def getEntityLoading(tree, t):
    dropdown = lambda e: 'true' if util.schema.guessType(e) == UI_TYPE_DROPDOWN \
                    else ''

    nodes = util.xml.getAll(tree, util.schema.hasEntity)
    refs  = [util.schema.getPathString(n) for n in nodes]
    dropdowns = [dropdown(n)              for n in nodes]

    fmt         = 'addOnEvent("%s", "click", "loadEntity(%s)");'
    placeholder = '{{entity-loading}}'
    replacement = format(zip(refs, dropdowns), fmt)

    return t.replace(placeholder, replacement)

def getHandWrittenLogic(tree, t):
    placeholder = '{{hand-written-logic}}'
    replacement = util.schema.getLogic(tree)

    return t.replace(placeholder, replacement)

def getUiLogic(tree):
    templateFileName = 'generator/module/uilogic-template.bsh'

    # Load template, `t`
    t = None
    with open(templateFileName, 'r') as tFile:
        t = tFile.read()
    if not t:
        raise Exception('"%s" could not be loaded' % templateFileName)

    t = getTabGroups(tree, t)
    t = getMenuTypes(tree, t)
    t = getMediaTypes(tree, t)
    t = getRefsToTypes(tree, t)
    t = getDataRefs(tree, t)
    t = getNodataTabGroups(tree, t)
    t = getPersistBinds(tree, t)
    t = getInheritanceBinds(tree, t)
    t = getDropdownValueGetters(tree, t)
    t = getGpsDiagUpdate(tree, t)
    t = getGpsDiagRef(tree, t)
    t = getUsers(tree, t)
    t = getUsersPopulateCall(tree, t)
    t = getUsersVocabId(tree, t)
    t = getMakeVocab(tree, t)
    t = getMakeVocabVp(tree, t)
    t = getValidation(tree, t)
    t = getAuthor(tree, t)
    t = getTimestamp(tree, t)
    t = getOnShowDefs(tree, t)
    t = getOnShowBinds(tree, t)
    t = getOnSaveBinds(tree, t)
    t = getOnClickDefs(tree, t)
    t = getOnClickBinds(tree, t)
    t = getMediaBinds(tree, t)
    t = getFileBinds(tree, t)
    t = getTabGroupsToValidate(tree, t)
    t = getDefsTabGroupBinds(tree, t)
    t = getNavButtonBindsDel(tree, t)
    t = getNavButtonBindsAdd(tree, t)
    t = getSearchBinds(tree, t)
    t = getSearchEntities(tree, t)
    t = getSearchType(tree, t)
    t = getSearchTabGroup(tree, t)
    t = getLoadEntityDefs(tree, t)
    t = getTakeFromGpsBinds(tree, t)
    t = getTakeFromGpsMappings(tree, t)
    t = getControlStartingIdPaths(tree, t)
    t = getQrBinds(tree, t)
    t = getAutonumBinds(tree, t)
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

# Useful for debugging
#print etree.tostring(
        #tree,
        #pretty_print=True,
        #xml_declaration=True,
        #encoding='utf-8'
#)

print getUiLogic(tree),
