import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import baostock as bs
import os 


for s in range(5):
    all = 0
    win = 0
    year = s + 2016
    files = []
    for file in os.listdir("D:\\stocks"):
        if file.startswith('sz.30'):
            continue
        dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
        num = dataset.to_numpy()
        if num.shape[0] == 0:
            continue
        for i in range(num.shape[0]):
            if str(year)+"-01" in num[i,0]:
                minPrice = num[i:i+45,1].min()
                minInd = i + 45
                hDate = max([0, i - 1200])
                if hDate < i and minPrice < 15:
                    hmin = num[hDate:i, 1].min()
                    hmax = num[hDate:i, 1].max()
                    if hmax > hmin and (minPrice - hmin) / (hmax-hmin) <0.10 and minInd< min([i+250, num.shape[0]-1]):
                        if num[minInd: min([i+250, num.shape[0]-1]),1].max() > minPrice * 1.5:
                            win += 1
                            files.append(file)
                        all += 1
                break
    print(year, win, all, win/all)
    # if year == 2018:
    #     print(files)


    
