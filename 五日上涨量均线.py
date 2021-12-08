import matplotlib.pyplot as plt
import numpy as np

L = 5
lz = [2515,1600,902,1033,3500,3111,1111,2985,3311,1974,2591,3098,2727,3014,2710,3023,1230,3828,1277,3295,2417,2396,
2304,1976,1545,1615,2884,3220,1097,2642,958,1715]
res = []
for i in range(L, len(lz) + 1):
    res.append(np.mean(lz[i-L:i-1]))
print(res)
x = [x for x in range(1,len(res) + 1)]
plt.plot(x,res)
plt.plot(x, [2342 for x in range(0,len(res))])
plt.show()


import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
rs = bs.query_history_k_data_plus("sh.000001",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date='2021-01-01', end_date='2021-12-07', frequency="d")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
# result.to_csv("D:\\history_Index_k_data.csv", index=False)
print(result)

# 登出系统
bs.logout()