import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
LOW = 1
R = 1.12
LEN = 120
LOG = False
MIN = 0.003
def c(file, num, i):
    i = 0
    j = 0
    ps = []
    basePrice = 0
    baseIndex = 0
    buyPrice = 0
    step = 0
    ks = []
    mrs = []
    waitBack = False
    win = 0
    def comK1(p1, p2, timeGap):
        return (p2 - p1) / timeGap * 100
    def comK2(i, j, ps):
        k = (ps[j, 2] - ps[i, 2]) / (j - i)
        b = ps[i, 2] - k*i
        return [k,b]
    def loss(ps, res):
        loss = 0
        for i in range(ps.shape[0]):
            r = ps[i, 2] - (res[0] * i + res[1])
            if r < 0:
                return 10000000
            loss += r
        return loss
    def getBestLine(ps):
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
    def comK(ps):
        if ps.shape[0] == 0:
            return [-1, 0, []]
        min = ps[:,1].min()
        index = 0
        k = 100
        ks = []
        for i in range(index + 1, ps.shape[0]):
            k1 = comK1(min, ps[i,1], i)
            ks.append(k1)
            if k1 < k:
                k = k1
        global MIN
        MIN = 0
        r = getBestLine(ps)
        
        if r[0] > num[r[2], 2] * 0.15 / 60:
            # print(file)
            # plt.figure()
            # x = np.arange(ps.shape[0])
            # plt.scatter(x,ps[:,1])
            # plt.plot(x, r[0]*x + r[1], label=ps[0,0])
            # plt.show()
            return [r[0], index, ks]
        return [-1, index, ks]

    if step == 0:
        ps = num[i: i + LEN]
        res = comK(ps)
        min = ps[:,1].argmin()
        max = ps[:,1].argmax()
        if min < LEN/6 and max > LEN / 6 *5 and res[0] > 0 and comK(num[i + 60: i+ LEN])[0] > 0 and comK(num[i: i+ 60])[0] > 0:
            step = 1
            # baseIndex = i + res[1]
            # basePrice = num[i + res[1],1]
            # buyPrice = num[i + LEN,1]
            ks.extend(res[2])
            if LOG:
                print('watch', num[i,0], res[0], buyPrice,num[i+LEN,0])
            i = i + LEN
            j = i + LEN
            return True
        else:
            if res[1] > 0:
                i += res[1]
            else:
                i += 1
    elif step == 1:
        k = comK1(basePrice, num[j,1], j - baseIndex)
        ks.append(k)
        # print(num[i,0], k, MIN)
        if k < MIN:
            basePrice = 0
            baseIndex = 0
            step = 0
            waitBack = False
            if buyPrice > 0:
                if LOG:
                    print('sale', num[j,0] ,round((num[j,1] / buyPrice - 1) * 100, 2), num[j, 1])
                mrs.append((num[j,1] / buyPrice - 1) *100)
                if num[j,1] / buyPrice - 1 > 0:
                    win += 1
            elif LOG :
                print('watch end', num[j,0])
            buyPrice = 0
            if len(ks) > 0 and LOG:
                plt.figure()
                plt.scatter(np.arange(len(ks)),ks)
                plt.show()
            ks = []
        elif k <= MIN * R:
            waitBack = True
        else:
            if waitBack and buyPrice == 0:
                if LOG:
                    print('buy', num[j,0], num[j, 1], k)
                buyPrice = num[j,1]
        j += 1
    # print(mrs)
    return False

