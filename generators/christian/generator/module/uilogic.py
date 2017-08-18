#!/usr/bin/env python2
from   lxml import etree
import sys
import util.schema
import util.gui
import util.arch16n
import util.xml
import util.data
from   util.consts import *
import subprocess

def format(tuples, fmt='%s', indent='', newline='\n'):
    sep = newline + indent
    return sep.join(fmt % tuple for tuple in tuples)

def getUserMenuUiType(tree):
    isFlagged = lambda e: util.schema.isFlagged(e, FLAG_USER)
    nodes = util.xml.getAll(tree, isFlagged)
    if len(nodes) != 1: return None
    node = nodes[0]
    return util.schema.getUiType(node)

def isGuiAndData(e):
    return util.gui. isGuiNode    (e) and \
           util.data.isDataElement(e)

def getFunName(node):
    pathSep = ''

    if type(node) == str: path = node.split('/')
    else:                 path = util.schema.getPath(node)

    if len(path) == 3:
        path = path[0], path[-1]

    return pathSep.join(path).replace('_', '')

def getHeader(tree, t):
    header  = '/*\n'
    header += ' * GENERATED WITH FAIMS-TOOLS, SHA1: '
    header += subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    header += ' */\n'

    return header + t

def getRefsToTypes(tree, t):
    hasRef = lambda n : bool(util.schema.getPathString(n))

    nodes = util.schema.getGuiDataElements(tree, keep=hasRef) + \
            util.schema.getTabs(tree, keep=hasRef)
    refs  = [util.schema.getPathString(n) for n in nodes]
    types = [util.schema.getUiType(n)     for n in nodes]

    fmt         = 'REF_TO_TYPE.put("%s", "%s");'
    placeholder = '{{refs-to-types}}'
    replacement = format(zip(refs, types), fmt)

    return t.replace(placeholder, replacement)

def getDataRefs(tree, t):
    nodes = util.schema.getGuiDataElements(tree, util.data.isDataElement)
    refs  = [util.schema.getPathString(n) for n in nodes]
    types = [util.schema.getUiType(n)     for n in nodes]

    fmt         = 'DATA_REFS.add("%s");'
    placeholder = '{{data-refs}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getNoUiRefs(tree, t):
    isNoUi = lambda e: util.schema.isFlagged(e, FLAG_NOUI)

    nodes = util.schema.getGuiDataElements(tree, isNoUi)
    refs  = [util.schema.getPathString(n) for n in nodes]
    types = [util.schema.getUiType(n)     for n in nodes]

    fmt         = 'NO_UI_REFS.add("%s");'
    placeholder = '{{no-ui-refs}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getVpRefs(tree, t):
    hasVp       = lambda e: util.xml.hasAttrib(e, ATTRIB_VP)
    nodes       = util.xml.getAll(tree, hasVp)
    refs        = [util.schema.getPathString(n) for n in nodes]
    linkedRefs  = [util.xml.getAttribVal(n, ATTRIB_VP)  for n   in nodes]
    linkedNodes = [util.schema.getNodeAtPath(tree, ref) for ref in linkedRefs]

    fmt         = 'VP_REF_TO_REF.put("%s", "%s");'
    placeholder = '{{vp-ref-to-ref}}'
    replacement = format(zip(refs, linkedRefs), fmt)

    return t.replace(placeholder, replacement)

def getHierRefs(tree, t):
    nodes = util.schema.getGuiDataElements(tree, util.schema.isHierarchical)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt         = 'HIER_REFS.add("%s");'
    placeholder = '{{hier-refs}}'
    replacement = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getTabGroups(tree, t):
    nodes = util.schema.getTabGroups(tree)
    refs  = [util.schema.getPathString(tg) for tg in nodes]

    fmt          = 'TAB_GROUPS_AS_LIST.add("%s");'
    placeholder  = '{{get-tab-groups}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getTabs(tree, t):
    nodes = util.schema.getTabs(tree)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt          = 'TABS_AS_LIST.add("%s");'
    placeholder  = '{{get-tabs}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getAttribNamesNonStandard(tree, t):
    hasNonStdAttr = lambda n: util.xml.hasAttrib(n, RESERVED_PROP_NAME)

    nodes     = util.xml.getAll(tree, hasNonStdAttr)
    refs      = [util.schema.getPathString(n) for n in nodes]
    attrNames = [util.data.getAttribName(n) for n in nodes]

    fmt         = 'ATTRIB_NAMES_NON_STANDARD.put("%s", "%s");'
    placeholder = '{{attrib-names-non-standard}}'
    replacement = format(zip(refs, attrNames), fmt)

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

