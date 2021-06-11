import akshare as ak
# stock_profit_forecast_df = ak.stock_board_concept_name_ths()
# print(stock_profit_forecast_df.to_numpy())
# stock_board_concept_index_ths_df = ak.stock_board_concept_index_ths(symbol="白酒概念")
# print(stock_board_concept_index_ths_df)
stock_board_industry_name_ths = ak.stock_board_industry_name_ths()
print(stock_board_industry_name_ths)

stock_board_industry_index_ths_df = ak.stock_board_industry_index_ths(symbol="半导体及元件")
print(stock_board_industry_index_ths_df.to_numpy()[4])