import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Sample data creation with returns and fundamental values
def create_sample_data():
    data = {
        "Security Id": ["RELIANCE.BO", "TCS.BO", "INFY.BO", "HDFC.BO"],
        "Security Name": ["Reliance", "TCS", "Infosys", "HDFC"],
        "Sector Name": ["Energy", "IT", "IT", "Finance"],
        "Industry": ["Oil & Gas", "Software", "Software", "Banking"],
        "Variation": [5, 3, -2, 4],
        "1M": [2.5, 1.8, -1.2, 2.1],
        "3M": [5.5, 3.4, -2.1, 4.3],
        "6M": [12.5, 8.2, -4.6, 10.7],
        "1Y": [25.6, 18.9, -8.3, 22.4],
        "5Y": [50.3, 37.8, -16.2, 47.1],
        "PE": [30.4, 32.1, 28.2, 29.5],
        "PB": [3.5, 6.2, 5.4, 4.8],
        "PS": [2.2, 5.1, 4.3, 3.9],
        "PEG": [1.5, 1.8, 1.7, 1.4]
    }
    return pd.DataFrame(data)

# Using sample data for testing
stock_list_df = create_sample_data()

# Create heatmap
def create_heatmap(returns_df):
    fig = px.imshow(
        returns_df[["Security Name", "1M", "3M", "6M", "1Y", "5Y"]].set_index('Security Name'),
        labels=dict(x="Period", y="Stock", color="Return (%)"),
        x=["1M", "3M", "6M", "1Y", "5Y"],
        y=returns_df['Security Name'],
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(title="Stock Returns Heatmap")
    st.plotly_chart(fig)

create_heatmap(stock_list_df)

# Mock data for the stock price and volume change
def get_mock_stock_data(ticker):
    dates = pd.date_range(start="2020-01-01", periods=100)
    return pd.DataFrame({
        "Date": dates,
        "Close": pd.Series(range(100)) + pd.np.random.randn(100).cumsum(),
        "Volume": pd.Series(range(1000, 1100)) + pd.np.random.randint(1, 10, size=100)
    }).set_index("Date")

# Display detailed information for a selected stock
def display_stock_details(stock_list_df, stock_name):
    stock_data = stock_list_df[stock_list_df['Security Name'] == stock_name].iloc[0]
    st.write(f"### {stock_data['Security Name']}")
    st.write(f"**Sector:** {stock_data['Sector Name']}")
    st.write(f"**Industry:** {stock_data['Industry']}")
    st.write(f"**PE Ratio:** {stock_data['PE']}")
    st.write(f"**PB Ratio:** {stock_data['PB']}")
    st.write(f"**PS Ratio:** {stock_data['PS']}")
    st.write(f"**PEG Ratio:** {stock_data['PEG']}")

    stock_price_data = get_mock_stock_data(stock_data['Security Id'])
    if not stock_price_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_price_data.index, y=stock_price_data['Close'], mode='lines', name='Close Price', yaxis='y', marker=dict(color='blue')))
        fig.add_trace(go.Bar(x=stock_price_data.index, y=stock_price_data['Volume'], name='Volume Change', yaxis='y2', marker=dict(color='orange')))
        fig.update_layout(
            yaxis2=dict(title='Volume', overlaying='y', side='right'),
            template="plotly_dark",
            showlegend=True
        )
        st.plotly_chart(fig)

# Function to create tabs and display data
def create_tabs(stock_list_df):
    stock_names = stock_list_df['Security Name'].unique()
    for stock_name in stock_names:
        if st.button(stock_name):
            display_stock_details(stock_list_df, stock_name)

# Create and display tabs
create_tabs(stock_list_df)
