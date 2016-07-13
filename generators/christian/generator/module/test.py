#!/usr/bin/env python2
import sys
import util.schema
import util.ui
import util.xml

# TODO: Safely handle case where dashes are included in function name
def functionName(node):
    pathSegments = util.schema.getPath(node)
    pathSegments = [path


    return 'get_' + node.tag

def parseJavaType(javaType):
    splitted = javaType.split('.')

    javaTypeShort = splitted[-1]
    javaTypeLong  = '.'.join(splitted)

    return javaTypeLong, javaTypeShort

def getFunctionString(ref, type, funName, javaType=None):
    if not javaType: javaType = 'android.view.View'

    javaTypeLong, javaTypeShort = parseJavaType(javaType)

    s  = '    /*\n'
    s += '        File: ui_schema.xml\n'
    s += '        Type: {type}\n'
    s += '        ref:  {ref}\n'
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
            type    = util.schema.guessType    (node),
            funName = functionName             (node)
    )
    return s

def tabToString(node):
    s = getFunctionString(
            ref     = util.schema.getPathString(node),
            type    = util.schema.guessType    (node),
            funName = functionName             (node)
    )
    return s

def uiElementToString(node):
    uiType   = util.schema.guessType(node)
    javaType = ''
    if uiType == 'input' and not util.schema.isFlagged(node, 'readonly'):
        javaType = 'android.widget.EditText'

    s = getFunctionString(
            ref      = util.schema.getPathString(node),
            type     = util.schema.guessType    (node),
            funName  = functionName             (node),
            javaType = javaType
    )
    return s

def getModuleFunctions(node):
    # 1. Produce lists of LXML nodes
    tabGroupNodes = util.ui.getUiNodes(node, 'tab group'       )
    tabNodes      = util.ui.getUiNodes(node, 'tab'             )
    guiNodes      = util.ui.getUiNodes(node, 'GUI/data element')

    # 2. Convert each LXML node into a string (i.e. a test function)
    tabGroupStrings = [tabGroupToString (n) for n in tabGroupNodes]
    tabStrings      = [tabToString      (n) for n in tabNodes     ]
    guiStrings      = [uiElementToString(n) for n in guiNodes     ]

    # 3. Flatten the lists of strings from step 2 into plain old strings
    flatTabGroupStrings = '\n'.join(tabGroupStrings)
    flatTabStrings      = '\n'.join(tabStrings     )
    flatGuiStrings      = '\n'.join(guiStrings     )

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

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithTypes(tree)
util.schema.expandCompositeElements(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
print moduleToString(tree)
