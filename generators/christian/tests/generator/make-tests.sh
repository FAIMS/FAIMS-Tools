#!/bin/sh

cd ../../

rm -rf      tests/generator/out/*

for input in $(find tests/generator/in/ -maxdepth 1 -name "*.xml" | sort)
do
    if [ ! -s "$input" ]
    then
        continue
    fi

    filename=$(basename "$input")  # tests/generator/in/1.xml -> 1.xml
    noextension="${filename%.*}"   # 1.xml -> 1
    echo "Making $filename..."
    ./generate.sh "$input" >/dev/null
    mkdir                          tests/generator/out/$noextension
    cp tests/generator/in/module/* tests/generator/out/$noextension/
done

rm -rf tests/generator/in/module
rm -rf tests/generator/in/wireframe
