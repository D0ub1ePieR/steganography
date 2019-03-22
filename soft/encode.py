from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import os
from hashlib import md5
from script.dss import dss
from script import color, grey
from stego_res import stego_res


class encode_ui(object):
    def __init__(self):
        # 初始化隐写选择界面实例
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

        self.img = 0
        self.img_region = 0
        self.region_mat = 0
        self.text = 0
        self.password = 0
        self.filename = ''

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
        self.cover_preview.setGeometry(QtCore.QRect(20, 120, 261, 251))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.cover_preview.setFont(font)
        self.cover_preview.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cover_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.cover_preview.setObjectName("cover_preview")
        self.region_preview = QtWidgets.QLabel(Dialog)
        self.region_preview.setGeometry(QtCore.QRect(300, 120, 261, 251))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.region_preview.setFont(font)
        self.region_preview.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.region_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.region_preview.setObjectName("region_preview")
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
        self.line.setGeometry(QtCore.QRect(20, 420, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.cal_region = QtWidgets.QPushButton(Dialog)
        self.cal_region.setGeometry(QtCore.QRect(200, 390, 101, 31))
        self.cal_region.setObjectName("pushButton")
        self.pwd = QtWidgets.QLabel(Dialog)
        self.pwd.setGeometry(QtCore.QRect(700, 90, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Subheading")
        font.setPointSize(15)
        self.pwd.setFont(font)
        self.pwd.setObjectName("pwd")
        self.passwd = QtWidgets.QLineEdit(Dialog)
        self.passwd.setGeometry(QtCore.QRect(820, 100, 211, 20))
        self.passwd.setObjectName("passwd")
        self.infotable = QtWidgets.QTableView(Dialog)
        self.infotable.setGeometry(QtCore.QRect(620, 200, 511, 291))
        self.infotable.setObjectName("infotable")
        self.generate = QtWidgets.QPushButton(Dialog)
        self.generate.setGeometry(QtCore.QRect(820, 760, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(15)
        self.generate.setFont(font)
        self.generate.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(760, 150, 241, 31))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Encode"))
        self.label.setText(_translate("Dialog", "请选择目标图片"))
        self.cover_choose.setText(_translate("Dialog", "..."))
        self.cover_preview.setText(_translate("Dialog", "Preview"))
        self.region_preview.setText(_translate("Dialog", "Preview"))
        self.label_2.setText(_translate("Dialog", "请输入写入信息"))
        self.info_choose.setText(_translate("Dialog", "..."))
        self.cal_region.setText(_translate("Dialog", "计算显著区域"))
        self.pwd.setText(_translate("Dialog", "Paasword"))
        self.generate.setText(_translate("Dialog", "generate"))
        self.label_3.setText(_translate("Dialog", "图像信息"))

        self.cover_choose.clicked.connect(self.img_choose)
        self.cover_path.textChanged.connect(self.img_show)

        self.info_choose.clicked.connect(self.txt_choose)
        self.info_path.textChanged.connect(self.txt_show)

        self.passwd.textChanged.connect(self.set_passwd)
        self.cal_region.clicked.connect(self.cal_dss)
        self.generate.clicked.connect(self.embed)
        #self.cover_preview.setPixmap(QPixmap(self.cover_path.text()))

    # 选择图像地址
    def img_choose(self):
        filename, _ = QFileDialog().getOpenFileName(self.figure, 'choose cover', '../LSB/LSB1')
        self.cover_path.setText(filename)

    # 显示图像
    def img_show(self):
        filename = self.cover_path.text()
        try:
            img = QImage(filename)
            scale1 = self.cover_preview.height() / img.height()
            scale2 = self.cover_preview.width() / img.width()
            scale = min(scale1, scale2)
            self.cover_preview.setPixmap(QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
        except:
            self.cover_preview.setText('cannot open image')
            self.img = 0
            self.img_region = 0
            self.region_mat = 0
        else:
            self.img = 1

    # 选择文本地址
    def txt_choose(self):
        filename, _ = QFileDialog().getOpenFileName(self.figure, 'choose text', '../LSB/LSB1',)
        self.info_path.setText(filename)

    # 显示嵌入文本
    def txt_show(self):
        filename = self.info_path.text()
        try:
            f = open(filename, 'r')
            with f:
                data = f.read()
                self.info_preview.setText(data)
        except:
            self.info_preview.setText('cannot open file')
            self.text = 0
        else:
            self.text = 1

    # 设置密码
    def set_passwd(self):
        passwd = self.passwd.text()
        if passwd:
            self.password = 1
        else:
            self.password = 0

    # 计算显著性区域
    def cal_dss(self):
        if self.img != 1:
            QtWidgets.QMessageBox.information(self.figure, 'warning', '没有选择图像',
                                              QtWidgets.QMessageBox.Ok)
        else:
            try:
                cal = dss.dss(self.cover_path.text())
                cal.generate()
            except:
                QtWidgets.QMessageBox.information(self.figure, 'warning', '生成错误',
                                                  QtWidgets.QMessageBox.Ok)
            else:
                if cal.status == 0:
                    QtWidgets.QMessageBox.information(self.figure, 'warning', cal.msg,
                                                      QtWidgets.QMessageBox.Ok)
                else:
                    img = QImage(cal.res_path)
                    scale1 = self.region_preview.height() / img.height()
                    scale2 = self.region_preview.width() / img.width()
                    scale = min(scale1, scale2)
                    self.region_preview.setPixmap(
                        QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
                    self.img_region = 1
                    self.filename = cal.filename
                    tmp = os.popen("python ./script/res2mat.py " + cal.filename).read()
                    print(tmp)
                    if tmp[:7] != 'success':
                        QtWidgets.QMessageBox.information(self.figure, 'warning', tmp,
                                                          QtWidgets.QMessageBox.Ok)
                    else:
                        self.region_mat = 1

    # 嵌入
    def embed(self):
        res_window = stego_res(self.cover_path.text())
        res_window.figure.show()
        res_window.show()
        res_window.figure.exec_()

'''
        if self.img == 1 and self.img_region == 1 and self.region_mat == 1 and self.text == 1 and self.password == 1:
            tseed = md5()
            tseed.update(self.passwd.text().encode('utf-8'))
            seed = int(tseed.hexdigest()[:6], 16)
            if self.filename[-3:] in ['jpg', 'png', 'bmp']:
                steg = color.color_stego('hide-region', self.cover_path.text(), self.info_path.text(), seed)
            else:
                steg = grey.grey_stego('hide-region', self.cover_path.text(), self.info_path.text(), seed)
            try:
                steg.run()
            except:
                print(steg.msg)
            res_window = stego_res(self.cover_path)
            res_window.figure.show()
            res_window.show()
        else:
            note = ''
            QtWidgets.QMessageBox.information(self.figure, 'warning', note,
                                              QtWidgets.QMessageBox.Ok)
'''