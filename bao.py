import baostock as bs
import pandas as pd
import datetime
def writeStock(stock, key):
    rs = bs.query_history_k_data_plus(stock,
        "date,close,low,high,pctChg,volume",
        start_date='2000-01-01', end_date=str(datetime.date.today()),
        frequency=key, adjustflag="2")
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        r = rs.get_row_data()
        data_list.append(r)
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv("D:\\stocksM\\" + stock + ".csv", index=False)

### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
dataset = pd.read_csv("D:\\stock_basic.csv", encoding='gbk')
for row in dataset.itertuples():
    if (row[1].startswith('sz.30') or row[1].startswith('sz.00') or row[1].startswith('sh.60')):
        print(row[1])
        writeStock(row[1], 'm')
#### 登出系统 ####
bs.logout()
