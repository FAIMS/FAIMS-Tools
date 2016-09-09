#!/usr/bin/env python2
import sys
import util.schema
import util.ui
import util.xml

# TODO: Safely handle case where dashes are included in function name
def functionName(node):
    return 'get_' + node.tag

def uiElementToString(node):
    s  = '    /*\n'
    s += '        File: ui_schema.xml\n'
    s += '        Type: {type}\n'
    s += '        ref:  {ref}\n'
    s += '     */\n'
    s += '    public static View {funName}(Solo solo) {{\n'
    s += '        String ref = "{ref}";\n'
    s += '        return solo.getView((Object) ref);\n'
    s += '    }}\n'
    s  = s.format(
            ref    =util.schema.getPathString(node),
            type   =util.schema.guessType    (node),
            funName=functionName             (node)
    )

    return s

def moduleToString(node):
    topMatter  = 'package au.org.intersect.faims.android.util;\n'
    topMatter += '\n'
    topMatter += 'import android.view.View;\n'
    topMatter += 'import android.widget.EditText;\n'
    topMatter += '\n'
    topMatter += 'import com.robotium.solo.Solo;\n'
    topMatter += '\n'
    topMatter += 'public class ModuleUtil {\n'

    uiNodes   = util.ui.getUiNodes(node, 'GUI/data element')
    functions = [uiElementToString(n) for n in uiNodes]
    functions = '\n'.join(functions)

    endMatter  = '}'

    return topMatter + functions + endMatter

################################################################################
#                                  PARSE XML                                   #
################################################################################
filenameModule = sys.argv[1]
tree = util.xml.parseXml(filenameModule)
util.schema.normalise(tree)
util.schema.annotateWithXmlTypes(tree)
util.schema.expandCompositeElements(tree)
util.schema.annotateWithXmlTypes(tree)

################################################################################
#                        GENERATE AND OUTPUT DATA SCHEMA                       #
################################################################################
print moduleToString(tree)
