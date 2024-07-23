from pathlib import Path

dbg_filepath = '/Logs/'
dbg_filename = 'Log_stockMe.log'
equity_list_path = '/Data/Inbound/'
equity_list_filename = 'Equity.csv'
data_filepath = '/Data/Outbound/'
data_filename = 'StockMe.xlsx'

noy = 5  # no of years to get data from Yahoo fin
dt_format = '%Y-%m-%d'
dt_time_format = '%Y/%m/%d %H:%M:%S'
today = None  # today in '%Y-%m-%d' format
