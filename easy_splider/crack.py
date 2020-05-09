#-*- coding:utf8 -*-
from PIL import  Image
import hashlib
import os
import math

class VectorCompare:
    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            # if concordance2.has_key(word):
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

# 加载训练集
def loads_train_sets( imageset ):
    iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    fileext=['.gif','.png']
    baseDir = './iconset'

    for letter in iconset:
        letterDir = os.path.join(baseDir, letter)
        for item in os.listdir(letterDir):
            basename,extname = os.path.splitext(item)
            if extname not in fileext:
                continue
            file = os.path.join(letterDir, item)
            # print(file)
            imageset.append({letter: buildvector(Image.open(file))})

imageset = []
loads_train_sets(imageset)

def verify_pic_convert(filename, letters):
    im = Image.open(filename)
    # 将图版转换为8位像素模式
    im.convert("P")

    # 打印颜色直方图
    # print(im.histogram())

    x = im.histogram()

    values = {}
    for i in range(256):
        values[i] = x[i]

    # for j,k in sorted(values.items(),key=lambda ax: ax[1],reverse=True)[:10]:
    #     print(j,k)

    im2 = Image.new("P", im.size, 255)

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            if pix == 220 or pix == 227:
                im2.putpixel((y, x), 0)

    inletter = False
    foundletter = False
    start = 0
    for x in range(im2.size[0]):
        for y in range(im2.size[1]):
            pix = im2.getpixel((x, y))
            if pix != 255:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = x
        if foundletter == True and inletter == False:
            foundletter = False
            end = x
            letters.append((start, end))

        inletter = False

    return im2
    # print(letters)
    #
    # print(im.size[0],im.size[1])
    # count = 0
    # for letter in letters:
    #     m = hashlib.md5()
    #     im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))
    #     str = "%s%s" % (time.time(),count)
    #     m.update(str.encode("utf8"))
    #     im3.save("temp\\%s.gif"%(m.hexdigest()))
    #     count+=1

def guss_verify_code(filename):
    global imageset
    v = VectorCompare()

    letters = []
    img = verify_pic_convert(filename, letters)

    for letter in letters:
        m = hashlib.md5()
        im3 = img.crop((letter[0],0,letter[1],img.size[1]))
        guess = []

        for image in imageset:
            for x,y in image.items():
                if len(y) != 0:
                    guess.append((v.relation(y, buildvector(im3)),x))

        guess.sort(reverse=True)

        yield guess[0]


if __name__ == "__main__":
    for i in guss_verify_code(r'D:\project\python\pylib\examples\p15jnd.gif'):
        print(i)
    for i in guss_verify_code(r'D:\project\python\pylib\examples\pin.png'):
        print(i)