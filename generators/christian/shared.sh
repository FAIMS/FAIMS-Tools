thisScriptPath=$(dirname "$(readlink -e "$0")")

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
    exit 1
fi

moduleFull=$( readlink -e "$module" )
modulePath=$( dirname  "$moduleFull")
moduleName=$( basename "$moduleFull")

get_next_source() {
    local unstripped=$(
        grep -m 1 "(?<=<\!--@SOURCE:).+(?=-->)" "$tmpModuleName" -RohP
    )
    echo -e "$unstripped" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

# Escape sed's special characters
escape_sed() {
    echo "$1" |
    sed \
        -e 's/\//\\\//g' \
        -e 's/\&/\\\&/g'
}

clean_up_and_exit() {
    rm -f "$tmpModuleFull"
    exit $@
}

prev_build_autogen_hash() {
    local logicFilePath="$modulePath/module/ui_logic.bsh"

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
    local prevHash=$(prev_build_autogen_hash)
    local thisHash=$(this_build_autogen_hash)

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
    # In module.xml, replace any line <!--@SOURCE: path/to/file--> with the
    # contents of the file at path/to/file.
    echo "Applying @SOURCE directives..."
    while [[ ! -z $(get_next_source) ]]
    do
        local filename=$(get_next_source)
        if [ ! -f "$filename" ]
        then
            echo "  File '$filename' not found"
        fi
        local whitespace='\s*'                           # \geq 0 whitespace
        local escaped_filename=$(escape_sed "$filename") # Escape slashes

        local tmp=$(tempfile)
        cat "$tmpModuleFull" | sed \
            -e "/<!--@SOURCE:$whitespace$escaped_filename$whitespace-->/{
            r $filename
            d
        }" >"$tmp"
        mv "$tmp" "$tmpModuleFull"
    done
    echo
}

apply_proc_directives() {
    local procUpper=$(echo "$1" | awk '{print toupper($1)}')
    local procLower=$(echo "$1" | awk '{print tolower($1)}')

    local cmd=$(
        grep '@'$procUpper'PROC:' "$tmpModuleName" | \
        head -n 1 | \
        sed -rn 's/^\s*<!--\s*@'$procUpper'PROC:\s*(.*[^ ])\s*-->\s*$/\1/p'
    )

    if [ ! -z "$cmd" ]
    then
        echo "Running ${procLower}-processing command:"
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

set_up () {
    tmpModuleFull=$( tempfile -d "$modulePath" -p '.mod-' -s '.xml')
    tmpModulePath=$( dirname  "$tmpModuleFull")
    tmpModuleName=$( basename "$tmpModuleFull")

    cp "$moduleFull" "$tmpModuleFull"
}

trap 'clean_up_and_exit 1' SIGHUP SIGINT SIGTERM
set_up
