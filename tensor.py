import akshare as ak
import numpy as np
import os
def downloadGL():
    stock_profit_forecast_df = ak.stock_board_concept_name_ths().to_numpy()
    print(stock_profit_forecast_df[:,0])
    for x in stock_profit_forecast_df[:,0]:
        try :
            print(x)
            stock_board_industry_index_ths_df = ak.stock_board_concept_index_ths(symbol=x)
            print()
            np.save("./glIndex/" + x, stock_board_industry_index_ths_df.to_numpy())
        except Exception:
            continue
    for f in os.listdir('./glIndex'):
        n1 = np.load('./glIndex/' + f, allow_pickle=True)
        if not str(n1[-1,0]).startswith('2021-07-20'):
            stock_board_industry_index_ths_df = ak.stock_board_concept_index_ths(symbol=f.split('.')[0])
            print(f, 'd', stock_board_industry_index_ths_df.to_numpy()[-1,0])
            np.save("./glIndex/" + f.split('.')[0], stock_board_industry_index_ths_df.to_numpy())
            print(f, n1[-1,0])
def donwloadHY():
    stock_board_industry_name_ths = ak.stock_board_industry_name_ths().to_numpy()
    print(stock_board_industry_name_ths[:,0])
    for x in stock_board_industry_name_ths[:,0]:
        try :
            print(x)
            stock_board_industry_index_ths_df = ak.stock_board_industry_index_ths(symbol=x)
            np.save("./hangye/" + x, stock_board_industry_index_ths_df.to_numpy())
        except Exception:
            continue
    for f in os.listdir('./hangye'):
        n1 = np.load('./hangye/' + f, allow_pickle=True)
        if str(n1[-1,0]) != '2021-06-11 00:00:00':
            stock_board_industry_index_ths_df = ak.stock_board_industry_index_ths(symbol=f.split('.')[0])
            print(f, 'd', stock_board_industry_index_ths_df.to_numpy()[-1,0])
            np.save("./hangye/" + f.split('.')[0], stock_board_industry_index_ths_df.to_numpy())
            print(f, n1[-1,0])
def sortS(path):
    mp = {}
    LEN = 60
    date = []
    for f in os.listdir(path):
        n1 = np.load(path + '/' + f, allow_pickle=True)
        n = n1[:,4].astype(np.float32)
        if len(n) < LEN:
            continue
        mp[f] = n[len(n) - LEN:len(n)]/n[len(n) - LEN - 1:len(n)-1]-1
        date = n1[len(n) - LEN:,0]
    for i in range(0, LEN):
        r = sorted(mp.items(), key = lambda k:(k[1][i]), reverse=True)
        ns = np.array(r)
        print(str(date[i])[0:10], ns[:3, 0], round(ns[0][1][i], 3), round(ns[1][1][i], 3), round(ns[2][1][i], 3))
# downloadGL()
# stock_board_concept_index_ths_df = ak.stock_board_concept_index_ths(symbol="丙烯酸")
# print(stock_board_concept_index_ths_df)
# stock_profit_forecast_df = ak.stock_board_concept_name_ths().to_numpy()
# print(stock_profit_forecast_df[:,0], len(stock_profit_forecast_df))
sortS('./glIndex')
