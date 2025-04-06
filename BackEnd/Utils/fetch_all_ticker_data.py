import os
import pandas as pd
from datetime import timedelta
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
from BackEnd.Utils import globals

MAX_TICKERS = 5000
MAX_WORKERS = os.cpu_count()

# Patch User-Agent once to avoid connection issues
import requests
yf.shared._requests = requests.Session()
yf.shared._requests.headers.update({'User-Agent': 'Mozilla/5.0'})

def get_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data for a given ticker using yfinance."""
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval='1d', progress=False, threads=False)
        return df
    except Exception:
        return pd.DataFrame()

def fetch_ticker_data(ticker, start_date, end_date):
    """Fetch data for a single ticker and add the ticker column."""
    data = get_stock_data(ticker, start_date, end_date)
    if not data.empty:
        data = data.reset_index()
        data['ticker'] = ticker
    return data

def get_all_data(stock_list):
    """Fetch historical data for all tickers using multithreading."""
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
