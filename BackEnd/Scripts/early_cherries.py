import pandas as pd
import warnings
from datetime import datetime, timedelta
from BackEnd.Utils import globals
from BackEnd.Utils.debug import debug

#pct_change = 0;
def dbg(msg):
    debug("early_cherries-->" + str(msg))


def analyze_stock(ticker_data,breakout_days):
    dbg("in analyze_stock")
    dbg(ticker_data)
    ##ticker_data.index.name = 'Date'
    ##ticker_data = ticker_data.rename_axis('Date').reset_index()
    ##ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
    #dbg("Column labels:" + ticker_data.columns)
    pct_change = 0
    end_date = datetime.now()
    start_date_one_year = end_date - timedelta(days=breakout_days)
    start_date_one_week = end_date - timedelta(days=7)

    last_year_data = ticker_data[(ticker_data['Date'] >= start_date_one_year) & (ticker_data['Date'] <= end_date)]
    last_week_data = ticker_data[(ticker_data['Date'] >= start_date_one_week) & (ticker_data['Date'] <= end_date)]
    if last_year_data is not None and last_week_data is not None:
        # Calculate average closing prices
        avg_close_one_year = last_year_data['close'].mean()
        avg_close_last_week = last_week_data['close'].mean()

        avg_volume_one_year = last_year_data['volume'].mean()
        avg_volume_last_week = last_week_data['volume'].mean()

        dbg('avg_volume_one_year ' + str(avg_volume_one_year))
        dbg('avg_volume_last_week ' + str(avg_volume_last_week))

        dbg('avg_close_one_year ' + str(avg_close_one_year))
        dbg('avg_close_last_week ' + str(avg_close_last_week))

        # Check if last week's average closing price is greater than one-year average closing price
        #if avg_close_one_year < avg_close_last_week and avg_volume_one_year < avg_volume_last_week:
        if avg_close_one_year < avg_close_last_week:
            st_max_date_row = last_year_data.loc[last_year_data['Date'].idxmin()]
            ed_max_date_row = last_week_data.loc[last_week_data['Date'].idxmax()]
            pct_change = ((ed_max_date_row['close']-st_max_date_row['close'])/st_max_date_row['close'])*100
            dbg('Early cherries '+str(pct_change))
            return pct_change
    return pct_change


def find_cherries(all_data, StockList):
    dbg("in find_cherries ")
    cherries_ticker_dtls = pd.DataFrame()
    ticker_stklist_dtls  = pd.DataFrame()
    '''DListLbl = ['Security Code', 'Issuer Name', 'Security Id', 'Security Name', 'Status', 'Group', 'Face Value',
                'ISIN No', 'Industry', 'Instrument', 'Sector Name', 'Industry New Name', 'Igroup Name',
                'ISubgroup Name']'''
    unique_tickers = all_data['ticker'].unique()
    for ticker in unique_tickers:
        dbg("ticker " + ticker)
        ticker_data = all_data[all_data['ticker'] == ticker]
        for break_out in globals.cherry_breakout:
            dbg('Y/M '+break_out[-1])
            dbg('val '+break_out[:-1])
            if break_out[-1] == 'Y':
                breakout_days = int(break_out[:-1])*365
            elif break_out[-1] == 'M':
                breakout_days = int(break_out[:-1])*30
            dbg('breakout days '+str(breakout_days))
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
                        dbg('SettingWithCopyWarning')
                    finally:
                        # Display any warnings caught
                        for warning in w:
                            dbg('SettingWithCopyWarning')
                        #print(f"Warning: {warning.message}")
                    cherries_ticker_dtls = pd.concat([cherries_ticker_dtls, ticker_stklist_dtls])
    
    return cherries_ticker_dtls
