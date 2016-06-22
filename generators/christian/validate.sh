#!/bin/bash

if [ -z "$1" ]
then
    module="module.xml"
else
    module="$1"
fi
modulePath=$( dirname  "$module" )
moduleName=$( basename "$module" )
thisScriptPath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$thisScriptPath"
python2 -m validator.module "$modulePath/$moduleName"
