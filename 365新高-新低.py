import os
import pandas as pd
import numpy as np

newTop = 0
newLow = 0
for file in os.listdir("./stock-today"):
    if file.startswith('sz.30') :
        continue
    dataset = pd.read_csv("./stock-today/" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    num = num[max(0, len(num) - 250):,1]
    if num.max() == num[-1]:
        newTop += 1
    if num.min() == num[-1]:
        newLow += 1
print(str(newTop)+"/"+str(newLow))