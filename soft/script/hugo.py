import os
from PIL import Image
import numpy
import struct
import matlab.engine

class hugo:
    def __init__(self, action, cover_path, info_path, region_type, seed):
        self.cover_path = cover_path
        self.info_path = info_path
        self.region_type = region_type
        self.seed = seed
        self.res_path = ''
        self.msg = ''
        self.mat_path = ''
        self.status = 0
        self.action = action
        self.payload_size = 0
        self.bit_num = 0
        #self.eng = matlab.engine.start_matlab('-nodesktop')

        index = self.cover_path.rfind('/')
        self.filename = self.cover_path[index + 1:]
        if action == 'hide':
            fid = open('tempfile.txt', 'w')
            fid.write(self.filename)
        else:
            fid = open('tempfile.txt', 'r')
            self.filename = fid.readline()

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
        img = Image.open(self.cover_path)
        (width, height) = img.size
        conv = img.convert("L").getdata()

        mat = []
        if self.mat_path == '':
            self.mat_path = './script/hugo/' + self.filename[:-4] + '.txt'
        file = open(self.mat_path, "r")
        for i in range(height):
            mat.append(file.readline())

        max_size = 0
        for j in range(width):
            for i in range(height):
                if mat[i][j] == str(self.region_type):
                    max_size = max_size + 1
        max_size = max_size / 8 / 1024

        f = open(self.info_path, "rb")
        data = f.read()
        f.close()
        v = self.decompose(data)
        while (len(v) % 3):
            v.append(0)

        payload_size = len(v) / 8 / 1024.0
        self.payload_size = payload_size
        # print("[+] Encrypted payload size: %.3f KB " % (payload_size))
        if (payload_size > max_size - 4 / 1024):
            self.status = 0
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
            #numpy.random.shuffle(random_array)

            for pix in random_array:
                (h, w) = (pix[0], pix[1])
                g = conv.getpixel((w, h))
                if idx < len(v):
                    if mat[h][w] == str(self.region_type) and g not in range(98, 102):
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
        img = Image.open(self.cover_path)
        (width, height) = img.size
        conv = img.convert("L").getdata()

        mat = []
        if self.mat_path == '':
            self.mat_path = './script/hugo/' + self.filename[:-4] + '.txt'
        file = open(self.mat_path, "r")
        for i in range(height):
            mat.append(file.readline())

        v = []
        numpy.random.seed(self.seed)
        random_array = []
        for h in range(height):
            for w in range(width):
                random_array.append([h, w])
        #numpy.random.shuffle(random_array)

        for pix in random_array:
            (h, w) = (pix[0], pix[1])
            if mat[h][w] == str(self.region_type) and conv.getpixel((w, h)) not in range(98, 102):
                g = conv.getpixel((w, h))
                v.append(g & 1)

        data_out = self.assemble(v)
        out_f = open(self.info_path, "wb")
        out_f.write(data_out)
        out_f.close()

    def run(self):
        file_size = 1024
        pwd = os.getcwd()
        #os.chdir('./script/hugo')
        if not os.path.exists('./script/hugo/'+self.filename[:-4]+'.txt'):
            self.eng.chdir('./script/hugo')
            self.eng.hugo(file_size, self.cover_path, nargout=0)
        # os.system('matlab -nojvm -nodesktop -nosplash -r hugo('+str(file_size)+',\''+self.cover_path+'\')')
        while not os.path.exists('./script/hugo/'+self.filename[:-4]+'.txt'):
            pass
        os.chdir(pwd)
        if self.action == 'hide':
            self.embed(0)
        else:
            self.extract(0)
        pass

