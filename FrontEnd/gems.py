import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
from FrontEnd.Utils.display_stocks import create_tabs

# Main logic to read stock data and create tabs
stock_list_file = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list_file)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

cherries_stock_list = stock_list_df[stock_list_df['Report'] == 'G']

tab_titles = {    
    "1W": "1 Week Breakout",
    "1M": "1 Month Breakout",
    "3M": "3 Month Breakout",
    "6M": "6 Month Breakout",
    "1Y": "1 Year Breakout"    
}

create_tabs(tab_titles, cherries_stock_list)
