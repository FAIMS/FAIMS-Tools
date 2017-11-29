#!/bin/bash

set -euo pipefail

if [ "$EUID" -eq 0 ]
then
    echo "Please don't run me with root privileges."    
    exit
fi

