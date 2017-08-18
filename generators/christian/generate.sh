#!/usr/bin/env bash

thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$thisScriptPath/shared.sh"

check_last_run_ended_cleanly

if [ "$WIREFRAME" != "true" ]
then
    echo "Notice: Wireframe not being generated. Run this script using the -w" \
      "argument to produce a wireframe."
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
python2 -m generator.module.arch16n       "$modulePath/$module" >"$modulePath/module/english.0.properties"
echo "Generating data schema..."
python2 -m generator.module.dataschema    "$modulePath/$module" >"$modulePath/module/data_schema.xml"
echo "Generating UI test helpers..."
python2 -m generator.module.test          "$modulePath/$module" >"$modulePath/tests/ModuleUtil.java"
echo "Generating logic..."
python2 -m generator.module.uilogic       "$modulePath/$module" >"$modulePath/module/ui_logic.bsh"
echo "Generating UI schema..."
python2 -m generator.module.uischema      "$modulePath/$module" >"$modulePath/module/ui_schema.xml"
echo "Generating CSS..."
python2 -m generator.module.uistyling     "$modulePath/$module" >"$modulePath/module/ui_styling.css"
echo "Generating validation schema..."
python2 -m generator.module.validation    "$modulePath/$module" >"$modulePath/module/validation.xml"
if [ "$WIREFRAME" = "true" ]
then
    echo "Generating wireframe .gv file..."
    python2 -m generator.wireframe.datastruct "$modulePath/$module" >"$modulePath/wireframe/datastruct.gv"
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

clean_up
