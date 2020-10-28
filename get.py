import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 


for gap in [20]:
    for WAIT in [10]:
        rs1 = 0
        rs2 = 0
        fs1 = []
        fs2 = []
        time1 = []
        time2 = []
        for file in os.listdir("D:\\stocks"):
            z1 = 1
            if file.startswith('sz.30'):
                continue
            dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
            num = dataset.to_numpy()
            if num.shape[0] == 0 or num[-1,1] > 10 or num[-1,-1] > 0:
                continue
            x = []
            buy = 0
            g = 0
            startInd = 0
            for i in range(gap, num.shape[0]):
                if num[i, 1] > num[i-gap:i,1].mean() and num[i-int(gap/2):i, 4].mean() > num[i-gap:i-int(gap/2), 4].mean():
                    if buy == 0:
                        if g == WAIT :
                            startInd = i
                            buy = num[i, 1]
                            # print('buy ' , num[i,0])
                        else :g += 1
                    else : g = WAIT
                if num[i, 1] < num[i-gap:i,1].mean():
                    if buy != 0:
                        if g <= 3:
                            if num[i, 1] > buy:
                                rs1 += 1
                            rs2 += 1
                            # print('sale ' , num[i,0], (num[i,1]/buy - 1) * 100)
                            rate = num[i,1]/buy
                            z1 *= (rate * 0.997)
                            qq = i - startInd
                            if qq > 150:
                                qq = 150
                            if rate > 1:
                                time1.append(qq)
                            else: time2.append(qq)
                            buy = 0
                        else :g -= 1
                    else: g=0
            fs1.append(z1)
        print(gap, WAIT, rs1, rs2, rs1/rs2, np.mean(fs1), np.mean(time1), np.mean(time2))
        # plt.figure()									#打印样本点
        # plt.scatter(range(len(time1)),time1)						#把x_data和y_data传进来
        # plt.show()

        # plt.figure()									#打印样本点
        # plt.scatter(range(len(time2)),time2)						#把x_data和y_data传进来
        # plt.show()
