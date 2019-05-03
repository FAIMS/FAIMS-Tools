#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
	echo "./makeVectors.sh targetDir targetEPSG $#"
	exit 1
fi


rm -rf $1/vectors
mkdir $1/vectors


find $1 -name "*.shp" -type f


rm spatialite.$1.$2.db


parallel --jobs 1 --will-cite "ogr2ogr -t_srs EPSG:$2 {//}/vectors/{/.}.$2.shp {}; spatialite_tool -i -shp {//}/vectors/{/.}.$2 -d spatialite.$1.$2.db -t {/.} -g Geometry -c utf-8 -s $2; sqlite3 spatialite.$1.$2.db \"SELECT CreateSpatialIndex('{/.}', 'Geometry');\"" ::: $(find $1 -name "*.shp" -type f)


#parallel --will-cite "gdalwarp -co TILED=YES -t_srs EPSG:$2 {} {//}/maps/{/.}.$2.tif;  gdaladdo -r nearest {//}/maps/{/.}.$2.tif 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192" ::: $(find $1 -name "*.tif" -type f)

cd $1 
tar -czf ../vectors.$1.$2.tar.gz vectors/