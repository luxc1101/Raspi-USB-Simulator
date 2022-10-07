# PRIAPOS
<img src="https://content.instructables.com/ORIG/F60/5H8G/KNHGQNWP/F605H8GKNHGQNWP.png?auto=webp&frame=1&width=810&fit=bounds&md=38489d1a10177d77d78f77287ad3bd0a" width="100" >

The idea comes from Mauch Nico to lighten the amount of work for USB sticks plug in&out during the media testing. Raspberry Pi Zero can be convert into a USB Drive emulator that can be accessed within a local network. This can be useful to transfer files into devices (e.g. DUT) that have a USB connection. It's also able to change different filesystems automatically in order to simulate the USB storage device with different filesystems.

In a word the plan is to have a dynamical usb storage device, which is configurable in format and content.
## Big Picture
<img src="BigPic.PNG" width="250">

## Preparation

| Hardware                   | Software                                                       |
| -------------              | -------------                                                  |
| RaspberryPi zero W         | [Raspberry Pi Imanger](https://www.raspberrypi.com/software/)  |
| USB OTG Cable (Data port)  | PuTTy                                                          |
| USB OTG Cable (Power)      |                                                                |
| micoSD Card (e.g. 128 GB)  |                                                                |
| micoSD Card Reader         |                                                                |
| TP-Link USB WiFi Receiver  |                                                                |

## Implementation of This Project
 [Confluence: USB Simulator](https://confluence.jnd.joynext.com/display/APP/USB+Simulator+Plus)

## Tutorial
**Paspberrypi Zero W**
- if WiFi was changed, `ssh`(without file typ) and `wpa_supplicant.config` (with new WiFi ssid and password) should be add into boot of SD card.
- power the Raspberrypi via PWR port (only power) or USB port (power and data transfer).
- connect USB port to your target via OTG cabel.

**PuTTY Configuration:**
- PuTTY logging of Default Settings should be active before using USB Simulator and copy the path of `PuTTy.log` file to "Log" in `Config.json`.
- to select "always overwirte it"
- to click checkbox "Flush log the file frequently"
- to browse a path to save PuTTY.log file and copy path.
- `Config.json` could assign parameters to app, because the app will direct read json file at startup. If certain parameters need to be changed, it is better to edit them in this file first rather than in the application.
    ```json
    {
        "PuTTYConf": {
        "PuTTYPath": "C:/Program Files/PuTTY/putty.exe",
        "IPAddress": "192.168.188.38",
        "Key": "raspberry",
        "Log": "C:/Users/lu_x4/Desktop/putty.log"
        },
        "Others": {
        "WoDa": false,
        "Samba": false
        }
    }
    ```
**USB Simulator**

- Menubar
    - _Setting_ (Anpassen): this function can configre the parameters for PuTTY in order to login and trace log data. It will open a configuration dialog, where could be configred. PuTTY logging should be active before using and copy the path of PuTTY.log file to "Log" in PuTTY Conf. Watchdog and Samba service could be active if they will be needed, but please make sure your PC is able to connect the internet.
    - _Connect_: this feature can mount filesystem of combobox and simulate a USB device plugin situation.
    - _Disconnect & Refresh_: this feature can simulate a USB device plug-out situation.
    - _Remote Folder_: this feature will open the remote folder only if samba service was active. It will provide a possibility to modify the files in remote folder. The modifications will also be synchronised in the USB device.
    - _Clear_: to clear the trace window.
    - _Delete Img_: to delete filesystem image in order to recreate a new filesystem.img with new size in this case.
    - _Quit_: to quit PuTTY.exe and delete `PuTTy.log` file.
    - _Help_: to open a quick user guaid.
- Mount Filesystem
    - _Combobox_: shows all current supported filesystems (`ext2`, `ext3`, `ext4`, `fat16`, `fat32(vfat)`, `exfat`, `ntfs`, `hfs+`, `partitions`).
    - _Status_: 3 Indicators (`Img`, `Watchdog`, `Samba`). If the selected Filesystem is existed, the Img idicator will be green otherwise be red. If Watchdog and Samba was checked at configuration dialog, it will be green otherwise red.
        ```python
        if os.path.exist(<".img">):
            StatusImg.setSheetStyle("green")
        else:
            StatusImg.setSheetStyle("red")
        if checkbox.checked:
            StatusWaDo.setSheetStyle("green")
        else:
            StatusWaDo.setSheetStyle("red")
        ```
- Trace
    - _Trace Window_: to show the PuTTY's output in read time (read only).
- Command Window:
    - Depending on the situation, sometimes an input is required and in this window the input can be send directly to the PuTTY terminal.

## Checklist
- [ ] RaspberryPi, OTG Cabel, USB TP-Link WiFi Receiver (if needed)
- [ ] PuTTY installed
- [ ] `wpa_supplicant.config` and `ssh` are written into boot SD, only if WiFi has to be changed. (Default: ssid="AMB-StreamWLAN"; psk="1bis56789")
- [ ] power RaspberryPi up and connect RaspberryPi to DUT, connect USB TP-Link WiFi Receiver to PC (if needed)
- [ ] check PuTTY' logging of Default Settings and check the parameters in `Config.json` 
- [ ] `Config.json` and USB Simulator should be put in same root path