def perfHierToComment(hier):
    return str(hier).replace('\n', '\n  //') \
            [3:] # Removes first two spaces and newline character

def perfHierToCode(hier):
    code  = getPerfCodeAssigns(hier)
    code += '\n'
    code += getPerfCodeCalls(hier)
    return code

def getPerfCodeAssigns(hier):
    assigns = ''
    for f in hier.flattened():
        assigns += '  n%s = Tree("%s", 1);\n' % (f.i, f.data)
    return assigns

def getPerfCodeCalls(hier):
    calls = ''

    for child in hier.children:
        calls += '  n%s.addChild(n%s);\n' % (hier.i, child.i)

    if len(hier.children):
        calls += '\n'

    for child in hier.children:
        calls += getPerfCodeCalls(child)

    return calls

def getPerfHierarchy(tree, t):
    hier = util.data.getHierarchy(tree)
    hier.applyNumbering()

    humanReadable   = perfHierToComment(hier)
    machineReadable = perfHierToCode   (hier)

    placeholder = '{{perf-type-hierarchy}}'
    replacement = humanReadable + '\n\n' + machineReadable

    return t.replace(placeholder, replacement)

def getIsInPerfTestTime(tree, t):
    isInTestTime = str(util.schema.isInTestTime(tree))

    placeholder = '{{is-in-perf-test-time}}'
    replacement = isInTestTime.lower()

    return t.replace(placeholder, replacement)

def getPerfTimedCalls(tree, t):
    anchorText  = '{{perf-anchor-end}}'
    anchorIndex = t.find(anchorText)

    if anchorText > -1 and util.schema.isInTestTime(tree):
        before = t[:anchorIndex]
        after  = t[anchorIndex:]

        after = after.replace('fetchAll',           'timedFetchAll')
        after = after.replace('fetchOne',           'timedFetchOne')
        after = after.replace('populateCursorList', 'timedPopulateCursorList')

        t = before + after

    return t.replace(anchorText, '')

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

def getNodataMenus(tree, t):
    isOpt    = lambda n: util.schema.getXmlType(n) == TAG_OPT
    isNodata = lambda n: util.schema.isFlagged(n, FLAG_NODATA)

    isNoDataOpt = lambda n: isOpt(n) and isNodata(n)

    noDataOptNodes = util.xml.getAll(tree, isNoDataOpt)
    parentNodes    = [util.schema.getParentGuiDataElement(n) for n in noDataOptNodes]

    refs = [util.schema.getPathString(n) for n in parentNodes]
    keys = [util.arch16n.getArch16nKey(n) for n in noDataOptNodes]
    vals = keys

    placeholder = '{{nodata-menus}}'
    fmt         = 'addNodataDropdownEntry("%s", "%s", "%s");'
    replacement = format(zip(refs, keys, vals), fmt)

    return t.replace(placeholder, replacement)

def getGpsDiagUpdate(tree, t):
    nodes = util.gui.getAll(tree, UI_TYPE_GPSDIAG)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt          = 'addOnEvent("%s", "show", "updateGPSDiagnostics()");'
    placeholder  = '{{gps-diag-update}}'
    replacement  = format(refs, fmt)

    return t.replace(placeholder, replacement)

def getMap(tree, t):
    mapNodes = util.gui.getAll(tree, UI_TYPE_MAP)
    btnNodes = [n.getnext() for n in mapNodes]
    mapRefs = [util.schema.getPathString(n) for n in mapNodes]
    btnRefs = [util.schema.getPathString(n) for n in btnNodes]

    fmt          = \
      'final String MAP_REF = "%s";' \
    '\nvoid centerMe() { centerOnCurrentPosition(MAP_REF); }' \
    '\naddOnEvent("%s", "click", "centerMe()");'
    placeholder  = '{{map}}'
    replacement  = format(zip(mapRefs, btnRefs), fmt)

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

