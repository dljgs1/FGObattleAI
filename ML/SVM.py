from sklearn import svm
from Wind import cpos
from Wind import cpic
import time
import os
import cv2
import numpy as np
# 训练了用于卡色识别的SVM分类器

def rgbfeature(img):
    ans = []
    img = cv2.resize(img, (32, 32))
    r, w, b = img.shape

    rsum = 0
    bsum = 0
    gsum = 0
    ct = 0
    for i in range(r):
        for j in range(w):
            dtemp = list(img[i][j])
            rsum += dtemp[0]
            bsum += dtemp[1]
            gsum += dtemp[2]
            ct += 1

    rsum /= ct
    bsum /= ct
    gsum /= ct

    for i in range(r):
        for j in range(w):
            dtemp = list(img[i][j])
            dtemp = [dtemp[0] / rsum, dtemp[1] / bsum, dtemp[2] / gsum]
            ans += dtemp

    return np.array(ans)


def recurdir(fname, excf):
    files = os.listdir(fname)
    print(files)
    for fi in files:
        fi_d = os.path.join(fname, fi)
        if os.path.isdir(fi_d):
            recurdir(fi_d, excf)
        else:
            excf(fi_d)


data = []
label = []
lab_t = {'b': 0, 'q': 1, 'a': 2}


def mkdata(fname):
    global data
    global label
    global lab_t

    s = fname.split('.')
    t = s[0].split('\\')[-1][0]
    if t in lab_t:
        label.append(lab_t[t])
    else:
        print("no!", s)
        return
    img = cv2.imread(fname)
    data.append(rgbfeature(img))

def reload(fname):
    global data
    global label
    data = []
    label = []
    recurdir(fname, mkdata)


# from ML import ELM

pos = cpos.pos()
t_lab = {0: 'b', 1: 'q', 2: 'a'}


class SVM_clf:
    def __init__(self):
        self.clf = svm.SVC()

    def train(self,fname):
        global data, label
        self.clf = svm.SVC()
        reload(fname)
        self.clf.fit(data, label)

    def judge(self, img):
        global t_lab
        try:
            img = img.img
        except AttributeError:
            pass
        return t_lab[self.clf.predict([rgbfeature(img)])[0]]


if __name__ == "__main__":
    clf = SVM_clf()
    pos = cpos.pos(posfile='/scene/pos.txt')
    while 1:
        clf.train('/pic/train_face/')
        pics = []
        pics = cpic.pic()
        for i in range(20, 25):
            pic = pics.getslice(pos.get_rio(i))
            print(clf.judge(pic))

        ctrl = input()
        ans = ctrl.split()
        for i in range(5):
            pics[i].save('pic/train_face/' + ans[i] + '%s.bmp' % (str(time.time())[-6:]))
