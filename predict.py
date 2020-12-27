import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json
import mplfinance as mpf

death = ['sh.600028', 'sh.601658', 'sh.601668', 'sh.601939.csv','sh.601997.csv','sh.603323.csv',
'sh.601818.csv','sz.002936.csv','sh.601577.csv',]
def pr(*arg):
    if False:
        print(arg)

def drawImage(file):
    columns_json_str = '{"date":"Date","open":"Open","close":"Close","high":"High","low":"Low","volume":"Volume"}'
    columns_dict = json.loads(columns_json_str)
    data=pd.read_csv('D:/stocks/'+file, index_col= 'date', usecols=['date','open','close','high','low','volume'])
    data.rename(columns=columns_dict, inplace=True)
    data.index = pd.DatetimeIndex(data.index)
    mpf.plot(data, type='candle', mav=(5, 10), volume=True, style='charles',savefig='C:/Users/gentl/Desktop/images/'+file+".png")
def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

PATHO = "D:/stocks-today"
PATH = "D:/AndroidStudioProjects/aStocks/app/src/main/assets/stocks/chan"
# setDir(PATH)
c=0
rs = []
ds = [0 for x in range(0, 20)]
for file in os.listdir(PATHO):
    if not (file.startswith('sh.60') or file.startswith('sz.00')):
        continue
    try:
        dataset = pd.read_csv(PATHO + "/" + file, encoding='gbk')
    except:
        continue
    num = dataset.to_numpy()
    if num.shape[0] == 0 or num[-1,-1] != 0:
        continue
    c += 1
    de = False
    for s in death:
        if file.startswith(s):
            de = True
            break
    if de:
        continue
    
    ns = num[:,1]
    m1 = ns.argmin()
    ns = ns[m1:len(ns)]
    if len(ns) < 40 or ns[-1] >= 10 or ns[-1]/ns[0] < 1.2 or len(ns) - ns.argmax() > 20 or ns.max()/ns.min() > 3:
        continue
    ns = np.array(ns/ns.min(),dtype='float32')
    x = np.array(np.arange(len(ns)),dtype='float32')*0.005
    res2 = np.polyfit(x, ns, 1)
    res3 = np.polyfit(np.array(np.arange(10),dtype='float32')*0.005, ns[len(ns)-10:len(ns)], 1)
    if res2[0] >= 0.03 and res3[0] < res2[0]/2:
        rc = np.poly1d(res2)
        start = max(m1, 30)
        tmp = num[:,1]
        tmp /= tmp.min()
        gank = False
        c2 = 0
        # for i in range(start, len(tmp)):
        #     arg = tmp[i-29:i+1].mean()
        #     if tmp[i] >= arg :
        #         gank = True
        #     elif tmp[i] < arg:
        #         if gank:
        #             c2 += tmp[i] - arg
        # if tmp[-1] >= tmp[-30:0].mean()*0.95:

        rs.append([c2, file, len(ns), num[m1,0]])
        # shutil.copy(PATHO + "/" + file, PATH + "/" + file.split('.')[1] + '.' + str(date))
rs.sort(key=lambda student: student[0])
for r in rs:
    print(r[1][3:9])
print(c)
print(len(rs))