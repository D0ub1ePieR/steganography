from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from single_img import *
from batch import *


class steg_ui(object):
    def __init__(self):
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

    def setupUi(self, Dialog):
        # ui界面布局
        Dialog.setObjectName("Dialog")
        Dialog.resize(560, 396)
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 251, 101))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 330, 181, 16))
        self.label_2.setObjectName("label_2")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(470, 320, 75, 23))
        self.exit.setObjectName("exit")

        self.single = QtWidgets.QPushButton(self.centralwidget)
        self.single.setGeometry(QtCore.QRect(190, 120, 171, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.single.setFont(font)
        self.single.setObjectName("single")

        self.bat = QtWidgets.QPushButton(self.centralwidget)
        self.bat.setGeometry(QtCore.QRect(190, 240, 171, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.bat.setFont(font)
        self.bat.setObjectName("bat")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "steganography"))
        self.label.setText(_translate("Dialog", "选择你要进行的操作"))
        self.label_2.setText(_translate("Dialog", "powered by:D0ub1ePieR"))
        self.exit.setText(_translate("Dialog", "Exit"))
        self.single.setText(_translate('Dialog', 'single process'))
        self.bat.setText(_translate('Dialog', 'batch process'))

        # 按钮跳转
        self.exit.clicked.connect(self.jump_to_exit)
        self.single.clicked.connect(self.jump_to_single)
        self.bat.clicked.connect(self.jump_to_bat)

    def jump_to_exit(self):
        self.figure.close()

    def jump_to_bat(self):
        #self.figure.hide()
        batch_window = batch()
        batch_window.figure.exec_()
        #self.figure.show()

    def jump_to_single(self):
        #self.figure.hide()
        single_window = single_img()
        single_window.figure.exec_()
        #self.figure.show()