#!/usr/bin/env bash

# This script validates the module the `module.xml` file by executing the
# Python scripts in the `validator` directory. Additionally, @PREPROC and
# @SOURCE directives are applied by this Bash script.

THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )
. "$THIS_SCRIPT_PATH/shared.sh"

cd "$MODULE_PATH" >/dev/null

apply_source_directives
apply_preproc_directives

cd "$THIS_SCRIPT_PATH"
python2 -m validator.module "$TMP_MODULE_FULL"

clean_up_and_exit $?
