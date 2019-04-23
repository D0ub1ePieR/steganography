import numpy as np
import math
import cv2
from PIL import Image


class calculate():
    def __init__(self, img1, img2):
        if img2[-3:] == 'pgm':
            self.type = 0
        else:
            self.type = 1
        self.stego = img2
        self.img1 = cv2.imread(img1)
        self.img2 = cv2.imread(img2)
        self.psnr = 100
        self.sp = {'r': 0, 'g': 0, 'b': 0, 'grey': 0}
        self.cal()

    def cal_psnr(self):
        mse = np.mean( (self.img1/255. - self.img2/255.) ** 2 )
        if mse < 1.0e-10:
            return 100
        PIXEL_MAX = 1
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    def get_psnr(self):
        return self.psnr

    def cal_sp(self):

        def sp(mat):
            (m, n) = mat.shape
            u = mat[:, 0:n-1]
            v = mat[:, 1:]
            '''
                X = { (u,v) | v even u<v or v odd u>v}
                Z = { (u,v) | u = v}
                W = { (u,v) | (u = 2k and v = 2k+1) or (u = 2k+1 and v = 2k)}
            '''
            xc = len(np.nonzero(((np.mod(v, 2) == 0) & (u < v)) | ((np.mod(v, 2) == 1) & (u > v)))[0])
            zc = len(np.nonzero(u == v)[0])
            t1 = np.floor(u / 2) == np.floor(v / 2)
            t2 = u != v
            wc = len(np.nonzero(t1 & t2)[0])
            vc = m * (n-1) - (xc + zc + wc)
            a = (wc + zc)/2
            b = 2 * xc - m * (n-1)
            c = vc + wc - xc
            d = b * b - 4 * a * c
            if a > 0:
                p1 = (-b + math.sqrt(d)) / (2 * a)
                p2 = (-b - math.sqrt(d)) / (2 * a)
            else:
                p1 = p2 = -1
            return min(p1, p2)

        if self.type == 1:
            img = np.asarray(Image.open(self.stego))
            r = img[:, :, 0]
            g = img[:, :, 1]
            b = img[:, :, 2]
            self.sp['r'] = sp(r)
            self.sp['g'] = sp(g)
            self.sp['b'] = sp(b)
        else:
            grey = self.img2
            self.sp['grey'] = sp(grey)

    def get_sp(self):
        return self.sp

    def cal(self):
        self.psnr = self.cal_psnr()
        self.cal_sp()