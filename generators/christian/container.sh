#!/usr/bin/env bash

if ! which docker >/dev/null
then
    printf 'Docker could not be found. Please install Docker and/or add it to '
    printf 'your $PATH.\n'
    exit 1
fi

# Get first argument, which will be passed to `docker run`. Remaining arguments
# will either be seen by `validate.sh` or `generate.sh` (i.e. `$cmd`).
cmd="$1"
shift

THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )
source "$THIS_SCRIPT_PATH/shared.sh"

docker build -t autogen:latest "$THIS_SCRIPT_PATH"
echo -e "\n\n\n"

docker run \
    -v "$THIS_SCRIPT_PATH":"$THIS_SCRIPT_PATH" \
    -v "$MODULE_PATH":"$MODULE_PATH" \
    -v "$TMP_MODULE_PATH":"$TMP_MODULE_PATH" \
    -v "$REPO_ROOT":"$REPO_ROOT" \
    -w $(pwd) \
    autogen \
    "$THIS_SCRIPT_PATH/$cmd.sh" \
    $@
