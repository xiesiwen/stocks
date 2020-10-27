import numpy as np
import pandas as pd
import os 

ds = {}
keys = []
for i in range(1,13):
    s = '-%02d-' % i
    ds[s] = []
    keys.append(s)
dd = [0 for i in range(13)]
for file in os.listdir("D:\\stocksM"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocksM\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    temp = {}
    count = {}
    arg = {}
    for k in keys:
        temp[k] = 0
        count[k] = 0
        arg[k] = 0
    if num.shape[0] == 0 or num[-1, 1] > 10 or int(num[0,0][0:4]) > 2012 or int(num[-1,0][0:4]) < 2020:
        continue
    for i in range(num.shape[0]):
        k = num[i,0][4:8]
        count[k] += 1
        if num[i,4] > 0:
            temp[k] += 1
            arg[k] = num[i,4]
    for k in keys:
        if temp[k]/count[k] >= 0.8:
            dd[int(k[1:3])] += 1
            if int(k[1:3]) == 11:
                print(file, k[1:3], temp[k], count[k], temp[k]/count[k], arg[k]/temp[k])
    
print(dd)