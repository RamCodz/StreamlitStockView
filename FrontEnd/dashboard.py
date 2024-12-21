import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals

# Main logic to read stock data and create tabs
stock_list_file = str(globals.data_filepath) + "/" + str(globals.current_report_name)  # Make sure there's a separator

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list_file)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

# Filter the DataFrame
dashboard_stock_list = stock_list_df[stock_list_df['Occurrence'] > 0].sort_values(by=['Industry New Name', 'ISubgroup Name'], ascending=[True, True])

# Define alias names for columns
alias_names = {
    'Security Name': 'Stock Name',
    'Industry New Name': 'Industry',
    'Occurrence': 'Occurrence Count'
}

# Rename the columns
#dashboard_stock_list = dashboard_stock_list.rename(columns=alias_names)

# Display data in Streamlit with the alias names, without the index
st.header('Turn around')
st.write(dashboard_stock_list)
#st.write(dashboard_stock_list['Security Name', 'Industry New Name'', 'Occurrence'])
