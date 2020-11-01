
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

for mon in [x +1 for x in [1]]:
    lasts = '-%02d-' % (mon -1)
    mons = '-%02d-' % (mon)
    if mon == 1:
        lasts = '-12-'
    c = 0
    w2 = 0
    w4 = 0
    base = 0
    base2 = 0
    base4 = 0
    ks = []
    kms = []
    for file in os.listdir("D:\\stocks"):
        if file.startswith('sz.30'):
            continue
        dataset = pd.read_csv("D:\\stocks\\"+file, encoding='gbk')
        num = dataset.to_numpy()
        if num.shape[0] < LEN or num[-1,-1] > 0:
            continue
        lastInd = -101
        
        for i in range(num.shape[0]):
            if  mons in num[i,0] and i > 1 and lasts in num[i-1,0] and num[i,1] < 10 and i > LEN:
                base+=1
                x = np.array([z for z in range(LEN + 1)])
                y = num[i-LEN:i + 1,1]/num[i-LEN,1]
                y = y.astype(np.float32)
                res = np.polyfit(x, y,2)
                kms.append(res[0])
                if i+20 < num.shape[0] and num[i + 20,1] > num[i,1]:
                    base2 += 1
                    ks.append(res[0])
                if i+40 < num.shape[0] and num[i + 40,1] > num[i,1]:
                    base4 += 1
                
                # plt.figure()
                # plt.scatter(x,num[i-LEN:i,1]/num[i-LEN,1])
                # plt.plot(x,np.array(x) * z[0] + z[1])
                # plt.show()
                if res[0] > 0:
                    c += 1
                    if i+20 < num.shape[0] and num[i + 20,1] > num[i,1]:
                        w2 += 1
                    if i+40 < num.shape[0] and num[i + 40,1] > num[i,1]:
                        w4 += 1
                    # plt.clf()
                    # plt.scatter([z for z in range(LEN*2)],num[i-LEN-LEN:i,1])
                    # plt.savefig('D:\\image\\'+file[3:9]+".png")
                    
                    # print(file[3:9],i+20 < num.shape[0] and num[i + 20,1] > num[i,1], i+40 < num.shape[0] and num[i + 40,1] > num[i,1])
                break
        # if lastInd > 0:
        #     break
    print(mon, c, w2/c, base2/base, w4/c, base4/base)  
    plt.figure()
    # print(ks)
    plt.scatter(np.arange(len(ks)),ks)
    plt.show()   

    plt.figure()
    # print(kms)
    plt.scatter(np.arange(len(kms)),kms)
    plt.show()   