wins = 0
s = 0
rs = 0
i = 0
z = []
ds = {}
ns = [0 for x in range(0, 14)]
zs = [0 for x in range(0, 32)] 
ins = [0 for x in range(0, 102)]
froms = [0 for x in range(0, 102)]
timeGaps = [0 for x in range(0, 300)]
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    thisK = num[0,0][0:4]
    startDate = ''
    startPrice = 0
    startInd = 0
    cs = 0
    for j in range(num.shape[0]):
        if num[j,0].startswith(thisK) and j < num.shape[0] - 1:
            continue
        else :
            startInd = num[cs:j,1].argmin() + cs
            startPrice = num[startInd, 1]
            if startPrice < 15:
                startDate = num[startInd, 0]
                maxInd = num[startInd:j,1].argmax() + startInd
                maxP = num[maxInd, 1]
                min = startInd
                if maxP > 10 and maxP > startPrice * 2 and maxInd - startInd > 20:
                    last = num[min, 1]
                    top10 = 0
                    q = 0
                    for s in range(min + 1, j):
                        if (num[s, 1]/last - 1)*100 > 9 :
                            top10 += 1
                            if q == 0:
                                q = s - min
                        last = num[s, 1]
                    if top10 > 100:
                        top10 = 99
                    ins[top10] += 1
                    if q > 100:
                        q = 99
                    froms[q] += 1
                    # print(file, num[min, 0], num[min, 1], startPrice)
                    z.append([file, num[min, 0], num[min, 1], num[min, 0][9:11]])
                    ns[int(num[min, 0][5:7])] += 1
                    zs[int(num[min, 0][8:10])] += 1
                    if (ds.get(thisK) == None):
                        ds[thisK] = []
                    # if  "2019-01-" in num[min, 0]:
                    ds[thisK].append([file, num[min, 0], num[min, 1], num[min, 0][8:10]])
                        # print(file, num[min, 0], (maxInd - startInd))
                    startDate = ''
                    startPrice = 0
                    timeGaps[maxInd - startInd] += 1
            cs = j
            thisK = num[j,0][0:4]
        # if num[j,0].startswith(thisK):
        #     if num[j, 1] <= 8 and startPrice == 0:
        #         startDate = num[j, 0]
        #         startPrice = num[j, 1]
        #         startInd = j
        #     if startPrice > 0 and num[j, 1] > startPrice * 2 and num[j, 1] > 10 and j - startInd >= 20:
        #         min = num[startInd:j, 1].argmin()
        #         last = num[min + startInd, 1]
        #         top10 = 0
        #         q = 0
        #         for s in range(min + 1 + startInd, j):
        #             if (num[s, 1]/last - 1)*100 > 9 :
        #                 top10 += 1
        #                 if q == 0:
        #                     q = s - min - startInd
                        
        #             last = num[s, 1]
        #         if top10 > 20:
        #             top10 = 20
        #         ins[top10] += 1
        #         if q > 40:
        #             q = 40
        #         froms[q] += 1
        #         print(file, num[min + startInd, 0], num[min + startInd, 1], startPrice)
        #         z.append([file, num[min + startInd, 0], num[min + startInd, 1], num[min + startInd, 0][9:11]])
        #         ns[int(num[min + startInd, 0][5:7])] += 1
        #         zs[int(num[min + startInd, 0][8:10])] += 1
        #         if (ds.get(thisK) == None):
        #             ds[thisK] = []
        #         ds[thisK].append([file, num[min + startInd, 0], num[min + startInd, 1], num[min + startInd, 0][8:10]])
        #         startDate = ''
        #         startPrice = 0
        # else:
        #     thisK = num[j,0][0:4]
        #     startDate = ''
        #     startPrice = 0


for i in ds:
    print(i, len(ds[i]))
# print(ds['2019'])
print(ns)
print(zs)
print(ins)
print(froms)
# print(timeGaps)
for i in range(1,13):
    s1 = 0
    for j in range (i *20, len(timeGaps)):
        if j < len(timeGaps):
            s1 += timeGaps[j]
    print(i, s1/sum(timeGaps) * 100)

# plt.figure()
# plt.scatter(range(102),froms)	
# plt.show()
# result = pd.DataFrame(np.array(z))
# result.to_csv("D:\\result.csv", index=False)