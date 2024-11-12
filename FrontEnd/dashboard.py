import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
from pandas.errors import EmptyDataError

# Sample data creation
def create_sample_data():
    data = {
        "Security Id": ["RELIANCE.BO", "TCS.BO", "INFY.BO", "HDFC.BO"],
        "Security Name": ["Reliance", "TCS", "Infosys", "HDFC"],
        "Sector Name": ["Energy", "IT", "IT", "Finance"],
        "Industry": ["Oil & Gas", "Software", "Software", "Banking"],
        "Variation": [5, 3, -2, 4],
        "Report": ["C", "C", "C", "C"],
        "Break Out": ["5Y", "1Y", "6M", "3M"]
    }
    return pd.DataFrame(data)

# Using sample data for testing
stock_list_df = create_sample_data()

# Function to get the stock data
def get_stock_data(ticker, period="5y", interval="1d"):
    # Create mock data instead of fetching from yfinance for testing purposes
    dates = pd.date_range(start="2020-01-01", periods=100)
    data = {
        "Date": dates,
        "Close": pd.Series(range(100)) + pd.np.random.randn(100).cumsum(),
        "Volume": pd.Series(range(1000, 1100)) + pd.np.random.randint(1, 10, size=100)
    }
    return pd.DataFrame(data).set_index("Date")

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

# Function to display stock data
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
