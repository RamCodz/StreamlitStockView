import os
import pandas as pd
from datetime import timedelta
from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor, as_completed
from BackEnd.Utils import globals

MAX_TICKERS = 5000  # Maximum number of tickers to process
MAX_WORKERS = min(os.cpu_count(), 10)  # Limit to 10 threads to avoid API blocking

def fetch_batch_data(tickers, start_date, end_date):
    """Fetch historical data for a batch of tickers using yahooquery."""
    try:
        stock_data = Ticker(tickers).history(start=start_date, end=end_date)
        
        if stock_data.empty:
            return pd.DataFrame()

        if isinstance(stock_data.index, pd.MultiIndex):
            stock_data.reset_index(inplace=True)  # Convert MultiIndex to columns

        stock_data.rename(columns={"symbol": "ticker"}, inplace=True)  # Standardize column name
        return stock_data
    except Exception as e:
        print(f"Error fetching data for batch {tickers}: {e}")
        return pd.DataFrame()

def get_all_data(stock_list):
    """Fetch historical data for all tickers in the stock list using parallel batch processing."""
    all_data = pd.DataFrame()
    five_year_ago = globals.today - timedelta(days=365 * globals.noy)
    
    # Create list of tickers
    tickers = [(row[1]['Security Id'] + '.NS') for i, row in enumerate(stock_list.iterrows(), start=1) if i <= MAX_TICKERS]
    
    # Split tickers into batches of 50 to avoid API overload
    batch_size = 50
    ticker_batches = [tickers[i:i + batch_size] for i in range(0, len(tickers), batch_size)]
    
    print('MAX_WORKERS:', MAX_WORKERS)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_batch_data, batch, five_year_ago, globals.today): batch for batch in ticker_batches}

        for future in as_completed(futures):
            data = future.result()
            if not data.empty:
                all_data = pd.concat([all_data, data], ignore_index=True)
    
    return all_data
