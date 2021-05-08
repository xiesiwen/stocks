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
    return round(c/(len(d)-mInd),2)
def getM2(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()

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
for file in os.listdir(PATHO):
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
    if len(ns) == 0 or len(ns) - ns.argmin() < 30 or ns[-1] >= 25 or len(ns) < 120:
        continue
    ns = np.array(ns/ns.min(),dtype='float32')
    g3 = getGap(num,30)
    n1 = getM(ns, 30)
    n2 = getM(ns, 60)
    if ns[-1] < n1 * 0.85 or ns[-1] < n2 * 0.85 or len(ns)-ns.argmin() < 60:
        continue
    top, btm = jacks(num[ns.argmin():], False)
    if g3 <= 0.3 and len(top) >= 2:
        g6 = getGap(num, 60)
        g250 = getGap(num, 250)
        if g6 <= 0.3 and g250 <= 0.3 and 'ST' not in names[file] and ns[-1]/getM(ns, 60) - 1 >= -0.11 and ns[-1]/getM(ns, 30) - 1 >= -0.11:
            ds.append([file, names[file], len(ns)-ns.argmin(), g3,g6, round(ns[-1]/getM(ns, 30) - 1,3)])
ds.sort(key=lambda b:b[-1])
for z in ds:
    print(z)
print(len(ds))