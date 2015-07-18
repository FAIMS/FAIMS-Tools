#!/bin/sh

proc="xsltproc"

mkdir -p module

touch                                              module/ui-styling.css
$proc generator/arch16n.xsl     module.xml | uniq >module/english.0.properties
$proc generator/data-schema.xsl module.xml        >module/data-schema.xml
$proc generator/ui-logic.xsl    module.xml        >module/ui-logic.bsh
$proc generator/ui-schema.xsl   module.xml        >module/ui-schema.xml
