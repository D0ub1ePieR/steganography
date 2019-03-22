from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from script.dss import dss
import os, hashlib
from script import color, grey

class decode_ui(object):
    def __init__(self):
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

        self.img = 0
        self.img_region = 0
        self.region_mat = 0
        self.password = 0
        self.result = 0
        self.filename = ''

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1167, 541)
        self.stego_path = QtWidgets.QLineEdit(Dialog)
        self.stego_path.setGeometry(QtCore.QRect(40, 70, 231, 20))
        self.stego_path.setObjectName("stego_path")
        self.stego_choose = QtWidgets.QToolButton(Dialog)
        self.stego_choose.setGeometry(QtCore.QRect(280, 70, 41, 21))
        self.stego_choose.setObjectName("stego_choose")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 161, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.stego_preview = QtWidgets.QLabel(Dialog)
        self.stego_preview.setGeometry(QtCore.QRect(30, 110, 261, 251))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.stego_preview.setFont(font)
        self.stego_preview.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stego_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.stego_preview.setObjectName("stego_preview")
        self.cal_region = QtWidgets.QPushButton(Dialog)
        self.cal_region.setGeometry(QtCore.QRect(250, 380, 101, 31))
        self.cal_region.setObjectName("cal_region")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(30, 430, 541, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.stego_region = QtWidgets.QLabel(Dialog)
        self.stego_region.setGeometry(QtCore.QRect(310, 110, 261, 251))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.stego_region.setFont(font)
        self.stego_region.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stego_region.setAlignment(QtCore.Qt.AlignCenter)
        self.stego_region.setObjectName("stego_region")
        self.passwd = QtWidgets.QLineEdit(Dialog)
        self.passwd.setGeometry(QtCore.QRect(160, 480, 211, 20))
        self.passwd.setObjectName("passwd")
        self.pwd = QtWidgets.QLabel(Dialog)
        self.pwd.setGeometry(QtCore.QRect(40, 470, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Subheading")
        font.setPointSize(15)
        self.pwd.setFont(font)
        self.pwd.setObjectName("pwd")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(640, 20, 101, 41))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.info = QtWidgets.QTextBrowser(Dialog)
        self.info.setGeometry(QtCore.QRect(640, 70, 471, 381))
        self.info.setObjectName("info")
        self.save_as = QtWidgets.QPushButton(Dialog)
        self.save_as.setGeometry(QtCore.QRect(880, 480, 75, 23))
        self.save_as.setObjectName("save_as")
        self.decode = QtWidgets.QPushButton(Dialog)
        self.decode.setGeometry(QtCore.QRect(430, 480, 75, 23))
        self.decode.setObjectName("decode")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "decode"))
        self.stego_choose.setText(_translate("Dialog", "..."))
        self.label.setText(_translate("Dialog", "请选择图片"))
        self.stego_preview.setText(_translate("Dialog", "Preview"))
        self.cal_region.setText(_translate("Dialog", "计算显著区域"))
        self.stego_region.setText(_translate("Dialog", "Preview"))
        self.pwd.setText(_translate("Dialog", "Paasword"))
        self.label_2.setText(_translate("Dialog", "Data"))
        self.save_as.setText(_translate("Dialog", "保存结果"))
        self.decode.setText(_translate("Dialog", "解码"))

        self.stego_choose.clicked.connect(self.img_choose)
        self.stego_path.textChanged.connect(self.img_show)
        self.cal_region.clicked.connect(self.cal_dss)
        self.passwd.textChanged.connect(self.set_passwd)
        self.decode.clicked.connect(self.extract)
        self.save_as.clicked.connect(self.save_text)

    def img_choose(self):
        filename, _ = QFileDialog().getOpenFileName(self.figure, 'choose cover', '../LSB/LSB1')
        self.stego_path.setText(filename)

    # 显示图像
    def img_show(self):
        filename = self.stego_path.text()
        try:
            img = QImage(filename)
            scale1 = self.stego_preview.height() / img.height()
            scale2 = self.stego_preview.width() / img.width()
            scale = min(scale1, scale2)
            self.stego_preview.setPixmap(QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
        except:
            self.stego_preview.setText('cannot open image')
            self.img = 0
            self.img_region = 0
        else:
            self.img = 1

    def cal_dss(self):
        if self.img != 1:
            QtWidgets.QMessageBox.information(self.figure, 'warning', '没有选择图像',
                                              QtWidgets.QMessageBox.Ok)
        else:
            try:
                cal = dss.dss(self.stego_path.text())
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
                    scale1 = self.stego_region.height() / img.height()
                    scale2 = self.stego_region.width() / img.width()
                    scale = min(scale1, scale2)
                    self.stego_region.setPixmap(
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

    def set_passwd(self):
        passwd = self.passwd.text()
        if passwd:
            self.password = 1
        else:
            self.password = 0

    def extract(self):
        if self.img == 1 and self.img_region == 1 and self.region_mat == 1 and self.password == 1:
            tseed = hashlib.md5()
            tseed.update(self.passwd.text().encode('utf-8'))
            seed = int(tseed.hexdigest()[:6], 16)
            if self.filename[-3:] in ['jpg', 'png', 'bmp']:
                steg = color.color_stego('extract-region', self.stego_path.text(), 'tmp.txt', seed)
            else:
                steg = grey.grey_stego('extract-region', self.stego_path.text(), 'tmp.txt', seed)
            try:
                steg.run()
            except:
                print(steg.msg)
            else:
                f = open('tmp.txt', 'r')
                with f:
                    data = f.read()
                    self.info.setText(data)
                self.result = 1
        else:
            note = ''
            QtWidgets.QMessageBox.information(self.figure, 'warning', note,
                                              QtWidgets.QMessageBox.Ok)

    def save_text(self):
        if self.result == 1:
            filename, _ = QFileDialog().getSaveFileName(self.figure, 'save as', './result.txt')
            if filename:
                tmp = os.popen(('copy tmp.txt ' + filename).replace('/', '\\')).read()
                print('copy tmp.txt ' + filename)
                print(tmp)
                if len(tmp) != 19:
                    QtWidgets.QMessageBox.information(self.figure, 'warning', '保存失败',
                                                      QtWidgets.QMessageBox.Ok)
                else:
                    os.popen('del tmp.txt')
                    QtWidgets.QMessageBox.information(self.figure, 'warning', '保存成功',
                                                      QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self.figure, 'warning', '无内容',
                                              QtWidgets.QMessageBox.Ok)