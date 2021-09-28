import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
GAP = 120
show = ['氟化工','有机硅','钠离子电池','军工','钴','储能','稀土永磁','稀缺资源','HIT电池','光伏建筑一体化','光伏概念','盐湖提锂','宁德时代概念','锂电池','国家大基金持股','第三代半导体','MCU芯片']
def filter(num, day, gap, loss, mrate, gls):
    x = 0
    for z in range(len(num) - gap, len(num)):
        m = getM(num[0:z,1], day)
        if num[z,1] < m:
            x+=1
    if x <= loss and round(min(abs(num[-1,3]/getM(num[:,1], day) - 1), abs(num[-1,4]/getM(num[:,1], day) - 1)),3) < mrate:
        for i in gls:
            if i in show:
                return (True, i)
    return (False, "")
def getM(d, g):
    if len(d) >= g:
        return d[len(d) -g:].mean()
    if len(d) == 0:
        return 0
    return d.mean()
def mg(d, g, gap):
    s = len(d) - gap
    c = 0
    z = 0
    for z in range(s, len(d)):
        m = getM(d[0:z,1], g)
        if d[z,1] < m:
            c+=1
    return round(c/(len(d)-s),2)
def getGap(d, g):
    if g == 30:
        return mg(d,g,120) <= 0.2 or mg(d,g,80) <= 0.16 or mg(d,g,60) <= 0.12 or mg(d,g,40) <= 0.1
    elif g == 60:
        return mg(d,g,120) <= 0.16 or mg(d,g,80) <= 0.12 or mg(d,g,60) <= 0.1 or mg(d,g,40) <= 0.08
    elif g == 250:
        return mg(d,g,60) <= 0. and mg(d,g,40) <= 0
    return False
def jacks2(num):
    L = 12
    temps = []
    tops = []
    bottoms = []
    i = L
    while(i < len(num) - L):
        if num[i,4] >= num[i-L : i+L, 4].max():
            temps.append(i)
            i += L - 1
        i += 1
    if len(temps) > 0:
        tops.append(temps[0])
        for i in range(1,len(temps)):
            if i == len(temps) -1 :
                z = 5
            else:
                z = 8
            am = num[tops[-1]:temps[i],3].argmin()
            if am >= z and temps[i] - am - tops[-1] >= z:
                if i < len(temps) - 2: 
                    if num[temps[i]:temps[i + 1],3].argmin() >= z:
                        bottoms.append(am+tops[-1])
                        tops.append(temps[i])
                else:
                    bottoms.append(am+tops[-1])
                    tops.append(temps[i])
    return tops, bottoms

n = pd.read_excel('2021-08-14.xlsx').to_numpy()
mp = {}
for x in n:
    mp[x[0][7:9].lower()+'.'+x[0][0:6]] = [x[1], x[5].split(';')]

PATHO = "./stock-today"
r = {}
for x in show:
    r[x] = []
c = 0
for file in os.listdir(PATHO):
    if file.startswith('sz.30') or file.startswith('sh.688'):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if len(num) < GAP or num[-1,1] > 70:
        continue
    if file[0:9] in mp and 'ST' not in mp[file[0:9]][0]:
        g3 = getGap(num, 30)
        g6 = getGap(num, 60)
        g250 = getGap(num, 250)
        if g3 and g6:
            for x in mp[file[0:9]][1]:
                if x in show:
                    r[x].append((file[0:9], mp[file[0:9]][0]))
for x in r:
    if len(r[x]) == 0:
        continue
    print(x, '\n',r[x])