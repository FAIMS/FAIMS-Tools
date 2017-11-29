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

check_last_run_ended_cleanly() {
    if [ -f ".$module.original" ]
    then
        echo "A previous run terminated unexpectedly. A backup of '$module'" \
          "was saved as '.$module.original'. Please either restore or delete" \
          "this backup file before running this script. Exiting."
        exit
    else
        cp "$module" ".$module.original"
    fi
}

get_next_source() {
    unstripped=$(grep -m 1 "(?<=<\!--@SOURCE:).+(?=-->)" "$moduleName" -RohP)
    echo -e "$unstripped" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

# Escape sed's special characters
escape_sed() {
    echo "$1" |
    sed \
        -e 's/\//\\\//g' \
        -e 's/\&/\\\&/g'
}

clean_up() {
    mv    "$modulePath/.$module.original" "$modulePath/$module"
    rm -f "$modulePath/$module.sed"
    exit
}
trap clean_up SIGHUP SIGINT SIGTERM

prev_build_autogen_hash() {
    logicFilePath="$modulePath/module/ui_logic.bsh"

    if [ -f "$logicFilePath" ]
    then
        sed \
          -e 's/.* //g' \
          -e '2q' \
          -e 'd' \
          "$logicFilePath"
    else
        printf ""
    fi
}

this_build_autogen_hash() {
    cd "$thisScriptPath" >/dev/null

    git log | sed \
      -e 's/.* //g' \
      -e '1q'

    cd - >/dev/null
}

check_backwards_compatibility() {
    prevHash=$(prev_build_autogen_hash)
    thisHash=$(this_build_autogen_hash)

    if [ "$prevHash" = "" ]
    then
        printf "1"
        return 0
    fi

    if [ "$prevHash" = "$thisHash" ]
    then
        printf "1"
    else
        printf "0"
    fi
}

apply_source_directives() {
    # In module.xml, replace any line <!--@SOURCE: path/to/file--> with the contents
    # of the file at path/to/file.
    echo "Applying @SOURCE directives..."
    while [[ ! -z $(get_next_source) ]]
    do
        filename=$(get_next_source)
        if [ ! -f "$filename" ]; then
            echo "  File '$filename' not found"
        fi
        whitespace='\s*'                           # Zero or more whitespace chars
        escaped_filename=$(escape_sed "$filename") # Escape slashes in filename

        sed -i.sed \
            -e "/<!--@SOURCE:$whitespace$escaped_filename$whitespace-->/{
            r $filename
            d
        }" "$module"
    done
    echo
}

apply_proc_directives() {
    procupper=$(echo "$1" | awk '{print toupper($1)}')
    proclower=$(echo "$1" | awk '{print tolower($1)}')

    cmd=$(
        grep '@'$procupper'PROC:' "$moduleName" | \
        head -n 1 | \
        sed -rn 's/^\s*<!--\s*@'$procupper'PROC:\s*(.*[^ ])\s*-->\s*$/\1/p'
    )

    if [ ! -z "$cmd" ]
    then
        echo "Running ${proclower}-processing command:"
        echo "  $cmd"
        eval "$cmd"
    fi
}

apply_preproc_directives() {
    apply_proc_directives 'pre'
}

apply_postproc_directives() {
    apply_proc_directives 'post'
}
