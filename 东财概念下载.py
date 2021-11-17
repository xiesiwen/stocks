import numpy as np
import pandas as pd
import akshare as ak
import datetime

PATH= './东财概念/'
TIME = str(datetime.date.today())
def downloadBK():
    err = []
    noUpdate = []
    stock_profit_forecast_df = ak.stock_board_concept_name_em().to_numpy()
    print(stock_profit_forecast_df[:,1])
    for x in stock_profit_forecast_df[:,1]:
        try :
            print(x)
            stock_board_industry_index_ths_df = ak.stock_board_concept_hist_em(symbol=x)
            if not str(stock_board_industry_index_ths_df.to_numpy()[-1,0]).startswith(TIME):
                try:
                    stock_board_industry_index_ths_df = ak.stock_board_concept_hist_em(symbol=x)
                except Exception:
                    noUpdate.append(x) 
            else:
                print('success download', stock_board_industry_index_ths_df.to_numpy()[-1])
            np.save(PATH + x, stock_board_industry_index_ths_df.to_numpy()) 
        except Exception:
            try:
                stock_board_industry_index_ths_df = ak.stock_board_concept_hist_em(symbol=x)
                np.save(PATH + x, stock_board_industry_index_ths_df.to_numpy())
            except Exception:
                err.append(x)
            continue
    print('not download', err)
    print('not update', noUpdate)
downloadBK()