
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 

for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocks\\"+file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0 or num[-1,1] > 10:
        continue
    x = []
    w10 = 0
    w20 = 0
    w30 = 0
    w40 = 0
    a10 = 0
    gap = 20
    win = []
    loss = []
    for i in range(60, num.shape[0]):
        if num[i-60:i+gap,1].argmin() == 60 and i + 60 + gap < num.shape[0]:
            buy = num[i+gap,1]
            minp = num[i-60:i+gap,1].min()
            if num[i+10+gap,1] > buy:
                w10 += 1
            if num[i+20+gap,1] > buy:
                w20 += 1
            if num[i+30+gap,1] > buy:
                w30 += 1
            if num[i+40+gap,1] > buy:
                w40 += 1
            a10 += 1
            JACK = 1 + (1 - minp/buy) * 3
            back = 0
            c = 0
            for j in range(i + gap, i+60+gap):
                if num[j, 1] <= minp:
                    loss.append(num[j,1]/buy - 1)
                    c = 2
                    break
                elif num[j,1] / buy > JACK:
                    if back == 1:
                        win.append(num[j,1]/buy - 1)
                        c = 1
                        break
                    back = 1
            if c == 0:
                if num[i+60+gap,1] > buy:
                     win.append(num[i+40+gap,1]/buy - 1)
                else : loss.append(num[i+40+gap,1]/buy - 1)
    if a10 > 0:
        print(file, w10/a10, w20/a10, w30/a10, w40/a10, a10, len(win)/(len(win) + len(loss)), np.mean(win), np.mean(loss))
    else : print(file)