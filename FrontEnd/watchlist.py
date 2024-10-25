import streamlit as st
from pathlib import Path
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data

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
        ticker_df = pd.read_csv(stock_list_path)
        tickers = ticker_df['Security Code'].tolist()  # Assumes ticker names are in a column named 'Ticker'
    except Exception as e:
        st.error(f"Error reading the ticker data file: {e}")
        tickers = []  # Initialize as empty list
else:
    tickers = []

# Define a function to get percentage change over specific periods
def calculate_percentage_change(ticker):
    stock = yf.Ticker(f"{ticker}.BO")  # Use .BO suffix for BSE stocks
    data = stock.history(period="1y", interval="1d")  # Get 1-year data

    # Check if sufficient data exists
    if len(data) < 252:
        st.warning(f"Insufficient data for {ticker}")
        return {}

    changes = {}
    periods = {
        "1 Week": 5,
        "1 Month": 21,
        "3 Months": 63,
        "6 Months": 126,
        "1 Year": 252
    }

    for period_name, period_days in periods.items():
        if len(data) > period_days:
            changes[period_name] = ((data['Close'][-1] - data['Close'][-period_days]) / data['Close'][-period_days]) * 100
        else:
            changes[period_name] = None  # Not enough data for the period

    return changes

# Create a DataFrame to store percentage changes for each ticker
changes_data = {}
for ticker in tickers:
    changes_data[ticker] = calculate_percentage_change(ticker)

changes_df = pd.DataFrame(changes_data).transpose()

# Display heatmap
if not changes_df.empty:
    st.write("### Stock Price Change Heatmap (in %)")
    plt.figure(figsize=(10, 6))
    sns.heatmap(changes_df, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    st.pyplot(plt.gcf())
else:
    st.write("No data to display.")
