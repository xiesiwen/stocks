import numpy as np
from numpy.core.defchararray import index
import pandas as pd
import akshare as ak
import os
import datetime
mp = []
c = 0
indexs = {}
ds = []
for f in os.listdir('./同花顺概念/'):
    if 'ST' in f:
        continue
    bb = np.load('./同花顺概念/' + f, allow_pickle=True)
    r = np.where(bb[:,0] > datetime.date(2021,2,18))
    ns = bb[r]
    ind = ns[:,3].argmin()
    if ns[0,0] == datetime.date(2021,2,19):
        ds = ns[1:,0]
    indexs[f[0:len(f)-4]] = ns
    for j in range(ind, len(ns)):
        if ns[j,4]/ns[ind,4] > 1.2:
            if ns[ind:,4].max() / ns[ind,4] >= 1.4:
                mp.append([f[0:len(f)-4], ns[ind,0], ns[j,0], 1])
                c += 1
            else:
                mp.append([f[0:len(f)-4], ns[ind,0], ns[j][0], 0])
            break
datas = {}
for i in ds:
    for j in indexs:
        ind = np.where(indexs[j] == i)[0]
        if len(ind) < 1:
            continue
        ind = ind[0]
        if i not in datas:
            datas[i] = []
        datas[i].append([j, round((indexs[j][ind,4]/indexs[j][ind - 1,4] - 1)*100, 2)])
for i in datas:
    datas[i] = sorted(datas[i], key=lambda d:d[1])
r = (sorted(mp, key=lambda d: d[2]))
print(len(r), c , c/len(r))
cc = 0
w = 0
C = []
Z = []
for x in r:
    print(x)
    con = 0
    for i in datas:
        if i >= x[1] and i <= min(x[2], datetime.date(2021,7,31)):
            if datas[i][0][0] == x[0] or datas[i][1][0] == x[0] or datas[i][2][0] == x[0]:
                con += 1
    if con >= 1:
        cc += 1
        C.append(x[0])
        if x[-1] == 1:
            w += 1
            Z.append(x[0])
print(w, cc, w/cc, Z, C)