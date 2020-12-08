import numpy as np
import pandas as pd
import os 
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

# for file in os.listdir("D:\\stocks"):
#     # if not file.startswith('sh.600141'):
#     #     continue
#     dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
#     num = dataset.to_numpy()
#     if num.shape[0] == 0:
#         continue
#     x = (int)(len(num)/2)
#     ind = num[x:len(num),3].argmin() + x
#     res = findJacks(num, ind)
#     jacks = res[0]
#     top = res[1]
#     bottom = res[2]
#     if num[-1, 1] < 20 and num[-1, -1] == 0:
#         if len(jacks) == 2 and len(top) > 0 and num[-1,1] >= jacks[0][4] * 0.95 and num[top[0]+ind,3] > num[-1,1]:
#             drawImage(file)
#             print(file, num[ind, 0],jacks)
#             c += 1

L = 250
buy = 0
win = 0
buy2 = 0
win2 = 0
buyJ = 0
winJ = 0
buy20 = 0
win20 = 0
c = 0
out = 0
cs = [0 for x in range(20)]
rs = [0 for x in range(20)]
for file in os.listdir("D:\\stocks-all"):
    dataset = pd.read_csv("D:\\stocks-all\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    # c += 1
    # if c > 1500:
    #     break
    if num.shape[0] <= L:
        continue
    for i in range(10, 11):
        x = num[i:i+L]
        h = (int)(L/2)
        ind = x[h:L,3].argmin() + h
        res = findJacks(num, ind)
        jacks = res[0]
        top = res[1]
        bottom = res[2]
        buy += 1
        if num[i + 10,1] > num[i,1]:
            win += 1
        if num[i + 20,1] > num[i,1]:
            win2 += 1
        t = 0
        x = []
        lt = 0
        rd = False
        for i in range(3, len(jacks), 2):
            if jacks[i][1] >= jacks[i-2][1] and jacks[i-1][1] >= jacks[i-3][1]:
                if len(x) > 3 and x[-1] == -1 and x[lt + 1] == -1:
                    for z in range(lt,len(x)):
                        if x[z] == 0:
                            rd = True
                            break
                t += 1
                x.append(1)
                lt = len(x) - 1
            elif jacks[i][1] <= jacks[i-2][1] and jacks[i-1][1] <= jacks[i-3][1]:
                if t >= 2:
                    cs[t] += 1
                    if rd: 
                        rs[t] += 1
                        
                x.append(-1)
                t = 0
                rd = False
            else: 
                # if t >= 2:
                #     cs[t] += 1
                #     if rd: 
                #         rs[t] += 1
                #         rd = False
                x.append(0)
                # t = 0

        print(file, len(jacks))
        # print(win, buy, win/buy, len(jacks))
        # if len(jacks) == 3 and len(bottom) > 0 and len(top) == 0 and x[bottom[0] + ind,1] > jacks[0][4] * 0.95 and L- bottom[0] - ind <= 5:
        #     buyJ += 1
        #     m = num[i+L,1]
        #     r = m
        #     for z in range(i + L, len(num)):
        #         if num[z,1]> m:
        #             m = num[z,1]
        #         if num[z,1] < m*0.9:
        #             r = num[z,1]
        #     if r > num[i+L,1]:
        #         out += 1
        #     if num[i + L + 10,1] > num[i+L,1]:
        #         winJ += 1
        #     if num[i + L + 20,1] > num[i+L,1]:
        #         win20 += 1
# print(win, buy, win/buy, win2/buy , winJ/buyJ, win20/buyJ, out/buyJ, buyJ)
print(cs, sum(cs[3:len(cs)])/sum(cs[2:len(cs)]))
print(rs, sum(rs[3:len(rs)])/sum(rs[2:len(rs)]))

