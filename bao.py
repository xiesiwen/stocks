import baostock as bs
import pandas as pd
import numpy as np
import datetime
import os
import shutil
import warnings
path = "./stock-today/"
columns = "date,close,open,low,high,volume,pctChg,isST"
def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
def writeStock(stock, key):
    print('write ' + stock)
    rs = bs.query_history_k_data_plus(stock,
        columns,
        start_date = '2021-01-01', end_date=str(datetime.date.today()),
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

def patch(stock, key):
    start = str(datetime.date.today() + datetime.timedelta(days=-350))
    p = path + "/" + stock + ".csv"
    num = np.array([])
    if os.path.exists(p):
        try:
            with warnings.catch_warnings():
                num = np.loadtxt(p ,str,delimiter = ",", skiprows = 1)
                if len(num) > 0 and num.shape[1] == len(columns.split(',')):
                    start = num[-1,0]
        except:
            writeStock(stock, key)
            return
    else:
        writeStock(stock, key)
        return
    if start == str(datetime.date.today()):
        return
    print('patch ' + stock)
    rs = bs.query_history_k_data_plus(stock, columns,
        start_date = start, end_date=str(datetime.date.today()),
        frequency=key, adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    if start == str(datetime.date.today() + datetime.timedelta(days=-500)):
        result = pd.DataFrame(data_list, columns=rs.fields)
        result.to_csv(p, index=False)
    else:
        if len(data_list) < 2:
            return
        if len(num) == 0:
            result = data_list
        else: 
            result = np.append(num, data_list[1:], axis=0)
        pd.DataFrame(result, columns=rs.fields).to_csv(p, index=False)

def writeStock30(stock):
    rs = bs.query_history_k_data_plus(stock,
        "date,close,open,low,high,volume,time",
        start_date = str(datetime.date.today() + datetime.timedelta(days=-30)), end_date=str(datetime.date.today()),
        frequency="30", adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    result = pd.DataFrame(data_list, columns=rs.fields)
    print(result)
    #### 结果集输出到csv文件 ####   
    result.to_csv(path + "\\" + stock + ".csv", index=False)

year = "today"
path = "./stock-today"
# setDir(path)
### 登陆系统 ####

lg = bs.login()
# 显示登陆返回信息
rs = bs.query_stock_basic()
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
s = False
for row in data_list:
    s = row[0].startswith('sh.68')
    # if not s:
    #     continue
    if row[0].startswith('sh.60') or row[0].startswith('sz.00') or row[0].startswith('sz.30') or row[0].startswith('sh.68'):
        patch(row[0], 'd')
#### 登出系统 ####
bs.logout()
