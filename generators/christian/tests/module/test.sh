#!/usr/bin/env bash
shopt -s globstar

# cd into this script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Add .jar files to `CLASSPATH`
for path in **/*.jar; do
    [[ ":$CLASSPATH:" != *":$path:"* ]] && CLASSPATH="$path:${CLASSPATH}"
done
export CLASSPATH

bsh test.bsh
