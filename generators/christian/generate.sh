#!/usr/bin/env bash

proc="saxonb-xslt"

############################## ARGUMENT HANDLING ###############################
module="module.xml"
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -w|--wireframe)
        WIREFRAME="true"
        ;;
        *)
        module=$key
        ;;
    esac

    shift
done

modulePath=$( dirname  $( readlink -e "$module" ))
moduleName=$( basename $( readlink -e "$module" ))
thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Escape sed's special characters
escape_sed() {
    echo "$1" |
    sed \
        -e 's/\//\\\//g' \
        -e 's/\&/\\\&/g'
}

cleanUp() {
    mv    "$modulePath/.$module.original" "$modulePath/$module"
    rm -f "$modulePath/$module.sed"
    exit
}
trap cleanUp SIGHUP SIGINT SIGTERM

if [ -f ".$module.original" ]
then
    echo "A previous run terminated unexpectedly. A backup of '$module' was" \
      "saved as '.$module.original'. Please either restore or delete this" \
      "backup file before running this script. Exiting."
    exit
else
    cp "$module" ".$module.original"
fi

if [ "$WIREFRAME" != "true" ]
then
    echo "Notice: Wireframe not being generated. Run this script using the -w" \
      "argument to produce a wireframe."
fi

cd "$modulePath" >/dev/null

# In module.xml, replace any line <!--@SOURCE: path/to/file--> with the contents
# of the file at path/to/file.
echo "Applying @SOURCE directives..."
for filename in $(grep "(?<=<\!--@SOURCE:).+(?=-->)" . -RohP)
do
    whitespace='\s*'                           # Zero or more whitespace chars
    escaped_filename=$(escape_sed "$filename") # Escape slashes in filename

    sed -i.sed \
        -e "/<!--@SOURCE:$whitespace$escaped_filename$whitespace-->/{
        r $filename
        d
    }" "$module"
done

####################### HANDLE PRE-PROCESSING DIRECTIVE ########################
# This will require some clean up after the transforms occur                   #
################################################################################
cmd=$( grep "@PREPROC:" "$moduleName" | head -n 1 | sed -rn 's/^\s*<!--\s*@PREPROC:\s*(.*[^ ])\s*-->\s*$/\1/p' )
if [ ! -z "$cmd" ]
then
    echo "Running pre-processing command:"
    echo "  $cmd"
    eval $cmd
fi
cd - >/dev/null

############################ PERFORM THE TRANSFORMS ############################
mkdir -p "$modulePath/module"
mkdir -p "$modulePath/wireframe"
mkdir -p "$modulePath/tests"

cp "$thisScriptPath/generator/wireframe/makeElement.sh"          "$modulePath/wireframe"
cp "$thisScriptPath/generator/wireframe/arch16nForWireframe.awk" "$modulePath/wireframe"
cp "$thisScriptPath/generator/wireframe/wireframeElements.xsl"   "$modulePath/wireframe"
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

################################## WIREFRAME ###################################
cd - >/dev/null
cd "$modulePath" >/dev/null
gawk    -f "$modulePath/wireframe/arch16nForWireframe.awk"   "$modulePath/module/english.0.properties" >"$modulePath/wireframe/arch16n.xml"
$proc -xsl:"$modulePath/wireframe/wireframeElements.xsl"  -s:"$modulePath/module/ui_schema.xml"        >"$modulePath/wireframe/wireframeElements.sh"

cd - >/dev/null
cd "$modulePath/wireframe/" >/dev/null
chmod +x wireframeElements.sh
if [ "$WIREFRAME" = "true" ]
then
    echo "Generating wireframe .pdf file..."
    ./wireframeElements.sh >/dev/null
    cairosvg wireframe.svg -d 70 -f pdf -o wireframe.pdf
    find . ! -name "wireframe.pdf" -type f -exec rm -f {} +
fi

cd - >/dev/null

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

cleanUp
