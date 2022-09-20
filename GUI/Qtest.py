import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QToolBar


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # set GUI icon
        self.setWindowIcon(QtGui.QIcon("GUI/Image/AppIcon.png"))
        self.setWindowTitle("Hello World")
        self.button = QtWidgets.QPushButton("My button")

        # icon = QtGui.QIcon("GUI/Image/AppIcon.png")
        # self.button.setIcon(icon)
        self.button.clicked.connect(self.change_icon)
        toolbar = QToolBar("My main toolbar")

        self.setCentralWidget(self.button)

        self.show()

    def change_icon(self):
        icon = QtGui.QIcon("animal-monkey.png")
        self.button.setIcon(icon)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
