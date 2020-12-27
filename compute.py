import numpy as np
import pandas as pd
import os 
import tensorflow as tf
import .pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
line = linear_model.LinearRegression()

def getK(dataset):
    m = 1.1
    x = np.linspace(1, m, num=len(dataset), endpoint=True)
    y = dataset/dataset[0]
    # print(dataset,x)
    z1 = np.polyfit(x.tolist(), y.tolist(), 1)
    return z1[0]
GAP1 = 60
GAP2 = 20
all = 0
g20 = 0
g30 = 0

yes = []
sc = MinMaxScaler(feature_range=(0, 1)) 
c = 100
g = 1
days = [0 for x in range(0,13)]
rates = [0 for x in range(0,26)]
months = [0 for x in range(0,13)]
emmonths = [0 for x in range(0,13)]
endmonths = [0 for x in range(0,13)]
ds = [0 for x in range(0,33)]
endds = [0 for x in range(0,33)]
fs = [0 for x in range(0,11)]
ks = []
cs = 0
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30') :
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    startYear = num[0,0][0:4]
    startInd = 0
    lastSt = 0
    lastEnd = 0
    for i in range(0,num.shape[0]):
        if num[i,0].startswith(startYear) or startInd == i - 1:
            continue
        end = i -1
        minInd = num[startInd:end,1].argmin() + startInd
        maxInd = num[startInd:end,1].argmax() + startInd
        emmonths[int(num[minInd,0][5:7])] += 1
        cs += 1
        if maxInd < minInd or num[maxInd,1] < num[minInd,1] * 1.5:
            startInd = i
            startYear = num[i,0][0:4]
            continue
        days[int((maxInd - minInd)/22)] += 1
        r = int(num[maxInd,1]/num[minInd,1]*10)
        if r > 40:
            r = 40
        rates[r-15] += 1
        months[int(num[minInd,0][5:7])] += 1
        endmonths[int(num[maxInd,0][5:7])] += 1
        ds[int(num[minInd,0][8:])] += 1
        endds[int(num[maxInd,0][8:])] += 1
        thisMin = num[startInd:end,1].min()
        if lastEnd > 0:
            x = (lastEnd - lastSt) / 10
            jank = int((thisMin - lastSt) /x)
            jank = max([min([jank,10]), 0])
            fs[jank] += 1
        lastSt = num[startInd:end,1].min()
        lastEnd = num[startInd:end,1].max()
        startInd = i
        startYear = num[i,0][0:4]
        # if i > 20:
        #     k = getK(num[i-20:i,1])
        #     if k > 8:
        #         k = 8
        #     ks.append(k)
s = sum(days)
print(s, cs)
print(days, np.array(days)/s)
print(rates, np.array(rates)/s)
print(months, np.array(months)/s)
print(emmonths, np.array(emmonths)/sum(emmonths))
print(endmonths, np.array(endmonths)/s)
print(ds, np.array(ds)/s)
print(endds, np.array(endds)/s)
print(fs, np.array(fs)/sum(fs))
# x = 0
# for i in ks:
#     if i < 0.5:
#         x += 1
# print(x, x/len(ks))
# plt.scatter([x for x in range(len(ks))],ks)
# plt.show()