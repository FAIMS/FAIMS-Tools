#!/usr/bin/env bash

thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$thisScriptPath/shared.sh"

check_last_run_ended_cleanly

cd "$modulePath" >/dev/null

apply_source_directives
apply_preproc_directives

cd - >/dev/null

cd "$thisScriptPath"
python2 -m validator.module "$modulePath/$moduleName"

clean_up
