#!/bin/bash

cd ..

numPassed=0
numTests=0
failures=( )

for input in $(find tests-generator/in/ -name "*.xml" | sort)
do
    if [ ! -s "$input" ]
    then
        continue
    fi

    filename=$(basename "$input")  # tests-generator/in/1.xml -> 1.xml
    noextension="${filename%.*}"   # 1.xml -> 1
    subject=$( grep "@TEST:" "$input" | sed -rn 's/^\s*<!--\s*@TEST:\s*(.*[^ ])\s*-->\s*$/\1/p' )
    didPass=1
    echo "Running $filename - \"$subject\"..."

    ./generate.sh "$input"
    for pathExpected_name_ext in $(find tests-generator/out/$noextension/ -type f | sort)
    do
        name_ext=$(basename "$pathExpected_name_ext")
        pathActual_name_ext="module/$name_ext"
        name="${name_ext%.*}"
        ext="${name_ext##*.}"

        if   [ "$ext" = "xml" ]
        then
            # Canononicalise XML
            xmllint --c14n "$pathExpected_name_ext" > /tmp/output-expected-$noextension.$ext
            xmllint --c14n "$pathActual_name_ext"   > /tmp/output-actual-$noextension.$ext
        elif [ "$ext" = "properties" ]
        then
            # Canonicalise arch16n's
            sort -s "$pathExpected_name_ext" | uniq | sed '/^\s*$/d' > /tmp/output-expected-$noextension.$ext
            sort -s "$pathActual_name_ext"   | uniq | sed '/^\s*$/d' > /tmp/output-actual-$noextension.$ext
        else
            # Move ouputs where XML would've gone
            cp "$pathExpected_name_ext" /tmp/output-expected-$noextension.$ext
            cp "$pathActual_name_ext"   /tmp/output-actual-$noextension.$ext
        fi

        colordiff -u /tmp/output-expected-$noextension.$ext \
                     /tmp/output-actual-$noextension.$ext
        if [ $? -eq 0 ]
        then
            continue
        fi
        didPass=0
        i=${#failures[@]}
        failures[$i]="Failure: $filename - \"$subject\". $name_ext generated incorrectly."
    done

    if [ $didPass -eq 1 ]
    then
        ((numPassed++))
    else
        didPass=1 # reset to default
    fi
    ((numTests++))
done

echo ""
echo "TEST SUMMARY:"

for f in "${failures[@]}"
do
    echo "  $f"
done

echo "$numTests test(s) completed with $numPassed pass(es) and $((($numTests - $numPassed))) failure(s)."
