#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
##########################
# Import all needed libs #
##########################
import json
import os
import sys
import time
from subprocess import PIPE, Popen, check_output, run

import fsc

##########################
#       Paramters        #
##########################
with open(os.path.join(os.getcwd(),"device.json"),'r', encoding="utf8") as f:
    device_dict = json.load(f)
    f.close()
FileImgDic, MPDic = {}, {}
for k in device_dict["FileSysRobot"].keys():
    FileImgDic[k] = device_dict["FileSysRobot"][k]["img"]
    MPDic[k] = device_dict["FileSysRobot"][k]["mnt"]

# others
WaDo = sys.argv[1]
Samba = sys.argv[2]
FS = sys.argv[3].upper()
dictkey = FileImgDic.keys()

# color
Cyan = '\033[1;96m'
Yellow = '\033[1;93m'
Green = '\033[1;92m'
Red = '\033[1;91m'
C_off = '\033[0m'

##########################
#       Functions        #
##########################
def getfsname(img: str):
    return img.split(".")[0]

# remount filesystem

def remount(file):
    os.system('sudo /sbin/modprobe g_multi -r')
    time.sleep(2)
    os.system(
        'sudo /sbin/modprobe g_multi file=./{} stall=0 removable=1'.format(file))

def installcheck(PKG: str):
    PKG_OK = "dpkg-query -W --showformat='${Status}\n' " + \
        "{}|grep 'install ok installed'".format(PKG)
    sys.stdout.write("Checking for {}: {}{}{}\n".format(
        PKG, Red, os.popen(PKG_OK).read().split("\n")[0], C_off))
    status = True
    if os.popen(PKG_OK).read() == "":
        status = False
        sys.stdout.write(
            "going to install {}{}{} first\n".format(Red, PKG, C_off))
        Install = 'sudo apt-get --yes install {}'.format(PKG)
        os.system(Install)
    return status

# configuration of samba conf file

def sambaconf(PKG: str, img: str, MP: str):
    conf = "/etc/samba/smb.conf"
    status = installcheck(PKG)
    if not status:
        # after installation first init the samba conf file
        os.system(
            "sudo sed -i -e '$a [raspiusb_{}]' {}".format(getfsname(img), conf))
        os.system("sudo sed -i -e '$a browseable = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a guest ok = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a creat mask = 0777' {}".format(conf))
        os.system("sudo sed -i -e '$a read only = no' {}".format(conf))
        os.system("sudo sed -i -e '$a writeable = yes' {}".format(conf))
        os.system("sudo sed -i -e '$a path = {}' {}".format(MP, conf))
    else:
        # rewrite folder path and rename remote folder
        lineNr = os.popen(
            "grep -n 'raspiusb' {} | cut -d: -f1".format(conf)).read().split("\n")[0]
        # print ("the lineNr is: {}".format(lineNr))
        os.system(
            "sudo sed -i '{}s/.*/[raspiusb_{}]/' {}".format(lineNr, getfsname(img), conf))
        os.system("sudo sed -i '/mnt/d' {}".format(conf))
        os.system("sudo sed -i -e '$a path = {}' {}".format(MP, conf))

    os.system("sudo systemctl restart smbd.service")
    sys.stdout.write("{}status of samba service-> \n".format(Cyan))
    sys.stdout.write("{}{}".format(Yellow, os.popen(
        "sudo systemctl status smbd.service | grep -E 'Loaded|Active|Status'").read()))
    sys.stdout.write("{}Network access: ".format(Cyan))
    sys.stdout.write("{}Hostname and IP: {} {}\n".format(Yellow, os.popen(
        'hostname').read().split("\n")[0], os.popen('hostname -I').read().split("\n")[0]))
    os.system('sudo chmod 777 {}'.format(MP))
    sys.stdout.write("{}file in {}: \n".format(Cyan, MP))
    for f in os.listdir(MP):
        path = os.path.join(MP, f)
        if os.path.isdir(path):
            sys.stdout.write(Yellow + "-" + f + " d" + "\n")
        elif os.path.isfile(path):
            sys.stdout.write(Yellow + "-" + f + " f" + "\n")
        else:
            sys.stdout.write(Yellow + "-" + f + " u" + "\n")

## menu
def menu():
    sys.stdout.write(Cyan + "Please select one filesystem to mount" + "\n")

def modifyfile(file:str, img:str, MP:str):
    
    # modify the watchdog file, the path unter wachting will be change mit mounted filsystem
    
    reading_file = open(file, "r")
    new_file_content = ""
    for line in reading_file:
        newline = line
        if "/home/pi/" in line:
            oldline = line
            newline = oldline.split("'/home/pi/")[0] + "'/home/pi/{}'".format(img)
            # print(oldline)
            newline = line.replace(oldline, newline) + "\n"
            # print(newline)
        elif "/mnt/" in line:
            oldline = line
            newline = oldline.split("'/mnt/")[0] + "'{}'".format(MP)
            newline = line.replace(oldline, newline) + "\n"
        
        new_file_content += newline 

    reading_file.close()

    writing_file = open(file, "w")
    writing_file.write(new_file_content)
    writing_file.close()

