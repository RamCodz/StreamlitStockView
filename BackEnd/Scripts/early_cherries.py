import pandas as pd
import warnings
from datetime import datetime, timedelta

def dbg(msg):
    debug("early_cherries-->" + str(msg))

def analyze_stock(ticker_data, breakout_days, w_or_m):
    print("in analyze_stock")
    pct_change = 0
    
    if w_or_m == 'M':
        if breakout_days <= 21:
            recent_data = ticker_data.iloc[-1]
            try:
                past_data = ticker_data.iloc[-breakout_days]
            except IndexError:
                print("Index is out of bounds")
                past_data = None
        else:
            recent_data = ticker_data.iloc[-(1+21)]
            try:
                past_data = ticker_data.iloc[-(breakout_days+21)]
            except IndexError:
                print("Index is out of bounds")
                past_data = None
    else:
        if breakout_days == 5:
            recent_data = ticker_data.iloc[-1]
            try:
                past_data = ticker_data.iloc[-breakout_days]
            except IndexError:
                print("Index is out of bounds")
                past_data = None
        else:
            recent_data = ticker_data.iloc[-(1+5)]
            try:
                past_data = ticker_data.iloc[-(breakout_days+5)]
            except IndexError:
                print("Index is out of bounds")
                past_data = None
    
    print(past_data)
    if past_data is not None:
        pct_change = round((((recent_data['close'] - past_data['close']) / past_data['close']) * 100), 2)
    return pct_change

def find_cherries(all_data, StockList, current_date):
    print("in find_cherries ")
    cherries_ticker_dtls = pd.DataFrame()
    ticker_stklist_dtls  = pd.DataFrame()
    m_ticker_stklist_dtls  = pd.DataFrame()
    breakout_name = ""
    unique_tickers = all_data['ticker'].unique()
    current_date = pd.to_datetime(current_date)
    
    for ticker in unique_tickers:
        print("ticker " + ticker)
        ticker_data = all_data[all_data['ticker'] == ticker]
        ticker_data = ticker_data[ticker_data['date'] <= current_date]
        ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                ticker_stklist_dtls.loc[:, 'Report'] = 'C'
                ticker_stklist_dtls.loc[:, '1W_value'] = 0.00
                ticker_stklist_dtls.loc[:, '1M_value'] = 0.00
                ticker_stklist_dtls.loc[:, '3M_value'] = 0.00
                ticker_stklist_dtls.loc[:, '6M_value'] = 0.00
                ticker_stklist_dtls.loc[:, '1Y_value'] = 0.00
                ticker_stklist_dtls.loc[:, '5Y_value'] = 0.00
                ticker_stklist_dtls.loc[:, '1W_FLG'] = 'N'
                ticker_stklist_dtls.loc[:, '1M_FLG'] = 'N'
                ticker_stklist_dtls.loc[:, '3M_FLG'] = 'N'
                ticker_stklist_dtls.loc[:, '6M_FLG'] = 'N'
                ticker_stklist_dtls.loc[:, '1Y_FLG'] = 'N'
                ticker_stklist_dtls.loc[:, '5Y_FLG'] = 'N'
            except SettingWithCopyWarning:
                print('SettingWithCopyWarning')
            finally:
                for warning in w:
                    print('SettingWithCopyWarning')
        m_ticker_stklist_dtls = ticker_stklist_dtls
        current_index = ticker_stklist_dtls.index
        for break_out in ['1W','1M','3M','6M','1Y','5Y']:
            print('Y/M ' + break_out[-1])
            print('val ' + break_out[:-1])
            if break_out[-1] == 'Y':
                breakout_days = int(break_out[:-1]) * 21
                breakout_name = break_out + "_value"
            elif break_out[-1] == 'M':
                breakout_days = int(break_out[:-1]) * 21
                breakout_name = break_out + "_value"
            elif break_out[-1] == 'W':
                breakout_days = int(break_out[:-1]) * 5
                breakout_name = break_out + "_value"
            print('breakout days ' + str(breakout_days))
            w_pct_change = 0
            m_pct_change = 0
            print("breakout_days " + str(breakout_days))
            w_pct_change = analyze_stock(ticker_data, breakout_days, 'W')
            m_pct_change = analyze_stock(ticker_data, breakout_days, 'M')
            print("w_pct change " + str(w_pct_change))
            print("current_index " + str(current_index))
            ticker_stklist_dtls.loc[current_index, breakout_name] = w_pct_change
            m_ticker_stklist_dtls.loc[current_index, breakout_name] = m_pct_change
        
        ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['1M_value'], '1M_FLG'] = 'Y'
        ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['3M_value'], '3M_FLG'] = 'Y'
        ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['6M_value'], '6M_FLG'] = 'Y'
        ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['1Y_value'], '1Y_FLG'] = 'Y'
        ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['5Y_value'], '5Y_FLG'] = 'Y'
        
        m_ticker_stklist_dtls.loc[m_ticker_stklist_dtls['1M_value'] > m_ticker_stklist_dtls['3M_value'], '3M_FLG'] = 'Y'
        m_ticker_stklist_dtls.loc[m_ticker_stklist_dtls['1M_value'] > m_ticker_stklist_dtls['6M_value'], '6M_FLG'] = 'Y'
        m_ticker_stklist_dtls.loc[m_ticker_stklist_dtls['1M_value'] > m_ticker_stklist_dtls['1Y_value'], '1Y_FLG'] = 'Y'
        m_ticker_stklist_dtls.loc[m_ticker_stklist_dtls['1M_value'] > m_ticker_stklist_dtls['5Y_value'], '5Y_FLG'] = 'Y'
        
        cherries_ticker_dtls = pd.concat([cherries_ticker_dtls, ticker_stklist_dtls])
    
    return cherries_ticker_dtls
