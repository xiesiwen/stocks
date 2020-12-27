import numpy as np
import pandas as pd
import os,shutil
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import joblib

GAP1 = 60
GAP2 = 20
g20 = 0
g30 = 0
sh = []
xs = []
ys = []
ys1 = []
ys2 = []
yes = []
xs_test = []
ys_test = []
files = []
dates = []
for file in os.listdir("D:/stocks"):
    if file.startswith('sz.30'):
        continue
    if len(xs) > 100000:
        break
    dataset = pd.read_csv("D:/stocks/" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(int(num.shape[0]/4), num.shape[0], 5):
        if i + GAP1 + GAP2 < num.shape[0]:
            if num[i, 0].startswith('2020'):
                xs_test.append((num[i:i+GAP1, 1]/num[i, 1] - 1) * 100)
            else:
                ps = []
                for z in range(i,i+GAP1):
                    ps.append((num[z, 1]/num[z-1, 1] -1) * 100)
                xs.append(ps)
                sh.append(num[i:i+GAP1,1])
                files.append((file,num[i, 0]))
                c = 0
                for x in range(i+GAP1,i+GAP1+GAP2):
                    if num[x,1] > num[i + GAP1,1]:
                        c += 1
                if c > GAP2 * 0.75:
                    ys.append(1)
                else: ys.append(0)
                if num[i+GAP1+GAP2,1] > num[i+GAP1, 1] * 1.3 :
                    ys1.append(1)
                else : ys1.append(0)
                if i+GAP1+60 < num.shape[0] and num[i+GAP1+60,1] > num[i+GAP1, 1] * 1.4 :
                    ys2.append(1)
                else : ys2.append(0)

xs = np.array(xs)
ys = np.array(ys)
ys1 = np.array(ys1)
ys2 = np.array(ys2)
shuffle_ix = np.random.permutation(np.arange(len(xs)))
xs = xs[shuffle_ix]
ys = ys[shuffle_ix]
ys1 = ys2[shuffle_ix]
ys2 = ys2[shuffle_ix]
points = np.array(xs)

num_clusters = 30
kms = KMeans(n_clusters=num_clusters).fit(xs)
joblib.dump(kms, 'C:/Users/gentl/Desktop/k50.pkl')
yys = kms.predict(xs)
js = [[] for x in range(num_clusters)]
js1 = [[] for x in range(num_clusters)]
js2 = [[] for x in range(num_clusters)]
fss = [[] for x in range(num_clusters)]
for i, point in enumerate(yys):
    js[point].append(ys[i])
    fss[point].append(files[i])
    js1[point].append(ys1[i])
    js2[point].append(ys2[i])

print(sum(ys)/len(ys),sum(ys1)/len(ys1),sum(ys2)/len(ys2),len(ys),'\n----------')
cs = 0
win0 = 0
win1 = 0
win2 = 0
for i in range(len(js)):
    cs += len(js[i])
    y0 = 0
    y1 = 0
    y2 = 0
    if len(js[i]) > 0:
        y0 = sum(js[i])/len(js[i])
        y1 = sum(js1[i])/len(js1[i])
        y2 = sum(js2[i])/len(js2[i])
    print(i, y0, len(js[i]), y1, len(js1[i]) ,y2, len(js2[i]))
    if y0 > 0.6:
        win0 += len(js[i])
        # print(fss[i])
        print('GKD!')
    if y1 > 0.6:
        win1 += len(js1[i])
    if y2 > 0.6:
        win2 += len(js2[i])
print(cs, win0, win0/cs, win1, win1/cs, win2, win2/cs)