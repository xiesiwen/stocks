import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import baostock as bs
import os 
g = 5
lim = -30
timeGap = [0 for x in range(0,71)]
def pp(w10):
    m = 0
    for i in w10:
        if i > 0:
            m += 1
    return  m/len(w10) 

def winr(w):
    m = 0
    for i in w:
        m += (100 + i) / 100
    return m / len(w)

class R:
    def __init__(self, day):
        self.day = day
        self.w10 = []
        self.w20 = []
        self.w30 = []
        self.w40 = []
        self.w50 = []
        self.w60 = []
        self.w70 = []

    def add(self, r, j ,num):
        if r>self.day and j > 30:
                
            s = [0 for i in range(7)]
            index = 0
            if j + 71 > num.shape[0]:
                return
            for i in range(j, j + 71):
                if (num[i + g, 1] / num[j + g, 1] -1) * 100 < lim:
                    timeGap[i-j] += 1
                    if index < 6:
                        for x in range(index, 7):
                            s[x] = lim
                    break
                if i - j == 10:
                    s[0] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 0
                if i - j == 20:
                    s[1] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 1
                if i - j == 30:
                    s[2] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 2
                if i - j == 40:
                    s[3] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 3
                if i - j == 50:
                    s[4] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 4
                if i - j == 60:
                    s[5] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 5
                if i - j == 70:
                    s[6] = ((num[i + g, 1] / num[j + g, 1] -1) * 100)
                    index = 6
            self.w10.append(s[0])
            self.w20.append(s[1])
            self.w30.append(s[2])
            self.w40.append(s[3])
            self.w50.append(s[4])
            self.w60.append(s[5])
            self.w70.append(s[6])


    def print(self):
        print(self.day, "10", pp(self.w10), len(self.w10))
        print(self.day, "20", pp(self.w20), len(self.w20))
        print(self.day, "30", pp(self.w30), len(self.w30))
        print(self.day, "40", pp(self.w40), len(self.w40))
        print(self.day, "50", pp(self.w50), len(self.w50))
        print(self.day, "60", pp(self.w60), len(self.w60))
        print(self.day, "70", pp(self.w70), len(self.w70))
        # print("")
        # print(self.day, "10", winr(self.w10))
        # print(self.day, "20", winr(self.w20))
        # print(self.day, "30", winr(self.w30))
        # print(self.day, "40", winr(self.w40))
        # print(self.day, "50", winr(self.w50))
        # print(self.day, "60", winr(self.w60))
        # print(self.day, "70", winr(self.w70))
        print("-----------")

ds = {}
for s in range(1, 13):
    print("\n", s)
    r12 = R(1.2)
    r13 = R(1.3)
    r14 = R(1.4)
    r15 = R(1.5)
    r16 = R(1.6)
    st1 = '%02d' % s
    st2 = '%02d' % (s+1)
    if s == 12:
        st2 = '01'
    for file in os.listdir("D:\\stocks"):
        if file.startswith('sz.30') or file.startswith('sh'):
            continue
        dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
        num = dataset.to_numpy()
        if num.shape[0] == 0:
            continue
        start = 0
        end = 0
        for i in range(num.shape[0]):
            thisK = num[0,0][0:4]
            if "-" + st1+ "-" in num[i,0] and start < g:
                start = i
                end = 0
            if ("-" + st2+ "-" in num[i,0] or i == num.shape[0]-1) and end == 0 and start > g and num[start, 1] < 20:
                end = i
                for j in range(start, end):
                    m1 = num[j-g: j, -1].mean()
                    m2 = num[j: j+g, -1].mean()
                    if m1 == 0:
                        break
                    r = m2 / m1
                    if r > 1.2 and j > 20  and num[j,1] / num[j - 20, 1] < 1.2:
                        if (ds.get(thisK) == None):
                            ds[thisK] = []
                        if '-01-' in num[start,0]:
                            ds[thisK].append([file, num[j,0], num[j + g + 10,1] / num[j + g,1], num[j + g + 20,1] / num[j + g,1],num[j + g + 30,1] / num[j + g,1]])  
                        r12.add(r,j,num)
                        r13.add(r,j,num)
                        r14.add(r,j,num)
                        r15.add(r,j,num)
                        r16.add(r,j,num)
                        break

    
    # r12.print()
    r13.print()
    # r14.print()
    # r15.print()
    # r16.print()
for x in ds:
    m1 = 0
    m2 = 0
    m3 = 0
    for i in ds[x]:
        if i[2] > 1:
            m1 += 1
        if i[3] > 1:
            m2 += 1
        if i[4] > 1:
            m3 += 1
    if (len(ds[x]) ==0):
        continue
    print(x, len(ds[x]), m1/len(ds[x]), m2/len(ds[x]), m3/len(ds[x]))
