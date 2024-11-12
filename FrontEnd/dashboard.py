import streamlit as st
import pandas as pd
import yfinance as yf
from pandas.errors import EmptyDataError
import plotly.graph_objs as go

# Create sample data
def create_sample_data():
    data = {
        "Security Id": ["RELIANCE.BO", "TCS.BO", "INFY.BO", "HDFC.BO"],
        "Security Name": ["Reliance", "TCS", "Infosys", "HDFC"],
        "Sector Name": ["Energy", "IT", "IT", "Finance"],
        "Industry": ["Oil & Gas", "Software", "Software", "Banking"],
        "1M": [2.5, 1.8, -1.2, 2.1],
        "3M": [5.5, 3.4, -2.1, 4.3],
        "6M": [12.5, 8.2, -4.6, 10.7],
        "1Y": [25.6, 18.9, -8.3, 22.4],
        "5Y": [50.3, 37.8, -16.2, 47.1],
        "Report": ["C", "C", "C", "C"],
        "Break Out": ["5Y", "1Y", "6M", "3M"]
    }
    return pd.DataFrame(data)

# Using sample data for testing
stock_list_df = create_sample_data()

# Function to get the stock data
def get_stock_data(ticker, period="1y", interval="1d"):
    dates = pd.date_range(start="2020-01-01", periods=365)
    data = pd.DataFrame({
        'Date': dates,
        'Close': pd.Series(range(365)) + pd.np.random.randn(365).cumsum(),
        'Volume': pd.Series(range(1000, 1365)) + pd.np.random.randint(1, 10, size=365)
    })
    data.set_index('Date', inplace=True)
    return data

# Function to get color based on returns
def get_color(value):
    if value > 0:
        return f'background-color: rgba(0, 255, 0, {value / 100})'  # Green for positive returns
    elif value < 0:
        return f'background-color: rgba(255, 0, 0, {-value / 100})'  # Red for negative returns
    else:
        return 'background-color: white'  # White for no change

# Common function to display stock data
def display_stock_data_from_df(df, key_prefix=""):
    if not df.empty:
        for index, row in df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            sector = row['Sector Name']
            industry = row['Industry']
            
            returns = [row['1M'], row['3M'], row['6M'], row['1Y'], row['5Y']]
            colors = [get_color(value) for value in returns]
            
            st.markdown(
                f'<div style="padding:10px; margin:5px; border-radius:5px; display:flex; flex-direction:row; align-items:center;">' +
                f'<div style="flex:1; {colors[0]}; padding:10px;">{tick}</div>' +
                f'<div style="flex:1; {colors[1]}; padding:10px;">{row["1M"]}%</div>' +
                f'<div style="flex:1; {colors[2]}; padding:10px;">{row["3M"]}%</div>' +
                f'<div style="flex:1; {colors[3]}; padding:10px;">{row["6M"]}%</div>' +
                f'<div style="flex:1; {colors[4]}; padding:10px;">{row["1Y"]}%</div>' +
                f'<div style="flex:1; {colors[5]}; padding:10px;">{row["5Y"]}%</div>' +
                '</div>', unsafe_allow_html=True
            )

            show_plot = st.checkbox(f"More about {tick}", key=f"{key_prefix}-{tick}")

            if show_plot:
                cherries_stock = get_stock_data(ticker)
                if not cherries_stock.empty:
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=cherries_stock.index, y=cherries_stock['Close'], mode='lines', name='Close Price', yaxis='y', marker=dict(color='blue')))
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
                    
                    st.plotly_chart(fig)
                else:
                    st.error(f"No data found for {ticker}. Please check the ticker symbol or try again later.")
    else:
        st.warning("No data available to display.")

# Function to create tabs and display data
def create_tabs(tab_titles, stock_list_df):
    tabs = st.tabs(tab_titles)
    for i, title in enumerate(tab_titles):
        with tabs[i]:
            if not stock_list_df.empty:
                display_stock_data_from_df(stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df['Break Out'] == title.split()[0])].sort_values(by='1Y', ascending=True), key_prefix=f"Cherries{title.split()[0]}")
            else:
                st.write("No data available to display.")

# Create and display tabs
tab_titles = ["5 Year Breakout", "1 Year Breakout", "6 Month Breakout", "3 Month Breakout", "1 Month Breakout"]
create_tabs(tab_titles, stock_list_df)
