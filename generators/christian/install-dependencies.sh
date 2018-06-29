#!/bin/bash
# Tested on: 16.04.03 LTS

# This script installs the programs that the autogen needs to run.

if [ "$EUID" -ne 0 ]
then
    echo "Please run me with root privileges. Example:"
    echo "    sudo $0"
    exit
fi

THIS_SCRIPT_PATH=$(dirname "$(readlink -e "$0")")
source "$THIS_SCRIPT_PATH/shared.sh" --defs-only

apt-get update
if [ "$(os_id)" = ubuntu ]
then
    apt-get install software-properties-common -y
    add-apt-repository universe
    apt-get update
fi
apt-get install \
        bc \
        bsh \
        gawk \
        git \
        graphviz \
        libsaxonb-java \
        pandoc \
        python-cairosvg \
        python-lxml \
        python-matplotlib \
        python-pysqlite2 \
        sqlite3 \
        -y
