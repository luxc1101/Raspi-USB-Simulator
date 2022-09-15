#!/usr/bin/python3
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
##########################
# Import all needed libs #
##########################
import sys
import os
import time
import fsc
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
    return img.split(".")[0]

### remount filesystem
def remount(file):
    os.system('sudo /sbin/modprobe g_multi -r')
    time.sleep(2)
    os.system('sudo /sbin/modprobe g_multi file=./{} stall=0 removable=1'.format(file))

#### check if a package installed or not and try to install it
def installcheck(PKG):
    PKG_OK = "dpkg-query -W --showformat='${Status}\n' " + "{}|grep 'install ok installed'".format(PKG)
    sys.stdout.write("Checking for {}: {}{}{}\n".format(PKG, Red, os.popen(PKG_OK).read().split("\n")[0],C_off))
    status = True
    if os.popen(PKG_OK).read() == "":
        status = False
        sys.stdout.write("going to install {}{}{} first\n".format(Red, PKG, C_off))
        Install = 'sudo apt-get --yes install {}'.format(PKG)
        os.system(Install)
    return status

### configuration of samba conf file       
def sambaconf(PKG, img, MP):
    conf = "/etc/samba/smb.conf"
    status = installcheck(PKG)
    if not status:
        # after installation first init the samba conf file
        os.system("sudo sed -i -e '$a [raspiusb_{}]' {}".format(getfsname(img),conf))
        os.system("sudo sed -i -e '$a browseable = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a guest ok = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a creat mask = 0777' {}".format(conf))
        os.system("sudo sed -i -e '$a read only = no' {}".format(conf))
        os.system("sudo sed -i -e '$a writeable = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a path = {}' {}".format(MP,conf))
    else:
        # rewrite folder path and rename remote folder 
        lineNr = os.popen("grep -n 'raspiusb' {} | cut -d: -f1".format(conf)).read().split("\n")[0]
        # print ("the lineNr is: {}".format(lineNr))
        os.system("sudo sed -i '{}s/.*/[raspiusb_{}]/' {}".format(lineNr,getfsname(img), conf))
        os.system("sudo sed -i '/mnt/d' {}".format(conf))
        os.system("sudo sed -i -e '$a path = {}' {}".format(MP,conf))
    
    os.system("sudo systemctl restart smbd.service")
    sys.stdout.write("{}status of samba service: \n".format(Cyan))
    sys.stdout.write("{}{}".format(Yellow,os.popen("sudo systemctl status smbd.service | grep -E 'Loaded|Active|Status'").read()))
    sys.stdout.write("{}Network access: ".format(Cyan))
    sys.stdout.write("{}Hostname and IP: {} {}\n".format(Yellow, os.popen('hostname').read().split("\n")[0], os.popen('hostname -I').read().split("\n")[0]))
    os.system('sudo chmod 777 {}'.format(MP))
    sys.stdout.write("{}file in {}: \n".format(Cyan, MP))
    for f in os.listdir(MP):
        path = os.path.join(MP,f)
        if os.path.isdir(path):
            sys.stdout.write(Yellow + "-" + f + " d" + "\n")
        elif os.path.isfile(path):
            sys.stdout.write(Yellow + "-" + f + " f" + "\n")
        else:
            sys.stdout.write(Yellow + "-" + f + " u" + "\n")

def menu():
    sys.stdout.write(Cyan + "Please select one filesystem to mount" + "\n")
    sys.stdout.write(Yellow + "0: MIB Compliance Media" + "\n")
    sys.stdout.write("1: ext2" + "\n")
    sys.stdout.write("2: ext3" + "\n")
    sys.stdout.write("3: ext4" + "\n")
    sys.stdout.write("4: fat16" + "\n")
    sys.stdout.write("5: fat32" + "\n")
    sys.stdout.write("6: ntfs" + "\n")
    sys.stdout.write("7: exfat" + "\n")
    sys.stdout.write("8: hfsplus" + "\n")
    sys.stdout.write("9: partitions" + "\n")
    sys.stdout.write("10: Software update" + "\n")
    sys.stdout.write(Green + "r: remount" + "\n")
    sys.stdout.write("q: quit and eject the usb" + "\n")
    sys.stdout.write("c: cancel or terminate the currently running program" + C_off + "\n")


fsc.Cfilesystem("fat32.img", "/mnt/usb_fat32")














