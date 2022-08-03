import os 
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
def printN(c):
    for y in range(2020, 2022):
        path = "./stocks/stock-"+str(y)+"/"
        all = 0
        inc = 0
        res = 1
        nums = {}
        for f in os.listdir(path):
            if f.startswith('sh.68') or f.startswith('sz.30'):
                continue
            dataset = pd.read_csv(path + f, encoding='gbk')
            num = dataset.to_numpy()
            if len(num) < 10:
                continue
            for i in range(0, len(num) - c - 1):
                t = True
                if num[i, -2] > 6 and num[i + c, 2] < num[i + c-1, 1]*1.099 and num[i + c, 2] > num[i + c-1, 1]*0.95:
                    for j in range(1, c):
                        t = t and (num[i+j, -2] > 9.9)
                    if t:
                        all += 1
                        if num[i + c + 1, 2] > num[i + c, 2]:
                            inc += 1
                        res *= (num[i + c + 1, 2] / num[i + c, 2]) * 0.99  
                        r = int(((num[i +  c + 1, 2] / num[i + c, 2]) - 1) * 100)
                        if r not in nums:
                            nums[r] = 0
                        nums[r] += 1
        if all > 0:
            print(y, c, inc/all, inc , all, '%.4f'%res)
        result = sorted(nums.items(), key = lambda k:(k[0]))
        print(result)

# for C in range(2, 7):
#     printN(C)
printN(3)
