#!/usr/bin/python3
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
import sys
import os


Cyan='\033[1;96m'
Yellow='\033[1;93m'
Green='\033[1;92m'
Red='\033[1;91m'
C_off='\033[0m'

def Cfilesystem(img, MP):
    try:
        sys.stdout.write(Cyan +
        "going to create filesystem and partitions this is " + C_off + Red + img + Cyan
        + " the mountpoint at " + Red + MP + C_off + "\n")
        size = input(Cyan + "To create {}{}{} with size (MB): ".format(Red, img, Cyan) + C_off)
        sys.stdout.write(Cyan + "Creating......" + C_off + "\n")
        os.system("sudo dd bs=1M if=/dev/zero of={} count={}".format(img,size))

        
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
