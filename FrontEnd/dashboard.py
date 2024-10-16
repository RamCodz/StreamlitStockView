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
cherries_5y = cherries_5y.drop(['Break Out', 'Variation'], axis=1)
cherries_1y = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1Y')]
cherries_1y = cherries_1y.drop(['Break Out', 'Variation'], axis=1)
cherries_6m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '6M')]
cherries_6m = cherries_6m.drop(['Break Out', 'Variation'], axis=1)
cherries_3m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '3M')]
cherries_3m = cherries_3m.drop(['Break Out', 'Variation'], axis=1)
cherries_1m = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1M')]
cherries_1m = cherries_1m.drop(['Break Out', 'Variation'], axis=1)

common_cherries = cherries_5y
for cherries in [cherries_1y, cherries_6m, cherries_3m, cherries_1m]:
    common_cherries = pd.merge(common_cherries, cherries, how='inner', on=['Security Code'])

gems_5y = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1W')]
gems_1y = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1M')]
gems_6m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '3M')]
gems_3m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '6M')]
gems_1m = stock_list_df[(stock_list_df['Report'] == 'G') & (stock_list_df['Break Out'] == '1Y')]

cherries = [cherries_5y, cherries_1y, cherries_6m, cherries_3m, cherries_1m]

# Filter out empty dataframes
non_empty_cherries = [df for df in cherries if not df.empty]

if non_empty_dfs:
    # Perform successive merges
    common_cherries = reduce(lambda left, right: pd.merge(left, right, on=['Security Code']), non_empty_cherries)

st.write('Dash Board')
if not common_cherries.empty:
    st.write('Common Cherries')
    st.write(non_empty_cherries)
