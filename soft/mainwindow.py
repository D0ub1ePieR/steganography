from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from encode import *


class mainwindow_ui(object):
    def __init__(self):
        # 初始化主界面实例
        window = QMainWindow()
        self.setupUi(window)
        self.figure = window

    def setupUi(self, MainWindow):
        # ui界面布局
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.decode = QtWidgets.QPushButton(self.centralwidget)
        self.decode.setGeometry(QtCore.QRect(340, 180, 101, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.decode.setFont(font)
        self.decode.setObjectName("decode")
        self.encode = QtWidgets.QPushButton(self.centralwidget)
        self.encode.setGeometry(QtCore.QRect(130, 180, 101, 41))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.encode.setFont(font)
        self.encode.setObjectName("encode")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 330, 181, 16))
        self.label_2.setObjectName("label_2")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(470, 320, 75, 23))
        self.exit.setObjectName("exit")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "steganography"))
        self.label.setText(_translate("MainWindow", "选择你要进行的操作"))
        self.decode.setText(_translate("MainWindow", "decode"))
        self.encode.setText(_translate("MainWindow", "encode"))
        self.label_2.setText(_translate("MainWindow", "powered by:D0ub1ePieR"))
        self.exit.setText(_translate("MainWindow", "Exit"))

        # 按钮跳转
        self.encode.clicked.connect(self.jump_to_encode)
        self.decode.clicked.connect(self.jump_to_decode)
        self.exit.clicked.connect(self.jump_to_exit)

    def jump_to_exit(self):
        self.figure.close()

    def jump_to_encode(self):
        self.figure.hide()
        encode_window = encode_ui()
        encode_window.figure.show()
        encode_window.figure.exec_()
        self.figure.show()

    def jump_to_decode(self):
        self.figure.hide()