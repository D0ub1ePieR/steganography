from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
from hashlib import md5
from PIL import Image
from script.dss import dss
from script.color import color_stego
from script.grey import grey_stego
from script.ras import ras


class batch(object):
    def __init__(self):
        window = QtWidgets.QDialog()
        self.setupUi(window)
        self.figure = window
        self.figure.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(766, 585)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(40, 280, 691, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 81, 31))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 310, 81, 31))
        font = QtGui.QFont()
        font.setFamily("华文新魏")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 70, 71, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.encode_pack = QtWidgets.QLineEdit(Dialog)
        self.encode_pack.setGeometry(QtCore.QRect(40, 100, 271, 20))
        self.encode_pack.setObjectName("encode_pack")
        self.encode_choose = QtWidgets.QToolButton(Dialog)
        self.encode_choose.setGeometry(QtCore.QRect(330, 100, 37, 20))
        self.encode_choose.setObjectName("encode_choose")
        self.decode_choose = QtWidgets.QToolButton(Dialog)
        self.decode_choose.setGeometry(QtCore.QRect(330, 380, 37, 20))
        self.decode_choose.setObjectName("decode_choose")
        self.decode_pack = QtWidgets.QLineEdit(Dialog)
        self.decode_pack.setGeometry(QtCore.QRect(40, 380, 271, 20))
        self.decode_pack.setObjectName("decode_pack")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 350, 71, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.encode_list = QtWidgets.QListWidget(Dialog)
        self.encode_list.setGeometry(QtCore.QRect(460, 50, 251, 231))
        self.encode_list.setObjectName("encode_list")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(460, 20, 54, 12))
        self.label_5.setObjectName("label_5")
        self.decode_list = QtWidgets.QListWidget(Dialog)
        self.decode_list.setGeometry(QtCore.QRect(460, 340, 251, 231))
        self.decode_list.setObjectName("decode_list")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(460, 310, 54, 12))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(40, 170, 61, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.encode_pwd = QtWidgets.QLineEdit(Dialog)
        self.encode_pwd.setGeometry(QtCore.QRect(120, 170, 161, 20))
        self.encode_pwd.setObjectName("encode_pwd")
        self.encode_start = QtWidgets.QPushButton(Dialog)
        self.encode_start.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.encode_start.setObjectName("encode_start")
        self.decode_start = QtWidgets.QPushButton(Dialog)
        self.decode_start.setGeometry(QtCore.QRect(300, 530, 75, 23))
        self.decode_start.setObjectName("decode_start")
        self.decode_pwd = QtWidgets.QLineEdit(Dialog)
        self.decode_pwd.setGeometry(QtCore.QRect(120, 420, 161, 20))
        self.decode_pwd.setObjectName("decode_pwd")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(40, 420, 61, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(40, 140, 61, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.encode_text = QtWidgets.QLineEdit(Dialog)
        self.encode_text.setGeometry(QtCore.QRect(120, 140, 191, 20))
        self.encode_text.setObjectName("encode_text")
        self.text_choose = QtWidgets.QToolButton(Dialog)
        self.text_choose.setGeometry(QtCore.QRect(330, 140, 37, 20))
        self.text_choose.setObjectName("text_choose")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(40, 210, 71, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.encode_output = QtWidgets.QLineEdit(Dialog)
        self.encode_output.setGeometry(QtCore.QRect(120, 210, 161, 20))
        self.encode_output.setObjectName("encode_output")
        self.decode_output = QtWidgets.QLineEdit(Dialog)
        self.decode_output.setGeometry(QtCore.QRect(120, 460, 161, 20))
        self.decode_output.setObjectName("decode_output")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(40, 460, 71, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "batch process"))
        self.label.setText(_translate("Dialog", "嵌入"))
        self.label_2.setText(_translate("Dialog", "提取"))
        self.label_3.setText(_translate("Dialog", "选择文件夹"))
        self.encode_choose.setText(_translate("Dialog", "..."))
        self.decode_choose.setText(_translate("Dialog", "..."))
        self.label_4.setText(_translate("Dialog", "选择文件夹"))
        self.label_5.setText(_translate("Dialog", "文件列表"))
        self.label_6.setText(_translate("Dialog", "文件列表"))
        self.label_7.setText(_translate("Dialog", "Password"))
        self.encode_start.setText(_translate("Dialog", "start"))
        self.decode_start.setText(_translate("Dialog", "start"))
        self.label_8.setText(_translate("Dialog", "Password"))
        self.label_9.setText(_translate("Dialog", "嵌入文本"))
        self.text_choose.setText(_translate("Dialog", "..."))
        self.label_10.setText(_translate("Dialog", "输出文件夹"))
        self.label_11.setText(_translate("Dialog", "输出文件夹"))

        self.encode_choose.clicked.connect(self.choose_encode_pack)
        self.decode_choose.clicked.connect(self.choose_decode_pack)
        self.text_choose.clicked.connect(self.choose_text)
        self.encode_start.clicked.connect(self.encode)
        self.decode_start.clicked.connect(self.decode)

    def choose_encode_pack(self):
        pack_path = QFileDialog.getExistingDirectory(self.figure, '选择文件夹', './')
        self.encode_pack.setText(pack_path)
        if pack_path:
            self.encode_output.setText(pack_path + '/output')

    def choose_decode_pack(self):
        pack_path = QFileDialog.getExistingDirectory(self.figure, '选择文件夹', './')
        self.decode_pack.setText(pack_path)
        if pack_path:
            self.decode_output.setText(pack_path + '/output')

    def choose_text(self):
        filename, _ = QFileDialog.getOpenFileName(self.figure, '选择输出路径', './')
        self.encode_text.setText(filename)

    def calmat(self, path, filename):
        img = Image.open(path)
        img = img.convert('L')
        mat = open('./tmp/'+filename, 'w')
        (width, height) = img.size
        for i in range(height):
            for j in range(width):
                pix = img.getpixel((j, i))
                if pix < 100:
                    mat.write('0')
                else:
                    mat.write('1')
            mat.write('\n')
        mat.close()

    def encode(self):
        gui = QtGui.QGuiApplication.processEvents
        if os.system('cd .\\tmp') == 1:
            os.system('mkdir tmp')
        pack_path = self.encode_pack.text()
        t = os.system('mkdir ' + self.encode_output.text().replace('/', '\\'))
        filelist = []
        self.encode_list.clear()
        try:
            for pwd, subfolder, files in os.walk(pack_path):
                for file in files:
                    if len(file) > 4 and file[-4:] in ['.png', '.pgm']:
                        self.encode_list.addItem(file)
                        filelist.append(file)
                        gui()
        except:
            QtWidgets.QMessageBox.information(self.figure, 'warning', 'cannot open folder!',
                                              QtWidgets.QMessageBox.Ok)
        else:
            cal = ras.ras()
            for file in filelist:
                cal.set_path(pack_path+'/'+file, './tmp/'+file[:-4]+'.png')
                cal.generate()
                self.calmat(cal.res_path, cal.filename[:-4]+'.txt')
                gui()
                tseed = md5()
                tseed.update(self.encode_pwd.text().encode('utf-8'))
                seed = int(tseed.hexdigest()[:6], 16)
                if file[-3:] in ['png']:
                    steg = color_stego('hide-region', pack_path+'/'+file, self.encode_text.text(), seed)
                    steg.set_path(self.encode_output.text()+'/'+file, './tmp/'+file[:-4]+'.txt')
                else:
                    steg = grey_stego('hide-region', pack_path + '/' + file, self.encode_text.text(), seed)
                    steg.set_path(self.encode_output.text() + '/' + file, './tmp/' + file[:-4] + '.txt')
                try:
                    index = filelist.index(file)
                    steg.run()
                except:
                    self.encode_list.item(index).setText(file + '|' + steg.msg)
                else:
                    if steg.status == 1:
                        self.encode_list.item(index).setText(file + '|done')
                    else:
                        self.encode_list.item(index).setText(file + '|' + steg.msg)

    def decode(self):
        gui = QtGui.QGuiApplication.processEvents
        if os.system('cd .\\tmp') == 1:
            os.system('mkdir tmp')
        pack_path = self.decode_pack.text()
        t = os.system('mkdir ' + self.decode_output.text().replace('/', '\\'))
        filelist = []
        self.decode_list.clear()
        try:
            for pwd, subfolder, files in os.walk(pack_path):
                for file in files:
                    if len(file) > 4 and file[-4:] in ['.png', '.pgm']:
                        self.decode_list.addItem(file)
                        filelist.append(file)
                        gui()
        except:
            QtWidgets.QMessageBox.information(self.figure, 'warning', 'cannot open folder!',
                                              QtWidgets.QMessageBox.Ok)
        else:
            cal = ras.ras()
            for file in filelist:
                cal.set_path(pack_path+'/'+file, './tmp/'+file[:-4]+'.png')
                cal.generate()
                self.calmat(cal.res_path, cal.filename[:-4]+'.txt')
                gui()
                tseed = md5()
                tseed.update(self.decode_pwd.text().encode('utf-8'))
                seed = int(tseed.hexdigest()[:6], 16)
                if file[-3:] in ['png']:
                    steg = color_stego('extract-region', pack_path+'/'+file,
                                       pack_path + './output/' + file[:-4] + '.txt', seed)
                    steg.set_path(self.decode_output.text()+'/'+file, './tmp/'+file[:-4]+'.txt')
                else:
                    steg = grey_stego('extract-region', pack_path + '/' + file,
                                      pack_path + '/output/' + file[:-4] + '.txt', seed)
                    steg.set_path(self.decode_output.text() + '/' + file, './tmp/' + file[:-4] + '.txt')
                try:
                    index = filelist.index(file)
                    steg.run()
                except:
                    self.decode_list.item(index).setText(file + '|' + steg.msg)
                else:
                    if steg.status == 1:
                        self.decode_list.item(index).setText(file + '|done')
                    else:
                        self.decode_list.item(index).setText(file + '|' + steg.msg)
                        self.decode_list.item(index).setText(file + '|' + steg.msg)

