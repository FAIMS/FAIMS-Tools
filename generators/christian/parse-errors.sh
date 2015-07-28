#!/bin/sh

find module -type f -print | xargs grep -nr --color="always" "ERROR" | sed -e 's/\s\+/ /g'
