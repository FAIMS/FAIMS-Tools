#!/usr/bin/env python2
import signal

signal.signal(signal.SIGINT, lambda a, b : sys.exit())

if __name__ == '__main__':
    print '.required {'
    print '}'
    print ''
    print '.required-label {'
    print '  color: red;'
    print '}'
