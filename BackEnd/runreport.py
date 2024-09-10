import pandas as pd
from datetime import datetime, timedelta
import os
##from predict_stk import filter_stocks  --
from BackEnd.Utils.debug import debug
from BackEnd.Utils import globals
from BackEnd.Utils.fetch_all_ticker_data import get_all_data
from BackEnd.Scripts.early_cherries import find_cherries
from BackEnd.Utils.creategitfiles import create_or_update_file
import streamlit as st

def dbg(msg):
    debug("main-->"+str(msg))

def main():
    current_directory = os.getcwd()
    globals.curr_dir = current_directory +"/"
    globals.dbg_filepath = str(globals.curr_dir) + str(globals.dbg_filepath)
    globals.equity_list_path = str(globals.curr_dir) + str(globals.equity_list_path)
    globals.data_filepath = str(globals.curr_dir) + str(globals.data_filepath)
    st.write("globals.curr_dir"+str(globals.curr_dir))
    globals.today = datetime.now().strftime(globals.dt_format)
    globals.dbg_filename = str(globals.dbg_filename).replace("*", str(globals.today))
    globals.data_filename = globals.data_filename.replace("*",str(globals.today))

    dbg("*********************STARTED**************************")
    dbg("in main module")
    dbg("Current Directory:"+str(current_directory))
    dbg("dbg filepath" +globals.dbg_filepath)
    dbg("dbg filename "+globals.dbg_filename)
    dbg("excel "+str(globals.equity_list_path) + str(globals.equity_list_filename))

    all_data = pd.DataFrame()
    dbg("reading stocklist from csv")
    StockList = pd.DataFrame()
    st.write(str(globals.equity_list_path) + str(globals.equity_list_filename))
    StockList = pd.read_csv(str(globals.equity_list_path) + str(globals.equity_list_filename))

    dbg("before fetching all tickers data ")
    all_data = get_all_data(StockList)
    dbg("after fetching all tickers data ")
    all_data = all_data.rename_axis('Date').reset_index()## assigning first col name in df and make it as column
    all_data['Date'] = pd.to_datetime(all_data['Date'])  

    dbg("lets find Early cherries ")
    cherries_ticker_dtls = find_cherries(all_data, StockList)
    dbg("Early cherries completed ")

    dbg("Lets find Fallen Gems")
    ##gems_ticker_dtls = fallen_gems(all_data, StockList)
    dbg("Fallen Gems Completed")


    ##new dataframes can be added and the same needs to be handled in gen_file module
    #create_or_update_file(globals.data_filepath,cherries_ticker_dtls)

    dbg("*********************COMPLETED**************************")'''

main()
