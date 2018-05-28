#!/usr/bin/env bash

if ! which docker >/dev/null
then
    printf 'Docker could not be found. Please install Docker and/or add it to '
    printf 'your $PATH.\n'
    exit
fi

# Get first argument, which will be passed to `docker run`. Remaining arguments
# will either be seen by `validate.sh` or `generate.sh` (i.e. `$cmd`).
cmd="$1"
shift

# `shared.sh` defines some variables. It also consumes arguments, so we save
# them in `args`.
thisScriptPath=$(dirname "$(readlink -e "$0")")
args=$@
source "$thisScriptPath/shared.sh"

docker build -t autogen:latest "$thisScriptPath"
echo -e "\n\n\n"

docker run \
    -v "$thisScriptPath":"$thisScriptPath" \
    -v "$modulePath":"$modulePath" \
    -v "$tmpModulePath":"$tmpModulePath" \
    -v "$repoRoot":"$repoRoot" \
    -w $(pwd) \
    autogen \
    "$thisScriptPath/$cmd.sh" \
    $args
