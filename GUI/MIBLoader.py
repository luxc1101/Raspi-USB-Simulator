# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mibloader.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import shutil
import sys
import urllib.request

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkReply,
                             QNetworkRequest)
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog

import Icons


class DownloadManager:
    LB_text = ""
    def __init__(self, parent=None,):
        self.parent = parent
        self.manager = QNetworkAccessManager()
        self.progress = QProgressDialog(parent)
        self.progress.setWindowTitle("download")
        self.progress.setWindowIcon(QtGui.QIcon(":/Image/download.png"))
        self.progress.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setAutoReset(False)
        self.progress.setAutoClose(True)
        self.progress.setLabelText(f"{self.LB_text}")
        self.progress.setMinimumDuration(0)
        self.progress.setValue(0)

    def download(self, url, save_path):
        self.request = QNetworkRequest(QUrl(url))
        self.reply = self.manager.get(self.request)
        self.reply.downloadProgress.connect(self.on_download_progress)
        self.reply.finished.connect(self.on_download_finished)
        self.save_path = save_path
        self.progress.show()

    def on_download_progress(self, bytes_received, bytes_total):
        try:
            percent = int(bytes_received * 100 / bytes_total)
            self.progress.setValue(percent)
        except ZeroDivisionError:
            pass

    def on_download_finished(self):
        if self.reply.error() == QNetworkReply.NoError:
            data = self.reply.readAll()
            with open(self.save_path, "wb") as f:
                f.write(data)
        else:
            error_msg = self.reply.errorString()
            # handle error
        self.progress.close()

