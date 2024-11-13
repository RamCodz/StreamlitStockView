import pandas as pd
import warnings
from datetime import datetime, timedelta


def analyze_stock(ticker_data, breakout_days, break_type):
    if break_type not in ['CO', 'BA']: #CO-Consecutive   BA-Break after
        raise ValueError(f"Invalid break type {break_type}. Must be 'CO' or 'BA'.")
    
    if break_type == 'BA':
        # Monthly data
        if breakout_days <= 21:
            recent_data = ticker_data.iloc[-1]
            past_data = ticker_data.iloc[-breakout_days] if len(ticker_data) >= breakout_days else None
        else:
            recent_data = ticker_data.iloc[-22]
            past_data = ticker_data.iloc[-(breakout_days + 21)] if len(ticker_data) >= (breakout_days + 21) else None
    else:
        # Weekly data
        if breakout_days == 5:
            recent_data = ticker_data.iloc[-1]
            past_data = ticker_data.iloc[-breakout_days] if len(ticker_data) >= breakout_days else None
        else:
            recent_data = ticker_data.iloc[-6]
            past_data = ticker_data.iloc[-(breakout_days + 5)] if len(ticker_data) >= (breakout_days + 5) else None
    
    # Only calculate pct_change if we have enough data
    if past_data is not None:
        pct_change = round(((recent_data['close'] - past_data['close']) / past_data['close']) * 100, 2)
        return pct_change
    return 0

def process_ticker_data(ticker_data, ticker_stklist_dtls):
    """Process and update the stock list for a given ticker."""
    ticker_stklist_dtls_copy = ticker_stklist_dtls.copy()

    # Initialize all the fields to avoid warnings and ensure safe modification
    ticker_stklist_dtls_copy.loc[:, 'Report'] = 'C'
    ticker_stklist_dtls_copy.loc[:, '1W_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '1M_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '3M_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '6M_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '1Y_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '5Y_value'] = 0.00
    ticker_stklist_dtls_copy.loc[:, '1W_FLG'] = 'N'
    ticker_stklist_dtls_copy.loc[:, '1M_FLG'] = 'N'
    ticker_stklist_dtls_copy.loc[:, '3M_FLG'] = 'N'
    ticker_stklist_dtls_copy.loc[:, '6M_FLG'] = 'N'
    ticker_stklist_dtls_copy.loc[:, '1Y_FLG'] = 'N'
    ticker_stklist_dtls_copy.loc[:, '5Y_FLG'] = 'N'

    return ticker_stklist_dtls_copy

def apply_flags(ticker_stklist_dtls):
    """Apply flags if one timeframe outperforms another."""
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['1M_value'], '1M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['3M_value'], '3M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['6M_value'], '6M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['1Y_value'], '1Y_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['5Y_value'], '5Y_FLG'] = 'Y'

def get_breakout_days(break_out):
    """Determine the number of breakout days based on the period."""
    if break_out[-1] == 'Y':
        return int(break_out[:-1]) * 21
    elif break_out[-1] == 'M':
        return int(break_out[:-1]) * 21
    elif break_out[-1] == 'W':
        return int(break_out[:-1]) * 5
    return 0

def find_cherries(all_data, StockList, current_date):
    cherries_ticker_dtls = pd.DataFrame()
    unique_tickers = all_data['ticker'].unique()
    current_date = pd.to_datetime(current_date)

    for ticker in unique_tickers:
        ticker_data = all_data[all_data['ticker'] == ticker]
        ticker_data = ticker_data[ticker_data['Date'] <= current_date]

        # Filter stock list based on ticker
        ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]

        # Process and initialize stock data
        ticker_stklist_dtls = process_ticker_data(ticker_data, ticker_stklist_dtls)

        for break_out in ['1W', '1M', '3M', '6M', '1Y', '5Y']:
            breakout_days = get_breakout_days(break_out)
            pct_change = analyze_stock(ticker_data, breakout_days, "BA")

            # Assign the calculated percentage change to the appropriate column
            breakout_name = f"{break_out}_value"
            ticker_stklist_dtls.loc[:, breakout_name] = pct_change

        # Apply flags based on breakout conditions
        apply_flags(ticker_stklist_dtls)

        # Concatenate the stock data for this ticker with the results
        cherries_ticker_dtls = pd.concat([cherries_ticker_dtls, ticker_stklist_dtls])

    return cherries_ticker_dtls
