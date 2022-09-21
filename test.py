
from hashlib import new


fs = "ext3.img"
MP = "/mnt/usb_ext3"
def modifyfile(file:str, img:str, MP:str):
    reading_file = open("fswd.py", "r")
    new_file_content = ""
    for line in reading_file:
        newline = line
        if "/home/pi/" in line:
            oldline = line
            newline = oldline.split("'/home/pi/")[0] + "'/home/pi/{}'".format(fs)
            # print(oldline)
            newline = line.replace(oldline, newline) + "\n"
            # print(newline)
        elif "/mnt/" in line:
            oldline = line
            newline = oldline.split("'/mnt/")[0] + "'{}'".format(MP)
            newline = line.replace(oldline, newline) + "\n"
        
        new_file_content += newline 

    reading_file.close()

    writing_file = open("fswd.py", "w")
    writing_file.write(new_file_content)
    writing_file.close()
