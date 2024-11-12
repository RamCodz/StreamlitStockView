import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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
        "5Y": [50.3, 37.8, -16.2, 47.1]
    }
    return pd.DataFrame(data)

# Using sample data for testing
stock_list_df = create_sample_data()

# Customize AgGrid
def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(df)
    options.configure_default_column(editable=True)
    options.configure_selection('single')
    
    # You can customize further features of AgGrid here

    grid_options = options.build()
    grid_response = AgGrid(
        df, 
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=350,
        reload_data=True
    )
    
    return grid_response

# Display the table
st.write("Interactive Stock Data Table:")
response = aggrid_interactive_table(stock_list_df)

# Retrieve and display the selected row
if response['selected_rows']:
    selected_row = response['selected_rows'][0]
    st.write("You selected:")
    st.json(selected_row)

    ticker = selected_row['Security Id']
    st.write(f"**Details for {ticker}:**")
    st.write(f"**Sector:** {selected_row['Sector Name']}")
    st.write(f"**Industry:** {selected_row['Industry']}")

    # Fetch the stock data (simulated in this case)
    def get_stock_data(ticker, period="1y", interval="1d"):
        dates = pd.date_range(start="2020-01-01", periods=365)
        data = pd.DataFrame({
            'Date': dates,
            'Close': pd.Series(range(365)) + pd.np.random.randn(365).cumsum(),
            'Volume': pd.Series(range(1000, 1365)) + pd.np.random.randint(1, 10, size=365)
        })
        data.set_index('Date', inplace=True)
        return data

    stock_data = get_stock_data(ticker)
    
    # Plot the Close price of the stock using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=f'Close Price - {ticker}'))
    fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name=f'Volume - {ticker}'))
    fig.update_layout(title=f"{ticker} Price and Volume over Time", template="plotly_dark")
    
    # Display the plot
    st.plotly_chart(fig)
else:
    st.warning("No row selected.")
