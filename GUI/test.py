import os
lpd = os.popen("lsblk -f | grep '/mnt/usb_fat32'").read().split("\n")[0].split(" ")[0]
print (lpd)
