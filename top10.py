import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt

ds = {}
doubles = {}
def findNextJack(num, ind, up):
    lMin = min(num[ind,1], num[ind,2])
    lMax = max(num[ind,1], num[ind,2])
    may = ind + 1
    change = 0
    cc = 0
    for i in range(ind, len(num)):
        iMin = min(num[i,1], num[i,2])
        iMax = max(num[i,1], num[i,2])
        print(num[i,0], iMin, iMax)
        # if (lMin - iMin) * (lMax-iMax) <= 0:
        #     if up:
        #         iMax = max(lMax,iMax)
        #         iMin = max(lMin, iMin)
        #     else:
        #         iMax = min(lMax,iMax)
        #         iMin = min(lMin, iMin)
        #     print("merge")
        # else :
        #     if up: 
        #         if lMax > iMax:
        #             print("trun down " + str(cc) + " " + str(max(num[may,1], num[may,2],num[may-1,1], num[may-1,2],num[may-2,1], num[may-2,2])) + " " + str(max(min(num[i,1], num[i,2]),min(num[i -1,1], num[i-1,2]),min(num[i-2,1], num[i-2,2]))))
        #             if cc >= 2 and max(num[may,1], num[may,2],num[may-1,1], num[may-1,2],num[may-2,1], num[may-2,2]) < max(min(num[i,1], num[i,2]),min(num[i -1,1], num[i-1,2]),min(num[i-2,1], num[i-2,2])):
        #                 change +=1
        #                 cc = 0
        #                 up = not up
        #                 may = i
        #             elif change == 1:
        #                 print("clean reset to down")
        #                 change -= 1
        #                 may = ind + 1
        #                 cc = 3
        #                 up = not up
        #         else:
        #             cc += 1
        #             print("up continum cc " + str(cc))
        #     elif not up:
        #         if lMax < iMax:
        #             print("trun up " + str(cc))
        #             if cc >= 2 and max(num[i,1], num[i,2],num[i-1,1], num[i-1,2],num[i-2,1], num[i-2,2]) < max(min(num[may,1], num[may,2]),min(num[may -1,1], num[may-1,2]),min(num[may-2,1], num[may-2,2])):
        #                 change +=1
        #                 cc = 0
        #                 up = not up
        #                 may = i
        #             elif change == 1:
        #                 print("clean reset to up")
        #                 change -= 1
        #                 may = ind + 1
        #                 cc = 3
        #                 up = not up
        #         else:
        #             cc += 1
        #             print("down continum cc " + str(cc))
        # if change == 2 or (change == 1 and cc >= 4):
        #     return [may, up]
        # lMin = iMin
        # lMax = iMax
    return [0, up]

for file in os.listdir("D:\\stocks"):
    if not file.startswith('sh.601816'):
        continue
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    ind = num[(int)(len(num)/2):len(num),1].argmin() + (int)(len(num)/2)
    if num[(int)(len(num)/2):len(num),1].min() > num[(int)(len(num)/2):len(num),2].min():
        ind = num[(int)(len(num)/2):len(num),2].argmin() + (int)(len(num)/2)
    jacks = []
    up = True
    while(True):
        res = findNextJack(num, ind, up)
        up = not up
        if res[0] == 0:
            break
        else: 
            ind = res[0] - 1
            jacks.append(num[ind,0])
    
    print(file, ind, jacks)