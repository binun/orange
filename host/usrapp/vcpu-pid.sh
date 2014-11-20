#!/bin/sh

VMNAME=$1
RT_DIR=/var/run/libvirt/qemu

cat $RT_DIR/$VMNAME.xml | grep 'vcpu pid=' | awk -F'[=/>]' '{print $2}' | tr -d \'\'