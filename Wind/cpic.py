import cv2
import os
import numpy as np

# 图片处理 默认读屏

class pic:
    def __init__(self, fname=None,slice=None):
        if fname:
            if len(fname) <= 1:
                self.img=None
            else:
                self.img = cv2.imread('pic/'+fname)
                    
        else:
            os.system('getwind.exe')
            self.img = cv2.imread('buffer.bmp')
        if slice:
            x1 = slice[0]
            x2 = slice[1]
            y1 = slice[2]
            y2 = slice[3]
            self.img = self.img[x1:x2,y1:y2]


    def show(self):
        cv2.imshow('w', self.img)
        cv2.waitKey(0)

    # 返回像素相似度
    def compare(self, other):
        try:
            other = other.img
        except AttributeError:
            pass
        img = self.img
        try:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            other=cv2.cvtColor(other, cv2.COLOR_BGR2GRAY)
        except :
            pass

        if img.shape != other.shape:
            other = other[0:img.shape[0], 0:img.shape[1]]
        ct = np.count_nonzero(cv2.bitwise_xor(img, other))
        fm = 1
        for it in other.shape:
            fm *= it
        return (fm - ct) / fm

    def getslice(self, slice):
        x1 = slice[0]
        x2 = slice[1]
        y1 = slice[2]
        y2 = slice[3]
        return self.img[x1:x2, y1:y2]

    def save(self, fname):
        cv2.imwrite(fname, self.img)
