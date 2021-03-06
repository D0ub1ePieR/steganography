import sys
import struct
import numpy
import matplotlib.pyplot as plt

from PIL import Image

class grey_stego:
    def __init__(self, action, image, payload, seed, type =1, flag=1):
        self.type = type
        self.flag = flag
        self.action = action
        self.image = image
        self.payload = payload
        self.bit_num = 0
        self.seed = seed
        self.status = 0
        self.msg = ''
        self.payload_size = 0
        self.info = {'image-size': [0, 0], 'usable-size': 0, 'payload-size': 0.0, 'extract-data': 0}
        index = self.image.rfind('/')
        self.filename = self.image[index + 1:]
        self.res_path = ''
        self.mat_path = ''

    def decompose(self, data):
        v = []
        # Pack file len in 4 bytes
        fSize = len(data)
        # print(fSize)
        bytes = [ord(chr(b)) for b in struct.pack("i", fSize)]
        bytes += [ord(chr(b)) for b in data]
        for b in bytes:
            for i in range(7, -1, -1):
                v.append((b >> i) & 0x1)
        return v

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

    def embed(self, flag):
        # Process source image
        try:
            img = Image.open(self.image)
        except:
            self.status = 0
            self.msg = 'cannot open file'
        else:
            (width, height) = img.size
            conv = img.convert("L").getdata()
            self.info['image-size'] = [width, height]

            # region
            if flag == 1 and flag == 0:
                mat = []
                if self.mat_path == '':
                    self.mat_path = './script/' + self.filename[:-4]+'.txt'
                file = open(self.mat_path, "r")
                for i in range(width):
                    mat.append(file.readline())

            if flag == 2:
                max_size = width * height / 8 / 1024  # max payload size
            else:
                max_size = 0
                for j in range(width):
                    for i in range(height):
                        if mat[i][j] == '1':
                            max_size = max_size + 1
                max_size = max_size / 8 / 1024
            self.info['usable-size'] = max_size

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
            # print("[+] Encrypted payload size: %.3f KB " % (payload_size))
            if (payload_size > max_size - 4 / 1024):
                self.status = 0
                self.msg = "[-] Cannot embed. File too large"
            else:
                # Create output image
                steg_img = Image.new('L', (width, height))
                data_img = steg_img.getdata()
                idx = 0
                numpy.random.seed(self.seed)
                random_array = []
                for h in range(height):
                    for w in range(width):
                        random_array.append([h, w])
                if flag == 1:
                    numpy.random.shuffle(random_array)

                for pix in random_array:
                    (h, w) = (pix[0], pix[1])
                    g = conv.getpixel((w, h))
                    if idx < len(v):
                        if (flag == 0 and mat[h][w] == str(self.type)) or (
                                flag == 1 and mat[h][w] == str(self.type) and g not in range(98, 102)):
                            tmp = g
                            g = self.set_bit(g, 0, v[idx])
                            if tmp != g:
                                self.bit_num += 1
                        else:
                            idx = idx - 1
                    data_img.putpixel((w, h), g)
                    idx = idx + 1
                if self.res_path == '':
                    self.res_path = './script/' + self.filename + "-stego.pgm"
                steg_img.save(self.res_path)
                self.status = 1

    def extract(self, flag):
        # Process source image
        try:
            img = Image.open(self.image)
        except:
            self.status = 0
            self.msg = 'cannot open file'
        else:
            (width, height) = img.size
            conv = img.convert("L").getdata()
            self.info['image-size'] = [width, height]
            # region
            if flag == 1 and flag == 0:
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

            for pix in random_array:
                (h, w) = (pix[0], pix[1])
                if (flag == 0 and mat[h][w] == str(self.type)) or (
                        mat[h][w] == str(self.type) and conv.getpixel((w, h)) not in range(98, 102)):
                    g = conv.getpixel((w, h))
                    v.append(g & 1)

            data_out = self.assemble(v)

            # Write decrypted data
            out_f = open(self.payload, "wb")
            out_f.write(data_out)
            out_f.close()

    def set_path(self, res_path, mat_path):
        self.res_path = res_path
        self.mat_path = mat_path

    def run(self):
        if self.action == 'hide':
            self.embed(0)
        elif self.action == 'hide-region':
            self.embed(self.flag)
        elif self.action == 'extract':
            self.extract(0)
        elif self.action == 'extract-region':
            self.extract(self.flag)