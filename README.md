# steganography
Steganographic Algorithms
# LSB
* LSB1 </br>
    存储嵌入信息长度：4字节 </br>
    Usage：</br>
    * encode </br>
        ***`python lsb.py hide [src img] [info file] [password]`*** </br>
        ***`python lsb.py hide-regin [src img] [info file] [password]`*** </br>
        ***`python lsb.py hide-random [src img] [info file] [password]`***
        ```
        在max.txt中存储M*N个0或1的字符表示目标图片中哪些像素可以取到用于隐写
    * decode</br>
        ***`python lsb.py extract [encode img] [output file] [password]`*** </br>
        ***`python lsb.py extract-regin [src img] [output file] [password]`***
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

# nsF5
```
对于JPEG格式图片，进行在DCT系数中的隐写，利用非0的DCT系数，随机选取的模拟程序
```
* encode </br>
运行**test.m**或执行
***`nsf5_simulation(COVER,STEGO,ALPHA,SEED)`***

    * cover为原图路径
    * stego为结果图像存放路劲
    * alpha为隐写系数，即利用多少可用隐写空间
    * seed为模拟中伪随机数生成种子
    * 在mat.txt中存入目标范围的01矩阵并将代码修改为(目前只支持限制DCT范围，还为装载根据矩阵限定范围)
    ``` matlab
    24    - nzAC = nnz(DCT)-nnz(DCT(1:8:end,1:8:end)); % number of nonzero AC DCT coefficients
    25    + nzAC = nnz(DCT)-nnz(DCT(1:8:end,1:8:end))-nnz(DCT(DCT<2));
    29    + % changeable(find(abs(DCT)<2)) = 0
    ```

* decode </br>
由于使用的是simulation，所以不能解码出所隐写部分的内容

# HUGO
