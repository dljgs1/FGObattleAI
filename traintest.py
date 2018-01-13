from ML import SVM
from Wind import cpic
from Wind import cpos

import time

if __name__ == "__main__":
    clf = SVM.SVM_clf()
    pos = cpos.pos()
    st = 49
    picfile = 'pic/train'
    while 1:
        clf.train(picfile)
        pics = []
        pic_ = cpic.pic()
        for i in range(st, st+5):
            pic = cpic.pic(' ')
            pic.img = pic_.getslice(pos.get_rio(i))
            print(clf.judge(pic))
            pics.append(pic)
        ctrl = input()
        ans = ctrl.split(' ')
        for i in range(5):
            pics[i].save(picfile+'/' + ans[i].strip() + '%s.bmp' % (str(time.time())[-7:]))
