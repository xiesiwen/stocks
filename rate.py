import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json

def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1].mean()
    if len(d) == 0:
        return 0
    return d.mean()
R = {30:0.9, 60:0.95}
def getGap0(d, g):
    s = 0
    mInd = d[len(d) - G:,1].argmin() + len(ns) - G
    for i in range(mInd, len(d)):
        if d[i, 1] >= getM(d[0:i,1],g):
            s = i
            break
    s = max(s, mInd)
    if s - mInd > (len(d) - mInd) / 2:
        return 0.5
    c = 0
    z = 0
    for z in range(s, len(d)):
        m = getM(d[0:z,1], g)
        if d[z,1] < m:
            c+=1
    print(c, s, len(d), mInd, g, round(c/(len(d)-s),2), d[s])
    return round(c/(len(d)-s),2)
def getGap(d, g):
    s = 0
    mInd = d[len(d) - G:,1].argmin() + len(ns) - G
    for i in range(mInd, len(d)):
        if d[i, 1] >= getM(d[0:i,1],g):
            s = i
            break
    s = max(s, mInd)
    if s - mInd > (len(d) - mInd) / 2:
        return 0.5
    c = 0
    z = 0
    for z in range(s, len(d)):
        m = getM(d[0:z,1], g)
        if d[z,1] < m:
            c+=1
    return round(c/(len(d)-s),2)
def getM2(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()

def pr(*arg):
    if False:
        print(arg)

def findJacks(num, ind):
    ps = []
    up = True
    lMin = num[ind,3]
    lMax = num[ind,4]
    jacks= []
    for i in range(ind, len(num)):
        ps.append([num[i,3], num[i,4], i])
    topJack = []
    bottomJack = [2]
    if len(ps) <= 4:
        return [jacks,topJack,bottomJack]
    lMin = ps[2][0]
    lMax = ps[2][1]
    up = True
    findUpJack = True
    LG = 4
    for i in range(3, len(ps)):
        if (ps[i][0] - lMin) * (ps[i][1] - lMax) <= 0:
            pr("merge", num[ps[i][-1],0],num[i,3], lMin, num[i,4], lMax)
            if up:
                lMin = max(lMin, ps[i][0])
                lMax = max(lMax, ps[i][1])
            else:
                lMin = min(lMin, ps[i][0])
                lMax = min(lMax, ps[i][1])
            continue
        if up and ps[i][1] < lMax:
            pr("find top", num[ps[i][-1],0])
            if len(bottomJack) == 0:
                topJack.append(i)
            else:
                pr(i - bottomJack[-1] >= LG, not findUpJack, num[ps[i-2][-1],0], num[ps[bottomJack[-1]-2][-1],0], min(ps[bottomJack[-1]-2][0], ps[i][0]),  max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]))
                if i - bottomJack[-1] >= LG and not findUpJack and min(ps[i-2][0], ps[i][0]) > max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]):
                    m = ps[bottomJack[-1]][0]
                    j = bottomJack[-1]
                    pr("confirm bottom")
                    jacks.append(num[ps[j][2] - 1])
                    findUpJack = True
                    bottomJack = []
                    topJack = [i]
                else :
                    if len(topJack) > 0:
                        if ps[i-1][1] > ps[topJack[0] - 1][1]:
                            topJack = [i]
                    else: topJack = [i]
            up = False
        elif not up and ps[i][1] > lMax:
            pr("find bottom", num[ps[i][-1],0])
            if len(topJack) == 0:
                bottomJack.append(i)
            else:
                if i - topJack[-1] >= LG and findUpJack and max(ps[i-2][1], ps[i][1]) < min(ps[topJack[-1]-2][0], ps[topJack[-1]][0]):
                    m = ps[topJack[-1]][1]
                    j = topJack[-1]
                    jacks.append(num[ps[j][2] - 1])
                    findUpJack = False
                    topJack = []
                    bottomJack = [i]
                else :
                    if len(bottomJack) > 0:
                        if ps[i-1][0] < ps[bottomJack[0]-1][0]:
                            bottomJack = [i]
                            pr("set bottom jack",)
                    else: bottomJack = [i]
            up = True
        lMin = ps[i][0]
        lMax = ps[i][1]
    return jacks, topJack, bottomJack

LEN = 15
def jacks(num, p):
    tops = [-LEN]
    bottoms = [-LEN]
    for i in range(LEN, len(num) - LEN):
        if '2021-01-22' == num[i,0] and p:
            print(num[i,4], num[i- LEN: i+LEN, 4])
        if num[i,4] >= num[i- LEN: i+LEN, 4].max():
            if p:
                print(tops, i)
            if i > tops[-1] + LEN:
                tops.append(i)
            elif num[i,4] > num[tops[-1], 4]:
                tops[-1] = i
        if num[i,3] <= num[i- LEN: i+LEN, 3].min():
            if i > bottoms[-1] + LEN:
                bottoms.append(i)
            elif bottoms[-1] > 0 and num[i,3] < num[bottoms[-1], 3]:
                bottoms[-1] = i
    return tops[1:], bottoms[1:]

