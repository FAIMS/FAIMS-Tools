#!/usr/bin/env bash

if [ -z "$1" ]
then
    module="module.xml"
else
    module=$1
fi
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
echo

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

cd "$thisScriptPath"
python2 -m validator.module "$modulePath/$moduleName"

cleanUp
