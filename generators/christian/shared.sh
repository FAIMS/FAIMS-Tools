module="module.xml"
while [[ $# -gt 0 ]]
do
    key="$1"

    case "$key" in
        -w|--wireframe)
        WIREFRAME="true"
        ;;
        *)
        module="$key"
        ;;
    esac

    shift
done

if [ ! -f "$module" ]
then
    echo "Module file not found: $module"
    exit
fi

moduleFull="$( readlink -e "$module" )"
modulePath="$( dirname  "$moduleFull")"
moduleName="$( basename "$moduleFull")"
thisScriptPath="$(dirname "$(readlink -e "$0")")"

check_last_run_ended_cleanly() {
    if [ -f "$moduleFull.original" ]
    then
        echo "A previous run terminated unexpectedly. A backup of"
          "'$moduleName' was saved as '$moduleFull.original'. Please either" \
          "restore or delete this backup file before running this script." \
          "Exiting."
        exit
    else
        cp "$moduleFull" "$moduleFull.original"
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
    mv    "$moduleFull.original" "$moduleFull"
    rm -f "$moduleFull.sed"
    exit
}

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
        if [ ! -f "$filename" ]
        then
            echo "  File '$filename' not found"
        fi
        whitespace='\s*'                           # Zero or more whitespace chars
        escaped_filename=$(escape_sed "$filename") # Escape slashes in filename

        temp=$(tempfile)
        cat "$moduleFull" | sed \
            -e "/<!--@SOURCE:$whitespace$escaped_filename$whitespace-->/{
            r $filename
            d
        }" >"$temp"
        mv "$temp" "$moduleFull"
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

trap clean_up SIGHUP SIGINT SIGTERM
check_last_run_ended_cleanly
