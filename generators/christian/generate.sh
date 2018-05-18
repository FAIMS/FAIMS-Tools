#!/usr/bin/env bash

thisScriptPath=$(dirname "$(readlink -e "$0")")
source "$thisScriptPath/shared.sh"

if [ "$WIREFRAME" != "true" ]
then
    echo "Notice: Wireframe not being generated. Run this script using the -w" \
      "argument to produce a wireframe."
    echo
fi

if [ $(check_backwards_compatibility) = "0" ]
then

    echo -e "Notice: The module produced during this run may be broken as it" \
      "was originally compiled with a different version of FAIMS-Tools. To" \
      "use the version of FAIMS-Tools that this module was compiled with" \
      "(recommended), run the following command in your FAIMS-Tools directory" \
      "and compile the module again:\n" \
      "  git checkout $(prev_build_autogen_hash)\n" \
      "\bThis message may not be displayed next run. If you are seeing this" \
      "after checking out the recommended version of FAIMS-Tools and" \
      "recompiling, you can safely ignore this message."
    echo
fi

cd "$modulePath" >/dev/null

apply_source_directives
apply_preproc_directives

cd - >/dev/null

############################ PERFORM THE TRANSFORMS ############################
mkdir -p "$modulePath/module"
mkdir -p "$modulePath/wireframe"
mkdir -p "$modulePath/tests"

if [ "$WIREFRAME" = "true" ]
then
    cp "$thisScriptPath/generator/wireframe/makeElement.sh"          "$modulePath/wireframe"
    cp "$thisScriptPath/generator/wireframe/arch16nForWireframe.awk" "$modulePath/wireframe"
    cp "$thisScriptPath/generator/wireframe/wireframeElements.xsl"   "$modulePath/wireframe"
fi
cp "$thisScriptPath/tests/module/mock.bsh"                       "$modulePath/tests"
cp "$thisScriptPath/tests/module/test.bsh"                       "$modulePath/tests"

cd "$thisScriptPath"
echo "Generating arch16n..."
python2 -m generator.module.arch16n       "$tmpModuleFull" >"$modulePath/module/english.0.properties"
echo "Generating data schema..."
python2 -m generator.module.dataschema    "$tmpModuleFull" >"$modulePath/module/data_schema.xml"
#echo "Generating UI test helpers..."
#python2 -m generator.module.test          "$tmpModuleFull" >"$modulePath/tests/ModuleUtil.java"
echo "Generating logic..."
python2 -m generator.module.uilogic       "$tmpModuleFull" >"$modulePath/module/ui_logic.bsh"
echo "Generating UI schema..."
python2 -m generator.module.uischema      "$tmpModuleFull" >"$modulePath/module/ui_schema.xml"
echo "Generating CSS..."
python2 -m generator.module.uistyling     "$tmpModuleFull" >"$modulePath/module/ui_styling.css"
echo "Generating validation schema..."
python2 -m generator.module.validation    "$tmpModuleFull" >"$modulePath/module/validation.xml"
if [ "$WIREFRAME" = "true" ]
then
    echo "Generating wireframe .gv file..."
    python2 -m generator.wireframe.datastruct "$tmpModuleFull" >"$modulePath/wireframe/datastruct.gv"
fi
cd - >/dev/null

################################## WIREFRAME ###################################
if [ "$WIREFRAME" = "true" ]
then
    cd "$modulePath" >/dev/null

    gawk          -f "$modulePath/wireframe/arch16nForWireframe.awk"   "$modulePath/module/english.0.properties" >"$modulePath/wireframe/arch16n.xml"
    saxonb-xslt -xsl:"$modulePath/wireframe/wireframeElements.xsl"  -s:"$modulePath/module/ui_schema.xml"        >"$modulePath/wireframe/wireframeElements.sh"

    cd - >/dev/null
    cd "$modulePath/wireframe/" >/dev/null
    chmod +x wireframeElements.sh
        echo "Generating wireframe .pdf file..."
        ./wireframeElements.sh >/dev/null
        cairosvg wireframe.svg -d 70 -f pdf -o wireframe.pdf
        find . ! -name "wireframe.pdf" -type f -exec rm -f {} +

    cd - >/dev/null
fi

####################### HANDLE POST-PROCESSING DIRECTIVE #######################
cd "$modulePath" >/dev/null
apply_postproc_directives
cd - >/dev/null

clean_up_and_exit
