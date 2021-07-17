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
    if len(temps) == 0:
        m = num[len(num)-L:, 4].argmax()
        if m <= 8:
            temps.append(len(num) - L + m)
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
data = pd.read_excel("./hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
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

PATHO = "./stock-today"
hrs = ss
c=0
r = 0
for file in os.listdir(PATHO):
    ppr = '000807' in file
    if file.startswith('sz.30'):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if num.shape[0] < 12 or num[-1,1] > 50:
        continue
    c += 1
    x = 0
    for z in range(len(num) - 12, len(num)):
        m = getM(num[0:z,1], 10)
        if num[z,1] < m:
            x+=1
    if x <= 1:
        print(file)
        r += 1
print(c , r)