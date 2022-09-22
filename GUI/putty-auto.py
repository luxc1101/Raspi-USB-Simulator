from curses import window
import imp
from turtle import title
import pyautogui as pa
import subprocess as sp
import time
import pywinauto
from pywinauto.application import Application
import pywinauto.keyboard

PuTTY_Path = 'C:\Program Files\PuTTY\putty.exe'
app = Application().start(r"{} -ssh pi@192.168.188.38".format(PuTTY_Path))
time.sleep(3)
pt = app.PuTTY
time.sleep(3)
pt.send_keystrokes("raspberry")
pt.send_keystrokes("{ENTER}")

# app = Application().connect(title="PuTTY Configuration")
# window = app.PuTTYConfigBox
# window.set_focus()
# window[u"Host Name (or IP address):Edit"].type_keys("raspberrypi.local")
# window["Open"].click()
#sp.Popen(PuTTY_Path)
#time.sleep(3)
# pa.screenshot('GUI/Image/Putty.png')
# print(pa.locateCenterOnScreen("GUI/Image/Putty.png"))
