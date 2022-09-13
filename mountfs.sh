#!/bin/bash
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
### parameter
declare -A FileImgArr
declare -A MPArr

FileImgArr[0]=mib_compliance.img # fat32 
FileImgArr[1]=ext2.img
FileImgArr[2]=ext3.img
FileImgArr[3]=ext4.img
FileImgArr[4]=fat16.img
FileImgArr[5]=fat32.img
FileImgArr[6]=ntfs.img
FileImgArr[7]=exfat.img
FileImgArr[8]=hfsplus.img
FileImgArr[9]=part.img
FileImgArr[10]=sw.img # ntfs

MPArr[0]=/mnt/usb_MIB_Compliance
MPArr[1]=/mnt/usb_ext2
MPArr[2]=/mnt/usb_ext3
MPArr[3]=/mnt/usb_ext4
MPArr[4]=/mnt/usb_fat16
MPArr[5]=/mnt/usb_fat32
MPArr[6]=/mnt/usb_ntfs
MPArr[7]=/mnt/usb_exFat
MPArr[8]=/mnt/usb_hfsplus
MPArr[9]=/mnt/usb_part_fat32
MPArr[10]=/mnt/usb_sw
menuArr=("q c r")

let arrlen=${#FileImgArr[@]}-1
# echo "$arrlen"
# color
Cyan='\033[1;96m'
Yellow='\033[1;93m'
Green='\033[1;92m'
Red='\033[1;91m'
Color_off='\033[0m'

### function definition
function getfilesysname()
{
 A="$(cut -d'.' -f1 <<<"$1")"
 A="${A,,}" # lowercase
 # echo "going to mount $A file system"
}

function menu()
{
sh ./logo.sh sh || echo -e "${Red}WITHOUT logo.sh${Color_off}"
echo -e "${Cyan}Please select one filesystem to mount"
echo -e "${Yellow}0: MIB Compliance Media"
echo -e "1: ext2"
echo -e "2: ext3"
echo -e "3: ext4"
echo -e "4: fat16"
echo -e "5: fat32"
echo -e "6: ntfs"
echo -e "7: exfat"
echo -e "8: hfsplus"
echo -e "9: partitions"
echo -e "10: Software update"
echo -e "${Green}r: remount"
echo -e "q: quit and eject the usb"
echo -e "c: cancel or temrinate the currently running program${Color_off}"
}

function repeat()
{
for i in {1..60}; do echo -n "$1"; done
echo " "
}

function remount()
{
sudo /sbin/modprobe g_multi -r # unmount first
/bin/sleep 2 # sleep 2 s
sudo /sbin/modprobe g_multi file=$1 stall=0 removable=1 # mount again
}

function Samba_Install()
{
REQUIRED_PKG=$1
MP=$2
file=/etc/samba/smb.conf
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo -e "Checking for $REQUIRED_PKG: ${Cyan}$PKG_OK${Color_off}"
if [ "" = "$PKG_OK" ];
then
    echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
    sudo apt-get --yes install $REQUIRED_PKG
    sudo sed -i -e '$a [raspiusb_"$A"]' $file
    sudo sed -i -e '$a browseable = yes' $file
    sudo sed -i -e '$a guest ok = yes' $file
    sudo sed -i -e '$a creat mask = 0777' $file

    sudo sed -i -e '$a writeable = yes' $file
    sudo sed -i -e '$a path = '"$MP"'' $file
else
    lineNr=$(grep -n "raspiusb" /etc/samba/smb.conf | cut -d: -f1)
    sudo sedcd / -i "${lineNr}s/.*/[raspiusb_"$A"]/" /etc/samba/smb.conf
    sudo sed -i '/mnt/d' $file
    sudo sed -i -e '$a path = '"$MP"'' $file

sudo systemctl restart smbd.service
echo -e "${Cyan}status of smbd service:${Yellow}"
sudo systemctl status smbd.service | grep -E "Loaded|Active|Status"
echo -e "${Cyan}Network access:"
echo -e "Hostname and IP:${Yellow}"
hostname && hostname -I
sudo chmod 777 $MP # set read write executable permission to somefile for all user groups
echo -e "${Cyan}files in MP:"
for eachfile in $MP/*
do
    echo -e "${Yellow} - $(basename "$eachfile")${Color_off}"
done
fi
}

### user guide menu:
menu
### unmount or mount file system
while :;
do
read -p "Enter a value: " value
## basic case 1: quit and eject
if [ "$value" == "q" ];
then
    echo "Quit and Eject"
    sudo /sbin/modprobe g_multi -r # unmount first
    repeat "="
    lsblk -f | grep "loop"
    repeat "="
    exit
fi
## basic case 2: cancel currently  program
if [ "$value" == "c" ];
then
    echo "terminate the program"
    repeat "="
    lsblk -f | grep "loop"
    repeat "="
    exit
fi
## basic case 4: check if input is valid
if [[ "$value" -gt "$arrlen" ]] && [[ ! ${menuArr[*]} =~ "$value" ]];
then
    echo "invalid input, retry to enter"
else
    if [ "$value" == "r" ];
    then
        echo -e "list the already mounted filesystems"
        repeat "="
        lsblk -f | grep "loop"
        repeat "="
        read -p "which FS will be remounted: " value
        echo -e "remount ${Red}${FileImgArr[$value]}${Color_off} filesystem"
        remount "${FileImgArr[$value]}"
    else
    # if the input is number
    for idx in "${!FileImgArr[@]}";
    do
        # if value == idx
        if [ "$value" == "$idx" ];
        then
            getfilesysname "${FileImgArr[$idx]}"
            lcimg="${FileImgArr[$idx],,}" # to lowercase
            MP="${MPArr[$idx]}"
            echo "prepare to mount $A file system"
            # check if the img file and mountpoint exist
            if [ -f $lcimg ] && [ -d $MP ];
            then
                echo -e "${Red}$lcimg${Color_off} and ${Red}$MP${Color_off} exist \n";
                # check if mp already be mounted
                if mountpoint -q $MP;
                then
                    echo -e "${Red}$MP${Color_off} already mounted"
                else
                    if [ "$value" != "9" ];then echo -e "going to mount ${Red}$lcimg${Color_off} at MP ${Red}$MP${Color_off}";fi
                    case $lcimg in # to lowercase
                         *"ext"*)
                         # ext filesystem without umask op
                         sudo mount -o rw,users,sync,nofail $lcimg $MP;;
                         *"fat"*)
                         # fat filesystem with umask op let it rw able
                         sudo mount -o rw,users,sync,nofail,umask=0000 $lcimg $MP;;
                         *"mib"*)
                         # mib compliance media (fat32)
                         sudo mount -o rw,users,sync,nofail,umask=0000 $lcimg $MP;;
                         *"part"*)
                         # partitions but check if alreay partitions is mounted
                         loopdev=$(lsblk -f | grep "loop")
                         # from all loop device looking for "p1" (loopxp1, loopxp2)if p1 not exist, paritions fs need to be mounted
                         if [[ ! $loopdev =~ "p1" ]];then echo -e "going to mount ${Red}NTFS${Color_off} and ${Red}FAT32${Color_off} partitions"; sudo losetup -fP $lcimg;
                         else echo -e "${Red}NTFS${Color_off} and ${Red}FAT32${Color_off} partitions already mounted";fi;;
                         *)
                         # other cases
                         sudo mount -o rw,users,sync,nofail $lcimg $MP;;
                    esac
                fi
                # showing info about the mounted filesystem
                echo -e "infomation about the mounted filesystem:"
                repeat '='
                if [ "$value" != "9" ]; then
                    # other filesystem
                    echo "TARGET(MP)        SOURCE      FSTYPE          OPTIONS"
                    findmnt | grep -i $A | grep "mnt"
                    echo "NAME        FSTYPE    FSAVAIL    FSUES%    MOUNTPOINT"
                    lsblk --fs -o NAME,FSTYPE,FSAVAIL,FSUSE%,MOUNTPOINT | grep -i $A | grep "mnt"
                    # remote file access which enable network access to the /mnt/usb_share folder
                    # check if package samba installed and edit smb.conf
                    repeat '='
					repeat '>'
                    Samba_Install "samba" $MP
					# reset watchdog filesystem and aktive watchdog service
                    echo -e "${Cyan}watchdog service status:${Yellow}"
					### python watchdog
                    #sudo sed -i -e "s|^Img.*|Img = '/home/pi/"${lcimg}"'|g" /home/pi/fswd.py
                    #sudo sed -i -e "s|^watch_path.*|watch_path = '"${MP}"'|g" /home/pi/fswd.py
                    #sudo systemctl restart fswd
                    #sudo systemctl status fswd | grep -E "Loaded|Active|CGroup|python"
                    ### bash watchdog
                    sudo sed -i -e "s|^Img.*|Img=/home/pi/${lcimg}|g" /home/pi/fswd.sh
                    sudo sed -i -e "s|^watchpath.*|watchpath=${MP}|g" /home/pi/fswd.sh
                    sudo systemctl restart fswd2
                    sudo systemctl status fswd2 | grep -E "Loaded|Active|CGroup|inotify"
                    echo -e "${Color_off}"
					repeat '<'
                else
                    # partions
                    echo "NAME        FSTYPE    FSAVAIL    FSUES%    MOUNTPOINT"
                    lsblk -f | grep -E "p1|p2" | grep "loop"
                    repeat '='
                fi
                # add or remove modules
                remount $lcimg
            else
                repeat "+"
                export lcimg MP
                bash ./fsc.sh || echo -e "missing the ${Red}fsc.sh${Color_off} in current path" 
                repeat "+"
            fi
            # break
        fi
    done
    fi
fi
# loop to main menu
menu
done