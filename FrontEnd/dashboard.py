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
        st.markdown(
            """
            <style>
            .no-space div[data-testid="stMarkdownContainer"] {
                margin-top: 0;
                margin-bottom: 0;
                padding: 0;
            }
            </style>
            """, unsafe_allow_html=True
        )
        for index, row in df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            
            # Create a checkbox to toggle plot display
            show_plot = st.checkbox(f"**{tick}** >>> ***{ticker}%***", key=f"{key_prefix}-{tick}")
            
            for check in show_plot:
                styled_checkbox("**Bold Item**")
                
            returns = [row['1M'], row['3M'], row['6M'], row['1Y'], row['5Y']]
            colors = [get_color(value) for value in returns]
            
            st.markdown(
                f'<div style="margin:0; padding:0; border-radius:5px; display:flex; flex-direction:row; align-items:center;" class="no-space">' +
                f'<div style="flex:1; {colors[0]}; margin:0; padding:10px;">{tick}</div>' +
                f'<div style="flex:1; {colors[0]}; margin:0; padding:10px;">{row["1M"]}%</div>' +
                f'<div style="flex:1; {colors[1]}; margin:0; padding:10px;">{row["3M"]}%</div>' +
                f'<div style="flex:1; {colors[2]}; margin:0; padding:10px;">{row["6M"]}%</div>' +
                f'<div style="flex:1; {colors[3]}; margin:0; padding:10px;">{row["1Y"]}%</div>' +
                f'<div style="flex:1; {colors[4]}; margin:0; padding:10px;">{row["5Y"]}%</div>' +
                '</div>', unsafe_allow_html=True
            )
    else:
        st.warning("No data available to display.")

# Function to create a styled checkbox
def styled_checkbox(label, checked=False):
    checkbox_id = label.lower().replace(" ", "-")
    html = f"""
    <style>
    .{checkbox_id} {{
        display: inline-block;
        vertical-align: middle;
        margin-right: 10px;
    }}
    </style>
    <input type="checkbox" class="{checkbox_id}" {'checked' if checked else ''}>
    <label for="{checkbox_id}">{label}</label>
    """
    return st.markdown(html, unsafe_allow_html=True)

# Create and display data
display_stock_data_from_df(stock_list_df)
