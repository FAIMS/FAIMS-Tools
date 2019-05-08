#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
	echo "./makeRasters.sh targetDir targetEPSG (3857 if importing to FAIMS)"
	exit 1
fi

find $1 -name "*.tif" -type f

rm -rf $1/maps
mkdir $1/maps

parallel --will-cite "gdalwarp -co compress=jpeg -wo OPTIMIZE_SIZE=YES -co TILED=YES -t_srs EPSG:$2 {} {//}/maps/{/.}.$2.tif;  gdaladdo -r nearest {//}/maps/{/.}.$2.tif 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192" ::: $(find $1 -name "*.tif" -type f)

cd $1 
tar -czf data-maps.$1.$2.tar.gz maps/