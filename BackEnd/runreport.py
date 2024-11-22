import pandas as pd
from datetime import datetime, timedelta
import os
import time
from BackEnd.Utils.debug import debug
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Scripts.fallen_gems import find_gems
from BackEnd.Utils.creategitfiles import create_or_update_file

def analyze_stock(ticker_data, breakout_days, break_type):
    if break_type not in ['CO', 'BA']: #CO-Consecutive   BA-Break after
        raise ValueError(f"Invalid break type {break_type}. Must be 'CO' or 'BA'.")
    
    if break_type == 'BA':
        # Monthly data
        if breakout_days <= 21:
            recent_data = ticker_data.iloc[-1]
            past_data = ticker_data.iloc[-breakout_days] if len(ticker_data) >= breakout_days else None
        else:
            recent_data = ticker_data.iloc[-22] if len(ticker_data) >= 22 else None
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
    ticker_stklist_dtls_copy = ticker_stklist_dtls.copy()
    fields = ['1W', '1M', '3M', '6M', '1Y', '5Y']

    for field in fields:
        ticker_stklist_dtls_copy[f'{field}_value'] = 0.00
        ticker_stklist_dtls_copy[f'{field}_FLG'] = 'N'
    ticker_stklist_dtls_copy['Report'] = 'C'

    return ticker_stklist_dtls_copy

def get_breakout_days(break_out):
    return int(break_out[:-1]) * {'Y': 365, 'M': 21, 'W': 5}[break_out[-1]]

def calculate_returns(all_data, StockList):
    ticker_dfs = []
    unique_tickers = all_data['ticker'].unique()

    for ticker in unique_tickers:
        ticker_data = all_data[all_data['ticker'] == ticker]
        ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]
        ticker_stklist_dtls = process_ticker_data(ticker_data, ticker_stklist_dtls)

        for break_out in ['1W', '1M', '3M', '6M', '1Y', '5Y']:
            breakout_days = get_breakout_days(break_out)
            pct_change = analyze_stock(ticker_data, breakout_days, "BA")
            ticker_stklist_dtls[f'{break_out}_value'] = pct_change

        ticker_dfs.append(ticker_stklist_dtls)
    
    return pd.concat(ticker_dfs, ignore_index=True)

def process_stock_data():

    try:
        # Step-1: Set/read the global variables
        start_time = time.time()
        gv_sys_date_str = datetime.now().strftime(globals.dt_format)
        # gv_sys_date_str = str("2024-11-21")
        globals.today = datetime.strptime(gv_sys_date_str, globals.dt_format)
        current_directory = os.getcwd()
        globals.curr_dir = current_directory + "/"
        globals.stockview_filename = globals.stockview_filename.replace("*", gv_sys_date_str)
        stock_list_path = os.path.join(globals.equity_list_path, globals.equity_list_filename)
        print(f"Time taken for step-1: {time.time() - start_time:.2f} seconds")
        
        # Step-2: Read the stock ticker details from inbound file
        start_time = time.time()
        StockList = pd.read_csv(stock_list_path)
        print(f"Time taken for step-2: {time.time() - start_time:.2f} seconds")
        
        # Step-3: Get the historical data for all the tickers
        start_time = time.time()
        all_data = get_all_data(StockList)
        all_data = all_data.rename_axis('Date').reset_index()  # Assign the first column name in df and make it a column
        all_data['Date'] = pd.to_datetime(all_data['Date'])  # Convert 'Date' column to datetime
        print(f"Time taken for step-3: {time.time() - start_time:.2f} seconds")
        
        # Step-4: Calculate the returns over mentioned periods
        start_time = time.time()
        calculated_ticker_dtls = calculate_returns(all_data, StockList)
        print(f"Time taken for step-4: {time.time() - start_time:.2f} seconds")
        
        # Step-5: Find the cherries
        start_time = time.time()
        cherries_ticker_dtls = find_cherries(calculated_ticker_dtls, all_data)
        print(f"Time taken for step-5: {time.time() - start_time:.2f} seconds")
        
        # Step-6: Find the gems (currently commented out)
        # start_time = time.time()
        # gems_ticker_dtls = find_gems(calculated_ticker_dtls)
        # final_df = pd.concat([cherries_ticker_dtls, gems_ticker_dtls])
        # print(f"Time taken for step-6: {time.time() - start_time:.2f} seconds")
        
        # Step-7: Create the report file     
        start_time = time.time()
        final_df = cherries_ticker_dtls
        output_file = os.path.join(globals.data_filepath, globals.stockview_filename)
        create_or_update_file(output_file, final_df)
        print(f"Time taken for step-7: {time.time() - start_time:.2f} seconds")
        
    except Exception as e:
        debug(f"An error occurred while processing stock data: {e}")
        raise
