import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

ds = {}
keys = []
for i in range(1,13):
    s = '-%02d-' % i
    ds[s] = []
    keys.append(s)
dd = [0 for i in range(13)]
rs = []
for file in os.listdir("D:\\stocksM"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocksM\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    temp = {}
    count = {}
    arg = {}
    for k in keys:
        temp[k] = []
        count[k] = 0
        arg[k] = []
    if num.shape[0] == 0 or num[-1, 1] > 10 or int(num[0,0][0:4]) > 2012 or int(num[-1,0][0:4]) < 2020:
        continue
    for i in range(num.shape[0]):
        k = num[i,0][4:8]
        count[k] += 1
        if num[i,4] > 0:
            temp[k].append(num[i,0][0:7])
            arg[k].append(num[i,4])
    for k in keys:
        if len(temp[k])/count[k] >= 0.7 and np.min(arg[k][len(arg[k]) - 5: len(arg[k]) - 1]) > 5:
            dd[int(k[1:3])] += 1
            if int(k[1:3]) == 11:
                print(file, len(temp[k]), count[k], len(temp[k])/count[k], np.mean(arg[k]))
                dataS = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
                ns = dataS.to_numpy()
                startPrice = 0
                for j in range(ns.shape[0]):
                    find = False
                    for month in temp[k]:
                        if ns[j,0].startswith(month):
                            find = True
                            if startPrice == 0:
                                startPrice = ns[j,1]
                            else : rs.append(ns[j,1]/startPrice - 1)
                    if find == False:
                        startPrice = 0
                    
print(dd)



# plt.figure()									#打印样本点
# plt.scatter(range(len(rs)),rs)						#把x_data和y_data传进来
# plt.show()