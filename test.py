
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 

def comK2(i, j, ps):
        k = (ps[j, 0] - ps[i, 0]) / (j - i)
        b = ps[i, 1] - k*i
        return [k,b]
def loss(ps, res):
    loss = 0
    for i in range(ps.shape[0]):
        r = ps[i, 0] - (res[0] * i + res[1])
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
    
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocks\\"+file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0 or num[-1,1] > 10:
        continue
    for i in range(num.shape[0]):
        if num[i,0].startswith('2019-02'):
            res = getBestLineDown((num[i-60:i,1]/num[i-60,1] -1) * 100)
            print((num[i-60:i,1]/num[i-60,1] -1) * 100)
            break            