import baostock as bs
import pandas as pd
import datetime
import os
import shutil
path = "./stock-today/"
def setDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
def writeStock(stock, key):
    rs = bs.query_history_k_data_plus(stock,
        "date,close,open,low,high,volume",
        start_date = str(datetime.date.today() + datetime.timedelta(days=-500)), end_date=str(datetime.date.today()),
        frequency=key, adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv(path + stock + ".csv", index=False)

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

    #### 结果集输出到csv文件 ####   
    result.to_csv(path + "\\" + stock + ".csv", index=False)

# setDir(path)
### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
dataset = pd.read_csv("./stock/all_stock.csv", encoding='gbk')
for row in dataset.itertuples():
    if row[1].startswith('sh.60') or row[1].startswith('sh.68') or row[1].startswith('sz.00') or row[1].startswith('sz.30'):
        print(row[1])
        writeStock(row[1], 'd')
#### 登出系统 ####
bs.logout()
