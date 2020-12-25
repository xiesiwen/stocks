import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os

def compute(num, n):
    # print(len(num), n)
    if num[-1,1] > num[len(num)-n:len(num),1].mean():
        return 1
    return 0
        
bks = {}
dataset = pd.read_excel("C:/Users/xiesiwen/Desktop/xx.xlsx")

num = dataset.to_numpy()
for i in range(len(num)):
    value = '-'.join(num[i,4].split('-')[0:2])
    bks[num[i,0][0:6]] = value

ranks = {}
nums = {}
lines = [5,13,21,34,55,89,144,233]
LEN = 200
for file in os.listdir("D:\\stocks"):
    if file[3:9] not in bks.keys():
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    key = bks[file[3:9]]
    if key not in ranks.keys():
        ranks[key] = [0 for x in range(LEN+1)]
        nums[key] = [0 for x in range(LEN+1)]
    if len(num) < LEN:
        continue
    for i in range(LEN,-1,-1):
        tmp = num[0:len(num)-i]
        if len(tmp) < 60:
            continue
        nums[key][LEN - i] += 1
        for x in lines:
            ranks[key][LEN - i] += compute(tmp, x)

res = {}
for k in ranks.keys():
    res[k] = np.array(ranks[k])/np.array(nums[k])
sortedDist = sorted(res.items(), key=operator.itemgetter(1)[-1], reverse=False)

# print(res[0], res[1])