#!/usr/bin/env python2
import sys
import util.schema
import util.xml

#from   lxml import etree
#import util.arch16n
#import util.consts
#import util.data

def getUiNodes(node, xmlType):
    exp     = './/*[@%s="%s"]' % (util.consts.RESERVED_XML_TYPE, xmlType)
    cond    = lambda e: not util.schema.isFlagged(e, 'noui')
    matches = node.xpath(exp)
    matches = filter(cond, matches)
    return matches

def uiElementToString(node):
    topMatter
    /*
        File: ui_schema.xml
        Type: Drop Down
        ref: User/User/Select_User
     */
    public static View get_UserUserSelect_User(Solo solo) {
        return solo.getView((Object) {ref});
    }

def moduleToString(node):
    topMatter  = "package au.org.intersect.faims.android.util;\n"
    topMatter += "\n"
    topMatter += "import android.view.View;\n"
    topMatter += "import android.widget.EditText;\n"
    topMatter += "\n"
    topMatter += "import com.robotium.solo.Solo;\n"
    topMatter += "\n"
    topMatter += "public class ModuleUtil {\n"

    uiNodes   = getUiNodes(node, 'GUI/data element')
    functions = [uiElementToString(n) for n in uiNodes]
    functions = '\n'.join(functions)

    endMatter  = "}\n"

    return topMatter + functions + endMatter


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
