#!/bin/sh
set -e
proc="saxonb-xslt"

#mkdir -p module

#$proc -xsl:generator/arch16n.xsl     		-s:module.xml   | sort | uniq >module/english.0.properties 
#$proc -xsl:generator/data-schema.xsl 		-s:module.xml                  >module/data-schema.xml
#$proc -xsl:generator/ui-logic.xsl    		-s:module.xml                 >module/ui-logic.bsh &
#$proc -xsl:generator/ui-schema.xsl   		-s:module.xml                 >module/ui-schema.xml 
#$proc -xsl:generator/ui-styling.xsl  		-s:module.xml                  >module/ui-styling.css &
#$proc -xsl:generator/validation.xsl  		-s:module.xml                  >module/validation.xml &
gawk -f generator/arch16nForWireframe.awk 		module/english.0.properties > module/arch16n.xml
$proc -xsl:generator/wireframeElements.xsl  -s:module/ui-schema.xml               >module/wireframeElements.sh
