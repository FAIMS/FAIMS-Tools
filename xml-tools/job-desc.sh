#!/bin/sh

# Convention: targets are augmented with contents of sources

id=1fh8muYLayDiIvuhLyl6ofrpm-SizARQpMLaNx_wKN6w

cp data_schema.xml target.xml
python data-schema-from-spreadsheet.py $id                                         >source.0.xml
exit
python clobber-copy-flagger.py         source.0.xml             -x '//description' >source.1.xml
python clobber-copy.py                 source.1.xml target.xml                     >data_schema.xml

grep "property name" target.xml >/tmp/diff1 && grep "property name" data_schema.xml >/tmp/diff2 && diff --side-by-side --suppress-common-lines /tmp/diff1 /tmp/diff2
