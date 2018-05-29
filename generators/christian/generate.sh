#!/usr/bin/env bash

THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )
. "$THIS_SCRIPT_PATH/shared.sh"

if [ "$WIREFRAME" = true ] && [ "$OLD_OS" = true ]
then
    printf "Notice: The wireframe produced during this run may not render "
    printf "correctly. Consider using a more recent OS or running FAIMS-Tools "
    printf "via Docker. More information about doing both these things can be "
    printf "found in the readme under 'Dependencies and Setup' and "
    printf "'Alternative Setup (Docker)'.\n\n"
fi

if [ "$WIREFRAME" != true ]
then
    printf "Notice: Wireframe not being generated. Run this script using the "
    printf -- "-w argument to produce a wireframe.\n\n"
fi

if [ "$(check_module_compatiblity)" != true ]
then
    printf "Notice: The module produced during this run may be broken as it "
    printf "was originally compiled with a different version of FAIMS-Tools. "
    printf "To use the version of FAIMS-Tools that this module was compiled "
    printf "with (recommended), run the following command in your FAIMS-Tools "
    printf "directory and compile the module again:\n"
    printf "    git checkout $(prev_build_autogen_hash)\n"
    printf "This message may not be displayed next run. If you are seeing this "
    printf "after checking out the recommended version of FAIMS-Tools and "
    printf "recompiling, you can safely ignore this message.\n\n"
fi

cd "$MODULE_PATH" >/dev/null

apply_source_directives
apply_preproc_directives

cd - >/dev/null

############################ PERFORM THE TRANSFORMS ############################
mkdir -p "$MODULE_PATH/module"
mkdir -p "$MODULE_PATH/wireframe"
mkdir -p "$MODULE_PATH/tests"

if [ "$WIREFRAME" = true ]
then
    cp "$THIS_SCRIPT_PATH/generator/wireframe/makeElement.sh"          "$MODULE_PATH/wireframe"
    cp "$THIS_SCRIPT_PATH/generator/wireframe/arch16nForWireframe.awk" "$MODULE_PATH/wireframe"
    cp "$THIS_SCRIPT_PATH/generator/wireframe/wireframeElements.xsl"   "$MODULE_PATH/wireframe"
fi
cp "$THIS_SCRIPT_PATH/tests/module/mock.bsh"                       "$MODULE_PATH/tests"
cp "$THIS_SCRIPT_PATH/tests/module/test.bsh"                       "$MODULE_PATH/tests"

cd "$THIS_SCRIPT_PATH"
echo "Generating arch16n..."
python2 -m generator.module.arch16n       "$TMP_MODULE_FULL" >"$MODULE_PATH/module/english.0.properties"
echo "Generating data schema..."
python2 -m generator.module.dataschema    "$TMP_MODULE_FULL" >"$MODULE_PATH/module/data_schema.xml"
#echo "Generating UI test helpers..."
#python2 -m generator.module.test          "$TMP_MODULE_FULL" >"$MODULE_PATH/tests/ModuleUtil.java"
echo "Generating logic..."
python2 -m generator.module.uilogic       "$TMP_MODULE_FULL" >"$MODULE_PATH/module/ui_logic.bsh"
echo "Generating UI schema..."
python2 -m generator.module.uischema      "$TMP_MODULE_FULL" >"$MODULE_PATH/module/ui_schema.xml"
echo "Generating CSS..."
python2 -m generator.module.uistyling     "$TMP_MODULE_FULL" >"$MODULE_PATH/module/ui_styling.css"
echo "Generating validation schema..."
python2 -m generator.module.validation    "$TMP_MODULE_FULL" >"$MODULE_PATH/module/validation.xml"
if [ "$WIREFRAME" = true ]
then
    echo "Generating wireframe .gv file..."
    python2 -m generator.wireframe.datastruct "$TMP_MODULE_FULL" >"$MODULE_PATH/wireframe/datastruct.gv"
fi
cd - >/dev/null

################################## WIREFRAME ###################################
if [ "$WIREFRAME" = true ]
then
    cd "$MODULE_PATH" >/dev/null

    gawk          -f "$MODULE_PATH/wireframe/arch16nForWireframe.awk"   "$MODULE_PATH/module/english.0.properties" >"$MODULE_PATH/wireframe/arch16n.xml"
    saxonb-xslt -xsl:"$MODULE_PATH/wireframe/wireframeElements.xsl"  -s:"$MODULE_PATH/module/ui_schema.xml"        >"$MODULE_PATH/wireframe/wireframeElements.sh"

    cd - >/dev/null
    cd "$MODULE_PATH/wireframe/" >/dev/null
    chmod +x wireframeElements.sh
        echo "Generating wireframe .pdf file..."
        ./wireframeElements.sh >/dev/null
        cairosvg wireframe.svg -d 70 -f pdf -o wireframe.pdf
        find . ! -name "wireframe.pdf" -type f -exec rm -f {} +

    cd - >/dev/null
fi

####################### HANDLE POST-PROCESSING DIRECTIVE #######################
cd "$MODULE_PATH" >/dev/null
apply_postproc_directives
cd - >/dev/null

########################### COPY CONVENIENCE SCRIPT ############################
cp "$THIS_SCRIPT_PATH/../../module-dev-scripts/upload.py" "$MODULE_PATH"

clean_up_and_exit
