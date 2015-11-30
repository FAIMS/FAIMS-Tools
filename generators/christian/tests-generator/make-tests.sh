#!/bin/sh

cd ..

rm -rf      tests-generator/out/*

for input in $(find tests-generator/in/ -name "*.xml")
do
    filename=$(basename "$input")  # tests-generator/in/1.xml -> 1.xml
    noextension="${filename%.*}"   # 1.xml -> 1
    ./generate.sh "$input"
    mkdir       tests-generator/out/$noextension
    cp module/* tests-generator/out/$noextension/
    rm          tests-generator/out/$noextension/upload.sh
done
