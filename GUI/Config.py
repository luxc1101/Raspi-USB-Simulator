# -*- coding: utf-8 -*-
#*****************************************************
# Project:   Raspberrypi Zero USB filesystem simulator
# Autor:     Xiaochuan Lu
# Abteilung: SWTE
#*****************************************************

import json
import os
import subprocess
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

import Icons


class Ui_ConfigDialog(QMainWindow):

    my_signal = pyqtSignal(dict)

    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName("ConfigDialog")
        ConfigDialog.resize(300, 280)
        ConfigDialog.setWindowIcon(QtGui.QIcon(":/Image/AnpassenIcon.png"))
        self.gridLayout_3 = QtWidgets.QGridLayout(ConfigDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(ConfigDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.LB_PTPath = QtWidgets.QLabel(self.groupBox)
        self.LB_PTPath.setObjectName("LB_PTPath")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.LB_PTPath)
        self.LE_PTPath = QtWidgets.QLineEdit(self.groupBox)
        self.LE_PTPath.setObjectName("LE_PTPath")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LE_PTPath)
        self.LB_IP = QtWidgets.QLabel(self.groupBox)
        self.LB_IP.setObjectName("LB_IP")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.LB_IP)
        self.LE_IP = QtWidgets.QLineEdit(self.groupBox)
        self.LE_IP.setObjectName("LE_IP")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LE_IP)
        self.LB_Key = QtWidgets.QLabel(self.groupBox)
        self.LB_Key.setObjectName("LB_Key")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.LB_Key)
        self.LE_Key = QtWidgets.QLineEdit(self.groupBox)
        self.LE_Key.setReadOnly(False)
        self.LE_Key.setObjectName("LE_Key")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LE_Key)
        self.LB_Log = QtWidgets.QLabel(self.groupBox)
        self.LB_Log.setObjectName("LB_Log")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.LB_Log)
        self.LE_LogPath = QtWidgets.QLineEdit(self.groupBox)
        self.LE_LogPath.setObjectName("LE_LogPath")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.LE_LogPath)
        self.gridLayout.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QtWidgets.QGroupBox(ConfigDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.LB_ssid = QtWidgets.QLabel(self.groupBox_3)
        self.LB_ssid.setObjectName("LB_ssid")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.LB_ssid)
        self.LE_ssid = QtWidgets.QLineEdit(self.groupBox_3)
        self.LE_ssid.setObjectName("LE_ssid")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LE_ssid)
        self.LB_psk = QtWidgets.QLabel(self.groupBox_3)
        self.LB_psk.setObjectName("LB_psk")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.LB_psk)
        self.LE_psk = QtWidgets.QLineEdit(self.groupBox_3)
        self.LE_psk.setObjectName("LE_psk")
        self.LE_psk.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LE_psk)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QtWidgets.QGroupBox(ConfigDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.checkBox_WaDo = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_WaDo.setObjectName("checkBox_WaDo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox_WaDo)
        self.checkBox_Samba = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_Samba.setObjectName("checkBox_Samba")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBox_Samba)
        # self.B_ImgPath = QtWidgets.QPushButton(self.groupBox_2)
        # self.B_ImgPath.setObjectName("B_ImgPath")
        # self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.B_ImgPath)
        # self.LE_Path = QtWidgets.QLineEdit(self.groupBox_2)
        # self.LE_Path.setText("")
        # self.LE_Path.setObjectName("LE_Path")
        # self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LE_Path)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)

        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox_Conf = QtWidgets.QDialogButtonBox(ConfigDialog)
        self.buttonBox_Conf.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_Conf.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_Conf.setObjectName("buttonBox_Conf")
        self.verticalLayout.addWidget(self.buttonBox_Conf)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        
###############################################################################################  
        self.buttonBox_Conf.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Config.json"),'r',encoding="utf8") as f:
        #     self.setup_dict = json.load(f) 
        #     f.close()

        # print(os.getcwd())

        with open(os.path.join(os.getcwd(), "Config.json"),'r',encoding="utf8") as f:
            self.setup_dict = json.load(f) 
            f.close()
        

        self.retranslateUi(ConfigDialog)
        self.buttonBox_Conf.accepted.connect(ConfigDialog.accept) # type: ignore
        self.buttonBox_Conf.rejected.connect(ConfigDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)
 

        # self.B_ImgPath.clicked.connect(self.OCfolder)
        self.buttonBox_Conf.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.configparameter)
        # self.buttonBox_Conf.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.OCfolder)

        self.checkBox_Samba.setChecked(self.setup_dict["Others"]["WoDa"])
        self.checkBox_WaDo.setChecked(self.setup_dict["Others"]["Samba"])

    def retranslateUi(self, ConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Configuration"))
        self.groupBox.setTitle(_translate("ConfigDialog", "PuTTY Conf"))
        self.LB_PTPath.setText(_translate("ConfigDialog", "PuTTYPath"))
        self.LE_PTPath.setText(_translate("ConfigDialog", self.setup_dict["PuTTYConf"]["PuTTYPath"]))
        self.LB_IP.setText(_translate("ConfigDialog", "IP Address"))
        self.LE_IP.setText(_translate("ConfigDialog", self.setup_dict["PuTTYConf"]["IPAddress"]))
        self.LB_Key.setText(_translate("ConfigDialog", "Key"))
        self.LE_Key.setText(_translate("ConfigDialog", self.setup_dict["PuTTYConf"]["Key"]))
        self.LB_Log.setText(_translate("ConfigDialog", "Log"))
        self.LE_LogPath.setText(_translate("ConfigDialog", self.setup_dict["PuTTYConf"]["Log"]))
        self.groupBox_2.setTitle(_translate("ConfigDialog", "Others"))
        self.groupBox_3.setTitle(_translate("ConfigDialog", "WiFi"))
        self.LB_ssid.setText(_translate("ConfigDialog", "SSID"))
        self.LB_psk.setText(_translate("ConfigDialog", "Password"))
        self.LE_ssid.setText(_translate("ConfigDialog", self.setup_dict["WiFi"]["ssid"]))
        self.LE_psk.setText(_translate("ConfigDialog", self.setup_dict["WiFi"]["psk"]))
        self.checkBox_WaDo.setText(_translate("ConfigDialog", "Watchdog Service"))
        self.checkBox_Samba.setText(_translate("ConfigDialog", "Samba Service"))
        # self.B_ImgPath.setText(_translate("ConfigDialog", "Open|Create"))
################################################################################################
        # self.LE_Path.setText(_translate("ConfigDialog", os.path.join(
            # os.path.dirname(os.path.realpath(__file__)), "filesystem")))


    # def OCfolder(self):
    #     '''
    #     to create filsystem folder to save the to be creadted .img files
    #     the usually the folder will be created in the path which shows in lineEdit
    #     but it could also be changed by ourselves if the path in the lineEdit come to be empty 
    #     '''
    #     QFileDialog.getExistingDirectory(parent=self, caption="Open directroy", directory="//{}".format("DEDREVMDC04.Joynext.com"))

        # try:
        #     QMessageBox.setWindowIcon(self, QtGui.QIcon(":/Image/AnpassenIcon.png"))
        #     path = self.LE_Path.text()
        #     check_folder = os.path.isdir(path)
        #     if not check_folder:
        #         os.makedirs(path)
        #         # QMessageBox.information(self, 'Info', 'create folder done')
        #     # else:
        #         #QMessageBox.information(self, 'Info', "folder is already existed")
        # except:
        #     root = QFileDialog.getExistingDirectory(
        #         parent=self, caption="Open directroy", directory=os.path.abspath(os.curdir))
        #     path = self.LE_Path.setText(root)
        #     return self.OCfolder
        # self.buttonBox_Conf.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

    # def PuTTYLogin(self):
    #     '''
    #     open PuTTY and login pi by ssh
    #     '''
    #     PuTTY_Path = self.LE_PTPath.text()
    #     IP = self.LE_IP.text()
    #     Key = self.LE_Key.text()
    #     app = Application().start(r"{} -ssh pi@{}".format(PuTTY_Path, IP))
    #     time.sleep(2)
    #     PT = app.PuTTY
    #     print(type(PT))
    #     time.sleep(2)
    #     PT.send_keystrokes(Key)
    #     PT.send_keystrokes("{ENTER}")
        
    def wificonnect(self):
        ssid = self.LE_ssid.text()
        # ssid = "Automotive-QS"
        psk = self.LE_psk.text()
        msg = QMessageBox()
        msg.setWindowTitle("WiFi Status")
        msg.setWindowIcon(QtGui.QIcon(":/Image/AnpassenIcon.png"))
        # connect a previously connected SSID
        WiFiexit = subprocess.getoutput('netsh wlan show networks | findstr {}'.format(ssid))
        if ssid in WiFiexit:
            # cmd to check the connected signal if signal -> echo oneline otherweis -> echo offline
            cmd_netsig = 'netsh wlan show interfaces | Findstr /c:"Signal" && Echo Online || Echo Offline'
            data = subprocess.check_output(cmd_netsig, shell=True).strip().decode('ascii', 'ignore')
            if 'Online' in data:
                msg.setIcon(QMessageBox.Information)
                msg.setText("WiFi connected")
                QTimer.singleShot(1500, lambda : msg.done(0))
                msg.exec()
                # os.system('cmd /c "netsh wlan disconnect"')
                return True
            else: 
                # connect wifi with ssid
                os.system(f'''cmd /c "netsh wlan connect name={ssid}"''')
                # wait a sec cause sometime connect to build needs time
                time.sleep(5)
                # data = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces']).strip().decode('ascii', 'ignore')
                data = subprocess.check_output(cmd_netsig, shell=True).strip().decode('ascii', 'ignore')
                if 'Online' in data:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("WiFi connected")
                    QTimer.singleShot(1500, lambda : msg.done(0))
                    msg.exec()
                    # os.system('cmd /c "netsh wlan disconnect"')
                    return True
                
                msg.setIcon(QMessageBox.Critical)
                msg.setText("WiFi connect fail")
                QTimer.singleShot(1500, lambda : msg.done(0))
                msg.exec()
                return False
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("WiFi {} not avaiable".format(ssid))
            QTimer.singleShot(1500, lambda : msg.done(0))
            msg.exec()
            return False        
        
    def configparameter(self):
        if self.wificonnect():
            PuTTY_Path = self.LE_PTPath.text()
            IP = self.LE_IP.text()
            Key = self.LE_Key.text()
            Log = self.LE_LogPath.text()
            Samba = self.checkBox_Samba.checkState()
            WaDo = self.checkBox_WaDo.checkState()
            # FSPath = self.LE_Path.text()
            param = {"PuTTY_Path": PuTTY_Path, "IP": IP,
                    "Key": Key, "Log": Log,"Samba": Samba, "WaDo": WaDo}
            self.my_signal.emit(param)
            return
        
        self.Confwin = QtWidgets.QDialog()
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self.Confwin)
        self.Confwin.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ConfigDialog = QtWidgets.QDialog()
    ui = Ui_ConfigDialog()
    ui.setupUi(ConfigDialog)
    ConfigDialog.show()
    sys.exit(app.exec_())
