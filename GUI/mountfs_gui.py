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
# # img file dict
# FileImgDic = {}
# FileImgDic[0] = "mib_compliance.img"  # ntfs
# FileImgDic[1] = "ext2.img"
# FileImgDic[2] = "ext3.img"
# FileImgDic[3] = "ext4.img"
# FileImgDic[4] = "fat16.img"
# FileImgDic[5] = "fat32.img"
# FileImgDic[6] = "ntfs.img"
# FileImgDic[7] = "exfat.img"
# FileImgDic[8] = "hfsplus.img"
# FileImgDic[9] = "part.img"
# FileImgDic[10] = "sw.img"  # ntfs
# # mount point dict
# MPDic = {}
# MPDic[0] = "/mnt/usb_mib_compliance"
# MPDic[1] = "/mnt/usb_ext2"
# MPDic[2] = "/mnt/usb_ext3"
# MPDic[3] = "/mnt/usb_ext4"
# MPDic[4] = "/mnt/usb_fat16"
# MPDic[5] = "/mnt/usb_fat32"
# MPDic[6] = "/mnt/usb_ntfs"
# MPDic[7] = "/mnt/usb_exfat"
# MPDic[8] = "/mnt/usb_hfsplus"
# MPDic[9] = "/mnt/usb_part_fat32"
# MPDic[10] = "/mnt/usb_sw"

with open(os.path.join(os.getcwd(),"device.json"),'r', encoding="utf8") as f:
    device_dict = json.load(f)
    f.close()
FileImgDic, MPDic = {}, {}
for i in range(len(device_dict["FileSys"])):
    FileImgDic[i] = device_dict["FileSys"][str(i)]["img"]
    MPDic[i] = device_dict["FileSys"][str(i)]["mnt"]

# others
# WaDo = sys.argv[0]
# Samba = sys.argv[1]
WaDo = sys.argv[1]
Samba = sys.argv[2]
# tab = sys.argv[3]
diclen = len(FileImgDic)

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
    sys.stdout.write("11: device simultion" + "\n")
    sys.stdout.write(Green + "r: remount" + "\n")
    sys.stdout.write("q: quit and eject the USB" + "\n")
    sys.stdout.write("e: eject current USB drive" + "\n")
    sys.stdout.write(
        "c: cancel or terminate the currently running program" + "\n")
    sys.stdout.write("d: delete filesystem image"+ C_off + "\n")

def modifyfile(file:str, img:str, MP:str):
    '''
    modify the watchdog file, the path unter wachting will be change mit mounted filsystem
    '''
    reading_file = open(file, "r")
    new_file_content = ""
    for line in reading_file:
        newline = line
        if "/home/pi/" in line:
            oldline = line
            # newline = oldline.split("'/home/pi/")[0] + "'/home/pi/{}'".format(img)
            newline = oldline.split("/home/pi/")[0] + "/home/pi/{}".format(img)
            # print(oldline)
            newline = line.replace(oldline, newline) + "\n"
            # print(newline)
        elif "/mnt/" in line:
            oldline = line
            # newline = oldline.split("'/mnt/")[0] + "'{}'".format(MP)
            newline = oldline.split("/mnt/")[0] + "{}".format(MP)
            newline = line.replace(oldline, newline) + "\n"
        
        new_file_content += newline 

    reading_file.close()

    writing_file = open(file, "w")
    writing_file.write(new_file_content)
    writing_file.close()

