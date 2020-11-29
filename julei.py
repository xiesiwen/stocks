import numpy as np
import pandas as pd
import os,json
import matplotlib.pyplot as plt
import mplfinance as mpf
import shutil
count = 0
filepath = "D:/image1"
RANGE = 120
DIFF = 40
def getRect(num, index):
    diff = num[index - 5:index].mean() - num[index - 10:index].mean()
    c = 0
    i = 0
    start = 0
    for x in range(index - 1, 20, -1):
        d = num[x - 5:x].mean() - num[x - 10:x].mean()
        if d * diff < 0:
            if start == 0:
                start = x
            c += abs(d)
            i = x
        elif c > 0:
            break
    return [c, i, start - x, index - start]
def save(file):
    columns_json_str = '{"date":"Date","open":"Open","close":"Close","high":"High","low":"Low","volume":"Volume"}'
    columns_dict = json.loads(columns_json_str)

    data=pd.read_csv('D:/stocks/'+file,index_col= 'date',usecols=['date','open','close','high','low','volume'])
    data.rename(columns=columns_dict, inplace=True)
    data.index = pd.DatetimeIndex(data.index)
    mpf.plot(data, type='candle', mav=(5, 10), volume=True, style='charles',savefig=filepath+"/" + file +'.png')
if not os.path.exists(filepath):
    os.mkdir(filepath)
else:
    shutil.rmtree(filepath)
    os.mkdir(filepath)

for file in os.listdir("D:/stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:/stocks/" + file, encoding='gbk').tail(RANGE+DIFF)
    num = dataset.to_numpy()[:,1]
    if num.shape[0] < RANGE + DIFF or dataset.to_numpy()[0,-1] != 0:
        continue
    size = num.shape[0]
    ind = num.argmin()
    
    if ind < size - DIFF:
        continue
    for x in range(ind, size):
        if num[x - 5:x].mean() > num[x - 10:x].mean():
            size = x
            break
    
    x = np.arange(0, RANGE)
    y = np.array(num[size - RANGE:size],dtype='float')
    f = np.polyfit(x, y, 1)
    ks = np.poly1d(f)
    if (ks[1] < 0 and num[size - 5:size].mean() > num[size - 10:size].mean() and num[size - 1] < 10):
        save1 = False
        for size in range(size, num.shape[0]):
            z = getRect(num, size)
            if z[1] == 0:
                continue
            y = getRect(num, z[1])
            if y[0] > z[0]:
                save1 = True
        if save1:
            print(file, z, y)
            count += 1
            save(file)
print(count)
