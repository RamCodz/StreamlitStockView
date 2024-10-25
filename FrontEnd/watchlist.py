import streamlit as st
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
from BackEnd.Utils.fetch_all_ticker_data import get_all_data

# Define a function to get the latest ticker file path
def get_stock_list_filepath(base_path):
    latest_file = get_latest_report_data.get_latest_file(base_path)
    if latest_file:
        return Path(base_path) / latest_file
    else:
        st.error("No stock data files found.")
        return None

# Load ticker list data
stock_list_path = get_stock_list_filepath(str(globals.data_filepath))
if stock_list_path and stock_list_path.exists():
    try:
        tickers = pd.read_csv(stock_list_path)
    except Exception as e:
        st.error(f"Error reading the ticker data file: {e}")
        tickers = []  # Initialize as empty list
else:
    tickers = []

# Define a function to get percentage change over specific periods
def calculate_percentage_change(ticker_data):
    changes = {}
    periods = {
        "1 Week": 5,
        "1 Month": 21,
        "3 Months": 63,
        "6 Months": 126,
        "1 Year": 252
    }
    end_date = ticker_data['Date'].max()  # Get the latest date in data

    for period_name, period_days in periods.items():
        start_date = end_date - timedelta(days=period_days)
        date_data = ticker_data[(ticker_data['Date'] >= start_date) & (ticker_data['Date'] <= end_date)]

        if len(date_data) > 0:
            try:
                # Calculate the percentage change over the specified period
                pct_change = ((date_data['Close'].iloc[-1] - date_data['Close'].iloc[0]) / date_data['Close'].iloc[0]) * 100
                changes[period_name] = pct_change
            except IndexError:
                changes[period_name] = None  # Not enough data for the period
        else:
            changes[period_name] = None  # No data for the period

    return changes

# Fetch and process data for each ticker
all_data = get_all_data(tickers)  # Assuming this function fetches data for all tickers at once
all_data['Date'] = pd.to_datetime(all_data['Date'])  # Ensure Date is in datetime format
st.write(all_data)
# Create a DataFrame to store percentage changes for each ticker
changes_data = {}
for ticker in tickers:
    ticker_data = all_data[all_data['Ticker'] == ticker]  # Filter data for each ticker
    changes_data[ticker] = calculate_percentage_change(ticker_data)
st.write(changes_data)
# Convert the dictionary to a DataFrame
changes_df = pd.DataFrame(changes_data).transpose()

# Display heatmap
if not changes_df.empty:
    st.write("### Stock Price Change Heatmap (in %)")
    plt.figure(figsize=(10, 6))
    sns.heatmap(changes_df, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    st.pyplot(plt.gcf())
else:
    st.write("No data to display.")
