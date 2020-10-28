
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 

def comK2(i, j, ps):
        k = (ps[j] - ps[i]) / (j - i)
        b = ps[i] - k*i
        return [k,b]
def loss(ps, res):
    loss = 0
    for i in range(ps.shape[0]):
        r = ps[i] - (res[0] * i + res[1])
        if r < 0:
            return 10000000
        loss += r
    return loss
def getBestLineUp(ps):
    minLoss = -1
    minLossRes = [-1, 0, 0]
    for i in range(ps.shape[0]):
        mink = -1
        minRes = []
        for j in range(i + 1, ps.shape[0]):
            res = comK2(i,j,ps)
            if mink == -1 or res[0] < mink:
                mink = res[0]
                minRes = res
                minRes.append(j)
        if len(minRes) > 0:
            loss1 = loss(ps, minRes)
            if minLoss == -1 or loss1 < minLoss:
                minLoss = loss1
                minLossRes = minRes
    return minLossRes

def getBestLineDown(ps):
    minLoss = -1
    minLossRes = [-1, 0, 0]
    for i in range(ps.shape[0]):
        mink = -1
        minRes = []
        for j in range(i + 1, ps.shape[0]):
            res = comK2(i,j,ps)
            if mink == -1 or res[0] < mink:
                mink = res[0]
                minRes = res
                minRes.append(j)
        if len(minRes) > 0:
            loss1 = loss(ps, minRes)
            if minLoss == -1 or loss1 < minLoss:
                minLoss = loss1
                minLossRes = minRes
    return minLossRes

LEN = 60   

for mon in [x +1 for x in range(12)]:
    mons = '-%02d-' % (mon)
    c = 0
    w2 = 0
    w4 = 0
    for file in os.listdir("D:\\stocks"):
        if file.startswith('sz.30'):
            continue
        dataset = pd.read_csv("D:\\stocks\\"+file, encoding='gbk')
        num = dataset.to_numpy()
        if num.shape[0] < LEN or num[-1,-1] > 0:
            continue
        lastInd = -101
        for i in range(num.shape[0]):
            if mons in num[i,0] and i - lastInd > 100 and num[i,1] < 10:
                lastInd = i
                array = (num[i-LEN:i+1,1]/num[i-LEN,1] -1) * 100
                x = [z for z in range(LEN+1)]
                res = getBestLineDown(array)
                g = (num[i,1]/num[i-LEN,1] -1) - (LEN*res[0] + res[1])/100
                if res[0] > 0.15 and g < 0.05:
                    # print(file[3:9], num[i,0])
                    c += 1
                    if i+20 < num.shape[0] and num[i + 20,1] > num[i,1]:
                        w2 += 1
                    if i+40 < num.shape[0] and num[i + 40,1] > num[i,1]:
                        w4 += 1
                    # plt.figure()									#打印样本点
                    # plt.scatter(x,array)						#把x_data和y_data传进来
                    # plt.plot(x, np.array(x)*res[0] + res[1])
                    # plt.show()
                # break
    print(mon, c, w2/c, w4/c)            