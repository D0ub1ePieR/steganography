import numpy as np
from PIL import Image
import os
import caffe
import cv2

class ras():
    def __init__(self, path=''):
        self.EPSILON = 1e-8
        # remove the following two lines if testing with cpu
        caffe.set_mode_gpu()
        # choose which GPU you want to use
        caffe.set_device(0)
        caffe.SGDSolver.display = 0
        # load net
        self.net = caffe.Net('./script/ras/deploy.prototxt', './script/ras/ras_iter_10000.caffemodel', caffe.TEST)
        self.img_path = path
        self.filename = ''
        self.status = 0
        self.msg = ''
        self.img = ''
        self.res_path = ''

    def get_img(self):
        try:
            self.img = Image.open(self.img_path)
        except:
            self.status = 0
            self.msg = 'ras: cannot open file'
        else:
            self.status = 1
            index = self.img_path.rfind('/')
            self.filename = self.img_path[index + 1:]
            self.img = self.img.convert('RGB')

    def generate(self):
        self.get_img()
        if self.status == 1:
            if os.path.exists('./script/ras/' + self.filename[:-4] + '.png'):
                self.res_path = './script/ras/' + self.filename[:-4] + '.png'
                return
            self.img = np.array(self.img, dtype=np.uint8)
            im = np.array(self.img, dtype=np.float32)
            im = im[:, :, ::-1]
            im -= np.array((104.00698793, 116.66876762, 122.67891434))
            im = im.transpose((2, 0, 1))

            # shape for input (data blob is N x C x H x W), set data
            self.net.blobs['data'].reshape(1, *im.shape)
            self.net.blobs['data'].data[...] = im

            # run net and take argmax for prediction
            self.net.forward()
            res = self.net.blobs['sigmoid-score1'].data[0][0, :, :]

            # normalization
            res = (res - np.min(res) + self.EPSILON) / (np.max(res) - np.min(res) + self.EPSILON)
            res = 255 * res

            if self.res_path == '':
                self.res_path = './script/ras/' + self.filename[:-4] + '.png'
            cv2.imwrite(self.res_path, res)

    def set_path(self, img_path, res_path):
        self.img_path = img_path
        self.res_path = res_path
