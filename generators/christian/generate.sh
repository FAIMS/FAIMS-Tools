#!/bin/sh
set -e

proc1="xsltproc"    # Lord, forgive me
proc2="saxonb-xslt"

mkdir -p module
mkdir -p wireframe

$proc1 generator/arch16n.xsl     module.xml | sort | uniq >module/english.0.properties
$proc1 generator/data-schema.xsl module.xml               >module/data_schema.xml
$proc1 generator/ui-logic.xsl    module.xml               >module/ui_logic.bsh
$proc1 generator/ui-schema.xsl   module.xml               >module/ui_schema.xml
$proc1 generator/ui-styling.xsl  module.xml               >module/ui_styling.css
$proc1 generator/validation.xsl  module.xml               >module/validation.xml

gawk    -f generator/arch16nForWireframe.awk   module/english.0.properties >wireframe/arch16n.xml
$proc2 -xsl:generator/wireframeElements.xsl  -s:module/ui_schema.xml        >wireframe/wireframeElements.sh
