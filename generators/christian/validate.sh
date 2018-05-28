#!/usr/bin/env bash

thisScriptPath=$(dirname "$(readlink -e "$0")")
. "$thisScriptPath/shared.sh"

cd "$modulePath" >/dev/null

apply_source_directives
apply_preproc_directives

cd "$thisScriptPath"
python2 -m validator.module "$moduleFull"

clean_up_and_exit $?
