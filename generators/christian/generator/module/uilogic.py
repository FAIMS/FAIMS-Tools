import sys
import util.schema
import util.xml

def getUiLogic(tree):
    templateFileName = 'generator/module/uilogic-template.bsh'

    # Load template
    template = None
    with open(templateFileName, 'r') as t:
        template = t.read()
    if not template:
        raise Exception('"%s" could not be loaded' % templateFileName)

    return template

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
#print etree.tostring(
        #tree,
        #pretty_print=True,
        #xml_declaration=True,
        #encoding='utf-8'
#)

print getUiLogic(tree),
