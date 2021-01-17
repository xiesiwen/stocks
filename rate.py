import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json

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


def getM2(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()

mp = {}
names = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    s0 = data[i,0].lower().split(".")
    f = s0[1]+"."+s0[0]+".csv"
    names[f] = data[i,1]
    if len(ss) >= 2:
        key = ss[0] + "-" + ss[1]
        if mp.get(key) == None:
            mp[key] = []
        mp[key].append(data[i])

scores = {}
ds = {}
LEN = 22
GAP = 0
lines = [5,13,21,34,55,89,144,233]
for z in range( 0,LEN, 1):
    for i in mp:
        c = 0
        scs = 0
        for j in mp[i]:
            ss = j[0].lower().split(".")
            file = ss[1]+"."+ss[0]+".csv"
            
            try:
                if file not in ds:
                    dataset = pd.read_csv("D:/stocks-today/" + file, engine='python').to_numpy()
                    ds[file] = dataset
                # dataset = ds[file][0:len(ds[file]) - z + 1]
                dataset = ds[file][0:len(ds[file]) - (LEN - z - 1) - GAP]
                # dataset = ds[file]
                if len(dataset) < 60:
                    continue
                c += 1
                for l in lines:
                    if dataset[-1,1] > getM2(dataset, l):
                        scs += 1
            except IOError:
                qqq = 1
        if scores.get(i) == None:
            scores[i] = []
        scores[i].append(round(scs/c,2))
r = (sorted(scores.items(), key=lambda d: 0.35*np.mean(d[1]) + 0.65*np.mean(d[1][len(d[1]) - 10:len(d[1])]), reverse=True))
ss = []
for z in r[0:25]:
    print(z, np.mean(z[1]))
    ss.append(z[0])
print(ss)

PATHO = "D:/stocks-today"
PATH = "D:/AndroidStudioProjects/aStocks/app/src/main/assets/stocks/chan"
hrs = ss
c=0
ks = 0
thisMonth = 0
win = 0
aa = 0
ds = []
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
    if len(ns) == 0 or len(ns) - ns.argmin() < 60 or ns[-1] >= 25 or len(ns) < 120:
        continue
    ns = np.array(ns/ns.min(),dtype='float32')
    g3 = getGap(num,30)
    n1 = getM(ns, 30)
    n2 = getM(ns, 60)
    if ns[-1] < n1 * 0.85 or ns[-1] < n2 * 0.9:
        continue
    if g3 >= 0 and g3 / (len(ns)-ns.argmin()) <= 0.25:
        g6 = getGap(num, 60)
        if g6 >= 0:
            ds.append([file, g3/(len(ns)-ns.argmin()),g6/(len(ns)-ns.argmin()), names[file], ns[-1]/getM(ns, 30) - 1])

ds.sort(key=lambda b:b[-1])
print(ds)
for z in ds:
    print(z[0], z[-2] ,z[-1])
print(len(ds))