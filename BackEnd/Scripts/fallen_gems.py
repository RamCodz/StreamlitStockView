import pandas as pd
import warnings
from datetime import datetime, timedelta
from BackEnd.Utils import globals
from BackEnd.Utils.debug import debug


def dbg(msg):
    debug("Fallen Gems-->" + str(msg))


def get_pct_change(ticker_data, breakout):
    dbg("in get_pct_change")
    pct_change = 0
    start_range_data = pd.DataFrame()
    end_range_data = pd.DataFrame()
    st_max_date_row = pd.DataFrame()
    ed_max_date_row = pd.DataFrame()
    ##ticker_data.index.name = 'Date'
    ##ticker_data = ticker_data.rename_axis('Date').reset_index()
    ##ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
    #dbg("Column labels:" + ticker_data.columns)
    
    end_date = datetime.now()
    start_date_one_year = end_date - timedelta(days=breakout)
    start_date_one_week = end_date - timedelta(days=1)
    dbg('1')
    start_range_data = ticker_data[ (ticker_data['Date'] >= start_date_one_year-timedelta(days=5)) & (ticker_data['Date'] <= start_date_one_year) ]
    end_range_data = ticker_data[(ticker_data['Date'] <= end_date-timedelta(days=5)) & (ticker_data['Date'] >= start_date_one_year)]
    dbg('2')
    if not start_range_data.empty  and not end_range_data.empty: 
        dbg('3')
        #start_range_data['Date'] = pd.to_datetime(start_range_data['Date'])
        dbg('4')
        #end_range_data['Date'] = pd.to_datetime(end_range_data['Date'])
        dbg('5 '+str(start_range_data))
        st_max_date_row = start_range_data.loc[start_range_data['Date'].idxmin()]
        ed_max_date_row = end_range_data.loc[end_range_data['Date'].idxmax()]
    dbg('6')
    if not st_max_date_row.empty and not ed_max_date_row.empty:
        pct_change =((ed_max_date_row['close']-st_max_date_row['close'])/st_max_date_row['close'])*100
        
    dbg('pct_change '+str(pct_change))
    return pct_change


def find_gems(all_data, StockList):
    dbg("in find_gems ")
    gems_ticker_dtls = pd.DataFrame()
    '''DListLbl = ['Security Code', 'Issuer Name', 'Security Id', 'Security Name', 'Status', 'Group', 'Face Value',
                'ISIN No', 'Industry', 'Instrument', 'Sector Name', 'Industry New Name', 'Igroup Name',
                'ISubgroup Name']'''
    unique_tickers = all_data['ticker'].unique()
    for ticker in unique_tickers:
        dbg("ticker " + ticker)
        ticker_data = all_data[all_data['ticker'] == ticker]
        
        for break_out in globals.gems_breakout:
            dbg('Y/M '+break_out[-1])
            dbg('val '+break_out[:-1])
            if break_out[-1] == 'Y':
                breakout_days = int(break_out[:-1])*365
            elif break_out[-1] == 'M':
                breakout_days = int(break_out[:-1])*30
            elif break_out[-1] == 'W':
                breakout_days = int(break_out[:-1])*7
            dbg('breakout days '+str(breakout_days))
            
            pct_change=get_pct_change(ticker_data, breakout_days)
            
            if pct_change >=globals.gems_pct_change:
                ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    try:
                        ticker_stklist_dtls.loc[:,'Break Out'] = break_out
                        ticker_stklist_dtls.loc[:,'Variation'] = pct_change
                        ticker_stklist_dtls.loc[:,'Report'] = 'G'
                        
                    except SettingWithCopyWarning:
                        dbg('SettingWithCopyWarning')
                    finally:
                        # Display any warnings caught
                        for warning in w:
                            dbg('SettingWithCopyWarning')
                        #print(f"Warning: {warning.message}")
                    gems_ticker_dtls = pd.concat([gems_ticker_dtls, ticker_stklist_dtls])
    return gems_ticker_dtls
