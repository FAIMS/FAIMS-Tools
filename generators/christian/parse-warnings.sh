#!/bin/sh

find module -type f -print | xargs grep -nr --color="always" "WARNING" | sed -e 's/\s\+</ </g'
