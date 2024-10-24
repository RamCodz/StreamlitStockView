import pandas as pd
from datetime import datetime, timedelta
import os
##from predict_stk import filter_stocks  --
from BackEnd.Utils.debug import debug
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Scripts.fallen_gems import find_gems
from BackEnd.Utils.creategitfiles import create_or_update_file
import streamlit as st

def dbg(msg):
    debug("main-->"+str(msg))

def main():
    current_directory = os.getcwd()
    globals.curr_dir = current_directory +"/"
    globals.today = datetime.now().strftime(globals.dt_format)
    globals.stockview_filename  = globals.stockview_filename.replace("*",str(globals.today))
    all_data = pd.DataFrame()
    StockList = pd.DataFrame()
    StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))
  
    all_data = get_all_data(StockList)
    all_data = all_data.rename_axis('Date').reset_index()## assigning first col name in df and make it as column
    all_data['Date'] = pd.to_datetime(all_data['Date'])  

    cherries_ticker_dtls = find_cherries(all_data, StockList)
    gems_ticker_dtls = find_gems(all_data, StockList)
    final_df = pd.DataFrame()
    final_df = pd.concat([final_df, cherries_ticker_dtls])
    final_df = pd.concat([final_df, gems_ticker_dtls])
    
    ##new dataframes can be added and the same needs to be handled in gen_file module
    ##create_or_update_file(str(globals.data_filepath) + "Cherries.csv" ,cherries_ticker_dtls)
    ##st.write("cherries path**** "+globals.data_filepath) + str(globals.cherries_filename))
    create_or_update_file((str(globals.data_filepath) + str(globals.stockview_filename)),final_df)

main()
