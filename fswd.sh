#!/bin/bash
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
##############
# parameters #
##############
Img=/home/pi/fat32.img
watchpath=/mnt/usb_fat32
act_time_out=5
while inotifywait -e modify -e create -e delete $watchpath;
do
    sleep $act_time_out
    echo -e "filesystem mcd under path $watchpath"
    # unmount
    sudo /sbin/modprobe g_multi -r
    sleep 1
	# sync
    sudo sync
    sleep 1
	# mount
    sudo /sbin/modprobe g_multi file=$Img stall=0 removable=1
    sleep 1
done
