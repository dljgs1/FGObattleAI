from numpy import *


def sig(tData, Iw, bias, num):
    v = tData * Iw.T  # 样本数*隐含神经元个数
    bias_1 = ones((num, 1)) * bias
    v = v + bias_1
    H = 1. / (1 + exp(-v))
    return H


class ELM:
    # 指定特征数N以及隐藏层单元数K
    def __init__(self, N, K=100, fun=sig):
        self.N = N
        self.K = K
        # 随机生成区间-1,1之间的随机矩阵
        self.Iw = mat(random.rand(self.K, self.N) * 2 - 1)
        self.bias = mat(random.rand(1, self.K))
        self.fun = fun
        self.beta = None
        self.M = None

    # 输入格式：firstTrainData为 样本数*特征数 的
    def train(self, data, label, labelnum=7):
        NO = len(data)
        p0 = mat(data)
        T0 = zeros((NO, labelnum))

        for i in range(0, NO):
            T0[i][int(label[i])] = 1

        T0 = T0 * 2 - 1
        H0 = self.fun(p0, self.Iw, self.bias, NO)  # 样本数*隐含神经元个数
        self.M = (H0.T * H0).I
        self.beta = self.M * H0.T * T0

    def OLtrain(self, data, label):
        Tn = zeros((1, 3))
        Tn[0][label] = 1
        Tn = Tn * 2 - 1
        pn = mat(data)
        M = self.M
        H = sig(pn, self.Iw, self.bias, 1)
        self.M = M - M * H.T * (eye(1,1) + H * M * H.T).I * H * M
        self.beta = self.beta + M * H.T * (Tn - H * self.beta)

    def test(self, inx, outtype='prob'):
        H = self.fun(inx, self.Iw, self.bias, len(inx))
        res = H * self.beta
        res = res.tolist()
        if outtype=='prob':
            return res
        # 返回每个数据的分类
        ans = []
        for it in res:
            ans.append(argmax(it))
        return ans