import baostock as bs
import pandas as pd
import numpy as np
import datetime
import os
import shutil
import warnings

columns = "date,close,open,low,high,volume,pctChg,isST"
def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
def writeStock(stock, key, year):
    rs = bs.query_history_k_data_plus(stock,
        columns,
        start_date = str(year)+'-01-01', end_date=str(year + 1)+'-01-01',
        frequency=key, adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv(path + "/"  + stock + ".csv", index=False)


### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
rs = bs.query_stock_basic()
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
for year in range(2015, 2022):
    path = "D:/workspace/stocks/stocks/stock-"+str(year)
    setDir(path)
    print('write ' , year)
    for row in data_list:
        s = row[0].startswith('sh.68')
        # if not s:
        #     continue
        if row[0].startswith('sh.60') or row[0].startswith('sz.00') or row[0].startswith('sz.30') or row[0].startswith('sh.68'):
            writeStock(row[0], 'd', year)
#### 登出系统 ####
bs.logout()