def reqcheck():
    '''
    Requirements
    ConfigFs must be avaiable, if it not avaiable it needs to be mounted firstly
    modules and device tree also
    '''
    cmdfindmnt = "findmnt | grep 'configfs'"
    status = True
    mount_OK = Popen(cmdfindmnt, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
    if 'configfs' not in mount_OK:
        status = False
        sys.stdout.write("Checking mount status of configfs: {} \n".format(status))
        Popen('sudo mount -t configfs none /sys/kernel/config',shell=True, stdout=None, stderr=None)
        return reqcheck()
    sys.stdout.write("Checking mount status of configfs: {} \n".format(status))

    devicetree = Popen("cat /boot/config.txt", shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
    if 'dwc2' not in devicetree:
        status = False
        sys.stdout.write("Checking devicetree: {} \n".format(status))
        Popen('echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt', shell=True, stdout=PIPE, stderr=PIPE)
        return reqcheck()
    sys.stdout.write("Checking devicetree: {} \n".format('dtoverlay=dwc2'))
    modules = Popen("cat /etc/modules", shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
    if 'libcomposite' not in modules:
        status = False
        sys.stdout.write("Checking modules: {} \n".format(status))
        sys.stdout.write("loading libcomposite modules \n")
        Popen('modprobe libcomposite', shell=True, stdout=PIPE, stderr=PIPE)
        Popen('echo "libcomposite" | sudo tee -a /etc/modules',shell=True, stdout=PIPE, stderr=PIPE)
        return reqcheck()
    if 'dwc2' not in modules:
        status = False
        sys.stdout.write("Checking modules: {} \n".format(status))
        Popen('echo "dwc2" | sudo tee -a /etc/modules', shell=True, stdout=PIPE, stderr=PIPE)
        return reqcheck()
    sys.stdout.write("Checking modules: {} {} \n".format('libcomposite', 'dwc2'))


##########################
#     Recursive Algo     #
##########################
def USBSIM(FileImgDic, MPDic, WaDo, Samba):

    def checkinput(Input):
        if (Input.lower() not in ["r", "q", "c", "e", "d"]) and (Input not in [str(i) for i in range(diclen+1)]):
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

        menu()
        Input = input(Cyan + "Enter a value: " + C_off)
        
        # base case: invalid input
        if not checkinput(Input):
            return USBSIM(FileImgDic, MPDic, WaDo, Samba)
        
        # base case: remount
        elif Input.lower() == "r":
            print(Cyan + "list the already remounted filesytems")
            lsblk()
            Input = input(
                Cyan + "which filesystem will be remounted: " + C_off)
            if checkinput(Input):
                print(Cyan + "remount " + Red +
                        Imgdic[int(Input)] + Cyan + " filesystem")
                remount(Imgdic[int(Input)])
                # check if samba and watchdog service active or not, active return '0' deactive return '2' 
                if int(Samba) == 2:
                    sambaconf(PKG='samba', img= Imgdic[int(Input)].lower(), MP= MPdic[int(Input)])
                if int(WaDo) == 2:
                    modifyfile(file="fswd.sh", img = Imgdic[int(Input)].lower(), MP= MPdic[int(Input)])
                    os.system("sudo systemctl restart fswd")
                return USBSIM(FileImgDic, MPDic, WaDo, Samba)
        
        # base case: cancel currently programm
        elif Input.lower() == "c":
            print(Cyan + "terminate the programm")
            lsblk()
            return

        # base case: quit and eject
        elif Input.lower() == "q":
            print(Cyan + "terminate the programm and eject")
            lsblk()
            os.system('sudo /sbin/modprobe g_multi -r')  # unmount first
            return

        # base case: eject current mounted USB Filesystem or refresh
        elif Input.lower() == "e":
            print(Cyan + "eject current USB drive and refresh")
            os.system('sudo /sbin/modprobe g_multi -r')  # unmount first
            os.system('udcname=""')
            os.system('sudo bash -c "echo $udcname > /sys/kernel/config/usb_gadget/g1/UDC"')
            return USBSIM(FileImgDic, MPDic, WaDo, Samba)

        # base case: delete filesystem img
        elif Input.lower() == "d":
            dInput = input(Cyan + "which filesystem will be deleted: " + C_off)
            try:
                os.system("sudo rm {}.img".format(dInput))
                lpd = os.popen("lsblk -f | grep '/mnt/usb_{}'".format(dInput)).read().split("\n")[0].split(" ")[0]
                os.system("sudo umount /dev/{}".format(lpd))
                os.system("sudo rm -r /mnt/usb_{}".format(dInput))
                print("delete {}.img -> umount {} -> remove /mnt/usb_{}".format(dInput, lpd, dInput))
            except FileExistsError as e:
                print(Red + e + C_off)
            return USBSIM(FileImgDic, MPDic, WaDo, Samba)
        elif Input == "11":
            # print("going to simulate device: xxx")
            Input_dev = input(Cyan + "emulated device: " + Yellow)
            reqcheck()
            VID             = Input_dev.split(' ')[-2]
            PID             = Input_dev.split(' ')[-1]
            root            = "/sys/kernel/config/usb_gadget"
            udcname         = ''
            bcdDevice       = "0x0100"                          # Device release number v1.0.0
            bcdUSB          = "0x0200"                          # Initialize this descriptor to the usb version that the device supportes (accceptatble version are 0x0110 0x0200 0x0300 0x0310)
            bDeviceClass    = "0xEF"                            # The class code indicating the behavior of this device. 
            bDeviceSubClass = "0x02"                            # The subclass code that further defines the behavior of this device.
            bDeviceProtocol = "0x01"                            # The protocol that the device supports.
            serialnumber    = "swtemedia9876543210"             # Device serial number
            manufacturer    = "SWTEMedia"                       # Manufacturer attribute
            product         = "SWTE Emulated multi USB Device"  # Cleartext product description
            configuration   = "Config 1"                        # Name of this configuration
            MaxPower        = "250"                             # max power this configuration can consume in mA
            bmAttributes    = "0x80"                            # Configuration characteristics (D7: Reserved (set to one), D6: Self-powered, D5: Remote Wakeup, D4...0: Reserved (reset to zero)) 
            HOST            = "00:dc:c8:f7:75:14"               # HOST PC
            SELF            = "00:dd:dc:eb:6d:a1"               # BadUSB
            print("VID: {} PID: {}".format(VID, PID))
            ### create the gadgets
            print("make dir g1")
            os.system("sudo mkdir -p {}/g1".format(root))                                       # create directory for gadget
            print("PID VID")
            os.system("sudo bash -c 'echo {} > {}/g1/idVendor'".format(VID, root))              # create vendor id
            os.system("sudo bash -c 'echo {} > {}/g1/idProduct'".format(PID, root))             # create product id
            print("bcd abd bDev")
            os.system("sudo bash -c 'echo {} > {}/g1/bcdUSB'".format(bcdUSB, root))
            os.system("sudo bash -c 'echo {} > {}/g1/bcdDevice'".format(bcdDevice, root))       # create device release number
            os.system("sudo bash -c 'echo {} > {}/g1/bDeviceClass'".format(bDeviceClass, root)) # create classification
            os.system("sudo bash -c 'echo {} > {}/g1/bDeviceSubClass'".format(bDeviceSubClass, root)) # create sub classification 
            os.system("sudo bash -c 'echo {} > {}/g1/bDeviceProtocol'".format(bDeviceProtocol, root))
            print("make dir strings/0x409")
            os.system("sudo mkdir -p {}/g1/strings/0x409".format(root)) # setup standard device attribute strings LANGID 0x409 US-Eng
            os.system("sudo bash -c 'echo {} > {}/g1/strings/0x409/serialnumber'".format(serialnumber, root))
            os.system("sudo bash -c 'echo {} > {}/g1/strings/0x409/manufacturer'".format(manufacturer, root))
            os.system("sudo bash -c 'echo {} > {}/g1/strings/0x409/product'".format(product, root))
            print("make dir configs/c.1/strings/0x409")
            ### create the configuration
            os.system("sudo mkdir -p {}/g1/configs/c.1/strings/0x409".format(root))                                                  # configuration directory
            os.system("sudo bash -c 'echo {} > {}/g1/configs/c.1/strings/0x409/configuration'".format(configuration, root))   # name of this configuration
            os.system("sudo bash -c 'echo {} > {}/g1/configs/c.1/MaxPower'".format(MaxPower, root))                           # some attrubutes setting for configuration, e.g. max power in mA
            os.system("sudo bash -c 'echo {} > {}/g1/configs/c.1/bmAttributes'".format(bmAttributes, root))                   # configuration characteristics

            ### create the function
            ## ethernet adapter ECMls 
            print("make dir /functions/ecm.usb0")
            os.system("sudo mkdir -p {}/g1/functions/ecm.usb0".format(root)) # add a function e.g. ecm (ethernet control model)
            os.system("sudo bash -c 'echo {} > {}/g1/functions/ecm.usb0/host_addr'".format(HOST, root))
            os.system("sudo bash -c 'echo {} > {}/g1/functions/ecm.usb0/dev_addr'".format(SELF, root))

            ## human interface device HID

            ### associatong the function with configuration
            print("ln")
            os.system("sudo ln -s {}/g1/functions/ecm.usb0 {}/g1/configs/c.1".format(root, root)) # put the function into the configuration by creating a symlink

            ### enable the gadget
            print("enable the gadget")
            print(os.popen("udcname='$(ls /sys/class/udc)'").read().split("\n")[0])
            os.system("sudo bash -c 'echo {} > {}/g1/UDC'".format(os.popen("udcname='$(ls /sys/class/udc)'").read().split("\n")[0], root))

            USBSIM(FileImgDic, MPDic, WaDo, Samba)


        # base case: USB simulator
        else:
            fsname = getfsname(Imgdic[int(Input)])
            lcimg = Imgdic[int(Input)].lower()
            MPpath = MPdic[int(Input)]
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
                if int(Input) != 9:
                    # other filesystem
                    os.system("findmnt | grep -i {} | while read MP SOURCE FS OP; do echo MountPoint:$MP Source:$SOURCE FStype:$FS Option:$OP; done".format(MPpath))
                    os.system("lsblk --fs -o NAME,FSTYPE,FSAVAIL,FSUSE%,MOUNTPOINT | grep -i {} | while read NAME FS FSAVAIL FSUSE MP; do echo Name:$NAME FStype:$FS FSavaiable:$FSAVAIL FSused:$FSUSE MountPoint:$MP; done".format(MPpath))
                    print(Cyan + "=" * 60)
                    print(">"*60)
                    # samba service config
                    if int(Samba) == 2:
                        sambaconf(PKG='samba', img= lcimg, MP= MPpath)
                    if int(WaDo) == 2:
                        print(Cyan + "status of watchdog service-> " + Yellow)
                        modifyfile(file="fswd.sh", img = lcimg, MP= MPpath)
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

            
            return USBSIM(FileImgDic, MPDic, WaDo, Samba)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

if __name__ == "__main__":
    USBSIM(FileImgDic, MPDic, WaDo, Samba)
