import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from pathlib import Path


# Function to get the stock data
def get_stock_data(ticker, period="1y", interval="1d"):
    stock = yf.Ticker(ticker + ".BO")  # Append .BO for BSE stocks
    return stock.history(period=period, interval=interval)


# Custom CSS for styling
custom_css = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f2f6; /* Light gray background */
}

.streamlit-tabs > .streamlit-tabsContainer {
    width: 100%; /* Full width of tabs */
    height: 200px !important; /* Adjust height of tabs */
    margin-bottom: 2rem; /* Adding margin at the bottom */
}

.stButton {
    background-color: #4CAF50; /* Green button color */
    color: white; /* White button text color */
    padding: 0.5rem 1rem; /* Padding inside button */
    border: none; /* No border */
    text-align: center; /* Centered text */
    text-decoration: none; /* No underline */
    display: inline-block; /* Inline block display */
    font-size: 1rem; /* Button font size */
    cursor: pointer; /* Pointer cursor on hover */
    border-radius: 0.25rem; /* Rounded corners */
}

.stButton:hover {
    background-color: #45a049; /* Darker green on hover */
}

.logo-container {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1;
}

.logo {
    height: 50px;
    width: auto;
}
</style>
"""

# Streamlit app configuration
st.set_page_config(layout="wide")

# Injecting custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Read stock data from file
file_path = Path(__file__).parent / 'data/Bse_Equity.csv'
logo_path = Path(__file__).parent / "data/logo.png"

try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error reading the file: {e}")
    df = pd.DataFrame()

# Stock filtering for Early Cherries
cherries_df = df

# Stock filtering for Fallen Gems
gems_d = df

# Logo
st.image(str(logo_path), width=100, use_column_width=False)

# Create tabs for "Early Cherries" and "Fallen Gems"
tabs = st.tabs(["Early Cherries", "Fallen Gems"])

# Early Cherries tab
with tabs[0]:
    if not cherries_df.empty:
        for index, row in cherries_df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            sector = row['Sector Name']
            industry = row['Industry']

            # Create a checkbox to toggle plot display
            show_plot = st.checkbox(f"**{tick}** - {sector} - {industry}",  key="Cherries-"+tick)

            if show_plot:
                cherries_stock = get_stock_data(ticker)
                if not cherries_stock.empty:

                    ### Add your details to be displayed when a stck is selected

                    # Plotting the stock price and volume change over time using Plotly
                    fig = go.Figure()

                    # Add trace for Close Price
                    fig.add_trace(
                        go.Scatter(x=cherries_stock.index, y=cherries_stock['Close'], mode='lines', name='Close Price',
                                   yaxis='y', marker=dict(color='blue')))

                    # Add trace for Volume Change
                    fig.add_trace(
                        go.Bar(x=cherries_stock.index, y=cherries_stock['Volume'], name='Volume Change', yaxis='y2',
                               marker=dict(color='orange')))

                    fig.update_layout(
                        yaxis2=dict(
                            title='Volume',
                            overlaying='y',
                            side='right'
                        ),
                        template="plotly_dark",  # Change template as needed for dark or light themes
                        showlegend=True
                    )

                    st.plotly_chart(fig)
                else:
                    st.error(f"No data found for {ticker}. Please check the ticker symbol or try again later.")
    else:
        st.warning("No data available to display.")

# Fallen Gems tab
with tabs[1]:
    if not cherries_df.empty:
        for index, row in cherries_df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            sector = row['Sector Name']
            industry = row['Industry']

            # Create a checkbox to toggle plot display
            show_plot = st.checkbox(f"**{tick}** - {sector} - {industry}", key="Gems-"+tick)

            if show_plot:
                cherries_stock = get_stock_data(ticker)
                if not cherries_stock.empty:

                    ### Add your details to be displayed when a stck is selected

                    # Plotting the stock price and volume change over time using Plotly
                    fig = go.Figure()

                    # Add trace for Close Price
                    fig.add_trace(
                        go.Scatter(x=cherries_stock.index, y=cherries_stock['Close'], mode='lines', name='Close Price',
                                   yaxis='y', marker=dict(color='blue')))

                    # Add trace for Volume Change
                    fig.add_trace(
                        go.Bar(x=cherries_stock.index, y=cherries_stock['Volume'], name='Volume Change', yaxis='y2',
                               marker=dict(color='orange')))

                    fig.update_layout(
                        yaxis2=dict(
                            title='Volume',
                            overlaying='y',
                            side='right'
                        ),
                        template="plotly_dark",  # Change template as needed for dark or light themes
                        showlegend=True
                    )

                    st.plotly_chart(fig)
                else:
                    st.error(f"No data found for {ticker}. Please check the ticker symbol or try again later.")
    else:
        st.warning("No data available to display.")
