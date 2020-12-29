import numpy as np
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt
import json
import mplfinance as mpf

def pr(*arg):
    if False:
        print(arg)

def findJacks(num, ind):
    ps = []
    up = True
    lMin = num[ind,3]
    lMax = num[ind,4]
    jacks= []
    for i in range(ind, len(num)):
        ps.append([num[i,3], num[i,4], i])
    topJack = []
    bottomJack = [2]
    if len(ps) <= 4:
        return [jacks,topJack,bottomJack]
    lMin = ps[2][0]
    lMax = ps[2][1]
    up = True
    findUpJack = True
    for i in range(3, len(ps)):
        if (ps[i][0] - lMin) * (ps[i][1] - lMax) <= 0:
            pr("merge", num[ps[i][-1],0],num[i,3], lMin, num[i,4], lMax)
            if up:
                lMin = max(lMin, ps[i][0])
                lMax = max(lMax, ps[i][1])
            else:
                lMin = min(lMin, ps[i][0])
                lMax = min(lMax, ps[i][1])
            continue
        if up and ps[i][1] < lMax:
            pr("find top", num[ps[i][-1],0])
            if len(bottomJack) == 0:
                topJack.append(i)
            else:
                pr(i - bottomJack[-1] >= 4, not findUpJack, num[ps[i-2][-1],0], num[ps[bottomJack[-1]-2][-1],0], min(ps[bottomJack[-1]-2][0], ps[i][0]),  max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]))
                if i - bottomJack[-1] >= 4 and not findUpJack and min(ps[i-2][0], ps[i][0]) > max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]):
                    m = ps[bottomJack[-1]][0]
                    j = bottomJack[-1]
                    pr("confirm bottom")
                    jacks.append(num[ps[j][2] - 1])
                    findUpJack = True
                    bottomJack = []
                    topJack = [i]
                else :
                    if len(topJack) > 0:
                        if ps[i-1][1] > ps[topJack[0] - 1][1]:
                            topJack = [i]
                    else: topJack = [i]
            up = False
        elif not up and ps[i][1] > lMax:
            pr("find bottom", num[ps[i][-1],0])
            if len(topJack) == 0:
                bottomJack.append(i)
            else:
                # pr(i - topJack[-1] >= 4, findUpJack, max(ps[i-2][1], ps[i][1]), min(ps[topJack[-1]-2][0], ps[topJack[-1]][0]))
                if i - topJack[-1] >= 4 and findUpJack and max(ps[i-2][1], ps[i][1]) < min(ps[topJack[-1]-2][0], ps[topJack[-1]][0]):
                    m = ps[topJack[-1]][1]
                    j = topJack[-1]
                    jacks.append(num[ps[j][2] - 1])
                    findUpJack = False
                    topJack = []
                    bottomJack = [i]
                else :
                    if len(bottomJack) > 0:
                        if ps[i-1][0] < ps[bottomJack[0]-1][0]:
                            bottomJack = [i]
                            pr("set bottom jack",)
                    else: bottomJack = [i]
            up = True
        lMin = ps[i][0]
        lMax = ps[i][1]
    return [jacks, topJack, bottomJack]

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
        rs.append([c2, file, len(ns), num[m1,0]])
        # shutil.copy(PATHO + "/" + file, PATH + "/" + file.split('.')[1] + '.' + str(date))
rs.sort(key=lambda student: student[0])
for r in rs:
    print(r[1][3:9])
print(c)
print(len(rs))