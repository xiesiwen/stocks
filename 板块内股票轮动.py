import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
n = pd.read_excel('2021-08-14.xlsx').to_numpy()
mp = {}
GL = '盐湖提锂'
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
    s = np.where(num == '2022-04-27')
    if len(s) == 0 or len(s[0]) == 0:
        continue
    s = s[0][0]
    name = f[1]
    rs.append([name, num[s:len(num) - 12]])
    lenz = len(num) - s - 12
    result[name] = []
for x in range(0, lenz):
    r = sorted(rs, key = lambda k:(k[1][x, -2]), reverse=True)
    for j in range(0, len(r)):
        result[r[j][0]].append(j)
result = sorted(result.items(), key = lambda k:(sum(k[1])))
for x in result:
    print(x)
    print([j for j in range(0, lenz)], x[1])
    plt.plot([j for j in range(0, lenz)], x[1], label=x[0])
    
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()