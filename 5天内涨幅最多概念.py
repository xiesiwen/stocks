import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
ignore = ['融资融券','转融券标的','富时罗素概念股','富时罗素概念','标普道琼斯A股','深股通','地方国资改革','半年报预增','沪股通',
'MSCI概念','新股与次新股','央企国资改革','ST板块',]
n = pd.read_excel('2021-08-14.xlsx').to_numpy()
mp = {}
for x in n:
    gl = []
    stock = x[0][7:9].lower()+'.'+x[0][0:6]
    if len(x[5]) > 0:
        gl.extend(x[5].split(';'))
    mp[stock] = []
    for g in gl:
        if g not in ignore:
            mp[stock].append(g)
dataset = pd.read_csv("./stock-today/sh.600000.csv", encoding='gbk')
num = dataset.to_numpy()
time = num[-1,0]
rs = {}
result = {}
lenz = 0
for f in os.listdir("./stock-today/"):
    dataset = pd.read_csv("./stock-today/" + f, encoding='gbk')
    num = dataset.to_numpy()
    s = np.where(num == time)
    if len(s) == 0 or len(s[0]) == 0 or num[-1,-1] != 0:
        continue
    s = s[0][0]
    if s-5 >0 and num[s, 1]/num[s-5, 2] > 1.18:
        result[f] = num[s, 1]/num[s-5, 2]
        f = f[0:9]
        if f in mp:
            for x in mp[f]:
                if x not in rs:
                    rs[x] = []
                rs[x].append(f)
result = sorted(rs.items(), key = lambda k:(len(k[1])), reverse=True)
for x in result[0:20]:
    print(x[0], len(x[1]), x[1])