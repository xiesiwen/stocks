import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
dataset = pd.read_csv("./stock-today/sh.600000.csv", encoding='gbk')
num6 = dataset.to_numpy()
time = num6[-1,0]
rs = {}
result = {}
lenz = 0
l2 = {}
l3 = {}
l4 = {}
l5 = {}
for f in os.listdir("./stock-today/"):
    dataset = pd.read_csv("./stock-today/" + f, encoding='gbk')
    num = dataset.to_numpy()
    if len(num) == 0:
        continue
    s = np.where(num == time)
    if num[-1,0] != time or num[-1,-1] != 0:
        continue
    s = np.where(num == '2022-04-08')
    if len(s) == 0 or len(s[0]) == 0 or num[-1,-1] != 0:
        continue
    s = s[0][0]
    if s < 5:
        continue
    for x in range(s, len(num)):
        date = num[x, 0]
        if date not in l2:
            l2[date] = 0
        if date not in l3:
            l3[date] = 0
        if date not in l4:
            l4[date] = 0
        if date not in l5:
            l5[date] = 0
        # print(num[x: x + 3, -2] > 0)
        if np.all(num[x -1: x+1, -2] > 0):
            l2[date] += 1
        if np.all(num[x -2: x+1, -2] > 0):
            l3[date] += 1
        if np.all(num[x - 3: x+1, -2] > 0):
            l4[date] += 1
        if np.all(num[x - 4: x+1, -2] > 0):
            l5[date] += 1
for k in range(1, len(l3.keys())):
    x = list(l3.items())[k][0]
    lk = list(l3.items())[k-1][0]
    print(x, l2[x], l3[x], round(l3[x]/l2[lk],2),  l4[x],round(l4[x]/l3[lk],2), l5[x],round(l5[x]/l4[lk],2))
    if l2[x] > 700 and (l3[x] > 250 or l4[x] > 200) and round(l3[x]/l2[lk],2) > 0.5 and round(l4[x]/l3[lk],2) > 0.5:
        print('good')
    if l2[x] < 500 or l3[x] < 200:
        print('out')
# plt.plot([x for x in l3.keys()], [l3[x] for x in l3.keys()])
# plt.xticks(rotation=-30)
# plt.show()