##########################
#     Recursive Algo     #
##########################
def USBSIM(FileImgDic, MPDic, WaDo, Samba, FS):

    def checkinput(Input):
        '''
        check if the input is valid, retrun True or False
        '''
        if (Input not in ["QUIT", "CANCEL"]) and (Input not in dictkey):
            print(Red + "Warning: " + "invalid input, retry to enter" + C_off)
            return False
        return True

    def lsblk():
        print(Cyan + "=" * 60 + Yellow)
        os.system("lsblk -f | grep 'loop'")
        print(Cyan + "=" * 60)
    
    try:
        Imgdic = FileImgDic
        MPdic = MPDic
        Input = FS.upper()
        menu()
        
        # base case: invalid input
        if not checkinput(Input):
            return
            # return USBSIM(FileImgDic, MPDic, WaDo, Samba)
        
        # base case: remount    NO USE
        
        # base case: cancel currently programm
        elif Input == "CANCEL":
            print(Cyan + "terminate the programm")
            lsblk()
            return

        # base case: quit and eject     NO USE
        elif Input == "QUIT":
            print(Cyan + "terminate the programm and eject")
            lsblk()
            os.system('sudo /sbin/modprobe g_multi -r')  # unmount first
            return

        # base case: eject current mounted USB Filesystem or refresh    NO USE

        # base case: delete filesystem img     NO USE

        # base case: USB simulator
        else:
            fsname = getfsname(Imgdic[Input])
            lcimg = Imgdic[Input].lower()
            MPpath = MPdic[Input]
            print(Cyan + "prepare to mount " + Red + fsname + Cyan + " filesystem" + C_off)
            # check if the img file is already existed or not
            if os.path.exists("./{}".format(lcimg)):
                print("{}{}{} is already existed{}".format(Red, lcimg.split(".")[0], Cyan, C_off))
                if os.path.ismount(MPpath):
                    print("{}{}{} already mounted".format(Red, MPpath, Cyan))
                else:
                    print(Cyan + "going to mount " + Red + lcimg.split(".")[0] + C_off)
                    if "fat" in lcimg: # fat: fat32 fat16 ; mib: fat32
                        os.system('sudo mount -o rw,users,sync,nofail,umask=0000 {} {}'.format(lcimg, MPpath))
                    elif "part" in lcimg: # partitions but check if it is already mounted 
                        loopdev = "lsblk -f | grep 'loop'"
                        # from all loop device looking for "p1 (loopxp1, loopxp2) if p1 not exist, partitions fs need to be mounted"
                        if "p1" not in os.popen(loopdev).read():
                            print("going to mount {}NTFS{} and {}FAT32{} partitions".format(Red, Cyan, Red, Cyan))
                            os.system("sudo losetup -fP {}".format(lcimg))
                        else:
                            print("{}NTFS{} and {}FAT32{} partitions already mounted".format(Red, Cyan, Red, Cyan))
                    else:
                        os.system('sudo mount -o rw,users,sync,nofail {} {}'.format(lcimg, MPpath))
                    # showing info about the mounted filesystem
                print(Cyan + "Information about the mounted filesystem:")
                print("="*60 + Yellow)
                if Input != "PARTITION":
                    # other filesystem
                    os.system("findmnt | grep -i {} | grep 'mnt'".format(fsname))
                    os.system("lsblk --fs -o NAME,FSTYPE,FSAVAIL,FSUSE%,MOUNTPOINT | grep -i {} | grep 'mnt'".format(fsname))
                    print(Cyan + "=" * 60)
                    print(">"*60)
                    # samba service config
                    if int(Samba) == 2:
                        sambaconf(PKG='samba', img= lcimg, MP= MPpath)
                    if int(WaDo) == 2:
                        print(Cyan + "status of watchdog service-> " + Yellow)
                        modifyfile(file="fswd.py", img = lcimg, MP= MPpath)
                        os.system("sudo systemctl restart fswd")
                        os.system("sudo systemctl status fswd | grep -E 'Loaded|Active|CGroup|python'")
                        print(Red + MPpath + Yellow + "  is unter watching, action timeout is 10s")
                    print(Cyan + "<"*60 + C_off)
                else:
                    os.system("lsblk -f | grep -E 'p1|p2' | grep 'loop'")
                    print(Cyan + "=" * 60)  

                remount(lcimg)
            else:
                print(Cyan + "+" * 60)
                fsc.Cfilesystem(lcimg, MPpath)
                # print("run fsc.py")
                print(Cyan + "+" * 60 + C_off)

            
            # return USBSIM(FileImgDic, MPDic, WaDo, Samba, FS)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

if __name__ == "__main__":
    # pass
    USBSIM(FileImgDic, MPDic, WaDo, Samba, FS)