def getUsersSelectedUser(tree, t):
    placeholder = '{{users-selecteduser}}'

    if   getUserMenuUiType(tree) == UI_TYPE_LIST:
        replacement = 'String selectedUser = getListItemValue();'
    elif getUserMenuUiType(tree) == UI_TYPE_DROPDOWN:
        replacement = 'String selectedUser = getFieldValue(USER_MENU_PATH);'
    else:
        replacement = 'return;'

    return t.replace(placeholder, replacement)

def getBindsOnClickSignup(tree, t):
    isSignupLink = lambda e: util.xml.getAttribVal(e, ATTRIB_L) == LINK_SIGNUP
    nodes = util.schema.getGuiDataElements(tree, isSignupLink)
    refs  = [util.schema.getPathString(n) for n in nodes]

    fmt         = 'addOnEvent("%s", "click", "onClickSignup__()");'
    placeholder = '{{binds-on-click-signup}}'
    replacement = format(refs, fmt)

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

def getAuthor(tree, t):
    isAuthor      = lambda e: util.schema.getXmlType(e) == TAG_AUTHOR
    authors       = util.xml.getAll(tree, isAuthor)
    tabGroupNames = [util.schema.getParentTabGroup(a).tag for a in authors]
    refs          = [util.schema.getPathString(a)         for a in authors]

    fmt         = 'tabgroupToAuthor.put("%s", "%s");'
    placeholder = '{{author}}'
    replacement = format(zip(tabGroupNames, refs), fmt, indent='  ')

    return t.replace(placeholder, replacement)

def getTimestamp(tree, t):
    isTimestamp   = lambda e: util.schema.getXmlType(e) == TAG_TIMESTAMP
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

def getXLinksToY(tree, attribName, isData):
    assert attribName in LINK_ATTRIBS

    hasAttrib = lambda e: util.xml.hasAttrib(e, attribName)
    notSignup = lambda e: util.xml.getAttribVal(e, attribName) != LINK_SIGNUP
    isLink    = lambda e: hasAttrib(e) and notSignup(e)
    isDataEl  = lambda e: util.data.isDataElement(util.schema.getLinkedNode(e))

    nodes = util.xml.getAll(tree)
    nodes = filter(isLink, nodes)
    if isData == True:     nodes = filter(lambda e :     isDataEl(e), nodes)
    if isData == False:    nodes = filter(lambda e : not isDataEl(e), nodes)

    return nodes

