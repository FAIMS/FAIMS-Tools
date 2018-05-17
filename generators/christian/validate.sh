#!/usr/bin/env bash

thisScriptPath="$(dirname "$(readlink -e "$0")")"
source "$thisScriptPath/shared.sh"

cd "$modulePath" >/dev/null

apply_source_directives
apply_preproc_directives

cd - >/dev/null

cd "$thisScriptPath"
python2 -m validator.module "$modulePath/$moduleName"

clean_up
