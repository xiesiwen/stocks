import numpy as np
import pandas as pd
import os 
import tensorflow as tf
import matplotlib.pyplot as plt

def getK(dataset):
    m = 1.1
    x = np.linspace(1, m, num=len(dataset), endpoint=True)
    y = dataset/dataset[0]
    # print(dataset,x)
    z1 = np.polyfit(x.tolist(), y.tolist(), 1)
    return z1[0]

ks = []
fs = [0 for x in range(0,11)]
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30') :
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(0,num.shape[0]):
        if num[i,0].startswith('2020') and i >= 250 and i + 40 < len(num):
            thisMin = num[i:i+40,1].min()
            lastEnd = num[i-250:i,1].max()
            lastSt = num[i-250:i,1].min()
            x = (lastEnd - lastSt) / 10
            if x == 0:
                break
            jank = int((thisMin - lastSt) /x)
            jank = max([min([jank,10]), 0])
            fs[jank] += 1
            if jank <= 0 and num[i:i+40,1].argmin() <= 30:
                if num[i+40,1] * 1.1 < num[i + 40:,1].max():
                    ks.append(1)
                else :
                    ks.append(0)
            break
print(fs, np.array(fs)/sum(fs), sum(ks)/len(ks))
