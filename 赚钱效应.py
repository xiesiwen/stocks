from audioop import avg
import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
n = pd.read_excel('2021-08-14.xlsx').to_numpy()
mp = {}
GL = '新能源整车'
for x in n:
    gl = []
    stock = x[0][7:9].lower()+'.'+x[0][0:6]
    if len(x[5]) > 0:
        gl.extend(x[5].split(';'))
    for g in gl:
        if g not in mp:
            mp[g] = []
        mp[g].append([stock, x[1]])
mpl.rc("font",family='YouYuan')
rs = []
result = {}
lenz = 0
for f in mp[GL]:
    dataset = pd.read_csv("./stock-today/" + f[0] + '.csv', encoding='gbk')
    num = dataset.to_numpy()
    s = np.where(num == '2022-04-01')
    if len(s) == 0 or len(s[0]) == 0:
        continue
    s = s[0][0]
    name = f[1]
    rs.append([name, num[s:len(num)]])
    lenz = len(num) - s
    result[name] = []
res = []
for x in range(0, lenz):
    amount = 0
    inc = 0
    print(x, rs[0][1][x, 0])
    for i in rs:
        item = i[1][x]
        if item[2] < item[1]:
            inc += item[-3]*(item[1] + item[2])/2
        amount += item[-3]*(item[1] + item[2])/2
    res.append(inc/amount)
resa = []
for i in range(0, lenz):
    if i < 2:
        resa.append(res[i])
    else:
        s = 0
        s += 1 if res[i- 2] > 0.5 else 0
        s += 1 if res[i- 1] > 0.5 else 0
        s += 1 if res[i] > 0.5 else 0
        resa.append(s/3)
plt.plot([j for j in range(0, lenz)], resa)
plt.plot([j for j in range(0, lenz)], [0.5 for j in range(0, lenz)])
plt.show()