class Ui_MIBloader(object):

    def setupUi(self, MIBloader):
        MIBloader.setObjectName("MIBloader")
        MIBloader.resize(238, 183)
        MIBloader.setWindowIcon(QtGui.QIcon(":/Image/download.png"))
        MIBloader.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.verticalLayout = QtWidgets.QVBoxLayout(MIBloader)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_rename = QtWidgets.QLineEdit(MIBloader)
        self.lineEdit_rename.setObjectName("lineEdit_rename")
        self.gridLayout.addWidget(self.lineEdit_rename, 0, 1, 1, 1)
        self.LE_source = QtWidgets.QLineEdit(MIBloader)
        self.LE_source.setObjectName("LE_source")
        self.gridLayout.addWidget(self.LE_source, 1, 1, 1, 1)
        self.LB_usbfreespace = QtWidgets.QLabel(MIBloader)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.LB_usbfreespace.setFont(font)
        self.LB_usbfreespace.setObjectName("LB_usbfreespace")
        self.gridLayout.addWidget(self.LB_usbfreespace, 3, 1, 1, 1)
        self.LB_TampoPathSpace = QtWidgets.QLabel(MIBloader)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.LB_TampoPathSpace.setFont(font)
        self.LB_TampoPathSpace.setObjectName("LB_TampoPathSpace")
        self.gridLayout.addWidget(self.LB_TampoPathSpace, 5, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LE_destination = QtWidgets.QLineEdit(MIBloader)
        self.LE_destination.setObjectName("LE_destination")
        self.horizontalLayout_2.addWidget(self.LE_destination)
        self.TB_browser1 = QtWidgets.QToolButton(MIBloader)
        self.TB_browser1.setObjectName("TB_browser1")
        self.horizontalLayout_2.addWidget(self.TB_browser1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LE_TempoPath = QtWidgets.QLineEdit(MIBloader)
        self.LE_TempoPath.setObjectName("LE_TempoPath")
        self.horizontalLayout.addWidget(self.LE_TempoPath)
        self.TB_browser2 = QtWidgets.QToolButton(MIBloader)
        self.TB_browser2.setObjectName("TB_browser2")
        self.horizontalLayout.addWidget(self.TB_browser2)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)
        self.LB_rename = QtWidgets.QLabel(MIBloader)
        self.LB_rename.setObjectName("LB_rename")
        self.gridLayout.addWidget(self.LB_rename, 0, 0, 1, 1)
        self.LB_source = QtWidgets.QLabel(MIBloader)
        self.LB_source.setObjectName("LB_source")
        self.gridLayout.addWidget(self.LB_source, 1, 0, 1, 1)
        self.LB_destination = QtWidgets.QLabel(MIBloader)
        self.LB_destination.setObjectName("LB_destination")
        self.gridLayout.addWidget(self.LB_destination, 2, 0, 1, 1)
        self.LB_tempopath = QtWidgets.QLabel(MIBloader)
        self.LB_tempopath.setObjectName("LB_tempopath")
        self.gridLayout.addWidget(self.LB_tempopath, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(MIBloader)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.msg = QMessageBox()
        self.msg.setWindowTitle("download file")
        self.msg.setWindowIcon(QtGui.QIcon(":/Image/download.png"))


        self.retranslateUi(MIBloader)
        self.buttonBox.accepted.connect(MIBloader.accept) # type: ignore
        self.buttonBox.rejected.connect(MIBloader.reject) # type: ignore

        # self.accepted.connect(lambda: self.download(url=self.LE_source.text(), newname=self.lineEdit_rename.text()))
        self.buttonBox.accepted.connect(lambda: self.download(url=self.LE_source.text(), newname=self.lineEdit_rename.text()))


        self.TB_browser1.clicked.connect(lambda: self.resetpath(self.LE_destination,self.LB_usbfreespace))
        self.TB_browser2.clicked.connect(lambda: self.resetpath(self.LE_TempoPath,self.LB_TampoPathSpace))
        QtCore.QMetaObject.connectSlotsByName(MIBloader)

    def retranslateUi(self, MIBloader):
        _translate = QtCore.QCoreApplication.translate
        MIBloader.setWindowTitle(_translate("MIBloader", "download dialog"))
        self.LE_TempoPath.setText(_translate("MIBloader", "{}".format(os.getcwd())))
        self.LB_TampoPathSpace.setText(_translate("MIBloader", "Free space: {} G".format(self.getfreespace(self.LE_TempoPath.text()))))
        self.LB_usbfreespace.setText(_translate("MIBloader", "Free sapce: -"))
        self.TB_browser1.setText(_translate("MIBloader", "Browse"))
        self.TB_browser2.setText(_translate("MIBloader", "Browse"))
        self.LB_rename.setText(_translate("MIBloader", "Rename"))
        self.LB_source.setText(_translate("MIBloader", "Source (url)"))
        self.LB_destination.setText(_translate("MIBloader", "Destination"))
        self.LB_tempopath.setText(_translate("MIBloader", "TempoPath"))
        self.LE_source.setText("http://artefact-repo.mib3.technisat-digital/bob_0_19/6d/3a/db613623031c69b6b94457b51b3590b0c5cd5f01b1460f7d999fe4228dfff9fa91b58634d59a-1.tgz")

    
    def download(self, url, newname):
        newname = self.lineEdit_rename.text()
        print(newname)
        # if rename is empty (no newname) try using the url name 
        if newname == "":
            print('name is None')
            # check if url string has character '/' if not return false
            if "/" in url:
                # use url als as newname (with extension like .tgz)
                newname = url.split('/')[-1]
            else:
                self.msg.setIcon(QMessageBox.Critical)
                self.msg.setText("file name error, please check the url or rename it")
                self.msg.exec()
                return False
        # check if the new name has extension, else return false
        if os.path.splitext(newname)[1] == "":
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("file has no extension")
            self.msg.exec()
            return False
        # download file by using url and with file name in tempopath
        self.tempopath = os.path.join(self.LE_TempoPath.text(), newname)
        DM = DownloadManager
        DM.LB_text = "Downloading..."



    def bytesto(self, bytes, to , bsize=1024):
        '''
        convert bytes to megabytes, etc
        '''
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        for _ in range(a[to]):
            r = r / bsize
        return round(r,2)

    def getfreespace(self, path):
        '''
        get current disk free space, return value in gigabyte
        '''
        stat = shutil.disk_usage(path)
        freesp = self.bytesto(bytes=stat.free, to = 'g')
        return freesp
    
    def openfolder(self):
        '''
        open browser, return selected folder path
        '''
        folderpath = QFileDialog.getExistingDirectory(parent=None, caption="select folder", directory= "{}".format(os.path.expanduser("~/Desktop")))
        return folderpath

    def resetpath(self, LineE, LB):
        '''
        get new path
        rewrite new path in line editor
        get free space of new path
        rewrite free space in label
        '''
        newpath = self.openfolder()
        LineE.setText(newpath)
        LB.setText("Free space: {} G".format(self.getfreespace(newpath)))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MIBloader = QtWidgets.QDialog()
    ui = Ui_MIBloader()
    ui.setupUi(MIBloader)
    MIBloader.show()
    if MIBloader.exec_() == QtWidgets.QDialog.Accepted:
        url = ui.LE_source.text()
        savepath = ui.tempopath
        print(url)
        print(savepath)
        manager = DownloadManager()
        # manager.download("http://artefact-repo.mib3.technisat-digital/bob_0_19/6d/3a/db613623031c69b6b94457b51b3590b0c5cd5f01b1460f7d999fe4228dfff9fa91b58634d59a-1.tgz", "E:/Raspberry+pi+conf+files/GUI/test.tgz")
        manager.download(url, savepath)
 
    sys.exit(app.exec_())
