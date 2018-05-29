#!/usr/bin/env bash

THIS_SCRIPT_PATH=$( dirname "$( readlink -e "$0" )" )

"$THIS_SCRIPT_PATH/container.sh" generate $@
