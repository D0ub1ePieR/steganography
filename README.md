# steganography
Steganographic Algorithms
# LSB
* LSB1 </br>
    存储嵌入信息长度：4字节 </br>
    Usage：</br>
    * encode </br>
        ***`python lsb.py hide [src img] [info file] [password]`***
    * decode</br>
        ***`python lsb.py extract [encode img] [output file] [password]`***
    * analyse </br>
        ***`python lsb.py analyse [encode img]`***
* LSB2
    存储嵌入信息长度：2字节 </br>
    Usage：</br>
    * encode text </br>
        ***`steg = LSBSteg(cv2.imread("my_image.png"))`*** </br>
        ***`img_encoded = steg.encode_text("my message")`*** </br>
        ***`cv2.imwrite("my_new_image.png", img_encoded)`***
    * decode text </br>
        ***`im = cv2.imread("my_new_image.png")`*** </br>
        ***`steg = LSBSteg(im)</br>print("Text value:",steg.decode_text())`***
