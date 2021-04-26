import numpy as np
import pandas as pd
import os 

LEN = 10
def jacks(num):
    tops = [-LEN]
    bottoms = [-LEN]
    for i in range(LEN, len(num) - LEN):
        if num[i,4] >= num[i- LEN: i+LEN, 4].max():
            if i > tops[-1] + LEN:
                tops.append(i)
        if num[i,3] <= num[i- LEN: i+LEN, 3].min():
            if i > bottoms[-1] + LEN:
                bottoms.append(i)
    return tops[1:], bottoms[1:]
names = {}
data = pd.read_excel("D:/stock/hangye.xlsx", usecols = [0, 1, 4]).to_numpy()
for i in range(len(data)):
    ss = data[i,2].split('-')
    if len(ss) >= 2:
        key = ss[2]
        ss = data[i,0].lower().split(".")
        file = ss[1]+"."+ss[0]+".csv"
        names[file] = data[i, 1]
c = 0
for file in os.listdir("D:\\stocks-today"):
    if file.startswith('sz.30') :
        continue
    dataset = pd.read_csv("D:\\stocks-today\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    if num[-1,1] > 20:
        continue
    mInd = num[:,1].argmin()
    tops, btms = jacks(num[mInd:])
    if len(tops) < 2 or len(btms) < 2 or len(num) - mInd < 40:
        continue
    p = True
    if len(btms) > 1:
        for i in range(max(1, len(btms)-3), len(btms)):
            if num[mInd+btms[i], 3] < num[mInd+btms[i-1], 3]*0.95:
                p = False
                break
    for i in range(max(1, len(tops)-3), len(tops)):
        if num[mInd+tops[i], 4] < num[mInd+tops[i-1], 4]*0.95:
            p = False
            break
    if '002015' in file:
        print(tops, btms, num[np.array(tops)+mInd], num[np.array(btms)+mInd], p)
    if p and num[mInd+tops[-1], 1] >= num[mInd+tops[-2], 1]*1.08 and 'ST' not in names[file]:
        print(file, names[file])
        c += 1
print(c)