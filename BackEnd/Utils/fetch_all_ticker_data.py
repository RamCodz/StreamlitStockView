import os
import pandas as pd
from datetime import timedelta
from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor, as_completed
from BackEnd.Utils import globals

MAX_TICKERS = 5000  # Limit the number of tickers to process
MAX_WORKERS = min(os.cpu_count(), 10)  # Limit threads to avoid API blocking
BATCH_SIZE = 50  # Fetch multiple tickers at once

def fetch_batch_data(tickers, start_date, end_date):
    """Fetch historical stock data for a batch of tickers using yahooquery."""
    try:
        stock_data = Ticker(tickers).history(start=start_date, end=end_date)

        # Ensure data exists
        if stock_data.empty:
            return pd.DataFrame()

        # Convert MultiIndex to columns if needed
        if isinstance(stock_data.index, pd.MultiIndex):
            stock_data.reset_index(inplace=True)

        stock_data.rename(columns={"symbol": "ticker"}, inplace=True)  # Standardize column name
        return stock_data

    except Exception as e:
        print(f"Error fetching data for batch {tickers}: {str(e)}")
        return pd.DataFrame()

def get_all_data(stock_list):
    """Fetch historical data for all tickers in the stock list using parallel batch processing."""
    all_data = pd.DataFrame()
    five_year_ago = globals.today - timedelta(days=365 * globals.noy)

    # Extract tickers from the stock list
    tickers = []
    for i, row in enumerate(stock_list.iterrows(), start=1):
        try:
            if i > MAX_TICKERS:
                break
            if "Security Id" not in row[1]:
                continue  # Skip row if missing 'Security Id'

            stk_symbol = row[1]["Security Id"] + ".NS"
            tickers.append(stk_symbol)

        except Exception as e:
            print(f"Error processing row {i}: {str(e)}")

    # Split tickers into batches
    ticker_batches = [tickers[i : i + BATCH_SIZE] for i in range(0, len(tickers), BATCH_SIZE)]

    print("MAX_WORKERS:", MAX_WORKERS)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_batch_data, batch, five_year_ago, globals.today): batch for batch in ticker_batches}

        for future in as_completed(futures):
            try:
                data = future.result()
                if not data.empty:
                    all_data = pd.concat([all_data, data], ignore_index=True)

            except Exception as e:
                print(f"Error processing batch {futures[future]}: {str(e)}")

    return all_data
