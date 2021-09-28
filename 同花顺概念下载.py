import numpy as np
import pandas as pd
import akshare as ak

PATH= './同花顺概念/'
TIME = "2021-09-03"
def downloadBK():
    err = []
    noUpdate = []
    stock_profit_forecast_df = ak.stock_board_concept_name_ths().to_numpy()
    print(stock_profit_forecast_df[:,0])
    for x in stock_profit_forecast_df[:,0]:
        try :
            print(x)
            stock_board_industry_index_ths_df = ak.stock_board_concept_hist_ths(symbol=x, start_year="2021")
            if not str(stock_board_industry_index_ths_df.to_numpy()[-1,0]).startswith(TIME):
                try:
                    stock_board_industry_index_ths_df = ak.stock_board_concept_hist_ths(symbol=x, start_year="2021")
                except Exception:
                    noUpdate.append(x) 
            np.save(PATH + x, stock_board_industry_index_ths_df.to_numpy()) 
        except Exception:
            try:
                stock_board_industry_index_ths_df = ak.stock_board_concept_hist_ths(symbol=x, start_year="2021")
                np.save(PATH + x, stock_board_industry_index_ths_df.to_numpy())
            except Exception:
                err.append(x)
            continue
    print('not download', err)
    print('not update', noUpdate)
downloadBK()