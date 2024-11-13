import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError  # Import EmptyDataError explicitly
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data

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

            # Calculate returns for each timeframe and apply color formatting
            returns = [row['1W_value'], row['1M_value'], row['3M_value'], row['6M_value'], row['1Y_value'], row['5Y_value']]
            colors = [get_color(value) for value in returns]
            
            st.markdown(
                f'<div style="margin:0; padding:0; border-radius:5px; display:flex; flex-direction:row; align-items:center;" class="no-space">' +
                f'<div style="flex:1; ; margin:0; padding:3px;">{tick}</div>' +
                f'<div style="flex:1; {colors[0]}; margin:0; padding:3px;">{row["1W_value"]}%</div>' +
                f'<div style="flex:1; {colors[1]}; margin:0; padding:3px;">{row["1M_value"]}%</div>' +
                f'<div style="flex:1; {colors[2]}; margin:0; padding:3px;">{row["3M_value"]}%</div>' +
                f'<div style="flex:1; {colors[3]}; margin:0; padding:3px;">{row["6M_value"]}%</div>' +
                f'<div style="flex:1; {colors[4]}; margin:0; padding:3px;">{row["1Y_value"]}%</div>' +
                f'<div style="flex:1; {colors[5]}; margin:0; padding:3px;">{row["5Y_value"]}%</div>' +
                '</div>', unsafe_allow_html=True
            )
    else:
        st.warning("No data available to display.")

# Function to load stock list from a file
def load_stock_data(file_path):
    try:
        stock_list_df = pd.read_csv(file_path)
        return stock_list_df
    except EmptyDataError:
        st.warning("The CSV file is empty.")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return pd.DataFrame()

# Function to create tabs and display data
def create_tabs(tab_titles, stock_list_df):
    tabs = st.tabs(list(tab_titles.values()))
    for i, title in enumerate(tab_titles.keys()):
        with tabs[i]:
            if not stock_list_df.empty:
                # Display the data filtered by the "Report" and the flag corresponding to each timeframe
                filtered_data = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df[str(title) + '_FLG'] == 'Y')]
                display_stock_data_from_df(filtered_data, key_prefix=f"Cherries{title.split()[0]}")
            else:
                st.write("No data available to display.")

# Main logic to read stock data and create tabs
stock_list = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

# Tab titles for each timeframe
tab_titles = {
    "5Y": "5 Year Breakout",
    "1Y": "1 Year Breakout",
    "6M": "6 Month Breakout",
    "3M": "3 Month Breakout",
    "1M": "1 Month Breakout"
    }

# Create and display tabs for stock data
create_tabs(tab_titles, stock_list_df)
