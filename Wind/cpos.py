# -*- coding: utf-8-*-

import pandas
import os


# 位置信息与操作

class pos:
    def __init__(self, posfile='scene/pos.txt'):
        self.data = pandas.read_table(posfile, sep=' ')

    def get_pos(self, id):
        return self.data.iloc[id]['x'], self.data.iloc[id]['y']

    # 获取该位置50*50的方域 返回四个角的坐标 x1,x2,y1,y2
    def get_rio(self, id, width=50):
        id = int(id)
        x = self.data.iloc[id]['x']
        y = self.data.iloc[id]['y']
        return int(x - width / 2), int(x + width / 2),int(y - width / 2), int(y + width / 2)

    # 点击某位置 (注意：xy是反的)
    def click(self, id):
        os.system('click.exe %s %s' % (self.data.iloc[id]['y'], self.data.iloc[id]['x']))