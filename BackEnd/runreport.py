import pandas as pd
from datetime import datetime, timedelta
import os
import time
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Scripts.fallen_gems import find_gems
from BackEnd.Scripts.dashboard_data import mark_occurrences
from BackEnd.Utils.creategitfiles import create_or_delete_file


def log_execution_time(step_name, start_time):
    """Helper function to log the time taken for each step."""
    elapsed_time = time.time() - start_time
    print(f"Time taken for {step_name}: {elapsed_time:.2f} seconds")


def analyze_stock(ticker_data, breakout_days, break_type):
    if break_type not in ['CO', 'BA']:
        raise ValueError(f"Invalid break type {break_type}. Must be 'CO' or 'BA'.")
    
    if break_type == 'BA':
        recent_data = ticker_data.iloc[-22] if breakout_days > 21 else ticker_data.iloc[-1]
        past_data = ticker_data.iloc[-(breakout_days + 21)] if breakout_days > 21 and len(ticker_data) >= (breakout_days + 21) else ticker_data.iloc[-breakout_days] if len(ticker_data) >= breakout_days else None
    else:
        recent_data = ticker_data.iloc[-6] if breakout_days != 5 else ticker_data.iloc[-1]
        past_data = ticker_data.iloc[-(breakout_days + 5)] if breakout_days != 5 and len(ticker_data) >= (breakout_days + 5) else ticker_data.iloc[-breakout_days] if len(ticker_data) >= breakout_days else None
    
    if past_data is not None:
        return round(((recent_data['close'] - past_data['close']) / past_data['close']) * 100, 2)
    return None


def process_ticker_data(ticker_data, ticker_stklist_dtls):
    fields = ['1W', '1M', '3M', '6M', '1Y', '5Y']
    ticker_stklist_dtls_copy = ticker_stklist_dtls.copy()
    
    for field in fields:
        ticker_stklist_dtls_copy[f'{field}_value'] = 0.00
        ticker_stklist_dtls_copy[f'{field}_FLG'] = 'N'
    ticker_stklist_dtls_copy['Report'] = ''
    
    return ticker_stklist_dtls_copy


def get_breakout_days(break_out):
    return int(break_out[:-1]) * {'Y': 232, 'M': 21, 'W': 5}[break_out[-1]]


def calculate_returns(all_data, stock_list):
    ticker_dfs = []
    for ticker in all_data['ticker'].unique():
        ticker_data = all_data[all_data['ticker'] == ticker]
        ticker_stklist_dtls = stock_list[stock_list['Security Id'] + '.NS' == ticker]
        ticker_stklist_dtls = process_ticker_data(ticker_data, ticker_stklist_dtls)
        
        for break_out in ['1W', '1M', '3M', '6M', '1Y', '5Y']:
            breakout_days = get_breakout_days(break_out)
            pct_change = analyze_stock(ticker_data, breakout_days, "BA")
            ticker_stklist_dtls[f'{break_out}_value'] = pct_change
        
        ticker_dfs.append(ticker_stklist_dtls)
    
    return pd.concat(ticker_dfs, ignore_index=True)


def process_stock_data():
    try:
        start_time = time.time()
        
        # Step 1: Initialize Globals
        gv_sys_date_str = datetime.now().strftime(globals.dt_format)
        globals.today = datetime.strptime(gv_sys_date_str, globals.dt_format)
        globals.curr_dir = os.getcwd() + "/"
        globals.stockview_filename = globals.stockview_filename.replace("*", gv_sys_date_str)
        stock_list_path = os.path.join(globals.equity_list_path, globals.equity_list_filename)
        log_execution_time("step-1", start_time)
        
        # Step 2: Load Stock List
        start_time = time.time()
        stock_list = pd.read_csv(stock_list_path)
        log_execution_time("step-2", start_time)
        
        # Step 3: Fetch Historical Data
        start_time = time.time()
        all_data = get_all_data(stock_list).rename_axis('Date').reset_index()
        all_data['Date'] = pd.to_datetime(all_data['Date'])
        log_execution_time("step-3", start_time)
        
        # Step 4: Calculate Returns
        start_time = time.time()
        calculated_ticker_details = calculate_returns(all_data, stock_list)
        log_execution_time("step-4", start_time)
        
        # Step 5: Find Cherries
        start_time = time.time()
        cherries_ticker_details = find_cherries(calculated_ticker_details)
        log_execution_time("step-5", start_time)
        
        # Step 6: Find Gems
        start_time = time.time()
        gems_ticker_details = find_gems(calculated_ticker_details)
        final_df = pd.concat([cherries_ticker_details, gems_ticker_details])
        log_execution_time("step-6", start_time)
        
        # Step 7: Mark Occurrences
        start_time = time.time()
        marked_df = mark_occurrences(final_df, globals.data_filepath)
        marked_df['Report Date'] = gv_sys_date_str
        log_execution_time("step-7", start_time)
        
        # Step 8: Create Report File
        start_time = time.time()
        create_or_delete_file(globals.data_filepath, globals.stockview_filename, marked_df)
        log_execution_time("step-8", start_time)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
