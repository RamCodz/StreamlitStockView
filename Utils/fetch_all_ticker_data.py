from yahoo_fin import stock_info as si
import pandas as pd
from datetime import datetime, timedelta
import globals
from debug import debug

def dbg(msg):
    debug("fetch_all_ticker_data-->"+str(msg))
    
def get_stock_data(ticker, start_date, end_date):  
    try:
        # Get historical data
        historical_data = si.get_data(ticker, start_date=start_date, end_date=end_date)
        return historical_data
    except Exception as e:
        dbg(f"Could not retrieve data for {ticker}: {e}")
        return pd.DataFrame()

def get_all_data(StockList):
    dbg("in get_all_data ")
    all_data = pd.DataFrame()
    today = datetime.today()
    five_year_ago = today - timedelta(days=365*globals.noy)
    DListLbl=['Security Name','Status','Group','Face Value','ISIN No','Industry','Instrument','Sector Name','Industry New Name','Igroup Name','ISubgroup Name'] 
    ##StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))
    i=1
    for index, row in StockList.iterrows():
        dbg(row['Security Id'])
        stkSymbol = row['Security Id']+'.NS'
        
        five_year_data = get_stock_data(stkSymbol, five_year_ago, today)
        if not five_year_data.empty:
            ##five_year_data['Security Name'] = row['Security Name'];
            ##for k in range(len(DListLbl)):
                ##five_year_data[DListLbl[k]] = row[DListLbl[k]]
            all_data = pd.concat([all_data, five_year_data])
        
        if i==5:
            break;
        i=i+1
        ##dbg(all_data)
    return all_data
        
##get_all_data()