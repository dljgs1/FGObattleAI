# -*- coding: utf-8-*-

import cv2
import os
import numpy as np



img2 = cv2.imread('scene/shajie.bmp')
r,w,c = img2.shape


from Wind import cpos
from Wind import cpic


pos = cpos.pos('scene/pos.txt')

while 1:
    cmd = input()
    cmds = cmd.split()
    ctr = cmds[0]
    i = int(cmds[1])
    w = 50
    if len(cmds) > 2:
        w = int(cmds[2])

    if ctr == 's':
        pic = None
        if i >= 0:
            pic = cpic.pic(slice=pos.get_rio(i,width=w))
        else:
            pic = cpic.pic()
        pic.show()
    elif ctr == 'c':
        pos.click(i)
    elif ctr == 'sc':
        f = open('clog.txt','a')
        f.write(i)
        f.write('\n')
        f.close()
    elif ctr == 'sp':   # save pic
        pic = None
        if int(i) >=0:
            pic = cpic.pic(slice=pos.get_rio(i,width=w))
        else:
            pic = cpic.pic()
        fname = input('input fname')
        pic.save('pic/'+fname)
    else:
        pass


    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('w', Harris(gray))

