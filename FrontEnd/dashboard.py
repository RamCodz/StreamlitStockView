import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals

# Main logic to read stock data and create tabs
stock_list_file = str(globals.data_filepath) + "/" + str(globals.current_report_name)  # Ensure proper separator between path and file name

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list_file)
    if stock_list_df.empty:
        st.warning("The file is empty!")
except EmptyDataError:
    st.warning("The file is empty!")
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

# Proceed if data is not empty
if not stock_list_df.empty:
    # Filter the DataFrame to only show records with Occurrence > 0
    dashboard_stock_list = stock_list_df[stock_list_df['Occurrence'] > 0].sort_values(by=['Occurrence'], ascending=True)

    # Define alias names for columns
    alias_names = {
        'Security Name': 'Stock Name',
        'Industry New Name': 'Industry Name',
        'Occurrence': 'Occurrence Count'
    }

    # Rename the columns
    dashboard_stock_list = dashboard_stock_list.rename(columns=alias_names)

    # Display data in Streamlit with the alias names, without the index
    st.subheader('Turn around')
    try:
        st.write(dashboard_stock_list[['Stock Name', 'Industry Name', 'Occurrence Count']])
    except KeyError as e:
        st.write(f"KeyError: {e}. Check if the columns are correctly renamed.")
else:
    st.warning("No data available to display.")
