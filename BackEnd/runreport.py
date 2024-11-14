import pandas as pd
from datetime import datetime
import os
from BackEnd.Utils.debug import debug
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Scripts.fallen_gems import find_gems
from BackEnd.Utils.creategitfiles import create_or_update_file


def process_stock_data(gv_sys_date):
    # Convert date to the appropriate format
    current_directory = os.getcwd()
    globals.curr_dir = current_directory + "/"
    globals.today = datetime.strptime(gv_sys_date, globals.dt_format)
    globals.stockview_filename = globals.stockview_filename.replace("*", str(globals.today))
    
    # Load stock list and data
    StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))
    all_data = get_all_data(StockList, globals.today)
    all_data = all_data.rename_axis('Date').reset_index()  # Assign first col name in df and make it a column
    all_data['Date'] = pd.to_datetime(all_data['Date'])

    # Filter data based on the selected date
    all_data = all_data[all_data['Date'] <= globals.today]

    # Find cherries and gems
    cherries_ticker_dtls = find_cherries(all_data, StockList, globals.today)
    # gems_ticker_dtls = find_gems(all_data, StockList)
    # Concatenate results
    # final_df = pd.concat([cherries_ticker_dtls, gems_ticker_dtls])
    final_df = cherries_ticker_dtls
    # Create or update the output file
    print(str(globals.stockview_filename))
    create_or_update_file((str(globals.data_filepath) + str(globals.stockview_filename)), final_df)
    print("Completed process_stock_data...")
