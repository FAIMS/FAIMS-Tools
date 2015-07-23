#!/bin/bash

set -e
source ~/.profile


if [ ! -z "$1" ]; then
	targetPath="$1"
else
	targetPath="."	
fi

BACKUPDIR=$targetPath

if [ ! -d "$BACKUPDIR" ]; then
	echo "Backup directory doesn't exist"
	exit 1
fi	

if [ ! -w "$BACKUPDIR" ]; then
	echo "Directory not writeable"
	exit 1
fi	

cd /var/www/faims
rake modules:archive



for oldBak in $(find $targetPath -name "*.tar.bz2")
do
	moduleName=$(echo "$oldBak" | gawk 'match($0, /-[A-Za-z]{3,3}-(.*.tar.bz2$)/, a) {print a[1]}')
	find $1 -name "*$moduleName" | sort -gr | tail --lines=+2 | xargs rm -f
done	

for tarball in $(find /var/www/faims/modules -name "*.tar.bz2")
do
	if [ -z "$2" ] || [ "$2" == "--" ]; then
		maxDate=$(tar -jtvf $tarball | awk '\
	BEGIN {FS=" "; \
		   maxDate="1970-01-01"; } \
	/[0-9-]{10,10}/	{if ($4 > maxDate) {maxDate = $4} } \
	END {print maxDate} \
	')
	else
		maxDate=$2
	fi
	

	tarballName=$(echo $tarball | awk '\
	              BEGIN {FS="/"} \
	              {print $8}' )

	tarFullName=$(date --date="$maxDate" "+FAIMS2ModuleBackup-%Y%m%d-D%j-%a-$tarballName")
	
	echo "rsync -az $tarball $targetPath/$tarFullName" | bash

	if [ ! -z "$3" ]; then
		echo "scp -q $tarball $3/$tarFullName" | bash
	fi

	echo "Backed up $tarballName from $maxDate."	

done	