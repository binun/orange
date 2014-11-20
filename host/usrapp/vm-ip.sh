#!/bin/sh

VMNAME=$1

MAC_ADDRESS=""
IP_ADDRESS=""

while true; do
	MAC_ADDRESS=$(virsh dumpxml $VMNAME | grep 'mac address' | awk -F'[=/>]' '{print $2}' | tr -d \'\')
	IP_ADDRESS=$(arp -n | grep $MAC_ADDRESS | awk '{print $1}')
	if [ -z "$IP_ADDRESS" ]; then
    	# echo "IP address is empty"
    	sleep 1
    else
    	break
fi
done # now IP_ADDRESS is nonempty
echo $IP_ADDRESS