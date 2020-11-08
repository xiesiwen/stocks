import numpy as np
import pandas as pd
import os,shutil
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import joblib

kms = joblib.load('C:/Users/gentl/Desktop/k50.pkl')
GAP1 = 60
GAP2 = 40
xs = []
buy = 0
win = 0
for file in os.listdir("D:/stocks"):
    if file.startswith('sz.30'):
        continue
    # if len(xs) > 20000:
    #     break
    dataset = pd.read_csv("D:/stocks/" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    start = False
    for i in range(1, num.shape[0], 5):
        if num[i,0].startswith('2020'):
            start = True
        if start and i > 1 and i + GAP1 + GAP2 < len(num):
            ps = []
            for z in range(i,i+GAP1):
                ps.append((num[z, 1]/num[z-1, 1] -1) * 100)
            x = np.array([ps])
            y = kms.predict(x)
            if y[0] == 21 :
                buy += 1
                if num[i + GAP1 + GAP2,1]/num[i + GAP1,1] > 1.2:
                    win += 1
print(buy, win, win/buy)
                
