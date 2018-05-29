#!/usr/bin/env bash

THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )
. "$THIS_SCRIPT_PATH/shared.sh"

cd "$MODULE_PATH" >/dev/null

apply_source_directives
apply_preproc_directives

cd "$THIS_SCRIPT_PATH"
python2 -m validator.module "$MODULE_FULL"

clean_up_and_exit $?
