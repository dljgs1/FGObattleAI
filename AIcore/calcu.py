# 通用计算函数


def star(cards, dstact=-1):
    score = {'b': 1, 'a': 1, 'q': 3}

    ans= 0
    for card in cards:
        ans += score[card['color']]
        if card['actor'] == dstact:
            ans += score[card['color']]

    return ans


def buster(cards,dstact=-1):
    score = {'b': 3, 'a': 1, 'q': 1}
    ans = 0
    for card in cards:
        ans += score[card['color']]
        if card['actor'] == dstact:
            ans += score[card['color']]
    return ans


# 传入选出的三张卡 计算其伤害 cards[{'atk':-,'color':-,'buff':-}]
def damage(cards, dstact=-1):
    clrpow = {'b': 1.5, 'q': 0.8, 'a': 1.0, 'ex': 1.0}
    fstpow = {'b': 0.5, 'q': 0, 'a': 0}
    pospow = [1.0, 1.2, 1.4, 1.0]

    atk_actor = [11971, 9049, 9819]

    first = fstpow[cards[0]['color']]

    sim = 0
    chain = 0
    last_act = -1

    ans = 0
    pos = 0
    for card in cards:
        color = card['color']
        actor = card['actor']
        atk = atk_actor[actor]
        if color == 'b':
            chain += 1
        if actor == last_act:
            sim += 1
        else:
            sim = 0
            last_act = actor

        if 'hook' in card:
            ans += atk * 0.23 * 1000
        else:
            ans += atk * 0.23 * (clrpow[color] * pospow[pos] + first)
        pos += 1

    if sim == 3:
        ans += atk * 0.23 * (pospow[pos] + first)
    if chain == 3:
        ans += atk * 0.23 * 0.2

    return ans


def npget(cards, dstact=-1):
    clrpow = {'b': 0, 'q': 1.0, 'a': 3.0}
    fstpow = {'b': 0, 'q': 0, 'a': 1.0}
    pospow = [1.0, 1.5, 2.0, 1.0]
    fst = fstpow[cards[0]['color']]

    ans = 0
    pos = 0
    sim = 0
    chain = 0
    last_act = -1

    for card in cards:
        color = card['color']
        actor = card['actor']

        if color == 'a':
            chain += 1

        if actor == last_act:
            sim += 1
        else:
            sim = 0
            last_act = actor

        if dstact < 0:
            ans += clrpow[color] * pospow[pos] + fst
        elif 0 <= dstact == actor:
            ans += clrpow[color] * pospow[pos] + fst
        pos += 1

    if sim == 3:
        ans += pospow[pos] + fst
    if chain == 3:
        ans += 20
    return ans


def max_get(cards, face, act_id, fun=npget):
    if act_id >= 0 and act_id not in face:
        return None  # 没有该角色的牌
    history_max = 0
    ans_max = []

    for i in range(5):
        for j in range(5):
            if j == i:
                continue
            for k in range(5):
                if k == i or k == j:
                    continue
                ans = [i, j, k]
                dst = [{'color': cards[ans[0]], 'actor': face[ans[0]]},
                       {'color': cards[ans[1]], 'actor': face[ans[1]]},
                       {'color': cards[ans[2]], 'actor': face[ans[2]]}]
                np = fun(dst, act_id)
                if np > history_max:
                    history_max = np
                    ans_max = ans

    print('max:', history_max)
    return ans_max


def max_dmgget(cards, face, act_id=-1):
    ans = max_get(cards, face, act_id, fun=damage)
    if ans:
        for i in range(5):
            if i not in ans:
                ans.append(i)
    return ans


# 获取某个角色np最大获取的卡序 不考虑宝具释放 回溯法求解cards:['a','b','q'..] face=[0,0,1,1]
def max_npget(cards, face, act_id=-1):
    ans = max_get(cards, face, act_id, fun=npget)
    if ans:
        for i in range(5):
            if i not in ans:
                ans.append(i)
    return ans

# 用于宝具后的绿卡
def max_starget(cards, face, act_id=-1):
    ans = max_get(cards,face,act_id,fun=star)
    if ans:
        for i in range(5):
            if i not in ans:
                ans.append(i)
    return ans



# 用于宝具后的红卡
def max_buster(cards,face,act_id = -1):
    return max_get(cards,face,act_id,fun=buster)


if __name__ == "__main__":
    import time

    c = ['q', 'a', 'q', 'q', 'a']
    f = [0, 2, 1, 1, 0]
    timest = time.time()
    print('dmg:',max_dmgget(c, f))
    print('np:',max_npget(c, f, 0))
    print('star:',max_starget(c, f))
    print('cost:', time.time() - timest)
