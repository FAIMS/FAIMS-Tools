#!/bin/sh

python data-schema-from-spreadsheet.py 1C4qShlu8mcxbQGuhjLy01-wG9G2iuCYKXkUXFXUgFgY                    >source.0.xml
python clobber-copy-flagger.py         source.0.xml                                 -x '//description' >source.1.xml
python clobber-copy-flagger.py         source.1.xml                                 -x '//lookup'      >source.2.xml
python clobber-copy.py                 source.2.xml target.xml                                         >data_schema.xml
