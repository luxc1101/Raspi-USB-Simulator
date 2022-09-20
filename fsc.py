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

def Cfilesystem(img:str, MP:str):
    limg = img.lower()
    try:
        sys.stdout.write(Cyan +
        "going to create filesystem and partitions this is " + C_off + Red + limg + Cyan
        + " the mountpoint at " + Red + MP + C_off + "\n")
        size = input(Cyan + "To create {}{}{} with size (MB): ".format(Red, limg, Cyan) + C_off)
        sys.stdout.write(Cyan + "Creating......" + C_off + "\n")
        os.system("sudo dd bs=1M if=/dev/zero of={} count={}".format(limg,size))
        if "mib" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.fat -F 32 {}".format(limg))
        elif "ext2" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.ext2 {}".format(limg))
            os.system("sudo tune2fs -c0 -i0 {}".format(limg))
        elif "ext3" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.ext3 {}".format(limg))
            os.system("sudo tune2fs -c0 -i0 {}".format(limg))
        elif "ext4" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.ext4 {}".format(limg))
            os.system("sudo tune2fs -c0 -i0 {}".format(limg))
        elif "fat16" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.fat -F 16 {}".format(limg))
        elif "fat32" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.fat -F 32 {}".format(limg))
        elif "exfat" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo mkfs.exfat {}".format(limg))
        elif "ntfs" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo apt-get install ntfs-3g")
            os.system("sudo losetup /dev/loop11 {}".format(limg))
            os.system("sudo mkfs.ntfs -Q /dev/loop11")
            os.system("sudo mount /dev/loop11 {}".format(MP))
        elif "hfs" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo apt-get install hfsutils hfsprogs hfsutils")
            os.system("sudo mkfs.hfsplus {} -v hfsplus".format(limg))
        elif "part" in limg:
            if not os.path.isdir("/mnt/usb_part_ntfs"): os.system("sudo mkdir /mnt/usb_part_ntfs")
            if not os.path.isdir("/mnt/usb_part_fat32"): os.system("sudo mkdir /mnt/usb_part_fat32")
            os.system("sudo losetup -fP {}".format(limg))
            lpd = os.popen("losetup -a | grep 'part'").read().split("\n")[0].split(":")[0]
            os.system("sudo fdisk {}".format(lpd))
            lpd += "p1"
            os.system("sudo mkfs.ntfs -Q {}".format(lpd))
            os.system("sudo mount -o rw,users,sync,nofail {} /mnt/usb_part_ntfs".format(lpd))
            lpd = lpd[:-2]
            lpd += "p2"
            os.system("sudo mkfs.fat -F 32 {}".format(lpd))
            os.system("sudo mount -o rw,users,sync,nofail,umask=0000 {} /mnt/usb_part_fat32".format(lpd))
            print (Red + "Info: " + Cyan + "partitions have no remote access please add test file into each USB drive partition!" + C_off)
        elif "sw" in limg:
            if not os.path.isdir(MP): os.system("sudo mkdir {}".format(MP))
            os.system("sudo apt-get install ntfs-3g")
            os.system("sudo losetup /dev/loop12 {}".format(limg))
            os.system("sudo mkfs.ntfs -Q /dev/loop12")
            os.system("sudo mount /dev/loop12 {}".format(MP))


    except KeyboardInterrupt:
        print("KeyboardInterrupt")
