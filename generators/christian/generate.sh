#!/bin/bash
set -e

proc1="xsltproc"    # Lord, forgive me
proc2="saxonb-xslt"


if [ -z $1 ]
then
    module="module.xml"
else
    module=$1
fi
modulePath=$( dirname "$module" )

mkdir -p "$modulePath/module"
mkdir -p "$modulePath/wireframe"

$proc1 generator/arch16n.xsl     $module | sort | uniq >"$modulePath/module/english.0.properties"
$proc1 generator/data-schema.xsl $module               >"$modulePath/module/data_schema.xml"
$proc1 generator/ui-logic.xsl    $module               >"$modulePath/module/ui_logic.bsh"
$proc1 generator/ui-schema.xsl   $module               >"$modulePath/module/ui_schema.xml"
$proc1 generator/ui-styling.xsl  $module               >"$modulePath/module/ui_styling.css"
$proc1 generator/validation.xsl  $module               >"$modulePath/module/validation.xml"

gawk     -f generator/arch16nForWireframe.awk   "$modulePath/module/english.0.properties" >"$modulePath/wireframe/arch16n.xml"
$proc2 -xsl:generator/wireframeElements.xsl  -s:"$modulePath/module/ui_schema.xml"        >"$modulePath/wireframe/wireframeElements.sh"

# Handle post-processing directive
cd "$modulePath"
cmd=$( grep "@POSTPROC:" "$module" | head -n 1 | sed -rn 's/^\s*<!--\s*@POSTPROC:\s*(.*[^ ])\s*-->\s*$/\1/p' )
eval $cmd # Yes, I've heard of the "eval is evil" dogma
