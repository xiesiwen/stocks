from numpy.lib.function_base import average
import pandas as pd
import os
import numpy as np
PATHO = "./stock-today"
c = 0
fx = []
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
    mv = np.mean(num[len(num)-12:len(num)-2,5])
    if num[-1,5] > mv * 2.6 and num[-2, 5] > mv*2.6 and num[-3,5] < mv*2.6 and num[-4,5] < mv*2.6 and num[-1, -2] > -num[-2,-2]/2 and num[-2,-2] > 0:
        fx[file] = np.mean(num[-2:-1,5]) / mv
        c += 1
r = sorted(fx.items(), key = lambda k:(k[1]), reverse=True)
print(r)
print(c)