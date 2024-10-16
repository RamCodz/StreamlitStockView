import streamlit as st
from pathlib import Path
import pandas as pd
import yfinance as yf
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
import plotly.graph_objs as go

# Read stock data from latest file
stock_list = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

try:
    stock_list_df = pd.read_csv(stock_list)
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

cherries_5y = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '5Y')]
cherries_1y = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1Y')]
cherries_6m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '6M')]
cherries_3m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '3M')]
cherries_1m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1M')]

gems_5y = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1W')]
gems_1y = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1M')]
gems_6m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '3M')]
gems_3m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '6M')]
gems_1m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1Y')]

common_cherries = cherries_5y[cherries_5y['Security Code'].isin(cherries_1y['Security Code'])]

st.write('Dash Board')
if not common_cherries.empty:
    st.write('Common Cherries')
    st.write(common_cherries)
