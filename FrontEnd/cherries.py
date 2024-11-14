import streamlit as st
import pandas as pd
import yfinance as yf
from pandas.errors import EmptyDataError
from BackEnd.Utils import globals
from FrontEnd.Utils import get_latest_report_data
import plotly.graph_objs as go

# Function to get the stock data
def get_stock_data(ticker, period="5y", interval="1d"):
    stock = yf.Ticker(str(ticker) + ".NS")  # Append .BO for BSE stocks
    return stock.history(period=period, interval=interval)
    
# Function to get color based on returns
def get_color(value):
    if value > 0:
        return f'background-color: rgba(0, 255, 0, {value / 100})'  # Green for positive returns
    elif value < 0:
        return f'background-color: rgba(255, 0, 0, {-value / 100})'  # Red for negative returns
    else:
        return 'background-color: white'  # White for no change

# Function to display detailed stock information
def display_stock_details(stock_data):
    st.subheader(f"Details for {stock_data['Security Name']}")

    # Assuming get_stock_data() is a function that returns a DataFrame for a given ticker
    cherries_stock = get_stock_data(stock_data['Security Id'])

    if not cherries_stock.empty:
        # Plotting the stock price and volume change over time using Plotly
        fig = go.Figure()

        # Add trace for Close Price
        fig.add_trace(
            go.Scatter(
                x=cherries_stock.index, 
                y=cherries_stock['Close'], 
                mode='lines', 
                name='Close Price',
                yaxis='y', 
                marker=dict(color='blue')
            )
        )

        # Add trace for Volume Change
        fig.add_trace(
            go.Bar(
                x=cherries_stock.index, 
                y=cherries_stock['Volume'], 
                name='Volume Change', 
                yaxis='y2',
                marker=dict(color='orange')
            )
        )

        # Update layout for the chart with two y-axes
        fig.update_layout(
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right'
            ),
            template="plotly_dark",  # Change template as needed for dark or light themes
            showlegend=True
        )

        # Create three columns to display additional information (e.g., PE and PB ratios)
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            st.write("PE : [Add PE value here]")
            st.write("PB : [Add PB value here]")
        with col2:
            st.write("PE : [Add PE value here]")
            st.write("PB : [Add PB value here]")
        with col3:
            st.write("PE : [Add PE value here]")
            st.write("PB : [Add PB value here]")

        # Display the plotly chart
        st.plotly_chart(fig)

    else:
        st.error(f"No data found for {stock_data['Security Id']}. Please check the ticker symbol or try again later.")

# Function to display stock data with checkboxes
def display_stock_data_from_df(df, key_prefix=""):
    """Display stock data from DataFrame with checkboxes and color-coded returns."""
    if not df.empty:
        # Adjust column widths for better layout
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.2, 3, 1, 1, 1, 1, 1, 1, 0.6])

        # Header row for the heatmap values (1W, 1M, 3M, 6M, 1Y, 5Y)
        with col1:
            st.write("")  # Empty space for the checkbox
        with col2:
            st.markdown("<b>Stock Name</b>", unsafe_allow_html=True)  # Bold header
        with col3:
            st.markdown("<b>1 Week</b>", unsafe_allow_html=True)  # Bold header
        with col4:
            st.markdown("<b>1 Month</b>", unsafe_allow_html=True)  # Bold header
        with col5:
            st.markdown("<b>3 Month</b>", unsafe_allow_html=True)  # Bold header
        with col6:
            st.markdown("<b>6 Month</b>", unsafe_allow_html=True)  # Bold header
        with col7:
            st.markdown("<b>1 Year</b>", unsafe_allow_html=True)  # Bold header
        with col8:
            st.markdown("<b>5 Year</b>", unsafe_allow_html=True)  # Bold header

        # Iterate through the rows and display stock names with checkboxes
        for index, row in df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']

            # Calculate returns for each timeframe and apply color formatting
            returns = [row['1W_value'], row['1M_value'], row['3M_value'], row['6M_value'], row['1Y_value'], row['5Y_value']]
            colors = [get_color(value) for value in returns]

            # Create columns for each part of the row (checkbox, stock name, and data columns)
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([0.2, 3, 1, 1, 1, 1, 1, 1, 0.6])

            with col1:
                show_details = st.checkbox('', key=f"{key_prefix}_{ticker}", label_visibility="hidden")
            with col2:
                st.write(tick)  # Stock Name            
            with col3:
                st.markdown(f'<div style="{colors[0]}">{row["1W_value"]}%</div>', unsafe_allow_html=True)            
            with col4:
                st.markdown(f'<div style="{colors[1]}">{row["1M_value"]}%</div>', unsafe_allow_html=True)
            with col5:
                st.markdown(f'<div style="{colors[2]}">{row["3M_value"]}%</div>', unsafe_allow_html=True)
            with col6:
                st.markdown(f'<div style="{colors[3]}">{row["6M_value"]}%</div>', unsafe_allow_html=True)
            with col7:
                st.markdown(f'<div style="{colors[4]}">{row["1Y_value"]}%</div>', unsafe_allow_html=True)
            with col8:
                st.markdown(f'<div style="{colors[5]}">{row["5Y_value"]}%</div>', unsafe_allow_html=True)

            # If checkbox is checked, display detailed information
            if show_details:
                display_stock_details(row)

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
                # Filter and display the data based on the "Report" and flag for each timeframe
                filtered_data = stock_list_df[(stock_list_df['Report'] == 'C') & (stock_list_df[str(title) + '_FLG'] == 'Y')]
                display_stock_data_from_df(filtered_data, key_prefix=f"Cherries{title.split()[0]}")
            else:
                st.write("No data available to display.")

# Main logic to read stock data and create tabs
stock_list_file = str(globals.data_filepath) + get_latest_report_data.get_latest_file(str(globals.data_filepath))

# Load stock data from CSV
try:
    stock_list_df = pd.read_csv(stock_list_file)
except EmptyDataError:
    stock_list_df = pd.DataFrame()
except Exception as e:
    st.error(f"Error reading the file: {e}")
    stock_list_df = pd.DataFrame()

tab_titles = {
    "5Y": "5 Year Breakout",
    "1Y": "1 Year Breakout",
    "6M": "6 Month Breakout",
    "3M": "3 Month Breakout",
    "1M": "1 Month Breakout"
}

create_tabs(tab_titles, stock_list_df)
