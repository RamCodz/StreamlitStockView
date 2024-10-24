import pandas as pd
import warnings
from datetime import datetime, timedelta
from BackEnd.Utils import globals
from BackEnd.Utils.debug import debug


def analyze_stock(ticker_data,breakout_days):
    pct_change = 0
    end_date = datetime.now()
    start_date_one_year = end_date - timedelta(days=breakout_days)
    start_date_one_week = end_date - timedelta(days=7)

    last_year_data = ticker_data[(ticker_data['Date'] >= start_date_one_year) & (ticker_data['Date'] <= end_date)]
    last_week_data = ticker_data[(ticker_data['Date'] >= start_date_one_week) & (ticker_data['Date'] <= end_date)]
    if last_year_data is not None and last_week_data is not None:
        # Calculate the percentage change over the last year
        year_start_price = data['Close'].iloc[0]
        year_end_price = data['Close'].iloc[-1]
        year_change = ((year_end_price - year_start_price) / year_start_price) * 100
        
        # Calculate the recent performance (last 30 days)
    
        recent_start_price = recent_data['Close'].iloc[0]
        recent_end_price = recent_data['Close'].iloc[-1]
        recent_change = ((recent_end_price - recent_start_price) / recent_start_price) * 100
        
        # Criteria for identifying underperformers that recently rallied
        if year_change < 0 and recent_change > 5:  # Adjust the thresholds as needed
            return pct_change
    return pct_change
       
def find_cherries(all_data, StockList):
    cherries_ticker_dtls = pd.DataFrame()
    ticker_stklist_dtls  = pd.DataFrame()
    '''DListLbl = ['Security Code', 'Issuer Name', 'Security Id', 'Security Name', 'Status', 'Group', 'Face Value',
                'ISIN No', 'Industry', 'Instrument', 'Sector Name', 'Industry New Name', 'Igroup Name',
                'ISubgroup Name']'''
    unique_tickers = all_data['ticker'].unique()
    for ticker in unique_tickers:
        ticker_data = all_data[all_data['ticker'] == ticker]
        for break_out in globals.cherry_breakout:
            if break_out[-1] == 'Y':
                breakout_days = int(break_out[:-1])*365
            elif break_out[-1] == 'M':
                breakout_days = int(break_out[:-1])*30
            pct_change = 0;
            pct_change = analyze_stock(ticker_data, breakout_days)
            if pct_change != 0:
                ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]
                #dbg("ticker stocklist " + str(ticker_stklist_dtls))
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    try:
                        ticker_stklist_dtls.loc[:,'Break Out'] = break_out
                        ticker_stklist_dtls.loc[:,'Variation'] = pct_change #add logic to get % growth
                        ticker_stklist_dtls.loc[:,'Report'] = 'C'
                    except SettingWithCopyWarning:
                        
                    finally:
                        # Display any warnings caught
                        for warning in w:
                        #print(f"Warning: {warning.message}")
                    cherries_ticker_dtls = pd.concat([cherries_ticker_dtls, ticker_stklist_dtls])
    
    return cherries_ticker_dtls
