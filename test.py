import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd
import time
import os
import operator

hys = {}
minY = 20209999
for i in os.listdir('hangye'):
    hys[i] = []
    with open('hangye/'+i, 'r', encoding='UTF-8') as f:
        fs = f.readlines()
        ds = []
        if minY > int(fs[0][0:8]):
            minY = int(fs[0][0:8])
        for s in fs:
            
            if s.startswith('2020') or s.startswith('201912'):
                ds.append(float(s.split(',')[-3]))
        for z in range(1, len(ds)):
            hys[i].append(round(ds[z]/ds[z-1],3))
print(minY)
for i in range(0, 12):
    r = sorted(hys.items(), key = lambda b : b[1][i], reverse=True)
    print(i+1)
    for z in r[0:8]:
        print(z[0].split('.')[0],z[1][i])
    print('\n')