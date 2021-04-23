import baostock as bs
import pandas as pd
import datetime
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

def download(stock):
    bs.login()
    rs = bs.query_history_k_data_plus(stock,
        "date,close,open,low,high,volume,amount,pctChg",
        start_date = str(datetime.date.today() + datetime.timedelta(days=-300)), end_date=str(datetime.date.today()),
        frequency="d", adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####   
    result[1,:].to_csv(stock + ".csv", index=False)
    bs.logout()
# download("sh.600219")
r = np.loadtxt('sh.600219.csv',dtype=np.str,delimiter=',')
s1 = []
s2 = []
for i in range(100, 200):
    s1.append(float(r[i,1]))
    arg = float(r[i,6])/float(r[i,5])
    s2.append(round(float(r[i,6])/float(r[i,5]),2))
plt.plot(np.arange(len(s1)), np.array(s1)/10)
rs = []
rs1 = []
ds = np.array(s2) - np.array(s1)
L = 5
L2 = 10
for i in range(0, len(ds)):
    if i < L-1:
        rs.append(ds[i])
    else: rs.append(ds[i-L+1:i+1].mean())
    if i < L2-1:
        rs1.append(ds[i])
    else: rs1.append(ds[i-L2+1:i+1].mean())
print(ds[-1], ds[len(ds)-1:len(ds)])
plt.plot(np.arange(len(s1)), np.array(rs) - np.array(rs1), c="red")
# plt.plot(np.arange(len(s1)), rs1, c="blue")
plt.show()