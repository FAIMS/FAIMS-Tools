#!/bin/sh

if [ -z $1 ]
then
    module="module.xml"
else
    module=$1
fi

python validator/module.py $module
