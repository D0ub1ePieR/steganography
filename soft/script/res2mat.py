import sys
from PIL import Image


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('input error\n')
        exit(-1)

    file = sys.argv[1]
    try:
        img = Image.open('./script/dss/' + file)
        img = img.convert('L')
        mat = open('./script/' + file[:-4] + '.txt', 'w')
    except:
        print('res2mat: cannot open file\n')
        exit(-1)
    else:
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
        print('success\n')