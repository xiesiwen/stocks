import pandas as pd
import os
import numpy as np
PATHO = "./stock-today"
c = 0
for file in os.listdir(PATHO):
    if file.startswith('sz.30'):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if len(num) < 30:
        continue
    mv = min(num[:,5])
    if num[-1,5] > mv * 2 and num[-2, 5] > mv*2 and num[-3,5] < mv*2 and num[-4,5] < mv*2 and num[-1, -2] > -num[-2,-2]/2 and num[-2,-2] > 0:
        print(file)
        c += 1
print(c)