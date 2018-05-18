#!/usr/bin/env python2
import sys
import util.schema
import util.gui
import util.xml
import signal

signal.signal(signal.SIGINT, lambda a, b : sys.exit())

def filterNonAlpha(string):
    return filter(str.isalnum, string)

def functionName(node):
    pathSegments = util.schema.getPath(node)
    pathSegments = [filterNonAlpha(s) for s in pathSegments]

    #nodeHash     = util.schema.nodeHash(node, hashLen=3)

    funName      = 'get_' + '_'.join(pathSegments) # + '_' + nodeHash

    return funName

def parseJavaType(javaType):
    splitted = javaType.split('.')

    javaTypeShort = splitted[-1]
    javaTypeLong  = '.'.join(splitted)

    return javaTypeLong, javaTypeShort

def getFunctionString(ref, type, funName, javaType=None):
    if not javaType: javaType = 'android.view.View'

    javaTypeLong, javaTypeShort = parseJavaType(javaType)

    s  = '    /*\n'
    s += '        Type: {type}\n'
    s += '        Ref:  {ref}\n'
    s += '     */\n'
    s += '    public static {javaTypeShort} {funName}(Solo solo) {{\n'
    s += '        String ref = "{ref}";\n'
    s += '        return ({javaTypeLong}) solo.getView((Object) ref);\n'
    s += '    }}\n'
    s  = s.format(
            ref           = ref,
            type          = type,
            funName       = funName,
            javaTypeLong  = javaTypeLong,
            javaTypeShort = javaTypeShort
    )

    return s

def tabGroupToString(node):
    s = getFunctionString(
            ref     = util.schema.getPathString(node),
            type    = util.schema.getUiType    (node),
            funName = functionName             (node)
    )
    return s

def tabToString(node):
    s = getFunctionString(
            ref     = util.schema.getPathString(node),
            type    = util.schema.getUiType    (node),
            funName = functionName             (node)
    )
    return s

def uiElementToString(node):
    uiType   = util.schema.getUiType(node)
    javaType = ''

    isEditText  = uiType == 'input'
    isEditText &= not util.schema.isFlagged(node, 'readonly')

    if uiType == 'group':
        return None
    if isEditText:
        javaType = 'android.widget.EditText'

    s = getFunctionString(
            ref      = util.schema.getPathString(node),
            type     = util.schema.getUiType    (node),
            funName  = functionName             (node),
            javaType = javaType
    )
    return s

# Sort a list of LXML nodes by path and group them by type
def sortedNodes(nodes):
    nodes = sorted(nodes, key=util.schema.getPathString)
    nodes = sorted(nodes, key=util.schema.getUiType)
    return nodes

def getModuleFunctions(node):
    # 1. Produce lists of LXML nodes
    tabGroupNodes = util.gui.getGuiNodes(node, 'tab group'       )
    tabNodes      = util.gui.getGuiNodes(node, 'tab'             )
    guiNodes      = util.gui.getGuiNodes(node, 'GUI/data element')

    # 2. In each list, sort the nodes by their path and group them by type
    tabGroupNodes = sortedNodes(tabGroupNodes)
    tabNodes      = sortedNodes(tabNodes     )
    guiNodes      = sortedNodes(guiNodes     )

    # 3. Convert each LXML node into a string (i.e. a test function)
    tabGroupStrings = [tabGroupToString (n) for n in tabGroupNodes]
    tabStrings      = [tabToString      (n) for n in tabNodes     ]
    guiStrings      = [uiElementToString(n) for n in guiNodes     ]

    # 4. Flatten the lists of strings from step 3 into plain old strings
    flatTabGroupStrings = '\n'.join(s for s in tabGroupStrings if s)
    flatTabStrings      = '\n'.join(s for s in tabStrings      if s)
    flatGuiStrings      = '\n'.join(s for s in guiStrings      if s)

    return flatTabGroupStrings + flatTabStrings + flatGuiStrings

def moduleToString(node):
    topMatter  = 'package au.org.intersect.faims.android.util;\n'
    topMatter += '\n'
    topMatter += 'import android.view.View;\n'
    topMatter += 'import android.widget.EditText;\n'
    topMatter += '\n'
    topMatter += 'import com.robotium.solo.Solo;\n'
    topMatter += '\n'
    topMatter += 'public class ModuleUtil extends ModuleHelper {\n'

    midMatter  = getModuleFunctions(node)

    endMatter  = '}'

    return topMatter + midMatter + endMatter

if __name__ == '__main__':
    # PARSE XML
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    # GENERATE AND OUTPUT UI TEST HELPER
    print moduleToString(tree),
