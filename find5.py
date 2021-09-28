import numpy as np
import pandas as pd
import os

def getM2(d, g):
    if len(d) >= g:
        return d[len(d) -g : len(d)-1,1].mean()
    return d[:,1].mean()

PATHO = "./stock-today"
c =0
for file in os.listdir(PATHO):
    if file.startswith('sz.30'):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if num.shape[0] < 100 or num[-1,1] > 20 or num[-1,1] < getM2(num, 60):
        continue
    n = num[:,6]
    for i in range(0, 5):
        x = n[len(n) - 5 - i: len(n) - i]
        if np.all(x > 0) and np.all(x <= 4):
            print(file)
            c += 1
            break
print(c)