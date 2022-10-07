# -*- coding: utf-8 -*-


import Icons
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(340, 230)
        Form.setWindowIcon(QtGui.QIcon(":/Image/help.png"))
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LB_Contact = QtWidgets.QLabel(Form)
        self.LB_Contact.setObjectName("LB_Contact")
        self.gridLayout.addWidget(self.LB_Contact, 0, 0, 1, 1)
        self.LB_Name = QtWidgets.QLabel(Form)
        self.LB_Name.setOpenExternalLinks(True)
        self.LB_Name.setObjectName("LB_Name")
        self.gridLayout.addWidget(self.LB_Name, 0, 1, 1, 1)
        self.LB_Tutorial = QtWidgets.QLabel(Form)
        self.LB_Tutorial.setObjectName("LB_Tutorial")
        self.gridLayout.addWidget(self.LB_Tutorial, 1, 0, 1, 1)
        self.LB_TutorialLink = QtWidgets.QLabel(Form)
        self.LB_TutorialLink.setOpenExternalLinks(True)
        self.LB_TutorialLink.setObjectName("LB_TutorialLink")
        self.gridLayout.addWidget(self.LB_TutorialLink, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 321, 178))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "About USB Simulator"))
        self.LB_Contact.setText(_translate("Form", "Contact: "))
        self.LB_Name.setText(_translate("Form", "<a href='mailto:xiaochuan.lu@joynext.com'>Xiaochuan Lu</a> (SWTE)"))
        self.LB_Tutorial.setText(_translate("Form", "Tutorial:"))
        self.LB_TutorialLink.setText(_translate("Form", "<a href=\"https://git1.jnd.joynext.com/lu_x4/priapos/-/blob/master/README.md\">USB filesystem simulator</a>"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">Quick User Guide:</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">1</span>. configure wpa_supplicant and write wpa_supplicant and ssh into boot folder SD card (only necessary if the WiFi was changed, default: AMB-StreamWLAN).</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">2</span>. power and data transfer via OTG cabel Paspberry Pi Zero W (USB port). Sometimes to power Paspi only vie USB port ist not enough, in this case PWR port could be used to power it and USB port to transfer data.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">3</span>. plugin in USB  TP-link WiFi receiver (only necessary: if your computer does not have a WiFi unit, this means that the computer cannot detect the existing WiFi)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">4</span>. click <span style=\" font-weight:600;\">Anpassen </span>with gear icon to set up putty configuration, watchdog and samba service are usually not nessary if you dont want to modify file in each USB filesystem.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">5</span>. select one of the supported filesystems in combobox and click <span style=\" font-weight:600;\">Connect.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">6</span>. in order to change filesystem only need to pick another filesystem from combobox and click <span style=\" font-weight:600;\">Connect</span>, to click disconnect first  is not nessary becasue it is automatic.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">7</span>. send value or commad to putty via GUI is auch possible.</p></body></html>"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())
