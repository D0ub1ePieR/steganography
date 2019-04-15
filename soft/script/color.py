import sys
import struct
import numpy
import matplotlib.pyplot as plt

from PIL import Image

class color_stego:
    def __init__(self, action, image, payload, seed, type =1, flag =1):
        self.type = type    # 在显著区域或取反区域隐写
        self.flag = flag    # 是否随机
        self.action = action    # 操作 嵌入或提取
        self.image = image  # 图像地址
        self.payload = payload  # 嵌入信息地址
        self.seed = seed    # 随机数种子
        self.status = 0     # 嵌入状态
        self.bit_num = 0    # 修改bit数目
        self.msg = ''       # 返回状态信息
        self.payload_size = 0   # 嵌入信息大小
        self.info = {'image-size': [0, 0], 'usable-size': 0, 'payload-size': 0.0, 'extract-data': 0}    # 图像信息
        index = self.image.rfind('/')
        self.filename = self.image[index + 1:]      # 图像文件名
        self.res_path = ''      # 结果存放地址
        self.mat_path = ''      # 显著性矩阵存放地址

    # 将嵌入信息转换为二进制序列
    def decompose(self, data):
        v = []
        # Pack file len in 4 bytes
        fSize = len(data)
        bytes = [ord(chr(b)) for b in struct.pack("i", fSize)]      # 在序列初始添加信息长度,以4字节存储
        bytes += [ord(chr(b)) for b in data]
        for b in bytes:
            for i in range(7, -1, -1):
                v.append((b >> i) & 0x1)
        return v

    # 从图像所有的最低有效位序列中提取出嵌入信息
    def assemble(self, v):
        bytess = ""
        length = len(v)
        for idx in range(0, len(v) // 8):
            byte = 0
            for i in range(0, 8):
                if (idx * 8 + i < length):
                    byte = (byte << 1) + v[idx * 8 + i]
            bytess = bytess + chr(byte)
        payload_size = 0
        for i in range(4):
            payload_size = payload_size + pow(256, i) * ord(bytess[i])
        self.payload_size = payload_size

        return bytes(bytess[4: payload_size + 4], encoding='utf-8')

    # Set the i-th bit of v to x
    def set_bit(self, n, i, x):
        mask = 1 << i
        n &= ~mask
        if x:
            n |= mask
        return n

    # 嵌入
    def embed(self, flag):
        # Process source image
        try:
            img = Image.open(self.image)
        except:
            self.status = 0
            self.msg = 'color_steg: cannot open file'
        else:
            (width, height) = img.size
            conv = img.convert("RGBA").getdata()
            self.info['image-size'] = [width, height]

            # region
            # 读取显著性区域矩阵
            if flag == 1 or flag == 0:
                mat = []
                if self.mat_path == '':
                    self.mat_path = './script/' + self.filename[:-4]+'.txt'
                file = open(self.mat_path, "r")
                for i in range(height):
                    mat.append(file.readline())

            # 计算最大嵌入信息长度
            if flag == 2:
                max_size = width * height * 3.0 / 8 / 1024  # max payload size
            else:
                max_size = 0
                for j in range(width):
                    for i in range(height):
                        if mat[i][j] == str(self.type):
                            max_size = max_size + 1
                max_size = max_size * 3.0 / 8 / 1024
            self.info['usable-size'] = max_size

            # 读取嵌入信息
            f = open(self.payload, "rb")
            data = f.read()
            f.close()
            self.info['payload-size'] = len(data) / 1024.0

            # Process data from payload file
            v = self.decompose(data)

            # Add until multiple of 3
            while (len(v) % 3):
                v.append(0)

            payload_size = len(v) / 8 / 1024.0
            self.payload_size = payload_size
            # print("[+] Encrypted payload size: %.3f KB " % (payload_size))
            # 嵌入信息,并判断提供图像是否能够满足嵌入
            if (payload_size > max_size - 4 / 1024):
                self.status = 0
                self.msg = "[-] Cannot embed. File too large"
            else:
                # Create output image
                steg_img = Image.new('RGBA', (width, height))
                data_img = steg_img.getdata()
                idx = 0
                # 根据密码生成随机数种子并生成随机矩阵
                numpy.random.seed(self.seed)
                random_array = []
                for h in range(height):
                    for w in range(width):
                        random_array.append([h, w])
                if flag == 1:
                    numpy.random.shuffle(random_array)

                # 对于取反区域模糊后的嵌入,判断是否为区域边缘
                def checkpix(h, w):
                    r = 15
                    if h not in range(r, height-r) or w not in range(r, width-r):
                        return True
                    else:
                        for i in range(-r, r+1):
                            for j in range(-r, r+1):
                                if mat[h+i][h+j] == '1':
                                    return False
                    return True

                # 嵌入
                for pix in random_array:
                    (h, w) = (pix[0], pix[1])
                    (r, g, b, a) = conv.getpixel((w, h))
                    if idx < len(v):
                        if (flag == 0 and mat[h][w] == str(self.type)) or (flag == 1 and mat[h][w] == str(self.type) and r not in range(98, 102)):
                            if self.type == 0 and not checkpix(h, w):
                                data_img.putpixel((w, h), (r, g, b, a))
                                continue
                            tmp = (r, g, b)
                            r = self.set_bit(r, 0, v[idx])
                            g = self.set_bit(g, 0, v[idx + 1])
                            b = self.set_bit(b, 0, v[idx + 2])
                            if tmp != (r, g, b):
                                self.bit_num += 1
                        else:
                            idx = idx - 3
                    data_img.putpixel((w, h), (r, g, b, a))
                    idx = idx + 3
                # 如果没有给定结果地址,则采用默认地址
                if self.res_path == '':
                    self.res_path = './script/' + self.filename + "-stego." + self.filename[-3:]
                steg_img.save(self.res_path)
                self.status = 1

    # 提取信息
    def extract(self, flag):
        # Process source image
        try:
            img = Image.open(self.image)
        except:
            self.status = 0
            self.msg = 'color_steg: cannot open file'
        else:
            (width, height) = img.size
            conv = img.convert("RGBA").getdata()
            self.info['image-size'] = [width, height]
            # region
            if flag == 1 or flag == 0:
                mat = []
                if self.mat_path == '':
                    self.mat_path = './script/' + self.filename[:-4]+'.txt'
                file = open(self.mat_path, "r")
                for i in range(height):
                    mat.append(file.readline())
            # Extract LSBs
            v = []
            numpy.random.seed(self.seed)
            random_array = []
            for h in range(height):
                for w in range(width):
                    random_array.append([h, w])

            if flag == 1:
                numpy.random.shuffle(random_array)

            def checkpix(h, w):
                r = 15
                if h not in range(r, height - r) or w not in range(r, width - r):
                    return True
                else:
                    for i in range(-r, r + 1):
                        for j in range(-r, r + 1):
                            if mat[h+i][h+j] == '1':
                                return False
                return True

            for pix in random_array:
                (h, w) = (pix[0], pix[1])
                if (flag == 0 and mat[h][w] == str(self.type)) or (flag == 1 and mat[h][w] == str(self.type) and conv.getpixel((w, h))[0] not in range(98, 102)):
                    if self.type == 0 and not checkpix(h, w):
                        continue
                    (r, g, b, a) = conv.getpixel((w, h))
                    v.append(r & 1)
                    v.append(g & 1)
                    v.append(b & 1)

            data_out = self.assemble(v)

            # Write decrypted data
            out_f = open(self.payload, "wb")
            out_f.write(data_out)
            out_f.close()
            self.status = 1

    def set_path(self, res_path, mat_path):
        self.res_path = res_path
        self.mat_path = mat_path

    # 执行
    def run(self):
        if self.action == 'hide-region':
            self.embed(self.flag)
        elif self.action == 'extract-region':
            self.extract(self.flag)