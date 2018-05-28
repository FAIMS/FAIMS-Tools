#!/usr/bin/env bash

thisScriptPath=$(dirname "$(readlink -e "$0")")

"$thisScriptPath/container.sh" validate $@