def getOnClickDefs(tree, t):
    placeholder = '{{defs-on-click}}'

    # @l or @ll link to 'nodata' tab or tab group
    fmtLND = \
      'void %s%s () {' \
    '\n  newTab("%s", true);' \
    '\n}'

    # @l or @ll link to savable tab group
    fmtLD = \
      'void %s%s () {' \
    '\n  parentTabgroup__ = "%s";' \
    '\n  new%s();' \
    '\n}'

    fmtLL = \
      'void onClick%s () {' \
    '\n  showVerifyUserDialog("onValidClick%s()");' \
    '\n}'

    # @lc link
    fmtLC = \
      'void onClick%s () {' \
    '\n  new%s("%s");' \
    '\n}'

    LNDNodes  = getXLinksToY(tree, ATTRIB_L,  isData=False)
    LDNodes   = getXLinksToY(tree, ATTRIB_L,  isData=True)
    LLNDNodes = getXLinksToY(tree, ATTRIB_LL, isData=False)
    LLDNodes  = getXLinksToY(tree, ATTRIB_LL, isData=True)
    LLNodes   = LLNDNodes + LLDNodes
    LCNodes   = getXLinksToY(tree, ATTRIB_LC, isData=True)

    strLND = format(
            zip(
                ['onClick'              for e in LNDNodes],
                [getFunName(e)          for e in LNDNodes],
                [util.schema.getLink(e) for e in LNDNodes]
            ),
            fmtLND,
            newline='\n\n'
    )

    strLD = format(
            zip(
                ['onClick'                            for e in LDNodes],
                [getFunName(e)                        for e in LDNodes],
                [util.schema.getParentTabGroup(e).tag for e in LDNodes],
                [getFunName(util.schema.getLink(e))   for e in LDNodes]
            ),
            fmtLD,
            newline='\n\n'
    )

    strLLND = format(
            zip(
                ['onValidClick'         for e in LLNDNodes],
                [getFunName(e)          for e in LLNDNodes],
                [util.schema.getLink(e) for e in LLNDNodes]
            ),
            fmtLND,
            newline='\n\n'
    )

    strLLD = format(
            zip(
                ['onValidClick'                       for e in LLDNodes],
                [getFunName(e)                        for e in LLDNodes],
                [util.schema.getParentTabGroup(e).tag for e in LLDNodes],
                [getFunName(util.schema.getLink(e))   for e in LLDNodes]
            ),
            fmtLD,
            newline='\n\n'
    )

    strLL = format(
            zip(
                [getFunName(e) for e in LLNodes],
                [getFunName(e) for e in LLNodes]
            ),
            fmtLL,
            newline='\n\n'
    )

    strLC = format(
            zip(
                [getFunName(e)                        for e in LCNodes],
                [getFunName(util.schema.getLink(e))   for e in LCNodes],
                [util.schema.getParentTabGroup(e).tag for e in LCNodes]
            ),
            fmtLC,
            newline='\n\n'
    )

    replacement = '\n\n'.join([strLND, strLD, strLLND, strLLD, strLL, strLC])

    return t.replace(placeholder, replacement)

def getOnClickBinds(tree, t):
    LNodes  = getXLinksToY(tree, ATTRIB_L,  isData=None)
    LLNodes = getXLinksToY(tree, ATTRIB_LL, isData=None)
    LCNodes = getXLinksToY(tree, ATTRIB_LC, isData=True)

    nodes = LNodes + LLNodes + LCNodes
    refs     = [util.schema.getPathString(n) for n in nodes]
    funNames = [getFunName(n)                for n in nodes]

    placeholder = '{{binds-on-click}}'
    fmt         = 'addOnEvent("%s", "click", "onClick%s()");'
    replacement = format(zip(refs, funNames), fmt)

    return t.replace(placeholder, replacement)

def getMediaBinds(tree, t):
    type2fun = {
        UI_TYPE_AUDIO  : 'attachAudioTo',
        UI_TYPE_CAMERA : 'attachPictureTo',
        UI_TYPE_FILE   : 'attachFileTo',
        UI_TYPE_VIDEO  : 'attachVideoTo'
    }

    nodes = []
    for type in MEDIA_UI_TYPES:
        nodes += util.gui.getAll(tree, type)

    refs    = [util.schema.getPathString(n) for n in nodes]
    btnRefs = [util.schema.getPathString(n.getnext()) for n in nodes]
    types   = [util.schema.getUiType(n) for n in nodes]
    funs    = [type2fun[type] for type in types]
    fmt     = 'addOnEvent("%s", "click", "%s(\\"%s\\")");'

    placeholder = '{{binds-media}}'
    replacement = format(zip(btnRefs, funs, refs), fmt)

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

    fmt = \
    '\nvoid new%s(String parent){' \
    '\n  String tabgroup = "%s";' \
    '\n  if (!isNull(parent)) {' \
    '\n    triggerAutoSave();' \
    '\n    parentTabgroup   = parent;' \
    '\n    parentTabgroup__ = parent;' \
    '\n  }' \
    '\n  %s' \
    '\n' \
    '\n  setUuid(tabgroup, null);' \
    '\n  newTabGroup(tabgroup);' \
    '\n  populateAuthorAndTimestamp(tabgroup);' \
    '\n  populateEntityListsInTabGroup(tabgroup);' \
    '\n  %s' \
    '\n' \
    '\n  executeOnEvent(tabgroup, "create");' \
    '\n}' \
    '\n' \
    '\nvoid new%s (){' \
    '\n  new%s(null);' \
    '\n}'

    return format(
            zip(
                newFunNames,
                refs,
                noNextIds,
                incAutoNums,
                newFunNames,
                newFunNames
            ),
            fmt
    )

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
    isMediaType = lambda e: util.schema.getUiType(e) in type2Fun
    nodes = util.xml.getAll(nodes, isMediaType)

    funs  = [type2Fun[util.schema.getUiType(n)] for n in nodes]
    refs  = [util.schema.getPathString(n)       for n in nodes]

    fmt = '%s("%s", new ArrayList());'
    return format(zip(funs, refs), fmt, indent='  ')

