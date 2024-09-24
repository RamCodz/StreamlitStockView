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
            show_plot = st.checkbox(f"**{tick}** - {variation} - {sector} - {industry}", key=f"{key_prefix}-{tick}")

            if show_plot:
                cherries_stock = get_stock_data(ticker)
                if not cherries_stock.empty:
                    # Add your details to be displayed when a stock is selected

                    # Plotting the stock price and volume change over time using Plotly
                    fig = go.Figure()

                    # Add trace for Close Price
                    fig.add_trace(
                        go.Scatter(x=cherries_stock.index, y=cherries_stock['Close'], mode='lines', name='Close Price',
                                   yaxis='y', marker=dict(color='blue'))
                    )

                    # Add trace for Volume Change
                    fig.add_trace(
                        go.Bar(x=cherries_stock.index, y=cherries_stock['Volume'], name='Volume Change', yaxis='y2',
                               marker=dict(color='orange'))
                    )

                    fig.update_layout(
                        yaxis2=dict(
                            title='Volume',
                            overlaying='y',
                            side='right'
                        ),
                        template="plotly_dark",  # Change template as needed for dark or light themes
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


Cherry_tabs = st.tabs(["5 Year Breakout", "1 Year Breakout", "6 Month Breakout", "3 Month Breakout", "1 Month Breakout"])
with Cherry_tabs[0]:
    display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '5Y')].sort_values(by='Variation',ascending=False), key_prefix="Cherries5Y")
with Cherry_tabs[1]:
    display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1Y')].sort_values(by='Variation',ascending=False), key_prefix="Cherries1Y")
with Cherry_tabs[2]:
    display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '6M')].sort_values(by='Variation',ascending=False), key_prefix="Cherries6M")
with Cherry_tabs[3]:
    display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '3M')].sort_values(by='Variation',ascending=False), key_prefix="Cherries3M")
with Cherry_tabs[4]:
    display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == '1M')].sort_values(by='Variation',ascending=False), key_prefix="Cherries1M")
