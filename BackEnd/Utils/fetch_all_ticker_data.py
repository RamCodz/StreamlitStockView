import os
import pandas as pd
from datetime import timedelta
from yahoo_fin import stock_info as si
from concurrent.futures import ThreadPoolExecutor, as_completed
from BackEnd.Utils import globals

MAX_TICKERS = 5000  # Maximum number of tickers to process
MAX_WORKERS = os.cpu_count() * 2  # Number of threads to use

def get_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data for a given ticker."""
    try:
        return si.get_data(ticker, start_date=start_date, end_date=end_date, interval='1d')
    except Exception:
        return pd.DataFrame()

def fetch_ticker_data(ticker, start_date, end_date):
    """Wrapper function to fetch data for a single ticker and add a ticker column."""
    data = get_stock_data(ticker, start_date, end_date)
    if not data.empty:
        data['ticker'] = ticker
    return data

def get_all_data(stock_list):
    """Fetch historical data for all tickers in the stock list using parallel processing."""
    all_data = pd.DataFrame()
    five_year_ago = globals.today - timedelta(days=365 * globals.noy)
    print('MAX_WORKERS', MAX_WORKERS)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, row in enumerate(stock_list.iterrows(), start=1):
            if i > MAX_TICKERS:
                break
            stk_symbol = row[1]['Security Id'] + '.NS'
            futures.append(executor.submit(fetch_ticker_data, stk_symbol, five_year_ago, globals.today))
        
        for future in as_completed(futures):
            data = future.result()
            if not data.empty:
                all_data = pd.concat([all_data, data], ignore_index=True)
    
    return all_data
