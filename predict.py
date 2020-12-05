import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import json
import mplfinance as mpf

def pr(*arg):
    print(arg)

def findJacks(num, ind):
    ps = []
    up = True
    lMin = num[ind,3]
    lMax = num[ind,4]
    jacks= []
    for i in range(ind + 1, len(num)):
        if (num[i,3] - lMin) * (num[i,4] - lMax) <= 0:
            if up:
                lMin = max(lMin, num[i,3])
                lMax = max(lMax, num[i,4])
            else:
                lMin = min(lMin, num[i,3])
                lMax = min(lMax, num[i,4])
        else:
            ps.append([lMin, lMax, i])
            print(lMin, lMax, num[i,0])
            if lMin < num[i,3]:
                up = True
            else: up = False
            lMin = num[i,3]
            lMax = num[i,4]
    topJack = []
    bottomJack = [2]
    if len(ps) <= 4:
        return jacks
    lMin = ps[0][0]
    lMax = ps[0][1]
    up = True
    findUpJack = True
    for i in range(3, len(ps)):
        if up and ps[i][1] < lMax:
            pr("find top", num[ps[i][-1],0])
            if len(bottomJack) == 0:
                topJack.append(i)
            else:
                pr(i - bottomJack[-1] >= 4, not findUpJack, num[ps[i-2][-1],0], num[ps[bottomJack[-1]-2][-1],0], min(ps[bottomJack[-1]-2][0], ps[i][0]),  max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]))
                if i - bottomJack[-1] >= 4 and not findUpJack and min(ps[i-2][0], ps[i][0]) > max(ps[bottomJack[-1]-2][1], ps[bottomJack[-1]][1]):
                    m = ps[bottomJack[-1]][0]
                    j = bottomJack[-1]
                    # for x in range(len(bottomJack)):
                    #     if ps[bottomJack[x]][0] < m:
                    #         m = ps[bottomJack[x]][0]
                    #         j = bottomJack[x]
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
                    # for x in range(len(bottomJack)):
                    #     if ps[topJack[x]][1] > m:
                    #         j = topJack[x]
                    #         m = ps[j][1]
                    # pr("confirm up")
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
    if len(topJack) > len(bottomJack) and topJack[-1] <= len(ps) - 4:
        m = ps[topJack[-1]][1]
        j = topJack[-1]
        z = topJack[-1]
        # for x in range(len(bottomJack)):
        #     if ps[topJack[x]][1] > m:
        #         j = topJack[x]
        #         m = ps[j][1]
        #         z= x
        if ps[-1][1] < min(ps[z-1][0], ps[z+1][0]):
            jacks.append(num[ps[j][2] - 1])
    if len(topJack) < len(bottomJack) and bottomJack[-1] <= len(ps) - 4:
        m = ps[bottomJack[-1]][0]
        j = bottomJack[-1]
        z = bottomJack[-1]
        # for x in range(len(bottomJack)):
        #     if ps[bottomJack[x]][0] < m:
        #         m = ps[bottomJack[x]][0]
        #         j = bottomJack[x]
        #         z = x
        if ps[-1][0] > max(ps[z-1][1], ps[z+1][1]):
            jacks.append(num[ps[j][2] - 1])
    return jacks

def drawImage(file):
    columns_json_str = '{"date":"Date","open":"Open","close":"Close","high":"High","low":"Low","volume":"Volume"}'
    columns_dict = json.loads(columns_json_str)
    data=pd.read_csv('D:/stocks/'+file, index_col= 'date', usecols=['date','open','close','high','low','volume'])
    data.rename(columns=columns_dict, inplace=True)
    data.index = pd.DatetimeIndex(data.index)
    mpf.plot(data, type='candle', mav=(5, 10), volume=True, style='charles',savefig='C:/Users/gentl/Desktop/images/'+file+".png")
c=0
for file in os.listdir("D:\\stocks"):
    if not file.startswith('sz.000040'):
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    x = (int)(len(num)/2)
    ind = num[x:len(num),3].argmin() + x
    jacks = findJacks(num, ind)
    print(file, num[ind, 0],jacks)
    if (len(jacks) == 2 or len(jacks) == 3) and num[-1, 1] < 20 and num[-1,1] < jacks[-1][4] and num[-1,1] >= jacks[0][4] * 0.95:
        m = True
        for i in range(len(jacks)-1):
            if jacks[-1][4] < jacks[i][4]*1.05:
                m = False
        if m and num[-1, -1] == 0:
            c += 1
            # drawImage(file)
            print(file, num[ind, 0],jacks)
print(c)

# L = 250
# buy = 0
# win = 0
# buyJ = 0
# winJ = 0
# c = 0
# out = 0
# for file in os.listdir("D:\\stocks-all"):
#     dataset = pd.read_csv("D:\\stocks-all\\" + file, encoding='gbk')
#     num = dataset.to_numpy()
#     # c += 1
#     # if c > 1000:
#     #     break
#     if num.shape[0] <= L:
#         continue
#     for i in range(10, len(num) - 10, 20):
#         x = num[i:i+L]
#         ind = x[(int)(len(x)/2):len(x),3].argmin() + (int)(len(x)/2)
#         jacks = findJacks(x, ind)
#         buy += 1
#         if num[i + 10,1] > num[i,1]:
#             win += 1
#         if len(jacks) >= 3 and len(jacks)%2 == 1 and x[-1, 1] < 20 and x[-1,1] < jacks[-1][4] and x[-1,1] >= jacks[0][4] * 0.95:
#             m = True
#             for x in range(len(jacks)-1):
#                 if jacks[-1][4] < jacks[x][4]*1.05:
#                     m = False
#             if m and num[-1, -1] == 0:
#                 b = False
#                 s = 0
#                 bi = 0
#                 for z in range(i + 1, len(num) - 2):
#                     if z>=4 and not b and num[z-2,1] == min(num[z-4:z,1]):
#                         b = True
#                         s = num[z,1]
#                         buyJ += 1
#                         bi = z
#                     if b and num[z-2,1] == max(num[z-5:z,1]) and z - bi >= 5:
#                         if num[z,1] > s:
#                             winJ += 1
#                         out += 1
#                         break
#                     if not b and z - i >= 20:
#                         break
# print(win, buy, win/buy, winJ, buyJ, winJ/buyJ, out)

