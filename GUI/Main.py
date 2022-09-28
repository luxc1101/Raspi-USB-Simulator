# -*- coding: utf-8 -*-
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFrame, QLabel
from Config import Ui_ConfigDialog
from PyQt5.QtCore import pyqtSignal, QThread, QDate, Qt
from pywinauto.application import Application
import sys
import Icons
import time

class VLine(QFrame):
    '''
    Setting up a customized status bar like:
    -------------------------------------------------
    |status message       |version: 1.x |Data: Y-M-D|
    -------------------------------------------------
    '''
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

class Ui_MainWindow(QMainWindow):
    Putty = None
    Logging = None
    # Param = None
    Filesysdict = {
        "MIB Compliance Media": ['mib_compliance', "0"],
        "ext2": ["ext2","1"],
        "ext3": ["ext3", "2"],
        "ext4": ["ext4", "3"],
        "fat16": ["fat16", "4"],
        "fat32": ["fat32", "5"],
        "ntfs": ["ntfs", "6"],
        "exfat": ["exfat", "7"],
        "hfsplus": ["hfsplus", "8"],
        "partitions": ["part", "9"],
        "Software update": ["sw", "10"],
    }

    def configWin(self):
        self.Confwin = QtWidgets.QDialog()
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self.Confwin)
        self.Confwin.show()
        self.ui.my_signal.connect(self.PuTTYLogin)

    def setupUi(self, MainWindow):
        # self.configWin()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 400)
        MainWindow.setWindowIcon(QtGui.QIcon(":/Image/AppIcon.png"))
###########################################################################
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_mtfs = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_mtfs.setObjectName("groupBox_mtfs")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_mtfs)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.LB_Filesystem = QtWidgets.QLabel(self.groupBox_mtfs)
        self.LB_Filesystem.setObjectName("LB_Filesystem")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.LB_Filesystem)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_mtfs)
        self.comboBox.setObjectName("comboBox")
        for _ in range(11):
            self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LB_Img = QtWidgets.QLabel(self.groupBox_mtfs)
        self.LB_Img.setAlignment(QtCore.Qt.AlignCenter)
        self.LB_Img.setObjectName("LB_Img")
        self.horizontalLayout.addWidget(self.LB_Img)
        self.LB_WaDo = QtWidgets.QLabel(self.groupBox_mtfs)
        self.LB_WaDo.setAlignment(QtCore.Qt.AlignCenter)
        self.LB_WaDo.setObjectName("LB_WaDo")
        self.horizontalLayout.addWidget(self.LB_WaDo)
        self.LB_Samba = QtWidgets.QLabel(self.groupBox_mtfs)
        self.LB_Samba.setAlignment(QtCore.Qt.AlignCenter)
        self.LB_Samba.setObjectName("LB_Samba")
        self.horizontalLayout.addWidget(self.LB_Samba)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.LB_Status = QtWidgets.QLabel(self.groupBox_mtfs)
        self.LB_Status.setObjectName("LB_Status")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.LB_Status)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_mtfs, 0, 0, 1, 1)
        self.groupBox_trace = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_trace.setObjectName("groupBox_trace")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_trace)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_trace = QtWidgets.QTextEdit(self.groupBox_trace)
        self.textEdit_trace.setObjectName("textEdit_trace")
        self.gridLayout.addWidget(self.textEdit_trace, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_trace, 1, 0, 1, 1)
        self.groupBox_Cmd = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_Cmd.setObjectName("groupBox_Cmd")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_Cmd)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LE_SendCmd = QtWidgets.QLineEdit(self.groupBox_Cmd)
        self.LE_SendCmd.setObjectName("LE_SendCmd")
        self.horizontalLayout_2.addWidget(self.LE_SendCmd)
        self.B_SendCmd = QtWidgets.QPushButton(self.groupBox_Cmd)
        self.B_SendCmd.setObjectName("B_SendCmd")
        self.horizontalLayout_2.addWidget(self.B_SendCmd)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_Cmd, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 349, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuCalls = QtWidgets.QMenu(self.menuBar)
        self.menuCalls.setObjectName("menuCalls")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setEnabled(True)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionAnpassen = QtWidgets.QAction(MainWindow)
        self.actionAnpassen.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/AnpassenIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAnpassen.setIcon(icon)
        self.actionAnpassen.setObjectName("actionAnpassen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Image/putty-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon1)
        self.actionQuit.setObjectName("actionQuit")
        self.actionEject = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Image/disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEject.setIcon(icon2)
        self.actionEject.setObjectName("actionEject")
        self.actionMount = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Image/connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMount.setIcon(icon3)
        self.actionMount.setObjectName("actionMount")
        self.actionClear = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Image/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon4)
        self.actionClear.setObjectName("actionClear")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Image/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon5)
        self.actionHelp.setObjectName("actionHelp")
        self.menuCalls.addAction(self.actionAnpassen)
        self.menuCalls.addAction(self.actionMount)
        self.menuCalls.addAction(self.actionEject)
        self.menuCalls.addAction(self.actionClear)
        self.menuCalls.addAction(self.actionQuit)
        self.menuCalls.addAction(self.actionHelp)
        self.menuBar.addAction(self.menuCalls.menuAction())
        self.mainToolBar.addAction(self.actionAnpassen)
        self.mainToolBar.addAction(self.actionMount)
        self.mainToolBar.addAction(self.actionEject)
        self.mainToolBar.addAction(self.actionClear)
        self.mainToolBar.addAction(self.actionQuit)

