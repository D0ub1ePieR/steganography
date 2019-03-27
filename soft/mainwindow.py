from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from steganography import *

class mainwindow_ui(object):
    def __init__(self):
        # 初始化主界面实例
        window = QMainWindow()
        self.setupUi(window)
        self.figure = window

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.steg = QtWidgets.QPushButton(self.centralwidget)
        self.steg.setGeometry(QtCore.QRect(130, 100, 171, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.steg.setFont(font)
        self.steg.setObjectName("steganoagraphy")
        self.task2 = QtWidgets.QPushButton(self.centralwidget)
        self.task2.setGeometry(QtCore.QRect(130, 180, 171, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.task2.setFont(font)
        self.task2.setObjectName("task2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "task"))
        self.steg.setText(_translate("MainWindow", "steganography"))
        self.task2.setText(_translate('MainWindow', 'task2'))

        # 按钮跳转
        self.steg.clicked.connect(self.jump_to_steg)

    def jump_to_steg(self):
        self.figure.hide()
        steg = steg_ui()
        steg.figure.exec_()
        self.figure.show()
