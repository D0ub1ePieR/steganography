import numpy as np
import math
import cv2


class psnr():
    def __init__(self, img1, img2):
        self.img1 = cv2.imread(img1)
        self.img2 = cv2.imread(img2)
        self.psnr = self.cal_psnr()

    def cal_psnr(self):
        mse = np.mean( (self.img1/255. - self.img2/255.) ** 2 )
        if mse < 1.0e-10:
            return 100
        PIXEL_MAX = 1
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    def get_psnr(self):
        return self.psnr
