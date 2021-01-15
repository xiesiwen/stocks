import numpy as np
import pandas as pd

file = "sh.601899.csv"
W = 100000
dataset = pd.read_csv("D:/stocks-today-m/" + file, encoding='gbk')
num = dataset.to_numpy()
dataStart = 202012161000 * W
dataEnd = 202012301500 * W
F = 0
s1 = (np.where(num == dataStart))[0][0]
s2 = (np.where(num == dataEnd))[0][0]
F = num[s1,3] * (num[s1+1,2] - num[s1,3]) + num[s2,2] * (num[s2,4] - num[s2,2])
print(num[s1], num[s2])
for i in range(s1 + 1, s2):
    F += num[i,2] * (num[i+1, 2] - num[i,2])
print(F)