def jacks2(num, p):
    L = 12
    temps = []
    tops = []
    bottoms = []
    i = L
    while(i < len(num) - L):
        if num[i,4] >= num[i-L : i+L, 4].max():
            temps.append(i)
            i += L - 1
        i += 1
    if len(temps) > 0:
        tops.append(temps[0])
        for i in range(1,len(temps)):
            if i == len(temps) -1 :
                z = 5
            else:
                z = 8
            am = num[tops[-1]:temps[i],3].argmin()
            if am >= z and temps[i] - am - tops[-1] >= z:
                if i < len(temps) - 2: 
                    if num[temps[i]:temps[i + 1],3].argmin() >= z:
                        bottoms.append(am+tops[-1])
                        tops.append(temps[i])
                else:
                    bottoms.append(am+tops[-1])
                    tops.append(temps[i])
    return tops, bottoms

mp = {}
names = {}
hys = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    s0 = data[i,0].lower().split(".")
    f = s0[1]+"."+s0[0]+".csv"
    names[f] = data[i,1]
    if len(ss) >= 2:
        key = ss[0] + "-" + ss[1]
        hys[f] = key
        if mp.get(key) == None:
            mp[key] = []
        mp[key].append(data[i])

scores = {}
ds = {}
GAP = 0
# lines = [5,13,21,34,55,89,144,233]
# for z in range( 0,LEN, 1):
#     for i in mp:
#         c = 0
#         scs = 0
#         for j in mp[i]:
#             ss = j[0].lower().split(".")
#             file = ss[1]+"."+ss[0]+".csv"
            
#             try:
#                 if file not in ds:
#                     dataset = pd.read_csv("D:/stocks-today/" + file, encoding='gbk').to_numpy()
#                     ds[file] = dataset
#                 # dataset = ds[file][0:len(ds[file]) - z + 1]
#                 dataset = ds[file][0:len(ds[file]) - (LEN - z - 1) - GAP]
#                 # dataset = ds[file]
#                 if len(dataset) < 60:
#                     continue
#                 c += 1
#                 for l in lines:
#                     if dataset[-1,1] > getM2(dataset, l):
#                         scs += 1
#             except IOError:
#                 qqq = 1
#         if scores.get(i) == None:
#             scores[i] = []
#         scores[i].append(round(scs/c,2))
# r = (sorted(scores.items(), key=lambda d: 0.35*np.mean(d[1]) + 0.65*np.mean(d[1][len(d[1]) - 10:len(d[1])]), reverse=True))
# ss = []
# for z in r[0:25]:
#     print(z, np.mean(z[1]))
#     ss.append(z[0])
# print(ss)

PATHO = "D:/stocks-today"
hrs = ss
c=0
ks = 0
thisMonth = 0
win = 0
aa = 0
ds = []
ds2 = {}
G = 150
for file in os.listdir(PATHO):
    ppr = '000807' in file
    if file.startswith('sz.30'):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    ns = num[:,1]
    mInd = ns[len(ns) - G:].argmin() + len(ns) - G
    if len(ns) == 0 or len(ns) - mInd < 40 or ns[-1] >= 25 or len(ns) < 120:
        continue
    ns = np.array(ns,dtype='float32')
    g3 = getGap(num,30)
    g6 = getGap(num, 60)
    g250 = getGap(num, 250)
    n1 = getM(ns, 30)
    n2 = getM(ns, 60)
    if ns[-1] < n1 * 0.85 or ns[-1] < n2 * 0.85:
        continue
    top, btm = jacks2(num[mInd:], ppr)
    if len(top) < 2:
        x = 0
    else:
        top, btm = num[np.array(top) + mInd], num[np.array(btm) + mInd]
        x = 0
        for i in range(1, len(top)):
            if top[i,1] >= top[i - 1,1] * 1.05:
                x += 1
        x = x/(len(top)-1)
    # if ppr:
    #     print(getGap0(num,30), getGap0(num,60), getGap0(num,250))
    # else: continue
    if (g3 <= 0.12 and g6 <= 0.15) or (g3 <= 0.3 and g6 <= 0.25 and x >= 0.6):
        if g250 <= 0.2 and ns[-1]/getM(ns, 60) - 1 >= -0.11 and ns[-1]/getM(ns, 30) - 1 >= -0.11:
            if file not in names.keys():
                names[file] = 'todo'
                hys[file] = 'todo'
            if 'ST' not in names[file]:
                ds.append([file, names[file], len(ns) - mInd, g3,g6, round(ns[-1]/getM(ns, 30) - 1,3)])
                if hys[file] not in ds2.keys():
                    ds2[hys[file]] = []
                ds2[hys[file]].append((file, names[file]))
ds.sort(key=lambda b:b[-1])
res = sorted(ds2.items(), key=lambda item:len(item[1]), reverse=True)
for z in ds:
    print(z)
i = 0
for x in res:
    if len(x[1]) >= len(res[min(10, len(res))][1]):
        print(x)
        i += len(x[1])
print(len(ds), i)