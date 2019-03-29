from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from encode import *
from decode import *

class single_img(object):
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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "steganography"))
        self.decode.setText(_translate("Dialog", "decode"))
        self.encode.setText(_translate("Dialog", "encode"))
        self.label.setText(_translate("Dialog", "对单张图片进行操作"))

        # 按钮跳转
        self.encode.clicked.connect(self.jump_to_encode)
        self.decode.clicked.connect(self.jump_to_decode)

    def jump_to_encode(self):
        # self.figure.hide()
        encode_window = encode_ui()
        # encode_window.figure.show()
        encode_window.figure.exec_()
        self.cleanfile()
        # self.figure.show()

    def jump_to_decode(self):
        # self.figure.hide()
        decode_window = decode_ui()
        decode_window.figure.exec_()
        self.cleanfile()
        # self.figure.show()

    def cleanfile(self):
        os.system('del *.txt')
        os.system('del *.png')
        os.system('del *.pgm')
        os.system('del .\script\*.txt')
        os.system('del .\script\*.png')
        os.system('del .\script\*.pgm')
        os.system('del .\script\dss\*.txt')
        os.system('del .\script\dss\*.png')
        os.system('del .\script\dss\*.pgm')