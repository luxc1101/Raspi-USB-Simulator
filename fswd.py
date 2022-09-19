#!/usr/bin/python3
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
##########################
# import all needed libs #
##########################
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import *
#############
# paramters #
#############
Img = '/home/pi/<?>.img'
watchpath = '/mnt/<?>'
cmd_mount = "sudo /sbin/modprobe g_multi file={} stall=0 removable=1".format(Img)
cmd_unmount = "sudo /sbin/modprobe g_multi -r"
cmd_sync = "sudo sync"
act_time_out = 10 # 10 s
act_events = [DirDeletedEvent, DirMovedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent]



class Handler(FileSystemEventHandler):
    def __init__(self):
        self.reset()

    def on_any_event(self,event):
        if type(event) in act_events:
            self._dirty = True
            self._dirty_time = time.time()

    def reset(self):
        self._dirty = False
        self._dirty_time = 0
        self._path = None

    @property
    def dirty(self):
        return self._dirty
    @property
    def dirty_time(self):
        return self._dirty_time

class OnMyWatch:
    # the folder on watch
    watchpath = watchpath
    def __init__(self):
        self.observer = Observer()

    def run(self):
        evh = Handler()
        self.observer.schedule(evh, path=self.watchpath, recursive=True)
        self.observer.start()
        try:
            while True:
                while evh.dirty:
                    time_out = time.time() - evh.dirty_time
                    if time_out >= act_time_out:
                        # change happend, cmd unmount
                        os.system(cmd_unmount)
                        time.sleep(1)
                        # cmd sync
                        os.system(cmd_sync)
                        time.sleep(1)
                        # cmd mount
                        os.system(cmd_mount)
                        evh.reset()
                    time.sleep(1)
               # print ("watching")
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
