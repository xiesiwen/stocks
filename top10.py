import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

ds = {}
doubles = {}
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(num.shape[0]):
        if "-01-" in num[i, 0]:
            if ds.get(num[i,0][0:7]) == None:
                ds[num[i,0][0:7]] = 0
                doubles[num[i,0][0:7]] = 0
            if i + 1 < num.shape[0] and num[i + 1,1]/num[i,1] > 1.099 and num[i,1] < 10:
                ds[num[i,0][0:7]] += 1
                maxc = i + 220
                if maxc > num.shape[0]:
                    maxc = num.shape[0]
                m1 = num[i:maxc,1].max()
                if m1 > 10 and m1 > num[i,1] * 2:
                    doubles[num[i,0][0:7]] += 1
                break
for i in ds:
    print(i, ds[i], doubles[i])