###########################################################################
        self.actionMount.setEnabled(False)
        self.actionEject.setEnabled(False)
        self.actionQuit.setEnabled(False)
        self.statusBar.showMessage("Status: not connected")
        self.VersionQL = QLabel("Version: 1.0")
        self.VersionQL.setStyleSheet('font-size:9px')
        date = "Data: {}".format(QDate.currentDate().toString(Qt.ISODate))
        self.DataQL = QLabel(date)
        self.DataQL.setStyleSheet('font-size:9px')
        self.statusBar.reformat()
        self.statusBar.setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.statusBar.setStyleSheet("QtWidgets.QStatusBar::item {border: none;}")
        self.statusBar.addPermanentWidget(VLine()) 
        self.statusBar.addPermanentWidget(self.VersionQL)
        self.statusBar.addPermanentWidget(VLine())
        self.statusBar.addPermanentWidget(self.DataQL)
        self.LB_Img.setStyleSheet("background-color: #f9e1dd; border: 1px solid black; border-radius: 4px")
        self.LB_Samba.setStyleSheet("background-color: #f9e1dd; border: 1px solid black; border-radius: 4px")
        self.LB_WaDo.setStyleSheet("background-color: #f9e1dd; border: 1px solid black; border-radius: 4px")


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionAnpassen.triggered.connect(self.configWin)
        self.actionMount.triggered.connect(self.Mount)
        self.actionEject.triggered.connect(self.Eject)
        self.actionQuit.triggered.connect(self.PuTTYExit)
        self.actionClear.triggered.connect(self.TraceClear)
        self.actionHelp.triggered.connect(lambda: Ui_MainWindow.MSG(title="help", 
                                                                    message="Tutorial: <a href=\"https://git1.jnd.joynext.com/lu_x4/priapos.git\">Raspberrypi Zero USB filesystem simulator</a>",
                                                                    type="i"))
        # self.B_SendCmd.clicked.connect(lambda: self.SendCommand(self.LE_SendCmd.text()))
        self.thread = {}
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "USB Simulator"))
        self.groupBox_mtfs.setTitle(_translate("MainWindow", "Mount Filesystem"))
        self.LB_Filesystem.setText(_translate("MainWindow", "Filesystem"))
        self.comboBox.setItemText(0, _translate("MainWindow", "MIB Compliance Media"))
        self.comboBox.setItemText(1, _translate("MainWindow", "ext2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "ext3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "ext4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "fat16"))
        self.comboBox.setItemText(5, _translate("MainWindow", "fat32"))
        self.comboBox.setItemText(6, _translate("MainWindow", "ntfs"))
        self.comboBox.setItemText(7, _translate("MainWindow", "exfat"))
        self.comboBox.setItemText(8, _translate("MainWindow", "hfsplus"))
        self.comboBox.setItemText(9, _translate("MainWindow", "partitions"))
        self.comboBox.setItemText(10, _translate("MainWindow", "Software update"))
        self.LB_Img.setText(_translate("MainWindow", "Img"))
        self.LB_WaDo.setText(_translate("MainWindow", "Watchdog"))
        self.LB_Samba.setText(_translate("MainWindow", "Samba"))
        self.LB_Status.setText(_translate("MainWindow", "Status"))
        self.groupBox_trace.setTitle(_translate("MainWindow", "Trace"))
        self.menuCalls.setTitle(_translate("MainWindow", "Calls"))
        self.actionAnpassen.setText(_translate("MainWindow", "Anpassen"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionEject.setText(_translate("MainWindow", "Eject"))
        self.actionMount.setText(_translate("MainWindow", "Mount"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.B_SendCmd.setText(_translate("MainWindow", "CMD Send"))
        self.groupBox_Cmd.setTitle(_translate("MainWindow", "Command Window"))
        self.textEdit_trace.setPlaceholderText(_translate("Form", "PuTTY's output is shown here"))
        self.LE_SendCmd.setPlaceholderText(_translate("Form", "Send the command manually here"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
    
    @staticmethod
    def MSG(title, message, type):
        '''
        configration message box
        '''
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setWindowIcon(QtGui.QIcon(":/Image/AppIcon.png"))
        if type == "i":
            msg.setIcon(QMessageBox.Information)
        elif type == "w":
            msg.setIcon(QMessageBox.Warning) 
        elif type == "e":
            msg.setIcon(QMessageBox.Critical) 
        msg.exec()

    def SendCommand(self, cmd:str):
        '''
        send command to PuTTY Terminal
        '''
        self.Putty.send_keystrokes(cmd)
        self.Putty.send_keystrokes("{ENTER}")

    def PuTTYLogin(self, param):
        '''
        trying to login Rapberry Pi zero by IP via PuTTY
        '''
        try:
            self.app = Application().start(
                r"{} -ssh pi@{}".format(param["PuTTY_Path"], param["IP"]))
            time.sleep(1)
            self.Putty = self.app.PuTTY
            self.Logging = param["Log"]
            PT_sec_alert = self.app.PuTTYSecurityAlert
            if PT_sec_alert.exists():
                PT_sec_alert.Yes.click()
                # PT_sec_alert.No.click()
                # PT_sec_alert.Cancel.click()
            if not os.path.exists(self.Logging):
                self.statusBar.showMessage("Login failed")
                Ui_MainWindow.MSG(title="Error", message="Please check PuTTY configuration and WiFi", type="e")
                return
            time.sleep(1)
            self.SendCommand(param["Key"])
            self.SendCommand("ls")
            if not param["Samba"]:
                self.SendCommand("sudo systemctl stop smbd")
            if not param["WaDo"]:
                self.SendCommand("sudo systemctl stop fswd")
            self.SendCommand("python mountfs_gui.py")
            # self.statusBar.showMessage("PuTTY open successfully")
            self.statusBar.showMessage("Login successfully")
            self.actionMount.setEnabled(True)
            self.actionQuit.setEnabled(True)
            self.comboBox.setEnabled(True)
        except:
            pass


    def PuTTYExit(self):
        '''
        exit PuTTY
        '''
        try:
            # self.SendCommand("q")
            # self.SendCommand("exit")
            os.system("taskkill /im PuTTY.exe")
            self.actionAnpassen.setEnabled(True)
            self.actionMount.setEnabled(False)
            self.actionQuit.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.statusBar.showMessage("Logout and PuTTY exited")
            try:
                # condition of threadstop is the threadstart first, otherweis error
                self.thread[1].stop()
                del(self.thread[1])
                print("del thread")
            except:
                pass            
        except:
            Ui_MainWindow.MSG(title="Info", message="please exicute putty first", type="i")
            self.statusBar.showMessage("PuTTY exit failed")
        trytimes = 5
        while trytimes>0:
            try:   
                os.remove(self.Logging)
                break
            except:
                time.sleep(1)
                trytimes-=1

    def TraceClear(self):
        '''
        clean all log in QTextExit but NOT the Putty.log
        '''
        self.textEdit_trace.clear()
    
    def Update_logging(self,msg):
        '''
        line by line append log messsage to QTextEdit
        '''
        self.textEdit_trace.append(msg)

    def Mount(self):
        '''
        run the TraceThread class
        '''
        self.textEdit_trace.clear()
        self.actionEject.setEnabled(True)
        self.actionMount.setEnabled(True)
        self.actionQuit.setEnabled(False)
        self.comboBox.setEnabled(True)
        try:
            self.thread[1].file.close()
            self.thread[1].stop()
            del(self.thread[1])
        except:
            pass
        self.thread[1] = TraceThread(parent=None, Logfile=self.Logging, 
                                    sleep_time_in_seconds=0.05, 
                                    img=self.Filesysdict[self.comboBox.currentText()][0],
                                    imgstaus=self.LB_Img
                                    )
        self.thread[1].start()
        self.thread[1].trace_singal.connect(self.Update_logging)
        self.SendCommand(self.Filesysdict[self.comboBox.currentText()][1])
        
    def Eject(self):
        '''
        eject the current USB drive device
        '''
        self.actionEject.setEnabled(False)
        self.actionMount.setEnabled(True)
        self.actionQuit.setEnabled(True)
        self.comboBox.setEnabled(True)
        try:
            # self.SendCommand("sudo /sbin/modprobe g_multi -r")
            self.SendCommand("e")
            # self.SendCommand("python mountfs_gui.py")
            self.thread[1].file.close()
            # self.thread[1].stop()
            # del(self.thread[1])
            self.statusBar.showMessage("{} eject successfully".format(self.comboBox.currentText()))
            print("file.close")
        except:
            self.statusBar.showMessage("{} eject failed".format(self.comboBox.currentText()))


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                                 
#                   Thread Class                   
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                                 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class TraceThread(QThread):
    '''
    read data from log file and send data to trace window of Main window class
    '''
    trace_singal = pyqtSignal(str)
    file = None
    # status_signal = pyqtSignal(int)
    def __init__(self, parent, Logfile, sleep_time_in_seconds, img, imgstaus):
        super(TraceThread, self).__init__(parent)
        self.Logfile = Logfile
        print("thread:" + self.Logfile)
        self.sleep_time_in_seconds = sleep_time_in_seconds
        self.img = img
        self.imgstatus = imgstaus
        self.file = open(self.Logfile, 'r', errors='ignore')

    def run(self):
        LogStartFlag = False
        try:
            # with open(self.Logfile, 'r', errors='ignore') as f:
            #     self.file = f
            while True:
                try:
                    line = self.file.readline().strip()
                    if "pi@raspberrypi" in line:
                            LogStartFlag = True
                    if LogStartFlag:   
                        if line:
                            if "enter" in line.lower():
                                color_content =  "<span style=\" font-size:8pt; font-weight:800; color:{};\" >".format("#32CD32")
                                color_content += line
                                color_content += "</span>"
                                self.trace_singal.emit(color_content)
                            elif "please" in line.lower():
                                color_content =  "<span style=\" font-size:8pt; font-weight:800; color:{};\" >".format("#00FFFF")
                                color_content += line
                                color_content += "</span>"
                                self.trace_singal.emit(color_content)
                            elif self.img in line:
                                self.imgstatus.setStyleSheet("background-color: #a4efaf; border: 1px solid black; border-radius: 4px")
                                self.imgstatus.setText(self.img)
                            elif ("status of samba" in line.lower()) or ("status of watchdog" in line.lower()):
                                color_content =  "<span style=\" font-size:8pt; font-weight:800; color:{};\" >".format("red")
                                color_content += line
                                color_content += "</span>"
                                self.trace_singal.emit(color_content)
                            else:
                                self.trace_singal.emit(line)
                    # for line in self.f:
                    #     if "pi@raspberrypi" in line:
                    #         LogStartFlag = True
                    #     if LogStartFlag:
                    #         if (line) and ("pi@raspberrypi" not in line):
                    #             if self.img in line:
                    #                 self.imgstatus.setStyleSheet("background-color: #a4efaf; border: 1px solid black; border-radius: 4px")
                    #             self.trace_singal.emit(line.strip()) 
                    #         else:
                    #             color_content =  "<span style=\" font-size:8pt; font-weight:800; color:{};\" >".format("#32CD32")
                    #             color_content += line.strip()
                    #             color_content += "</span>"
                    #             self.trace_singal.emit(color_content)
                    # time.sleep(self.sleep_time_in_seconds)
                except:
                    pass
        except IOError as e:
            line = 'Cannot open the file {}. Error: {}'.format(self.Logfile, e)
            self.trace_singal.emit(line)

    def stop(self):
        self.imgstatus.setStyleSheet("background-color: #f9e1dd; border: 1px solid black; border-radius: 4px")
        self.quit()

         


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
