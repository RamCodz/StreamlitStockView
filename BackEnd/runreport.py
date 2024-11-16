import pandas as pd
from datetime import datetime
import os
from BackEnd.Utils.debug import debug  # Ensure this is set up properly for logging
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Scripts.fallen_gems import find_gems
from BackEnd.Utils.creategitfiles import create_or_update_file

def process_stock_data():
    # Ensure gv_sys_date is a string and convert it to datetime
    #gv_sys_date = datetime.strptime("2022-11-18", globals.dt_format) 
    gv_sys_date = datetime.now().strftime(globals.dt_format)
    # Convert string to datetime object using the format from globals
    globals.today =  str(gv_sys_date) # Ensure globals.dt_format is defined
    print(f"System date as datetime object: {globals.today}")

    # Set current directory and stockview filename
    current_directory = os.getcwd()
    globals.curr_dir = current_directory + "/"
    globals.stockview_filename = globals.stockview_filename.replace("*", str(globals.today))
    print(f"Stockview filename: {globals.stockview_filename}")

    # Load stock list and data
    stock_list_path = str(globals.equity_list_path) + str(globals.equity_list_filename)
    StockList = pd.read_csv(stock_list_path)
    
    # Fetch all stock data based on the loaded stock list and today's date
    all_data = get_all_data(StockList, globals.today)
    
    # Ensure that the data is in proper format and contains a 'Date' column
    all_data = all_data.rename_axis('Date').reset_index()  # Assign the first column name in df and make it a column
    all_data['Date'] = pd.to_datetime(all_data['Date'])  # Convert 'Date' column to datetime

    # Filter data based on the selected system date
    all_data = all_data[all_data['Date'] <= globals.today]
    print(f"Filtered data for date {globals.today}: {all_data.shape[0]} records")

    # Find cherries (and optionally gems)
    cherries_ticker_dtls = find_cherries(all_data, StockList, globals.today)
    # Uncomment to include gems if needed:
    # gems_ticker_dtls = find_gems(all_data, StockList)
    
    # Concatenate cherries and gems data (if using gems)
    final_df = cherries_ticker_dtls  # Could include gems as well if uncommented
    # final_df = pd.concat([cherries_ticker_dtls, gems_ticker_dtls])

    # Create or update the output file
    output_file = str(globals.data_filepath) + str(globals.stockview_filename)
    create_or_update_file(output_file, final_df)
    print(f"Created/Updated the file at: {output_file}")
    print("Completed process_stock_data...")
