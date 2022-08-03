import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
fs = ['sz.002466','sz.000821', 'sh.601908', 'sh.603063']
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
if len(mp[GL]) > 40:
    bucket = len(mp[GL]) / 40
else:
    bucket = 0
mpl.rc("font",family='YouYuan')
i = 1
rs = []
for f in mp[GL]:
    # if i < bucket:
    #     i += 1
    #     continue
    # else :
    #     i = 1
    dataset = pd.read_csv("./stock-today/" + f[0] + '.csv', encoding='gbk')
    num = dataset.to_numpy()
    s = np.where(num == '2022-04-26')
    if len(s) == 0 or len(s[0]) == 0:
        continue
    s = s[0][0]
    # if num[-1, 1]/ num[s,1] < 2:
    #     continue
    plt.plot([x-s for x in range(s, len(num))], num[s:len(num), 1]/ num[s,1], label=f[1])
    rs.append([f[1], num[-1, 1]/ num[s,1]])
r = sorted(rs, key = lambda k:(k[1]), reverse=True)
print(r)
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()