from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
import os
import cv2
import copy
from PIL import Image
from hashlib import md5
from script.dss import dss
from script import color, grey, hugo
from stego_res import stego_res


class encode_ui(object):
    def __init__(self):
        # 初始化隐写选择界面实例
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

        self.region_type = 1
        self.steg_type = 0
        self.img = 0
        self.img_region = 0
        self.region_mat = 0
        self.text = 0
        self.password = 0
        self.filename = ''
        self.set_infotable()

    def set_infotable(self):
        self.infotable.verticalHeader().setVisible(False)
        self.infotable.horizontalHeader().setVisible(False)
        self.infotable.setColumnCount(2)
        self.infotable.setRowCount(4)
        self.infotable.setColumnWidth(0, int(self.infotable.width() / 2) - 1)
        self.infotable.setColumnWidth(1, int(self.infotable.width() / 2) - 1)
        self.infotable.setItem(0, 0, QTableWidgetItem('image-size'))
        self.infotable.setItem(1, 0, QTableWidgetItem('image-type'))
        self.infotable.setItem(2, 0, QTableWidgetItem('embed max size'))
        self.infotable.setItem(3, 0, QTableWidgetItem('text size'))

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
        self.infotable = QtWidgets.QTableWidget(Dialog)
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

        self.check = QtWidgets.QCheckBox(Dialog)
        self.check.setGeometry(330, 390, 20, 20)
        self.check.setWindowTitle('Checkbox')
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(350, 380, 131, 41))
        self.label_4.setObjectName("label_3")

        self.combo = QtWidgets.QComboBox(Dialog)
        self.combo.setGeometry(QtCore.QRect(50, 390, 120, 35))
        self.combo.setObjectName('combo')
        self.combo.addItem('please choose')
        self.combo.addItem('dss')
        self.combo.addItem('...')

        self.c1c = QtWidgets.QCheckBox(Dialog)
        self.c2c = QtWidgets.QCheckBox(Dialog)
        self.c3c = QtWidgets.QCheckBox(Dialog)
        self.c4c = QtWidgets.QCheckBox(Dialog)
        self.c1t = QtWidgets.QLabel(Dialog)
        self.c2t = QtWidgets.QLabel(Dialog)
        self.c3t = QtWidgets.QLabel(Dialog)
        self.c4t = QtWidgets.QLabel(Dialog)
        self.c1c.setGeometry(QtCore.QRect(720, 550, 20, 20))
        self.c2c.setGeometry(QtCore.QRect(900, 550, 20, 20))
        self.c3c.setGeometry(QtCore.QRect(720, 600, 20, 20))
        self.c4c.setGeometry(QtCore.QRect(900, 600, 20, 20))
        self.c1t.setGeometry(QtCore.QRect(750, 550, 120, 20))
        self.c2t.setGeometry(QtCore.QRect(930, 550, 120, 20))
        self.c3t.setGeometry(QtCore.QRect(750, 600, 120, 20))
        self.c4t.setGeometry(QtCore.QRect(930, 600, 120, 20))
        self.c1c.setWindowTitle('c1c')
        self.c2c.setWindowTitle('c2c')
        self.c3c.setWindowTitle('c3c')
        self.c4c.setWindowTitle('c4c')
        self.c1t.setObjectName("c1t")
        self.c2t.setObjectName("c2t")
        self.c3t.setObjectName("c3t")
        self.c4t.setObjectName("c4t")

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
        self.pwd.setText(_translate("Dialog", "Password"))
        self.generate.setText(_translate("Dialog", "generate"))
        self.label_3.setText(_translate("Dialog", "图像信息"))
        self.label_4.setText(_translate('Dialog', '是否在反选区域隐写'))
        self.c1t.setText(_translate('Dialog', '不随机'))
        self.c2t.setText(_translate('Dialog', '随机'))
        self.c3t.setText(_translate('Dialog', 'HUGO'))
        self.c4t.setText(_translate('Dialog', 'nsF5'))

        self.cover_choose.clicked.connect(self.img_choose)
        self.cover_path.textChanged.connect(self.img_show)

        self.info_choose.clicked.connect(self.txt_choose)
        self.info_path.textChanged.connect(self.txt_show)

        self.passwd.textChanged.connect(self.set_passwd)
        self.cal_region.clicked.connect(self.cal_dss)
        self.generate.clicked.connect(self.embed)
        self.check.stateChanged.connect(self.set_type)
        self.c1c.stateChanged.connect(self.c1)
        self.c2c.stateChanged.connect(self.c2)
        self.c3c.stateChanged.connect(self.c3)
        self.c4c.stateChanged.connect(self.c4)
        #self.cover_preview.setPixmap(QPixmap(self.cover_path.text()))

    def set_type(self):
        if self.check.isChecked():
            self.region_type = 0
        else:
            self.region_type = 1

    def c1(self):
        if self.c1c.isChecked():
            self.steg_type = 1
        else:
            if self.steg_type == 1:
                self.steg_type = 0

    def c2(self):
        if self.c2c.isChecked():
            self.steg_type = 2
        else:
            if self.steg_type == 2:
                self.steg_type = 0

    def c3(self):
        if self.c3c.isChecked():
            self.steg_type = 3
        else:
            if self.steg_type == 3:
                self.steg_type = 0

    def c4(self):
        if self.c4c.isChecked():
            self.steg_type = 4
        else:
            if self.steg_type == 4:
                self.steg_type = 0

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
            self.infotable.setItem(0, 1, QTableWidgetItem(str(img.width()) + '*' + str(img.height())))
            if filename[-4:] == '.pgm':
                self.infotable.setItem(1, 1, QTableWidgetItem('grey'))
            else:
                self.infotable.setItem(1, 1, QTableWidgetItem('color'))
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
            self.infotable.setItem(3, 1, QTableWidgetItem(str(os.path.getsize(self.info_path.text()) / 1024) + 'KB'))
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
        if self.img != 1 or self.combo.currentIndex() == 0:
            QtWidgets.QMessageBox.information(self.figure, 'warning', '没有选择图像或显著性算法',
                                              QtWidgets.QMessageBox.Ok)
        else:
            try:
                if self.combo.currentIndex() == 1:
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
                        file = open('./script/'+cal.filename[:-4]+'.txt', 'r')
                        mat = []
                        max_size = 0
                        (width, height) = Image.open(cal.res_path).size
                        for i in range(height):
                            mat.append(file.readline())
                        for i in range(height):
                            for j in range(width):
                                if mat[i][j] == str(self.region_type):
                                    max_size = max_size + 1
                        max_size = max_size * 3.0 / 8 / 1024
                        self.infotable.setItem(2, 1, QTableWidgetItem(str(max_size)+'KB'))
                        file.close()
                        self.region_mat = 1

    # 嵌入
    def embed(self):
        if self.img == 1 and self.img_region == 1 and self.region_mat == 1 and self.text == 1 and self.password == 1 and self.steg_type != 0:
            tseed = md5()
            tseed.update(self.passwd.text().encode('utf-8'))
            seed = int(tseed.hexdigest()[:6], 16)
            path = self.cover_path.text()
            if self.steg_type in [1, 2]:
                if self.filename[-3:] in ['jpg', 'png', 'bmp']:
                    if self.region_type == 0:
                        img = cv2.imread(self.cover_path.text())
                        img2 = copy.copy(img)
                        img = cv2.GaussianBlur(img, (5,5), 1.5)
                        fid = open('./script/'+self.filename[:-4]+'.txt', 'r')
                        mat = []
                        t = ' '
                        while t:
                            t = fid.readline()
                            mat.append(t)
                        for i in range(img.shape[0]):
                            for j in range(img.shape[1]):
                                if mat[i][j] == '1' or (i in range(3, img.shape[0]-3) and j in range(3, img.shape[1]-3) and (
                                        mat[i-3][j-3] == '1' or mat[i-3][j+3] == '1' or mat[i+3][j-3] == '1' or mat[i+3][j+3] == '1')):
                                    img[i][j] = img2[i][j]
                        cv2.imwrite(self.filename, img)
                        pwd = os.getcwd()
                        path = pwd + '/' + self.filename
                    steg = color.color_stego('hide-region', path, self.info_path.text(), seed, self.region_type, self.steg_type-1)
                else:
                    steg = grey.grey_stego('hide-region', self.cover_path.text(), self.info_path.text(), seed, self.region_type, self.steg_type-1)
            elif self.steg_type == 3 and self.filename[-4:] == '.pgm':
                steg = hugo.hugo('hide', self.cover_path.text(), self.info_path.text(), self.region_type, seed)
            else:
                pass

            try:
                steg.run()
            except:
                QtWidgets.QMessageBox.information(self.figure, 'warning', 'stego fail',
                                                  QtWidgets.QMessageBox.Ok)
            else:
                res_window = stego_res(path, steg.payload_size, steg.bit_num)
                res_window.figure.show()
                res_window.show()
                res_window.figure.exec_()
        else:
            note = ''
            QtWidgets.QMessageBox.information(self.figure, 'warning', note,
                                              QtWidgets.QMessageBox.Ok)
