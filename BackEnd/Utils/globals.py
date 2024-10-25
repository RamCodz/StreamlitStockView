curr_dir = None
#dbg_filepath = 'G:/python/Stock_prediction/App_core/Logs/'
dbg_filepath = 'BackEnd/Logs/'
dbg_filename = 'Log_stockMe_*.txt'
#equity_list_path = 'G:/python/Stock_prediction/App_core/'
equity_list_path = 'BackEnd/Data/Inbound/'
equity_list_filename = 'Equity.csv'
#data_filepath = 'G:/python/Stock_prediction/App_core/Data/'
data_filepath = 'BackEnd/Data/Outbound/'
stockview_filename = 'StockView_*.csv'

noy = 1 ## no of years to get data from Yahoo fin
dt_format = '%Y-%m-%d'
dt_time_format = '%Y/%m/%d %H:%M:%S'
today = None  ##today in '%Y-%m-%d' format

cherry_breakout = ['5Y','1Y','6M','3M','1M']  ##as of now Year(Y) and Month(M) allowed
gems_breakout = ['1W','1M','3M','6M','1Y']  
gems_pct_change = -15
