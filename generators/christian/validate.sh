#!/bin/bash

thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z $1 ]
then
    module="module.xml"
else
    module=$1
fi

python "$thisScriptPath/validator/module.py" $module
