import pandas as pd
import numpy as np
import streamlit as st
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

# Function to get the stock data (simulated data for now)
def get_stock_data(ticker, period="1y", interval="1d"):
    dates = pd.date_range(start="2020-01-01", periods=365)
    data = pd.DataFrame({
        'Date': dates,
        'Close': np.random.randn(365).cumsum() + 1000,  # Simulated close price
        'Volume': np.random.randint(1, 10, size=365) * 1000  # Simulated volume
    })
    data.set_index('Date', inplace=True)
    return data

# Function to get color based on returns
def get_color(value):
    if value > 0:
        return 'background-color: rgba(0, 255, 0, 0.5)'  # Green for positive returns
    elif value < 0:
        return 'background-color: rgba(255, 0, 0, 0.5)'  # Red for negative returns
    else:
        return 'background-color: rgba(255, 255, 255, 0.5)'  # White for no change

# Common function to display stock data with clickable rows
def display_stock_data_from_df(df):
    if not df.empty:
        # Displaying a header row
        st.markdown(
            '<div style="display: flex; font-weight: bold; padding: 5px; background-color: #f4f4f4;">' +
            '<div style="flex:1; padding:5px;">Stock</div>' +
            '<div style="flex:1; padding:5px;">1M</div>' +
            '<div style="flex:1; padding:5px;">3M</div>' +
            '<div style="flex:1; padding:5px;">6M</div>' +
            '<div style="flex:1; padding:5px;">1Y</div>' +
            '<div style="flex:1; padding:5px;">5Y</div>' +
            '</div>', unsafe_allow_html=True
        )
        
        for index, row in df.iterrows():
            ticker = row['Security Id']
            tick = row['Security Name']
            
            # Get color based on return values
            returns = [row['1M'], row['3M'], row['6M'], row['1Y'], row['5Y']]
            colors = [get_color(value) for value in returns]
            
            # Create an interactive row with a clickable link
            row_html = (
                f'<div style="display: flex; flex-direction: row; align-items: center; padding: 5px; cursor: pointer; {colors[0]}">'
                f'<a href="javascript:void(0)" onclick="window.parent.postMessage({{"ticker": "{ticker}"}})">'  # Make the row clickable
                f'<div style="flex:1; padding:10px;">{tick}</div>'
                f'<div style="flex:1; padding:10px;">{row["1M"]}%</div>'
                f'<div style="flex:1; padding:10px;">{row["3M"]}%</div>'
                f'<div style="flex:1; padding:10px;">{row["6M"]}%</div>'
                f'<div style="flex:1; padding:10px;">{row["1Y"]}%</div>'
                f'<div style="flex:1; padding:10px;">{row["5Y"]}%</div>'
                '</a></div>'
            )

            st.markdown(row_html, unsafe_allow_html=True)

            # Listen for a click (simulated in Streamlit)
            if 'ticker' in st.session_state and st.session_state['ticker'] == ticker:
                st.write(f"**Details for {tick}:**")
                st.write(f"**Sector:** {row['Sector Name']}")
                st.write(f"**Industry:** {row['Industry']}")

                # Fetch the stock data (simulated in this case)
                stock_data = get_stock_data(ticker)
                
                # Plot the Close price of the stock using Plotly
                fig = go.Figure()

                # Add trace for Close Price
                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=f'Close Price - {tick}'))

                # Add trace for Volume
                fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name=f'Volume - {tick}'))

                fig.update_layout(title=f"{tick} Price and Volume over Time", template="plotly_dark")

                # Display the plot
                st.plotly_chart(fig)
    
    else:
        st.warning("No data available to display.")

# Main app logic
stock_list_df = create_sample_data()

# Check if data exists
if stock_list_df.empty:
    st.error("The stock data is empty. Please check the data source.")
else:
    # Show the raw DataFrame to ensure it is not empty
    st.write("Stock Data (Raw DataFrame):")
    st.write(stock_list_df)

# Create and display the stock table with clickable rows
    display_stock_data_from_df(stock_list_df)
