import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.cm as cm
import scipy.misc
from PIL import Image
import scipy.io
import os
import sys
import caffe

class dss():
    def __init__(self, path=''):
        self.EPSILON = 1e-8
        # remove the following two lines if testing with cpu
        # caffe.set_mode_gpu()
        # choose which GPU you want to use
        # caffe.set_device(0)
        caffe.SGDSolver.display = 0
        self.net = caffe.Net('./script/dss/deploy.prototxt', './script/dss/dss_model_released.caffemodel', caffe.TEST)
        self.img_path = path
        self.filename = ''
        self.status = 0
        self.msg = ''
        self.img = ''
        self.res_path = ''

    def getimg(self):
        try:
            self.img = Image.open(self.img_path)
        except:
            self.status = 0
            self.msg = 'dss: cannot open file'
        else:
            self.status = 1
            index = self.img_path.rfind('/')
#            if index == -1:
#                index = 0
            self.filename = self.img_path[index+1:]
            # if self.filename[-3:] not in ['jpg', 'png', 'bmp', 'jpeg']:
            self.img = self.img.convert('RGB')

    def generate(self):
        self.getimg()
        if self.status == 1:
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
            out3 = self.net.blobs['sigmoid-dsn3'].data[0][0, :, :]
            out4 = self.net.blobs['sigmoid-dsn4'].data[0][0, :, :]
            out5 = self.net.blobs['sigmoid-dsn5'].data[0][0, :, :]
            fuse = self.net.blobs['sigmoid-fuse'].data[0][0, :, :]
            res = (out3 + out4 + out5 + fuse) / 4
            res = (res - np.min(res) + self.EPSILON) / (np.max(res) - np.min(res) + self.EPSILON)

            if self.res_path == '':
                self.res_path = './script/dss/' + self.filename[:-4] + '.png'
            plt.imsave(self.res_path, res, cmap=cm.Greys_r)

    def set_path(self, img_path, res_path):
        self.img_path = img_path
        self.res_path = res_path