#!/bin/sh

SYSMAP_DIR=/usr/src
SYSMAP_FILE=$(find $SYSMAP_DIR -name 'System.map*' | grep $(uname -r))

echo "System map file is $SYSMAP_FILE"
insmod ivmagent.ko mapFile="$SYSMAP_FILE"