import akshare as ak
import numpy as np
import os
def downloadBK():
    stock_profit_forecast_df = ak.stock_board_concept_name_ths().to_numpy()
    print(stock_profit_forecast_df[:,0])
    for x in stock_profit_forecast_df[:,0]:
        # try :
            print(x)
            stock_board_industry_index_ths_df = ak.stock_board_concept_index_ths(symbol=x)
            print()
            np.save("./hankuai/" + x, stock_board_industry_index_ths_df.to_numpy())
        # except Exception:
            # continue
    for f in os.listdir('./hankuai'):
        n1 = np.load('./hankuai/' + f, allow_pickle=True)
        if str(n1[-1,0]) != '2021-06-11 00:00:00':
            stock_board_industry_index_ths_df = ak.stock_board_concept_index_ths(symbol=f.split('.')[0])
            print(f, 'd', stock_board_industry_index_ths_df.to_numpy()[-1,0])
            np.save("./hankuai/" + f.split('.')[0], stock_board_industry_index_ths_df.to_numpy())
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
    LEN = 20
    for f in os.listdir(path):
        n1 = np.load(path + '/' + f, allow_pickle=True)
        n = n1[:,4].astype(np.float32)
        mp[f] = n[len(n) - LEN:len(n)]/n[len(n) - LEN - 1:len(n)-1]-1
    L2 = 10
    res= {}
    for i in range(0, LEN):
        r = sorted(mp.items(), key = lambda k:(k[1][i]), reverse=True)
        r = np.array(r[0:L2])[:,0]
        for i in range(0,L2):
            k = r[i]
            if k not in res.keys():
                res[k] = 0
            if i == 0:
                res[k] += 4
            elif i >= 1 and i <= 2:
                res[k] += 3
            elif i >= 3 and i <= 5:
                res[k] += 2
            else :
                res[k] += 1
    print(sorted(res.items(), key = lambda k:(k[1]), reverse=True))
# downloadBK()
stock_board_concept_index_ths_df = ak.stock_board_concept_index_ths(symbol="丙烯酸")
print(stock_board_concept_index_ths_df)