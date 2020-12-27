import numpy as np
import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt
import json
import mplfinance as mpf
dirs = "D:\\stocks-2020"
def drawImage(file, end):
    columns_json_str = '{"date":"Date","open":"Open","close":"Close","high":"High","low":"Low","volume":"Volume"}'
    columns_dict = json.loads(columns_json_str)
    data=pd.read_csv(dirs + "\\" + file, index_col= 'date', usecols=['date','open','close','high','low','volume'])
    data = data[0:end]
    data.rename(columns=columns_dict, inplace=True)
    data.index = pd.DatetimeIndex(data.index)
    mpf.plot(data, type='candle', mav=(5, 10), volume=True, style='charles',savefig='C:/Users/gentl/Desktop/images/'+file+".png")

def pr(*arg):
    if False:
        print(arg)

def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
setDir('C:/Users/gentl/Desktop/images')
c=0
rs = []
ds = [0 for x in range(0, 25)]
ks = []
win = 0
buy = 0
win20 = 0
buy20 = 0
s21 = 0
s22 = 0
s1 = 0
s2 = 0
PP = 10
Gap = 10
SG = 50

for file in os.listdir(dirs):
    # if not file.startswith("sh.601919"):
    #     continue
    dataset = pd.read_csv(dirs + "\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    ns = num[:,1]
    c += 1
    startWatch = False
    count = 0
    ci = 0
    m1 = 0
    simple = 0
    lasti = 0
    for i in range(SG, len(ns)-Gap):
        if count>=3:
            break
        buy20 += 1
        if num[i+Gap,1] > num[i,1]:
            win20 += 1
            s21 += ((num[i+Gap,1]/ num[i,1]) - 1) *100
        else: s22 += ((num[i+Gap,1]/ num[i,1]) - 1) *100
        if not startWatch and i - ns[0:i].argmin() >= SG:
            m1 = ns[0:i].argmin()
            startWatch = True
            if ns[0:i].min() > PP or num[i,-1] != 0:
                break
        if startWatch:
            m2 = i
            tmpns = np.array(ns[m1:m2]/ns.min(),dtype='float32')
            x = np.array(np.arange(m2-m1),dtype='float32')*0.005
            res2 = np.polyfit(x, tmpns, 1)
            res = np.polyfit(np.arange(10,dtype="float32")*0.005, tmpns[len(tmpns) - 10: ], 1)
            if res[0] <= res2[0]/2:
                simple += 1
            else:
                if simple >= 3:
                    count += 1
                    if (count == 3 or count == 2) and num[i,-1] == 0 and i - ns[0:i].argmax() <= 20:
                        out = num[i+Gap,1]
                        c2 = 0
                        rc = np.poly1d(res2)
                        if res2[0] > 0.3:
                            drawImage(file, i)
                            buy += 1
                            for Z in range(len(x)):
                                c2 += abs((rc(Z*0.005) - ns[Z]))
                            if out > num[i,1]:
                                win+=1
                                s1 += ((out/ num[i,1]) - 1) *100
                                rs.append([c2/len(x), file, num[i,0], res2[0], True])
                                # print(file, i, num[i,0], res2[0], True)
                            else: 
                                s2 += ((out/ num[i,1]) - 1) *100
                                rs.append([c2/len(x), file, num[i,0], res2[0], False])
                                # print(file, i, num[i,0], res2[0], False)
                lasti = i
                simple = 0
print(win, buy, win/buy, s1/win, s2/(buy-win), win20/buy20, s21/win20, s22/(buy20-win20), (s1+s2)/buy)         

rs.sort(key=lambda student: student[0])
w = 0
wa = 0
for x in range(len(rs)):
    print(rs[x])
    if rs[x][-1]:
        wa += 1
        if x < len(rs)/2:
            w += 1
print(w/len(rs)*2, wa/len(rs))

# print(ds, sum(ds), sum(ds[0:20]), len(ds)/1000)
# print(np.array(rs)[:,1:4])
# for i in range(100):
#     plt.scatter(rs[i][-3],rs[i][-2])
#     plt.plot(rs[i][-3],rs[i][-1])
#     plt.title(rs[i][1])
#     plt.show()
# plt.plot(np.arange(len(ks)),ks)
# plt.show()

