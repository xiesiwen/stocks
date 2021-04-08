import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
LEN = 5
L2 = 15
class Inc:
    month = 0
    minInd = 0
    maxInd = 0
    def __init__(self, mon, mi):
        self.month = mon
        self.minInd = mi

def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()
def getDataSet(f):
    try:
        dataset = pd.read_csv("D:/stocks-today/" + f, engine='python').to_numpy()
        res = np.where(dataset == '2021-03-15')
        return dataset[res[0][0] - LEN + 1 : res[0][0] + 1], dataset[res[0][0] - LEN + 1 : res[0][0] + 1 + L2]
    except Exception:
        return [],[]
def getL():
    mp = {}
    names = {}
    data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
    for i in range(len(data)):
        ss = data[i,2].split('-')
        if len(ss) >= 2:
            key = ss[2]
            if mp.get(key) == None:
                mp[key] = []
            ss = data[i,0].lower().split(".")
            file = ss[1]+"."+ss[0]+".csv"
            names[file] = data[i, 1]
            mp[key].append(file)
    dataset, odataset = getDataSet('sh.000001.csv')
    sh1 = dataset[:, 1]
    r = dataset[len(dataset)-1,1]/dataset[0,1]
    ds = {}
    for k in mp.keys():
        ls = mp[k]
        s0 = 0
        s5 = 0
        os0 = 0
        os5 = 0
        rs = {}
        shx = np.zeros(LEN)
        for f in ls:
            dataset, odataset = getDataSet(f)
            print(len(dataset), len(odataset))
            if len(dataset) >= LEN and len(odataset) > L2:
                s0 += dataset[0,1]
                s5 += dataset[len(dataset)-1,1]
                
                os0 += odataset[len(odataset)-L2,1]
                os5 += odataset[len(odataset)-1,1]
                if 'sz.30' not in f:
                    rs[f] = round(dataset[len(dataset)-1,1]/dataset[0,1], 2)
                shx = shx + dataset[:,1]
        up = 0
        for i in range(0, LEN - 1):
            if shx[i] > 0 and shx[i+1]/shx[i] > sh1[i+1]/sh1[i]:
                up += 1
        
        if up >= LEN / 2:
            res = []
            rs = (sorted(rs.items(), key=lambda d: d[1], reverse=True))
            for z in rs:
                if z[1] > s5/s0:
                    x = list(z)
                    x.append(names[x[0]])
                    # res.append(x)
            ds[k] = [up,os5/os0, res]
    r = (sorted(ds.items(), key=lambda d: d[1][0], reverse=True))
    c = 0
    for x in r:
        # c += len(x[1][-1])
        print(x[0], x[1][0], x[1][1], '\n')
    print(len(r), c)
    return r
# r5 = getL()
# LEN = 10
# r10 = getL()
# z = 0
# c = 0
# a,b=getDataSet('sh.000001.csv')
# for x1 in r5:
#     for x2 in r10:
#         if x1[0] == x2[0]:
#             print(x1[0], x1[1][1])
#             if x1[1][1] > b[len(b)-1,1]/b[len(b)-L2,1]:
#                 c += 1
#             z += 1
#             break
# print(z, c, c/z, b[len(b)-1,1]/b[len(b)-L2,1])

mp = {}
names = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    if len(ss) >= 2:
        key = ss[1]
        if mp.get(key) == None:
            mp[key] = []
        ss = data[i,0].lower().split(".")
        file = ss[1]+"."+ss[0]+".csv"
        names[file] = data[i, 1]
        mp[key].append(file)
# scores = {}
# ds = {}
# LEN = 20
# lines = [5,13,21,34,55,89,144,233]
# for z in range( 0,LEN, 1):
#     for i in mp:
#         c = 0
#         scs = 0
#         for j in mp[i]:
#             file = j
#             try:
#                 if file not in ds:
#                     dataset = pd.read_csv("D:/stocks-today/" + file, engine='python').to_numpy()
#                     ds[file] = dataset
#                 # dataset = ds[file][0:len(ds[file]) - z + 1]
#                 dataset = ds[file][0:len(ds[file]) - (LEN - z - 1)]
#                 # dataset = ds[file]
#                 if len(dataset) < 60:
#                     continue
#                 c += 1
#                 for l in lines:
#                     if dataset[-1,1] > getM(dataset, l):
#                         scs += 1
#             except IOError:
#                 qqq = 1
#         if scores.get(i) == None:
#             scores[i] = []
#         scores[i].append(round(scs/c,2))
# r = (sorted(scores.items(), key=lambda d: d[1][-1], reverse=True))
# ss = {}
# for z in r:
#     print(z)

hang = {}
sh001 = []
sh1DS = pd.read_csv("D:/stocks-2020/sh.000001.csv", engine='python').to_numpy()
m1 = sh1DS[0,1]
mon = 1
for i in range(1, len(sh1DS)):
    if int(sh1DS[i,0][5:7]) != mon:
        sh001.append(round(sh1DS[i-1, 1]/m1, 3))
        m1 = sh1DS[i, 1]  
        mon = int(sh1DS[i,0][5:7])
sh001.append(round(sh1DS[i-1, 1]/m1, 3))
for key in mp:
    gg = {}
    for j in mp[key]:
        file = j
        try:
            dataset = pd.read_csv("D:/stocks-2020/" + file, engine='python').to_numpy()
            if len(dataset) < len(sh1DS):
                continue
            mon = 1
            gg[file] = [Inc(mon, dataset[0,1])]
            for i in range(1, len(dataset)):
                if int(dataset[i,0][5:7]) != mon:
                    gg[file][-1].maxInd = dataset[i-1, 1]  
                    mon = int(dataset[i,0][5:7])
                    gg[file].append(Inc(mon, dataset[i, 1]))
            gg[file][-1].maxInd = dataset[-1, 1] 
        except IOError:
            qqq = 1
    hang[key] = []
    for m in range(1,13):
        s = Inc(m, 0)
        for x in gg:
            s.minInd += gg[x][m-1].minInd
            s.maxInd += gg[x][m-1].maxInd
        hang[key].append(round(s.maxInd/s.minInd, 3))
for i in range(0,12):
    r = (sorted(hang.items(), key=lambda d: d[1][i], reverse=True))
    print(i+1, sh001[i])
    for j in range(0,8):
        print(r[j][0], r[j][1][i])
    print()