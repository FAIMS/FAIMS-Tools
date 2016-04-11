#!/usr/bin/env bash
proc1="xsltproc"    # Lord, forgive me
proc2="saxonb-xslt"


if [ -z "$1" ]
then
    module="module.xml"
else
    module=$1
fi
modulePath=$( dirname  "$module" )
moduleName=$( basename "$module" )
thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

####################### HANDLE PRE-PROCESSING DIRECTIVE ########################
# This will require some clean up after the transforms occur                   #
################################################################################
cp "$module" "${module}.original"

cd "$modulePath" >/dev/null
cmd=$( grep "@PREPROC:" "$moduleName" | head -n 1 | sed -rn 's/^\s*<!--\s*@PREPROC:\s*(.*[^ ])\s*-->\s*$/\1/p' )
if [ ! -z "$cmd" ]
then
    echo "Running pre-processing command:"
    echo "  $cmd"
    eval $cmd # Yes, I've heard of the "eval is evil" dogma
fi
cd - >/dev/null

############################### GENERATE MODULE ################################
mkdir -p "$modulePath/module"

$proc1 "$thisScriptPath/generator/module/arch16n.xsl"     $module | sort | uniq >"$modulePath/module/english.0.properties"
$proc1 "$thisScriptPath/generator/module/data-schema.xsl" $module               >"$modulePath/module/data_schema.xml"
$proc1 "$thisScriptPath/generator/module/ui-logic.xsl"    $module               >"$modulePath/module/ui_logic.bsh"
$proc1 "$thisScriptPath/generator/module/ui-schema.xsl"   $module               >"$modulePath/module/ui_schema.xml"
$proc1 "$thisScriptPath/generator/module/ui-styling.xsl"  $module               >"$modulePath/module/ui_styling.css"
$proc1 "$thisScriptPath/generator/module/validation.xsl"  $module               >"$modulePath/module/validation.xml"

####################### HANDLE PRE-PROCESSING DIRECTIVE ########################
# This is the clean up step mentioned near the start of this script            #
################################################################################
mv "${module}.original" "$module"

################################ DISPLAY ERRORS ################################
# Parse errors
find "$modulePath/module" -type f -print | xargs grep -nr --color="always" "ERROR"   | sed -e 's/\s\+</ </g'
# Parse warnings
find "$modulePath/module" -type f -print | xargs grep -nr --color="always" "WARNING" | sed -e 's/\s\+</ </g'

####################### HANDLE POST-PROCESSING DIRECTIVE #######################
cd "$modulePath" >/dev/null
cmd=$( grep "@POSTPROC:" "$moduleName" | head -n 1 | sed -rn 's/^\s*<!--\s*@POSTPROC:\s*(.*[^ ])\s*-->\s*$/\1/p' )
if [ ! -z "$cmd" ]
then
    echo "Running post-processing command:"
    echo "  $cmd"
    eval $cmd
fi
cd - >/dev/null

############################## GENERATE WIREFRAME ##############################
mkdir -p "$modulePath/wireframe"

export PYTHONPATH="$thisScriptPath/validator" #TODO: This isn't a real great idea, apparently

cp          "$thisScriptPath/generator/wireframe/wireframeElements.xsl"     "$modulePath/wireframe"
cp          "$thisScriptPath/generator/wireframe/makeElement.sh"            "$modulePath/wireframe"

gawk     -f "$thisScriptPath/generator/wireframe/arch16nForWireframe.awk"   "$modulePath/module/english.0.properties" >"$modulePath/wireframe/arch16n.xml"
python      "$thisScriptPath/generator/wireframe/datastruct.py"              $module                                  >"$modulePath/wireframe/datastruct.gv"

cd "$modulePath/wireframe/" >/dev/null
$proc2 -xsl:wireframeElements.xsl  -s:"../module/ui_schema.xml"        >wireframeElements.sh
chmod +x wireframeElements.sh
./wireframeElements.sh
dot -Tsvg datastruct.gv > wireframe.svg
cd - >/dev/null
