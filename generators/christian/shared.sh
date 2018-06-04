parse_args() {
    # Parse arguments to this script
    MODULE="module.xml"
    while [ $# -gt 0 ]
    do
        local key="$1"

        case "$key" in
            -w|--wireframe)
            WIREFRAME=true
            ;;
            --defs-only)
            DEFS_ONLY=true
            ;;
            *)
            MODULE="$key"
            ;;
        esac

        shift
    done
}

validate_module_location() {
    if [ ! -f "$MODULE" ]
    then
        echo "Module file not found: $MODULE"
        exit 1
    fi
}

repo_root() {
    # Prints the full root directory of the autogen's git repo.
    local dir="$1"
    while [ ! -d "$dir/.git" ]
    do
        [ "$dir" = '/' ] && return
        dir=$( dirname "$( readlink -m "$dir" )" )
    done

    echo "$dir"
}

get_next_source() {
    # Prints the first @SOURCE direcive's filename
    local unstripped=$(
        grep -m 1 "(?<=<\!--@SOURCE:).+(?=-->)" "$TMP_MODULE_NAME" -RohP
    )
    printf "$unstripped" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

escape_sed() {
    # Escape sed's special characters
    echo "$1" |
    sed \
        -e 's/\//\\\//g' \
        -e 's/\&/\\\&/g'
}

clean_up_and_exit() {
    rm -f "$TMP_MODULE_FULL"
    exit $@
}

prev_build_autogen_hash() {
    # Prints the hash of the autogen which already built the module
    local logicFilePath="$MODULE_PATH/module/ui_logic.bsh"

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
    # Prints the git hash of this autogen
    cd "$THIS_SCRIPT_PATH" >/dev/null

    git log | sed \
      -e 's/.* //g' \
      -e '1q'

    cd - >/dev/null
}

check_module_compatiblity() {
    local prevHash=$( prev_build_autogen_hash )
    local thisHash=$( this_build_autogen_hash )

    if [ "$prevHash" = "" ]
    then
        printf true
        return 0
    fi

    if [ "$prevHash" = "$thisHash" ]
    then
        printf true
    else
        printf false
    fi
}

apply_source_directives() {
    # In module.xml, replace any line <!--@SOURCE: path/to/file--> with the
    # contents of the file at path/to/file.
    echo "Applying @SOURCE directives..."
    while [ ! -z $( get_next_source ) ]
    do
        local filename=$( get_next_source )
        if [ ! -f "$filename" ]
        then
            echo "  File '$filename' not found"
        fi
        local whitespace='\s*'                             # \geq 0 whitespace
        local escaped_filename=$( escape_sed "$filename" ) # Escape slashes

        local tmp=$(tempfile)
        cat "$TMP_MODULE_FULL" | sed \
            -e "/<!--@SOURCE:$whitespace$escaped_filename$whitespace-->/{
            r $filename
            d
        }" >"$tmp"
        mv "$tmp" "$TMP_MODULE_FULL"
    done
    echo
}

apply_proc_directives() {
    # Apply @POSTPROC or @PREPROC
    local procUpper=$( echo "$1" | awk '{print toupper($1)}' )
    local procLower=$( echo "$1" | awk '{print tolower($1)}' )

    local cmd=$(
        grep '@'$procUpper'PROC:' "$TMP_MODULE_NAME" | \
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

release() {
    for file in /etc/*release;
    do
        out="$(. "$file"; echo "${!1}" | tr '[A-Z]' '[a-z]')"
        if [ -n "$out" ]
        then
            echo "$out"
            break
        fi
    done
}

os_id() {
    # Prints the name of your operating system e.g. 'debian', 'ubuntu', etc
    release ID
}

os_ver() {
    # Prints your operating system's version number e.g. '16.04' if you're
    # running Ubuntu 16.04
    release VERSION_ID
}

set_up() {
    # Declare useful global variables
    THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )

    REPO_ROOT=$( repo_root "$THIS_SCRIPT_PATH")

    MODULE_FULL=$( readlink -e "$MODULE" )
    MODULE_PATH=$( dirname  "$MODULE_FULL")
    MODULE_NAME=$( basename "$MODULE_FULL")

    # Make temporary files and declare more useful global variables
    TMP_MODULE_FULL=$( tempfile -d "$MODULE_PATH" -p '.mod-' -s '.xml')
    TMP_MODULE_PATH=$( dirname  "$TMP_MODULE_FULL")
    TMP_MODULE_NAME=$( basename "$TMP_MODULE_FULL")

    cp "$MODULE_FULL" "$TMP_MODULE_FULL"

    # Check if autogen is running on an old OS
    local osId="$(  os_id )"
    local osVer="$( os_ver )"

    if { [ "$osId" = ubuntu ] && dpkg --compare-versions "$osVer" lt 16; } || \
       { [ "$osId" = debian ] && dpkg --compare-versions "$osVer" lt  8; }
    then
        OLD_OS=true
    fi
}

##################################### MAIN #####################################

trap 'clean_up_and_exit 1' HUP INT TERM

parse_args $@
if [ "$DEFS_ONLY" != true ]
then
    validate_module_location
    set_up
fi
