import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json

openLog = False
def pr(*arg):
    if openLog:
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
                pr(i - bottomJack[-1] >= 4, not findUpJack, num[ps[i-2][-1],0], num[ps[bottomJack[-1]-2][-1],0], min(ps[bottomJack[-1]-2][0], ps[i][0]),  max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]))
                if i - bottomJack[-1] >= 4 and not findUpJack and min(ps[i-2][0], ps[i][0]) > max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]):
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
                # pr(i - topJack[-1] >= 4, findUpJack, max(ps[i-2][1], ps[i][1]), min(ps[topJack[-1]-2][0], ps[topJack[-1]][0]))
                if i - topJack[-1] >= 4 and findUpJack and max(ps[i-2][1], ps[i][1]) < min(ps[topJack[-1]-2][0], ps[topJack[-1]][0]):
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
    return [jacks, topJack+ind, bottomJack+ind]

def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1].mean()
    if len(d) == 0:
        return 0
    return d.mean()
R = {30:0.9, 60:0.95}
def getGap(d, g):
    s = 0
    mInd = d[:,1].argmin()
    for i in range(mInd, len(d)):
        if d[i, 1] >= getM(d[0:i,1],g):
            s = i
            break
    c = 0
    z = 0
    
    jacks = findJacks(d,mInd)
    for i in range(1,len(jacks[0]), 1):
        b = np.where(d == jacks[0][i][0])
        ind = b[0][0]
        if d[ind,1] < getM(d[0:ind,1], g) * R[g]:
            z +=1
    if len(jacks[2]) > 0 and  d[jacks[2][0],1] < getM(d[0:jacks[2][0],1], g) * R[g]:
        z += 1
    if openLog:
        print('z is',z)
    if z > 1:
        return -1
    for z in range(s, len(d)):
        m = getM(d[0:z,1], g)
        if d[z,1] < m:
            c+=1
    return c

def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
mp = {}
mpn = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    if len(ss) >= 2:
        key = ss[0] + "-" + ss[1]
        mp[data[i,0][0:6]] = key
        mpn[data[i,0][0:6]] = data[i, 1]

PATHO = "D:/stocks-today"
PATH = "D:/AndroidStudioProjects/aStocks/app/src/main/assets/stocks/chan"
# setDir(PATH)
c=0
ks = 0
rs = []
hs = {}
ds = [0 for x in range(0, 20)]
for file in os.listdir(PATHO):
    if not (file.startswith('sh.60') or file.startswith('sz.00')):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if num.shape[0] == 0 or num[-1,-1] != 0:
        continue
    
    ns = num[:,1]
    if len(ns) - ns.argmin() < 40 or ns[-1] >= 25 or len(ns) < 120:
        continue
    ns = np.array(ns/ns.min(),dtype='float32')
    x = np.array(np.arange(len(ns)-ns.argmin()),dtype='float32')*0.005
    res2 = np.polyfit(x, ns[ns.argmin():], 1)
    c += 1
    ks += res2[0]
    # res3 = np.polyfit(np.array(np.arange(10),dtype='float32')*0.005, ns[len(ns)-10:len(ns)], 1)
    if file[3:9] not in mp.keys():
        continue
    key = mp[file[3:9]]
    if key not in hs.keys():
        hs[key] = []
    g3 = getGap(num,30)
    if g3 >= 0 and g3 / (len(ns)-ns.argmin()) <= 0.25:
        g6 = getGap(num, 60)
        if g6 >= 0:
            hs[key].append([file,g3/(len(ns)-ns.argmin()),g6/(len(ns)-ns.argmin()), key, mpn[file[3:9]], ns[-1]/getM(ns, 30) - 1])
c1 = 0
t = ks/c
xs = []
for k in hs.keys():
    a = hs[k]    
    # a = [i for i in a if i[3] > t]
    a.sort(key=lambda b:b[1] * 2 + b[2])
    c1 += len(a)
    if len(a) > 0:
        print(k, a, len(a))
        xs.extend(a)
xs.sort(key=lambda b:b[1] * 2 + b[2])
print('-------------------\n')
for x in xs:
    print(x)
print(c1)