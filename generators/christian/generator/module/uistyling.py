#!/usr/bin/env python2
from   util.consts import *
import sys
import util.schema
import util.xml
import signal

signal.signal(signal.SIGINT, lambda a, b : sys.exit())

if __name__ == '__main__':
    filenameModule = sys.argv[1]
    tree = util.xml.parseXml(filenameModule)
    tree = util.schema.parseSchema(tree)

    cssNodes = util.xml.getAll(tree, keep=lambda e: e.tag == TAG_CSS)
    cssText  = cssNodes[0].text if len(cssNodes) else ''

    print '.required {'
    print '}'
    print ''
    print '.required-label {'
    print '  color: red;'
    print '}'
    if cssText:
        print cssText
