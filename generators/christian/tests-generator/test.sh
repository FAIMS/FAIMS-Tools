#!/bin/bash

cd ..

numTests=0
failures=( )

for input in $(find tests-generator/in/ -name "*.xml")
do
    filename=$(basename "$input")  # tests-generator/in/1.xml -> 1.xml
    noextension="${filename%.*}"   # 1.xml -> 1
    subject=$( grep "@TEST" "$input" | sed -rn 's/^\s*<!--\s*@TEST:\s*(.*)\s*-->\s*$/\1/p' )

    ./generate.sh "$input"
    for pathExpected_name_ext in $(find tests-generator/out/$noextension/ -type f)
    do
        name_ext=$(basename "$pathExpected_name_ext")
        pathActual_name_ext="module/$name_ext"
        name="${name_ext%.*}"
        ext="${name_ext##*.}"

        if   [ "$ext" = "xml" ]
        then
            # Canononicalise XML
            xmllint --c14n "$pathExpected_name_ext" > /tmp/output-expected.$ext
            xmllint --c14n "$pathActual_name_ext"   > /tmp/output-actual.$ext
        elif [ "$ext" = "properties" ]
        then
            # Canonicalise arch16n's
            sort -s "$pathExpected_name_ext" | uniq | sed '/^\s*$/d' > /tmp/output-expected.$ext
            sort -s "$pathActual_name_ext"   | uniq | sed '/^\s*$/d' > /tmp/output-actual.$ext
        else
            # Move ouputs where XML would've gone
            cp "$pathExpected_name_ext" /tmp/output-expected.$ext
            cp "$pathActual_name_ext"   /tmp/output-actual.$ext
        fi

        colordiff -u /tmp/output-expected.$ext \
                     /tmp/output-actual.$ext
        if [ $? -eq 0 ]
        then
            continue
        fi
        i=${#failures[@]}
        failures[$i]="Failure: $filename - \"$subject\". $name_ext generated incorrectly."
    done
    ((numTests++))
done

echo "TEST SUMMARY:"

for f in "${failures[@]}"
do
    echo "  $f"
done

echo "$numTests tests completed with $((($numTests - ${#failures[@]}))) passes and ${#failures[@]} failures."
