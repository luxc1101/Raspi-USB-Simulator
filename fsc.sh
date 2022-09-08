#!/bin/bash
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
Cyan='\033[1;96m'
Yellow='\033[1;93m'
Green='\033[1;92m'
Red='\033[1;91m'
Color_off='\033[0m'

echo -e "going to create filesystem and partitions this is ${Red}$lcimg${Color_off} the mountpoint at ${Red}$MP${Color_off}"
read -p "To create $lcimg with size(MB): " size
echo -e "creating..."
sudo dd bs=1M if=/dev/zero of=$lcimg count=$size

case $lcimg in
*"mib"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.fat -F 32 $lcimg;;
*"ext2"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.ext2 ext2.img
sudo tune2fs -c0 -i0 ext2.img;;
*"ext3"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.ext3 ext3.img
sudo tune2fs -c0 -i0 ext3.img;;
*"ext4"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.ext4 ext4.img
sudo tune2fs -c0 -i0 ext4.img;;
*"fat16"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.fat -F 16 fat16.img;;
*"fat32"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.fat -F 32 fat32.img;;
*"exfat"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo mkfs.exfat exfat.img;;
*"ntfs"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo apt-get install ntfs-3g
sudo losetup /dev/loop11 $lcimg
sudo mkfs.ntfs -Q /dev/loop11
sudo mount /dev/loop11 $MP;;
*"hfs"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo apt-get install hfsutils hfsprogs hfsutils
sudo mkfs.hfsplus hfsplus.img -v hfsplus;;
*"part"*)
sudo mkdir /mnt/usb_part_ntfs
sudo mkdir /mnt/usb_part_fat32
sudo losetup -fP part.img
lpd="$(losetup -a | grep "part")"
lpd="$(cut -d':' -f1 <<<"$lpd")"
echo $lpd
sudo fdisk $lpd
lpd+="p1"
sudo mkfs.ntfs -Q $lpd
sudo mount -o rw,users,sync,nofail $lpd /mnt/usb_part_ntfs
lpd=${lpd::-2}
lpd+="p2"
sudo mkfs.fat -F 32 $lpd
sudo mount -o rw,users,sync,nofail,umask=0000 $lpd /mnt/usb_part_fat32;;
*"sw"*)
sudo mkdir $MP || echo -e "$MP already exist"
sudo apt-get install ntfs-3g
sudo losetup /dev/loop12 $lcimg
sudo mkfs.ntfs -Q /dev/loop12
sudo mount /dev/loop12 $MP;;
esac