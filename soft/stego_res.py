from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import os
from script.assess.assess import calculate


class stego_res(object):
    def __init__(self, cover_path, size, bit_num):
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window

        self.cover_path = cover_path
        index = cover_path.rfind('/')
        self.filename = cover_path[index + 1:]
        self.stego_path = './script/' + self.filename + '-stego.' + self.filename[-3:]
        self.assess_d = calculate(self.cover_path, self.stego_path)
        self.size = size
        self.bit_num = bit_num
        if self.filename[-3:] == 'pgm':
            self.set_table(5)
        else:
            self.set_table(7)

    def set_table(self, row):
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.setColumnCount(2)
        self.tableView.setRowCount(row)
        self.tableView.setColumnWidth(0, int(self.tableView.width() / 2) - 2)
        self.tableView.setColumnWidth(1, int(self.tableView.width() / 2) - 2)
        self.tableView.setItem(0, 0, QTableWidgetItem('image-size'))
        self.tableView.setItem(1, 0, QTableWidgetItem('embed-size'))
        self.tableView.setItem(2, 0, QTableWidgetItem('change-bit'))
        self.tableView.setItem(3, 0, QTableWidgetItem('psnr'))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(669, 559)
        self.cover = QtWidgets.QLabel(Dialog)
        self.cover.setGeometry(QtCore.QRect(30, 70, 181, 201))
        self.cover.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cover.setObjectName("cover")
        self.stego = QtWidgets.QLabel(Dialog)
        self.stego.setGeometry(QtCore.QRect(240, 70, 181, 201))
        self.stego.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stego.setObjectName("stego")
        self.sub = QtWidgets.QLabel(Dialog)
        self.sub.setGeometry(QtCore.QRect(450, 70, 181, 201))
        self.sub.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.sub.setObjectName("sub")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(510, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.save_as = QtWidgets.QPushButton(Dialog)
        self.save_as.setGeometry(QtCore.QRect(290, 290, 75, 23))
        self.save_as.setObjectName("save_as")
        self.tableView = QtWidgets.QTableWidget(Dialog)
        self.tableView.setGeometry(QtCore.QRect(30, 350, 601, 192))
        self.tableView.setObjectName("tableView")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 320, 91, 16))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cover.setText(_translate("Dialog", "Cover"))
        self.stego.setText(_translate("Dialog", "Stego"))
        self.sub.setText(_translate("Dialog", "Cover"))
        self.label.setText(_translate("Dialog", "cover"))
        self.label_2.setText(_translate("Dialog", "stego"))
        self.label_3.setText(_translate("Dialog", "diff"))
        self.save_as.setText(_translate("Dialog", "保存结果"))
        self.label_4.setText(_translate("Dialog", "图像信息"))

        self.save_as.clicked.connect(self.save_img)

    def save_img(self):
        filename, _ = QFileDialog().getSaveFileName(self.figure, 'save as', './stego.'+self.filename[-3:])
        try:
            img = Image.open(self.stego_path)
            img.save(filename)
        except:
            QtWidgets.QMessageBox.information(self.figure, 'warning', '保存失败',
                                              QtWidgets.QMessageBox.Ok)

    def show(self):
        img_cover = Image.open(self.cover_path)
        img_cover = img_cover.convert('RGB')
        img_stego = Image.open(self.stego_path)
        img_stego = img_stego.convert('RGB')
        (width, height) = img_stego.size
        img_sub = Image.new('RGB', (width, height))
        data = img_sub.getdata()
        for i in range(height):
            for j in range(width):
                (r1, g1, b1) = img_cover.getpixel((j, i))
                (r2, g2, b2) = img_stego.getpixel((j, i))
                data.putpixel((j, i), (abs(r1-r2)*255, abs(g1-g2)*255, abs(b1-b2)*255))
        img_sub.save('tmp.png')

        f = open(self.cover_path, 'rb')
        img = QImage.fromData(f.read())
        f.close()
        scale1 = self.cover.height() / img.height()
        scale2 = self.cover.width() / img.width()
        scale = min(scale1, scale2)
        self.cover.setPixmap(QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
        f = open(self.stego_path, 'rb')
        img = QImage.fromData(f.read())
        f.close()
        self.stego.setPixmap(QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
        f = open('tmp.png', 'rb')
        img = QImage.fromData(f.read())
        f.close()
        self.sub.setPixmap(QPixmap.fromImage(img.scaled(img.width() * scale, img.height() * scale)))
        os.popen('del tmp.png')

        self.tableView.setItem(0, 1, QTableWidgetItem(str(img.height())+'*'+str(img.width())))
        self.tableView.setItem(1, 1, QTableWidgetItem(str(self.size)))
        self.tableView.setItem(2, 1, QTableWidgetItem(str(self.bit_num)))
        self.tableView.setItem(3, 1, QTableWidgetItem(str(self.assess_d.get_psnr())))
        self.sp = self.assess_d.get_sp()
        if self.filename[-3:] == 'pgm':
            self.tableView.setItem(4, 0, QTableWidgetItem('sp_grey'))
            self.tableView.setItem(4, 1, QTableWidgetItem(str(self.sp['grey'])[:7]))
        else:
            self.tableView.setItem(4, 0, QTableWidgetItem('sp_r'))
            self.tableView.setItem(5, 0, QTableWidgetItem('sp_g'))
            self.tableView.setItem(6, 0, QTableWidgetItem('sp_b'))
            self.tableView.setItem(4, 1, QTableWidgetItem(str(self.sp['r'])[:7]))
            self.tableView.setItem(5, 1, QTableWidgetItem(str(self.sp['g'])[:7]))
            self.tableView.setItem(6, 1, QTableWidgetItem(str(self.sp['b'])[:7]))