def getDefsTabGroupBindsDuplicateMP(nodes):
    return [getDefsTabGroupBindsDuplicateMP_(n) for n in nodes]

def getDefsTabGroupBindsDuplicateME_(nodes):
    isMediaType = lambda e: util.schema.getUiType(e) in MEDIA_UI_TYPES
    nodes       = util.xml.getAll(nodes, isMediaType)
    attribNames   = [util.data.getAttribName(n) for n in nodes]

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
    '\n  executeOnEvent(tabgroup, "copy");' \
    '\n' \
    '\n  saveCallback = new SaveCallback() {' \
    '\n    onSave(uuid, newRecord) {' \
    '\n      setUuid(tabgroup, uuid);' \
    '\n' \
    '\n      timedFetchAll(getDuplicateRelnQuery(uuidOld), new FetchCallback(){' \
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
    '\n  timedFetchAll(getDuplicateAttributeQuery(uuidOld, extraDupeAttributes), new FetchCallback(){' \
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
                mediaExcludes
            ),
            fmt
    )

def getDefsTabGroupBinds(tree, t):
    placeholder = '{{defs-tabgroup-binds}}'
    replacement = '\n'.join([
        getDefsTabGroupBindsNew         (tree),
        getDefsTabGroupBindsDuplicate   (tree),
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
    hasSearchType = lambda e: util.schema.getXmlType(e) == TYPE_SEARCH
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
    hasSearchType = lambda e: util.schema.getXmlType(e) == TYPE_SEARCH
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
    '\n      executeOnEvent(tabgroup, "fetch");' \
    '\n    }' \
    '\n  };' \
    '\n' \
    '\n  executeOnEvent(tabgroup, "prefetch");' \
    '\n  showTabGroup(tabgroup, uuid, cb);' \
    '\n}'
    replacement = format(zip(funNames, refs), fmt)

    return t.replace(placeholder, replacement)

def getTakeFromGpsBinds(tree, t):
    isGps  = lambda e: util.schema.getXmlType(e) == TYPE_GPS
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
    isGps  = lambda e: util.schema.getXmlType(e) == TYPE_GPS
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
    nodes      = getXLinksToY(tree, ATTRIB_LQ,  isData=None)
    nodes     += getXLinksToY(tree, ATTRIB_LCQ, isData=None)

    buttonRefs = [util.schema.getPathString(n)      for n in nodes]
    fieldRefs  = [util.schema.getLink(n)            for n in nodes]
    isChild    = [util.xml.hasAttrib(n, ATTRIB_LCQ) for n in nodes]
    isChild    = [str(c).lower()                    for c in isChild]

    fmt         = 'bindQrScanning("%s", "%s", %s);'
    placeholder = '{{binds-qr}}'
    replacement = format(zip(buttonRefs, fieldRefs, isChild), fmt);

    return t.replace(placeholder, replacement)

def getIncAutonumMap(tree, t):
    wasAutoNum = lambda e: util.xml.getAttribVal(e, ORIGINAL_TAG) == TAG_AUTONUM
    nodes      = util.xml.getAll(tree, wasAutoNum)
    srcRefs    = [util.schema.getPathString(n)           for n in nodes]
    dstRefs    = [util.xml.getAttribVal(n, AUTONUM_DEST) for n in nodes]

    fmt         = 'AUTONUM_DEST_TO_SOURCE.put("%s", "%s");'
    placeholder = '{{incautonum-map}}'
    replacement = format(zip(dstRefs, srcRefs), fmt)

    return t.replace(placeholder, replacement)

def markdownToHtml(markdown):
    markdown = markdown or ''
    markdown = markdown.strip()

    try:
        p = subprocess.Popen(
                ['pandoc', '-S', '--normalize'],
                stdout=subprocess.PIPE,
                stdin =subprocess.PIPE,
                stderr=subprocess.STDOUT
        )
        stdout, stderr = p.communicate(input=markdown.encode('utf-8'))
        return stdout.decode('utf-8')
    except:
        sys.stderr.write(
                '    Executable `pandoc` could not be found. '
                'Please install pandoc and try again.'
                '\n'
        )
        exit()

def getPopulationMarkdown(tree, t):
    nodes = util.xml.getAll(tree, lambda n: n.tag == TAG_MARKDOWN)
    refs  = [util.schema.getParentGuiDataElement(n) for n in nodes]
    refs  = [util.schema.getPathString(r)           for r in refs]
    html  = [markdownToHtml(n.text)                 for n in nodes]
    html  = [util.escape(h)                         for h in html]

    fmt         = 'populateWebViewHtml("%s", "%s");'
    placeholder = '{{population-markdown}}'
    replacement = format(zip(refs, html), fmt)

    return t.replace(placeholder, replacement)

def getEntityMenus(tree, t):
    isEntList    = lambda e: util.xml.hasAttrib(e, ATTRIB_E ) or \
                             util.xml.hasAttrib(e, ATTRIB_EC)

    nodes    = util.xml.getAll(tree, isEntList)
    parTgs   = [util.schema.getParentTabGroup(n) for n in nodes]

    refs         = [util.schema.getPathString     (n)  for n  in nodes]
    parTgRefs    = [util.schema.getPathString     (n)  for n  in parTgs]
    archEntNames = [util.schema.getEntity         (n)  for n  in nodes]
    relNames     = [util.data.getRelNameEntityList(n)  for n  in nodes]

    fmt = \
        'ENTITY_MENUS.add(new String[] {' \
      '\n    "%s",' \
      '\n    "getUuid(\\"%s\\")",' \
      '\n    "%s",' \
      '\n    "%s"' \
      '\n});'
    placeholder = '{{entity-menus}}'
    replacement = format(
            zip(refs, parTgRefs, archEntNames, relNames),
            fmt
    )

    return t.replace(placeholder, replacement)

def getEntityLoading(tree, t):
    dropdown = lambda e: 'true' if util.schema.getUiType(e) == \
                                    UI_TYPE_DROPDOWN \
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

    t = t.decode('utf-8')
    t = getHeader(tree, t)
    t = getTabGroups(tree, t)
    t = getTabs(tree, t)
    t = getAttribNamesNonStandard(tree, t)
    t = getMenuTypes(tree, t)
    t = getMediaTypes(tree, t)
    t = getRefsToTypes(tree, t)
    t = getDataRefs(tree, t)
    t = getNoUiRefs(tree, t)
    t = getVpRefs(tree, t)
    t = getHierRefs(tree, t)
    t = getNodataTabGroups(tree, t)
    t = getPerfHierarchy(tree, t)
    t = getIsInPerfTestTime(tree, t)
    t = getPersistBinds(tree, t)
    t = getInheritanceBinds(tree, t)
    t = getNodataMenus(tree, t)
    t = getGpsDiagUpdate(tree, t)
    t = getMap(tree, t)
    t = getGpsDiagRef(tree, t)
    t = getUsers(tree, t)
    t = getUsersSelectedUser(tree, t)
    t = getBindsOnClickSignup(tree, t)
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
    t = getIncAutonumMap(tree, t)
    t = getPopulationMarkdown(tree, t)
    t = getEntityMenus(tree, t)
    t = getEntityLoading(tree, t)
    t = getHandWrittenLogic(tree, t)
    t = getPerfTimedCalls(tree, t)

    return t

if __name__ == '__main__':
    # PARSE XML
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    # GENERATE AND OUTPUT UI LOGIC
    print getUiLogic(tree).encode('utf-8'),
