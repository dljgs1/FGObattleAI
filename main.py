from Wind import cpic
from Wind import cpos
from ML import SVM
import numpy as np
import time
import datetime
import pygame
import os
from AIcore import calcu


class procdure:
    def __init__(self,t=1):
        self.cur = 0
        self.turn = 1
        self.state = 0
        self.hook = [0, 0, 0]
        self.card = ['', '', '', '', '']
        self.face = ['', '', '', '', '']
        self.clf = SVM.SVM_clf()  # 卡色训练识别
		
        self.clf_face = SVM.SVM_clf()  # 脸谱训练识别
        if t:
            self.clf.train('pic/train')
            self.clf_face.train('pic/train_face')

        self.pos = cpos.pos()
        self.key_dict = {'fb': 48, 'zhuzhan': 40, 'start': 41, 'attack': 15, 'btres': 38,
                         'swc_spd': 25, 'next': 37, 'scene': 54, 'card_st': 49, 'hook_st': 34,
                         'np1': 10, 'np2': 12, 'np3': 14, 'apple': 43, 'apple_ok': 44, 'retblank': 55,
                         'master_sk': 16, 'sk_st': 0, 'face_st': 20, 'manpo': 56, 'flush': 57,
                         'flush_ok': 58, 'enm_blank': 28, 'chouj': 59, 'chongzhi': 60, 'chongzhi_ok': 61,
                         'chongzhi_done': 62
                         }
        self.thr = {'next': 0.7, 'attack': 0.3, 'btres': 0.2, 'swc_spd': 0.2, 'manpo': 0.9}

        self.skill_img = []
        for i in range(0, 9):
            fname = 'skill/%d.bmp' % i
            pic = cpic.pic(fname)
            self.skill_img.append(pic)

        self.skill_cdwn = [1, 1, 1, 1, 1, 1, 1, 1, 1]

        self.scene1 = cpic.pic('scene1.bmp')
        self.scene2 = cpic.pic('scene2.bmp')
        self.scene3 = cpic.pic('scene3.bmp')

        self.count_time = time.time()

        self.curpic = None  # use for detect

    def flush(self):
        ct = time.time() - self.count_time
        cr = self.cur
        print("use time:", ct)
        print("rouns num:", cr)
        f = open('log.txt', 'a', encoding='utf-8')
        now = datetime.datetime.now()
        s = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write("%s %d %f\n" % (s, cr, ct))
        f.close()

        self.count_time = time.time()
        self.cur = 0
        self.turn = 1
        self.state = 0
        self.hook = [0, 0, 0]
        self.card = [0, 0, 0, 0, 0]
        self.skill_cdwn = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def skill_cold_check(self):
        curp = cpic.pic()
        cursk = cpic.pic(' ')
        st = self.key_dict['sk_st']
        pos = self.pos
        if len(self.skill_img) < 9:
            return

        for i in range(st, st + 9):
            cursk.img = curp.getslice(pos.get_rio(i, width=20))
            # sim = cursk.compare(self.skill_img[i - st])
            # print("sk", i, ":", sim)
            if cursk.compare(self.skill_img[i - st]) < 0.95:
                self.skill_cdwn[i - st] = 0  # 不可使用
            else:
                self.skill_cdwn[i - st] = 1  # 可使用

    def out_skill(self, actor, sknum):
        if actor > 0:
            actor -= 1
            sknum -= 1
            skid = 3 * actor + sknum
            if self.skill_cdwn[skid] == 0:
                print("skill", skid, "is colding..")
                return
            self.pos.click(skid)
            time.sleep(1)
            self.curpic = cpic.pic()
            self.detect_and_wait('attack')
        else:
            st = self.key_dict['master_sk']
            self.pos.click(st)
            time.sleep(0.7)
            self.pos.click(st + sknum)
            time.sleep(1)
            self.curpic = cpic.pic()
            self.detect_and_wait('attack')

    def log_skill(self):
        if len(self.skill_img) > 1:
            return
        img = cpic.pic()
        st = self.key_dict['sk_st']
        pos = self.pos
        self.skill_img = []
        for i in range(st, st + 9):
            pic = cpic.pic(' ')
            pic.img = img.getslice(pos.get_rio(i, width=20))
            pic.save('pic/skill/%d.bmp' % i)
            self.skill_img.append(pic.img)

    def log_face(self):
        img = cpic.pic()
        temp = cpic.pic(' ')
        st = self.key_dict['face_st']
        pos = self.pos
        self.skill_img = []
        ans = input()
        ans = ans.split(' ')
        mesh = {'0': 'b', '1': 'q', '2': 'a'}

        for i in range(st, st + 5):
            temp.img = img.getslice(pos.get_rio(i))
            tp = mesh[ans[i - st]]
            tp += str(time.time())[-6:]
            temp.save('pic/train_face/%s.bmp' % tp)
        print("face log!")

    # ai card
    def ai_card(self):
        pass

    # 策略阶段1：
    def strategy_skill(self):
        pos = self.pos
        if len(self.skill_img) > 0:
            self.skill_cold_check()
            print("cold state:", self.skill_cdwn)
        #
        if self.turn == 1:
            if self.state < 2:  # 技能初始化
                self.log_skill()
                self.state = 2
            self.out_skill(3, 2)  # 金时充电
        elif self.turn == 2:
            self.out_skill(3, 2)
            if self.state < 3:
                self.out_skill(0, 2)
                self.state = 3
            if self.hook[2]:
                self.out_skill(3, 1)

        elif self.turn == 3:
            self.out_skill(1, 3)
            self.out_skill(1, 2)
            self.out_skill(1, 1)
            self.out_skill(3, 2)
            self.check_hook()
            if self.hook[1] and self.state < 4:
                self.out_skill(2, 3)
                self.out_skill(0, 1)
                self.state = 4
            if self.hook[2]:
                self.out_skill(3, 1)
                self.out_skill(3, 3)
        elif self.cur >= 7:
            self.out_skill(3, 3)
        pos.click(self.key_dict['attack'])

    # 策略阶段2
    def strategy_card(self):
        time.sleep(0.4)  # 等暴击星撒完
        self.cardcolor()
        self.cardface()

        pos = self.pos
        st = self.key_dict['card_st']
        hk_st = self.key_dict['hook_st']

        get_np = lambda x: calcu.max_npget(self.card, self.face, x)
        get_dmg = lambda x: calcu.max_dmgget(self.card, self.face, x)
        get_star = lambda x: calcu.max_starget(self.card, self.face, x)
        get_buster = lambda x: calcu.max_buster(self.card, self.face, x)

        cards = []
        if self.turn == 1:
            if self.cur > 2:
                cards = get_dmg(-1)
            elif self.hook[1] == 0:
                cards = get_np(1)
                if not cards:
                    cards = get_dmg(-1)
            else:
                cards = get_dmg(-1)
        if self.turn == 2:
            if self.hook[2]:
                pos.click(hk_st + 2)
                cards = get_np(-1)
            elif self.hook[1] == 0:
                cards = get_np(1)
                if not cards:
                    cards = get_np(-1)
            elif self.hook[0] == 0:
                cards = get_np(0)
                if not cards:
                    cards = get_np(-1)
            else:
                cards = get_dmg(-1)
        if self.turn == 3:
            if self.cur > 10:
                cards = get_dmg(-1)
            elif self.state >= 5:
                cards = get_dmg(-1)
            else:
                hk = [0, 0, 0]
                for i in range(hk_st, hk_st + 3):
                    if self.hook[i - hk_st] > 0:
                        hk[i - hk_st] = 1
                        pos.click(i)
                if hk[0] and hk[1]:
                    self.state = 5
                    cards = get_buster(0)
                elif hk[0]:
                    cards = get_buster(0)
                elif self.state == 4:
                    cards = get_star(0)
                else:
                    cards = get_np(-1)

        if cards:
            cards = list(np.array(cards) + st)
        else:
            scorenp = {'b': 1, 'a': 3, 'q': 2}
            scoredm = {'b': 3, 'a': 2, 'q': 1}
            cards = [i for i in range(st, st + 5)]
            score = scorenp
            if self.turn == 1:
                score = scoredm
            elif self.turn == 2:
                score = scorenp
            else:
                score = scorenp
            cards.sort(key=lambda x: score[self.card[x - st]], reverse=True)
            # 放宝具：

            # hkcard = []#
            # if self.turn == 2 and self.hook[2]:
            #    hkcard.append(hk_st + 2)
            # if self.turn == 3:
            #    for i in range(hk_st, hk_st + 3):
            #        if self.hook[i - hk_st] > 0:
            #            hkcard.append(i)
            # cards = hkcard + cards
        print('cur card query', cards)
        for i in cards:
            pos.click(i)

    def cardface(self):
        st = self.key_dict['face_st']
        pos = self.pos
        pic = cpic.pic()
        ids = {'b': 0, 'q': 1, 'a': 2}
        for i in range(st, st + 5):
            self.face[i - st] = ids[self.clf_face.judge(pic.getslice(slice=pos.get_rio(i)))]
        print('card actor:', self.face)

    def cardcolor(self):
        st = self.key_dict['card_st']
        pic = cpic.pic()
        pos = self.pos
        for i in range(st, st + 5):
            self.card[i - st] = self.clf.judge(pic.getslice(slice=pos.get_rio(i, width=70)))
        print('card color:', self.card)

    # test ok!?
    def check_hook(self):
        pos = self.pos
        key_dict = self.key_dict

        pic = cpic.pic()
        npc = []
        for i in range(1, 4):
            ptemp = cpic.pic(' ')
            ptemp.img = pic.getslice(slice=pos.get_rio(key_dict['np%d' % i], width=20))
            npc.append(ptemp)

        time.sleep(0.2)
        npp = cpic.pic()
        for i in range(1, 4):
            np = npp.getslice(slice=pos.get_rio(key_dict['np%d' % i], width=20))
            cmp = npc[i - 1].compare(np)
            print(cmp)
            if cmp == 1.0:
                print("error hook state!!!")
                return self.check_hook()
            if cmp < 0.7:
                self.hook[i - 1] = 1
            else:
                self.hook[i - 1] = 0

        print("hook state:", self.hook)
        return 0

    #  每回合的检查
    def check_turn(self):
        # 回合数检查
        print("checking...")
        p1 = self.scene1
        p2 = self.scene2
        p3 = self.scene3
        score = np.array([0., 0., 0.])
        for i in range(3):
            p = cpic.pic(slice=self.pos.get_rio(self.key_dict['scene'], width=20))
            score += np.array([p.compare(p1), p.compare(p2), p.compare(p3)])
            time.sleep(0.2)
        turn = np.argmax(score) + 1
        if 0 <= turn - self.turn <= 1:
            self.turn = turn
            print("new turn:", self.turn)
        else:
            print("wrong turn:", turn)
        # 宝具检查：
        self.check_hook()
        print("checking done")

    # --------------------------------------------

    def detect(self, fn, w=50, thr=0.9, dtype='judg'):
        pos = self.pos
        fname = fn + '.bmp'
        idp = self.key_dict[fn]
        try:
            thr = self.thr[fn]
        except KeyError:
            pass
        pic_cmp = cpic.pic(fname)
        pic = cpic.pic(' ')
        pic.img = self.curpic.getslice(slice=pos.get_rio(idp, w))
        how = pic_cmp.compare(pic)

        if dtype == 'how':
            return how
        elif how < thr:
            return False
        else:
            print('detect-:', fn, ' !')
            return True

    def detect_and_wait_with_click(self, fn, dst, thr=0.9, w=50, jud=False):
        ct = 5
        while self.detect(fn, w, thr, dtype='judg') == jud and ct:
            self.click(dst)
            self.curpic = cpic.pic()
            ct -= 1

    def detect_and_wait(self, fn, thr=0.9, w=50, jud=False):
        ct = 0
        while self.detect(fn, w, thr, dtype='judg') == jud and ct < 68:
            time.sleep(1)
            self.curpic = cpic.pic()
            if ct >= 5 and ct % 5 == 0:
                pass  # self.click('enm_blank')
            if ct == 66:
                os.system('shutdown -s -t 30')
                # pygame.mixer.init()
                # pygame.mixer.music.load('reminder.mp3')
                # pygame.mixer.music.play()
                input()
                pygame.mixer.music.stop()
            ct += 1

    def click(self, spos):
        self.pos.click(self.key_dict[spos])
        time.sleep(0.7)

    def get_new_pic(self):
        time.sleep(1)
        self.curpic = cpic.pic()

    # 根据状态决定当前动作
    def subrun(self):
        pos = self.pos
        key_dict = self.key_dict
        n = self.state
        self.get_new_pic()

        if n == 0:
            self.detect_and_wait('fb')  # detect_and_wait('fb.bmp', key_dict['fb'])
            self.click('fb')
            self.get_new_pic()

            if self.detect('apple'):
                self.click('apple')
                self.click('apple_ok')
                self.detect_and_wait('fb')
                self.click('fb')
                self.get_new_pic()
            tpct = 0
            while not self.detect('manpo', w=20) and tpct < 5:
                if tpct > 0:
                    time.sleep(15)
                self.click('flush')
                time.sleep(1)
                self.click('flush_ok')
                time.sleep(10)
                self.get_new_pic()
                tpct += 1

            self.click('zhuzhan')
            self.detect_and_wait('start')
            self.click('start')
            time.sleep(2)
            self.click('start')
            self.state = 1
            return 1  # 进本前一套
        elif n >= 1:
            if self.detect('attack'):
                return 2
            elif self.detect('swc_spd'):
                return 3
            elif self.detect('btres'):
                self.state = -1
                return -1
            else:
                time.sleep(1)  # 战斗回
                return 1
        elif n == -1:  # 战斗结束
            self.detect_and_wait('btres')
            self.click('btres')
            self.click('btres')

            self.detect_and_wait_with_click(fn='next', dst='retblank')
            self.click('next')
            self.click('retblank')
            time.sleep(2)
            self.click('retblank')
            time.sleep(2)
            self.click('retblank')

            self.flush()
            return 0

    def run(self, cur=0):
        self.state = cur
        self.turn = cur
        while True:
            n = self.subrun()
            if n == 0:
                print("start battle")
            elif n == 1:
                pass
            elif n == 2:
                self.cur += 1
                print("round ", self.cur)
                print("skill interface")
                self.check_turn()
                self.strategy_skill()
            elif n == 3:
                print("card interface")
                self.strategy_card()
            elif n == -1:
                print("end battle:", self.cur)
            else:
                print("wrong state!:,", self.state)

    def chouj(self):
        sturn = 5
        while True:
            while sturn:
                self.get_new_pic()
                if self.detect(fn='chongzhi',thr=0.7):
                    self.click('chongzhi')
                    time.sleep(1)
                    self.click('chongzhi_ok')
                    time.sleep(1)
                    self.click('chongzhi_done')
                    sturn-=1
                else:
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
                    self.click('chouj')
            print("\a\a go on? input turns")
            sturn = int(input())


    def unit_test(self, cmd):
        if cmd == '1':
            self.check_turn()
            print(self.turn, self.hook)

        elif cmd == '6':
            self.log_skill()
        elif cmd == '7':
            self.skill_cold_check()
            self.out_skill(2, 1)


if __name__ == '__main__':
    p = procdure(0)
    print("start")
    p.chouj()
    #p.run(0)
    while 1:
        p.unit_test(input())
