import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 


for gap in [10,20,30,40,50,60,70]:
    for WAIT in [3,4,5]:
        rs1 = 0
        rs2 = 0
        fs1 = []
        fs2 = []
        for file in os.listdir("D:\\stocks"):
            if file.startswith('sz.30'):
                continue
            dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
            num = dataset.to_numpy()
            if num.shape[0] == 0 or num[-1,1] > 10:
                continue
            x = []
            buy = 0
            g = 0
            for i in range(gap, num.shape[0]):
                if num[i, 1] > num[i-gap:i,1].mean():
                    if buy == 0:
                        if g == WAIT :
                            buy = num[i, 1]
                            # print('buy ' , num[i,0])
                        else :g += 1
                    else : g = WAIT
                if num[i, 1] < num[i-gap:i,1].mean():
                    if buy != 0:
                        if g <= 0:
                            if num[i, 1] > buy:
                                rs1 += 1
                            rs2 += 1
                            # print('sale ' , num[i,0], (num[i,1]/buy - 1) * 100)
                            rate = (num[i,1]/buy - 1)
                            if rate > 0:
                                fs1.append(rate)
                            else :
                                fs2.append(rate)
                            buy = 0
                        else :g -= 1
                    else: g=0
        print(gap, WAIT, rs1, rs2, rs1/rs2, np.mean(fs1), np.mean(fs2), (sum(fs1) - sum(fs2))/rs2)

# plt.figure()									#打印样本点
# plt.scatter(range(len(fs)),fs)						#把x_data和y_data传进来
# plt.show()