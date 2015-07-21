#!/bin/bash
source ~/.profile

/usr/local/sbin/backup.sh $1 1970-01-01

cd /var/www/faims
rake modules:clear
for file in $2/*.bz2; do
	
	rake modules:create module="$file"
done
