#!/usr/bin/env bash
set -e

proc1="xsltproc"    # Lord, forgive me
proc2="saxonb-xslt"


if [ -z "$1" ]
then
    module="module.xml"
else
    module=$1
fi
modulePath=$( dirname  $( readlink -e "$module" ))
moduleName=$( basename $( readlink -e "$module" ))
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

############################ PERFORM THE TRANSFORMS ############################
mkdir -p "$modulePath/module"
mkdir -p "$modulePath/wireframe"

cd "$thisScriptPath"
python2 -m generator.module.arch16n    "$modulePath/$module" >"$modulePath/module/english.0.properties"
python2 -m generator.module.dataschema "$modulePath/$module" >"$modulePath/module/data_schema.xml"
python2 -m generator.module.test       "$modulePath/$module" >"$modulePath/module/ModuleUtil.java"
$proc1  "$thisScriptPath/generator/module/ui-logic.xsl"   "$modulePath/$module" >"$modulePath/module/ui_logic.bsh"
python2 -m generator.module.uischema   "$modulePath/$module" >"$modulePath/module/ui_schema.xml"
python2 -m generator.module.uistyling  "$modulePath/$module" >"$modulePath/module/ui_styling.css"
python2 -m generator.module.validation "$modulePath/$module" >"$modulePath/module/validation.xml"

gawk     -f "$thisScriptPath/generator/wireframe/arch16nForWireframe.awk"   "$modulePath/module/english.0.properties" >"$modulePath/wireframe/arch16n.xml"
$proc2 -xsl:"$thisScriptPath/generator/wireframe/wireframeElements.xsl"  -s:"$modulePath/module/ui_schema.xml"        >"$modulePath/wireframe/wireframeElements.sh"
python2 -m generator.wireframe.datastruct "$modulePath/$module"            >"$modulePath/wireframe/datastruct.gv"
cd -

cp          "$thisScriptPath/generator/wireframe/makeElement.sh"            "$modulePath/wireframe"
cd "$modulePath/wireframe/"
chmod +x wireframeElements.sh
./wireframeElements.sh
cd - >/dev/null

####################### HANDLE PRE-PROCESSING DIRECTIVE ########################
# This is the clean up step mentioned near the start of this script            #
################################################################################
mv "$modulePath/${module}.original" "$modulePath/$module"

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
