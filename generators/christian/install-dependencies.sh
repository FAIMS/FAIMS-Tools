#!/bin/bash
# Tested on: 16.04.03 LTS

if [ "$EUID" -ne 0 ]
then
    echo "Please run me with root privileges. Example:"
    echo "    sudo $0"
    exit
fi

apt-get update
if [ -n "$(grep -s Ubuntu /etc/*release)" ]
then
    apt-get install software-properties-common -y
    add-apt-repository universe
    apt-get update
fi
apt-get install \
        bc \
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
