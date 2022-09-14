#!/usr/bin/python3
#*****************************************************
# Project:   Raspberrypi Zero usb filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
##########################
# Import all needed libs #
##########################
import sys
import os
import time
##########################
#       Paramters        #
##########################
# img file dict
FileImgDic={}
FileImgDic[0]="mib_compliance.img" # fat32
FileImgDic[1]="ext2.img"
FileImgDic[2]="ext3.img"
FileImgDic[3]="ext4.img"
FileImgDic[4]="fat16.img"
FileImgDic[5]="fat32.img"
FileImgDic[6]="ntfs.img"
FileImgDic[7]="exfat.img"
FileImgDic[8]="hfsplus.img"
FileImgDic[9]="part.img"
FileImgDic[10]="sw.img" # ntfs
# mount point dict
MPDic={}
MPDic[0]="/mnt/usb_MIB_Compliance"
MPDic[1]="/mnt/usb_ext2"
MPDic[2]="/mnt/usb_ext3"
MPDic[3]="/mnt/usb_ext4"
MPDic[4]="/mnt/usb_fat16"
MPDic[5]="/mnt/usb_fat32"
MPDic[6]="/mnt/usb_ntfs"
MPDic[7]="/mnt/usb_exfat"
MPDic[8]="/mnt/usb_hfsplus"
MPDic[9]="/mnt/usb_part_fat32"
MPDic[10]="/mnt/usb_sw"

diclen = len(FileImgDic)
#color
# sys.stdout.write("{}hallo".format(Cyan))
Cyan='\033[1;96m'
Yellow='\033[1;93m'
Green='\033[1;92m'
Red='\033[1;91m'
C_off='\033[0m'

##########################
#       Functions        #
##########################
def getfsname(img):
    return img.split(".")[-1]

def remount(file):
    os.system('sudo /sbin/modprobe g_multi -r')
    time.sleep(2)
    os.system('sudo /sbin/modprobe g_multi file=./{} stall=0 removable=1'.format(file))

def installcheck(PKG):
    PKG_OK = "dpkg-query -W --showformat='${Status}\n' " + "{}|grep 'install ok installed'".format(PKG)
    sys.stdout.write("Checking for {}: {}{}{}".format(PKG, Cyan, os.popen(PKG_OK).read(),C_off))



