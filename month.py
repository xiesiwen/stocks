import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json
import mplfinance as mpf

death = ['sh.600028', 'sh.601658', 'sh.601668', 'sh.601939.csv','sh.601997.csv','sh.603323.csv',
'sh.601818.csv','sz.002936.csv','sh.601577.csv',]
def pr(*arg):
    if False:
        print(arg)

def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1].mean()
    if len(d) == 0:
        return 0
    return d.mean()
R = {30:0.9, 60:0.95}
def getGap(d, g):
    s = 0
    for i in range(d.argmin(),len(d)):
        if d[i] >= getM(d[0:i],g):
            s = i
            break
    c = 0
    for z in range(s, len(d)):
        m = getM(d[0:z], g)
        if d[z] < m:
            c+=1
        
        if m > 0 and d[z] <= m*R[g]:
            return -1
    return c

def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
mp = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    if len(ss) >= 2:
        key = ss[0] + "-" + ss[1]
        mp[data[i,0][0:6]] = key
        
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
    
    de = False
    
    # itemindex = np.argwhere(num == '2019-09-30')
    # if len(itemindex) < 1:
    #     continue
    # num = num[0:itemindex[0][0]]

    if de:
        continue
    
    ns = num[:,1]
    if len(ns) - ns.argmin() < 60 or ns[-1] >= 30:
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
    g3 = getGap(ns,30)
    g6 = getGap(ns, 60)
    if g3 >= 0 and g6 >= 0:
        hs[key].append([file,g3,g6, res2[0]])
c1 = 0
t = ks/c
for k in hs.keys():
    a = hs[k]    
    a = [i for i in a if i[3] > t]
    a.sort(key=lambda b:b[1] * 1000 + b[2])
    c1 += len(a)
    print(k, a, len(a))
print(c1)