from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QSize

class encode_ui(object):
    def __init__(self):
        # 初始化隐写选择界面实例
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

        self.img = 0
        self.text = 0

    def setupUi(self, Dialog):
        # 隐写选择界面ui布局
        Dialog.setObjectName("Dialog")
        Dialog.resize(1167, 836)
        self.cover_path = QtWidgets.QLineEdit(Dialog)
        self.cover_path.setGeometry(QtCore.QRect(30, 70, 231, 20))
        self.cover_path.setObjectName("cover_path")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 161, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.cover_choose = QtWidgets.QToolButton(Dialog)
        self.cover_choose.setGeometry(QtCore.QRect(270, 70, 41, 21))
        self.cover_choose.setObjectName("cover_choose")
        self.cover_preview = QtWidgets.QLabel(Dialog)
        self.cover_preview.setGeometry(QtCore.QRect(40, 120, 261, 251))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.cover_preview.setFont(font)
        self.cover_preview.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cover_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.cover_preview.setObjectName("cover_preview")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 440, 161, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.info_path = QtWidgets.QLineEdit(Dialog)
        self.info_path.setGeometry(QtCore.QRect(30, 480, 231, 20))
        self.info_path.setObjectName("info_path")
        self.info_choose = QtWidgets.QToolButton(Dialog)
        self.info_choose.setGeometry(QtCore.QRect(270, 480, 41, 21))
        self.info_choose.setObjectName("info_choose")
        self.info_preview = QtWidgets.QTextBrowser(Dialog)
        self.info_preview.setGeometry(QtCore.QRect(40, 530, 461, 251))
        self.info_preview.setObjectName("info_preview")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 400, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Encode"))
        self.label.setText(_translate("Dialog", "请选择目标图片"))
        self.cover_choose.setText(_translate("Dialog", "..."))
        self.cover_preview.setText(_translate("Dialog", "Preview"))
        self.label_2.setText(_translate("Dialog", "请输入写入信息"))
        self.info_choose.setText(_translate("Dialog", "..."))

        self.cover_choose.clicked.connect(self.img_choose)
        self.info_choose.clicked.connect(self.txt_choose)
        #self.cover_preview.setPixmap(QPixmap(self.cover_path.text()))

    def img_choose(self):
        filename, _ = QFileDialog().getOpenFileName(self.figure, 'choose cover', '.')
        if filename:
            img = QImage(filename)
            scale1 = self.cover_preview.height() / img.height()
            scale2 = self.cover_preview.width() / img.width()
            scale = min(scale1, scale2)
            self.cover_path.setText(filename)
            self.cover_preview.setPixmap(QPixmap.fromImage(img.scaled(img.width()*scale, img.height()*scale)))
            self.img = 1

    def txt_choose(self):
        filename, _ = QFileDialog().getOpenFileName(self.figure, 'choose text', '.',)
        if filename:
            self.info_path.setText(filename)
            f = open(filename, 'r')
            with f:
                data = f.read()
                self.info_preview.setText(data)
            self.text = 1