from yahoo_fin import stock_info as si
import pandas as pd
from datetime import datetime, timedelta
from BackEnd.Utils import globals
from BackEnd.Utils.debug import debug

def dbg(msg):
    debug("fetch_all_ticker_data-->"+str(msg))
    
def get_stock_data(ticker, start_date, end_date):  
    try:
        # Get historical data
        historical_data = si.get_data(ticker, start_date=start_date, end_date=end_date, interval='1d')

        return historical_data
    except Exception as e:
        dbg(f"Could not retrieve data for {ticker}: {e}")
        return pd.DataFrame()

def get_all_data(StockList):
    all_data = pd.DataFrame()
    print('inside get_all_data', globals.today)
    print(type(globals.today))
    five_year_ago = globals.today - timedelta(days=365*globals.noy)
    DListLbl=['Security Name','Status','Group','Face Value','ISIN No','Industry','Instrument','Sector Name','Industry New Name','Igroup Name','ISubgroup Name'] 
    ##StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))
    
    i = 0
    for index, row in StockList.iterrows():
        i=i+1
        if i == 1000:
            break
        stkSymbol = row['Security Id']+'.NS'
        five_year_data = get_stock_data(stkSymbol, five_year_ago, globals.today)

        if not five_year_data.empty:
            ##five_year_data['Security Name'] = row['Security Name'];
            ##for k in range(len(DListLbl)):
            ##five_year_data[DListLbl[k]] = row[DListLbl[k]]
            all_data = pd.concat([all_data, five_year_data])

    return all_data
        
##get_all_data()
