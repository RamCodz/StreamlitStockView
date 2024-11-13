import streamlit as st
from pathlib import Path
import pandas as pd
import yfinance as yf
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
import plotly.graph_objs as go

# Read stock data from latest file
stock_list = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

# Define a checklist for applying HTML for styling 
checklist = ['Item 1', 'Item 2', 'Item 3']
for item in checklist: 
    st.markdown(f'<input type="checkbox"> {item}', unsafe_allow_html=True)

try:
    stock_list_df = pd.read_csv(stock_list)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

# Function to get the stock data
def get_stock_data(ticker, period="1y", interval="1d"):
    stock = yf.Ticker(ticker + ".BO")  # Append .BO for BSE stocks
    return stock.history(period=period, interval=interval)

# Common function to display stock data
def display_stock_data_from_df(df, key_prefix=""):
    if not df.empty:
        for index, row in df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            sector = row['Sector Name']
            industry = row['Industry']
            variation = round(row['Variation'])

            # Create a checkbox to toggle plot display
            show_plot = st.checkbox(f"**{tick}** >>> ***{variation}%*** - {sector} - {industry}", key=f"{key_prefix}-{tick}")

            if show_plot:
                cherries_stock = get_stock_data(ticker)
                if not cherries_stock.empty:
                    # Plotting the stock price and volume change over time using Plotly
                    fig = go.Figure()

                    # Add trace for Close Price
                    fig.add_trace(go.Scatter(x=cherries_stock.index, y=cherries_stock['Close'], mode='lines', name='Close Price', yaxis='y', marker=dict(color='blue')))

                    # Add trace for Volume Change
                    fig.add_trace(go.Bar(x=cherries_stock.index, y=cherries_stock['Volume'], name='Volume Change', yaxis='y2', marker=dict(color='orange')))

                    fig.update_layout(
                        yaxis2=dict(
                            title='Volume',
                            overlaying='y',
                            side='right'
                        ),
                        template="plotly_dark",
                        showlegend=True
                    )
                    
                    col1, col2, col3 = st.columns(3, gap="small")
                    with col1:
                        st.write("PE : ")
                        st.write("PB : ")
                    with col2:
                        st.write("PE : ")
                        st.write("PB : ")
                    with col3:
                        st.write("PE : ")
                        st.write("PB : ")
                    
                    st.plotly_chart(fig)
                else:
                    st.error(f"No data found for {ticker}. Please check the ticker symbol or try again later.")
    else:
        st.warning("No data available to display.")

# Function to create tabs and display data
def create_tabs(tab_titles, stock_list_df):
    tabs = st.tabs(list(tab_titles.values()))
    for i, title in enumerate(tab_titles.keys()):
        with tabs[i]:
            if not stock_list_df.empty:
                display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df[title + '_FLG'] == 'Y')], key_prefix=f"Cherries{title.split()[0]}")
            else:
                st.write("No data available to display.")

# Create and display tabs
tab_titles = {"5Y":"5 Year Breakout", "1Y":"1 Year Breakout", "6M":"6 Month Breakout", "3M":"3 Month Breakout", "1M":"1 Month Breakout"}
create_tabs(tab_titles, stock_list_df)
