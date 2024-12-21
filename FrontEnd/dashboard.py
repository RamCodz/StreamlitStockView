import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
from FrontEnd.Utils.display_stocks import create_tabs


# Main logic to read stock data and create tabs
stock_list_file = str(globals.data_filepath) + str(globals.current_report_name)

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list_file)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

dashboard_stock_list = stock_list_df[stock_list_df['Occurrence'] > 0].sort_values(by=['Industry New Name','ISubgroup Name'], ascending=[True, True])

st.header('Turn around')
st.write(dashboard_stock_list['Security Name', 'Face Value', 'Industry New Name', 'Igroup Name', 'Occurrence'])
