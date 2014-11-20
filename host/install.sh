#!/bin/sh

LIBFILES=$(find / -name 'libvmi*.so')
# SYSMAP_DIR=/usr/src
# SYSMAP_FILE=$(find $SYSMAP_DIR -name 'System.map*' | grep $(uname -r))

for LIB in $LIBFILES
do
	if [ -f "${LIB}" ] 
	then
   		LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(dirname $LIB)
   	fi
done
echo "Libraries will be searched in $LD_LIBRARY_PATH"
make install
