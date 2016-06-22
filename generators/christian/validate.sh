#!/bin/bash

thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z $1 ]
then
    module="$(pwd)/module.xml"
else
    module="$(pwd)/$1"
fi

cd "$thisScriptPath"
python -m validator.module "$module"
