import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()

mp = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    if len(ss) >= 2:
        key = ss[0] + "-" + ss[1]
        if mp.get(key) == None:
            mp[key] = []
        mp[key].append(data[i])

scores = {}
ds = {}
LEN = 20
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
                dataset = ds[file][0:len(ds[file]) - (LEN - z - 1)]
                # dataset = ds[file]
                if len(dataset) < 60:
                    continue
                c += 1
                for l in lines:
                    if dataset[-1,1] > getM(dataset, l):
                        scs += 1
            except IOError:
                qqq = 1
        if scores.get(i) == None:
            scores[i] = []
        scores[i].append(round(scs/c,2))
r = (sorted(scores.items(), key=lambda d: d[1][-1], reverse=True))
ss = {}
for z in r:
    print(z)
    # for x in z[1]:
    #     if x > 6.5:        
    #         ss[z[0]] = z[1]
    # plt.plot(np.arange(len(z[1])),z[1])
    # plt.show()
# zs = {}
# for i in range(LEN):
#     r = (sorted(scores.items(), key=lambda d: d[1][i], reverse=True))
#     for ind,z in enumerate(r):
#         if z[0] not in zs:
#             zs[z[0]] = 0
#         zs[z[0]] += ind
# print((sorted(zs.items(), key=lambda d: d[1])))