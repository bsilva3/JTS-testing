#!/bin/bash
# $Header: /cvs/secondo/Optimizer/MemoryAllocation/nrwtest/testnrw.sh,v 1.2 2012/11/19 09:27:51 nvkempen Exp $
# @author Nikolai van Kempen
#

#old: P=http://download.geofabrik.de/osm/europe/germany/
P=http://download.geofabrik.de/openstreetmap/europe/germany/
F=nordrhein-westfalen.shp.zip
PF=$P$F

T=$SECONDO_BUILD_DIR/bin/nrw/
[ -d $T ] || mkdir $T || return 2

cd $T || return 4

if [ ! -f "$F" ]; then
	wget "$PF" || return 1
fi

unzip $F #&& rm $F

echo "Using now SecondoBDB, please make sure no secondo server proccess is running and press return."
read trash

cd $SECONDO_BUILD_DIR/bin
SecondoBDB <<<"delete database nrw2;"

# The author of this script is unkown
SCMDF=$SECONDO_BUILD_DIR/Optimizer/MemoryAllocation/nrwtest/nrwImportShape.SEC
SecondoBDB < $SCMDF

# eof
