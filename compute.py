import numpy as np
import pandas as pd
import os 
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
line = linear_model.LinearRegression()

def getK(dataset):
    x = np.arange(len(dataset)) + 1
    # print(dataset,x)
    z1 = np.polyfit(x.tolist(), dataset.tolist(), 1)
    plt.scatter(x, dataset)
    plt.plot(x, z1[0] * x + z1[1])
    # plt.show()
    return z1[0]
GAP1 = 60
GAP2 = 20
all = 0
g20 = 0
g30 = 0
xs = []
ys = []
yes = []
xs_test = []
ys_test = []
sc = MinMaxScaler(feature_range=(0, 1)) 
c = 100
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    # print(file)
    c -= 1
    if c == 0:
        break
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(120,num.shape[0],5):
        if i + GAP1 + GAP2 < num.shape[0]:
            z = 0
            for x in range(i+1,i+21):
                if num[x,1] > num[i,1]:
                    z += 1
            if z >= 20 * 0.9:
                y = 1
            else : y = 0
            xs.append(y)
            k1 = getK(num[i-60:i,1])
            k2 = getK(num[i-120:i,1])
            if k1 > k2 and k1 >= 0:
                ys.append(y)
print(len(xs), len(ys), sum(xs)/len(xs), sum(ys)/len(ys))
