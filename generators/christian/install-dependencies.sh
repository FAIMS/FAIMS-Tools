#!/bin/bash
# Tested on: 16.04.03 LTS

if [ "$EUID" -ne 0 ]
then
    echo "Please run me with root privileges. Example:"
    echo "    sudo $0"
    exit
fi

if [ -n "$(grep -s Ubuntu /etc/*release)" ]
then
    add-apt-repository universe
fi
apt-get update
apt-get install \
        bsh \
        default-jre \
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
