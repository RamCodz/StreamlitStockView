import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data

# Read stock data from latest file
stock_list = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

try:
    stock_list_df = pd.read_csv(stock_list)
except EmptyDataError:
    st.warning("The file is empty. Please check the file or upload a valid data file.")
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

# Function to get the stock data
def get_stock_data(ticker, period="5y", interval="1d"):
    stock = yf.Ticker(ticker + ".BO")  # Append .BO for BSE stocks
    return stock.history(period=period, interval=interval)

# Calculate returns for each stock over specified periods
def calculate_returns(stock_list_df):
    periods = {"3M": "3mo", "6M": "6mo", "1Y": "1y", "5Y": "5y"}
    returns_df = pd.DataFrame(columns=["Stock", "3M", "6M", "1Y", "5Y"])
    
    for index, row in stock_list_df.iterrows():
        ticker = row['Security Id']
        stock_data = get_stock_data(ticker)
        
        if not stock_data.empty:
            returns = {}
            returns['Stock'] = row['Security Name']
            for period_name, period in periods.items():
                period_data = get_stock_data(ticker, period=period)
                if not period_data.empty:
                    start_price = period_data['Close'].iloc[0]
                    end_price = period_data['Close'].iloc[-1]
                    returns[period_name] = ((end_price - start_price) / start_price) * 100
                else:
                    returns[period_name] = None
            returns_df = returns_df.append(returns, ignore_index=True)
    return returns_df

# Create heatmap
def create_heatmap(returns_df):
    fig = px.imshow(
        returns_df.set_index('Stock').T,
        labels=dict(x="Stock", y="Period", color="Return (%)"),
        x=returns_df['Stock'],
        y=["3M", "6M", "1Y", "5Y"],
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(title="Stock Returns Heatmap")
    st.plotly_chart(fig)

returns_df = calculate_returns(stock_list_df)
create_heatmap(returns_df)

# Function to create tabs and display data
def create_tabs(tab_titles, stock_list_df):
    tabs = st.tabs(tab_titles)
    for i, title in enumerate(tab_titles):
        with tabs[i]:
            if not stock_list_df.empty:
                display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == title.split()[0])].sort_values(by='Variation', ascending=True), key_prefix=f"Cherries{title.split()[0]}")
            else:
                st.write("No data available to display.")

# Create and display tabs
tab_titles = ["5 Year Breakout", "1 Year Breakout", "6 Month Breakout", "3 Month Breakout", "1 Month Breakout"]
create_tabs(tab_titles, stock_list_df)
