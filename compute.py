import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
LOW = 1
R = 1.12
LEN = 120
LOG = False
MIN = 0.003

wins = 0
s = 0
rs = 0
i = 0
z = []
dso = {}
ds = {}
for i in range(21):
    ds[str(2000 + i)] = []
    dso[str(2000 + i)] = []
ns = [0 for x in range(0, 14)]
zs = [0 for x in range(0, 32)] 
ins = [0 for x in range(0, 102)]
froms = [0 for x in range(0, 102)]
timeGaps = [0 for x in range(0, 300)]
zd = []
cj = []
dayGap = []
downs = []
ups = []
pr = []
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    thisK = num[0,0][0:4]
    startDate = ''
    startPrice = 0
    startInd = 0
    cs = 0
    for j in range(num.shape[0]):
        if num[j,0].startswith(thisK) and j < num.shape[0] - 1:
            continue
        else :
            startInd = num[cs:j,1].argmin() + cs
            startPrice = num[startInd, 1]
            if startPrice < 10:
                startDate = num[startInd, 0]
                maxInd = num[startInd:j,1].argmax() + startInd
                maxP = num[maxInd, 1]
                min = startInd
                if maxP > 10 and maxP > startPrice * 1.5 and maxInd - startInd > 20 and startInd > 60:
                    if '2020' in startDate or '2018' in startDate or '2019' in startDate and startInd > 480:
                        hs = max([startInd-1200, 0])
                        hmin = num[hs:startInd, 1].min()
                        hmax = num[hs:startInd, 1].max()
                        pp = (startPrice - hmin)/(hmax - hmin) * 100
                        pr.append(pp)
                    dayGap.append(maxInd - startInd)
                    last = num[min, 1]
                    top10 = 0
                    q = 0
                    for s in range(min + 1, j):
                        if (num[s, 1]/last - 1)*100 > 9.9 :
                            top10 += 1
                            if q == 0:
                                q = s - min
                        last = num[s, 1]
                    if top10 > 100:
                        top10 = 99
                    ins[top10] += 1
                    if q > 100:
                        q = 99
                    froms[q] += 1
                    ns[int(num[min, 0][5:7])] += 1
                    zs[int(num[min, 0][8:10])] += 1
                    if  "-01-" in num[min, 0]:
                        dso[thisK].append([file, num[min, 0], num[min, 1], num[min, 0][8:10]])
                        for z in range(min, min +22):
                            if z + 1 < num.shape[0] and "-01-" in num[z,0] and num[z + 1,1]/num[z,1] > 1.099 and num[min,1] < 10:
                                ds[thisK].append([file, num[min, 0], num[min, 1], num[min, 0][8:10]])
                                break
                    startDate = ''
                    startPrice = 0
                    timeGaps[maxInd - startInd] += 1
            cs = j
            thisK = num[j,0][0:4]

c = 0
for i in ds:
    c += len(ds[i])
    print(i, len(ds[i]), len(dso[i]))
print(c)
print(ns, sum(ns))
print(zs, sum(zs[0:15]))
print(ins)
print(froms, sum(froms[0:30]))
# print(timeGaps)
# for i in range(1,13):
#     s1 = 0
#     for j in range (i *20, len(timeGaps)):
#         if j < len(timeGaps):
#             s1 += timeGaps[j]
#     print(i, s1/sum(timeGaps) * 100)
l = [0,0,0,0,0]
for i in dayGap:
    l[int(i/50)] += 1   
print(l, len(dayGap))
# plt.figure()									#打印样本点
# plt.scatter(range(len(downs)),downs)						#把x_data和y_data传进来
# plt.show()
lin0 = 0
lin10 = 0
lin20 =0
for x in pr:
    if x < 0:
        lin0+=1
    if x < 15:
        lin10 +=1
    if x < 25:
        lin20 += 1
print(pr)
print(lin0/len(pr),lin10/len(pr),lin20/len(pr))
plt.figure()									#打印样本点
plt.scatter(range(len(pr)),pr)						#把x_data和y_data传进来
plt.show()