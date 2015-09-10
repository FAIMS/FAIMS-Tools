#!/bin/sh

# Convention: targets are augmented with contents of sources

id=1C4qShlu8mcxbQGuhjLy01-wG9G2iuCYKXkUXFXUgFgY

python arch-from-spreadsheet.py        $id                                         >source.0.properties
cat    target.0.properties             source.0.properties                         >source.1.properties
python arch-normalise.py               source.1.properties                         >faims.0.properties

python data-schema-from-spreadsheet.py $id                                         >source.0.xml
python clobber-copy-flagger.py         source.0.xml             -x '//description' >source.1.xml
python clobber-copy-flagger.py         source.1.xml             -x '//lookup'      >source.2.xml
python clobber-copy.py                 source.2.xml target.xml                     >data_schema.xml

grep "property name" target.xml >/tmp/diff1 && grep "property name" data_schema.xml >/tmp/diff2 && diff --side-by-side --suppress-common-lines /tmp/diff1 /tmp/diff2

cd cp-attrib-location
python main.py                         source.csv   target.csv                     >out.csv
cd ..
