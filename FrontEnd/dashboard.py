import streamlit as st
import pandas as pd
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

# Display detailed information for a selected stock
def display_stock_details(stock_data):
    ticker = stock_data['Security Id']
    tick = stock_data['Security Name']
    sector = stock_data['Sector Name']
    industry = stock_data['Industry']
    returns = [stock_data['1M'], stock_data['3M'], stock_data['6M'], stock_data['1Y'], stock_data['5Y']]

    st.write(f"### {tick}")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Industry:** {industry}")

    st.write("#### Returns")
    for period, value in zip(["1M", "3M", "6M", "1Y", "5Y"], returns):
        st.write(f"{period}: {value}%")

    stock_price_data = get_stock_data(ticker)
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

# Display stock data in rows
def display_stock_data_from_df(df):
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
            tick = row['Security Name']
            sector = row['Sector Name']
            industry = row['Industry']
            returns = [row['1M'], row['3M'], row['6M'], row['1Y'], row['5Y']]
            colors = [get_color(value) for value in returns]

            with st.expander(f"{tick} >>> {row['1Y']}% - {sector} - {industry}"):
                st.markdown(
                    f'<div style="margin:0; padding:0; border-radius:5px; display:flex; flex-direction:row; align-items:center;" class="no-space">' +
                    f'<div style="flex:1; {colors[0]}; margin:0; padding:10px;">1M: {row["1M"]}%</div>' +
                    f'<div style="flex:1; {colors[1]}; margin:0; padding:10px;">3M: {row["3M"]}%</div>' +
                    f'<div style="flex:1; {colors[2]}; margin:0; padding:10px;">6M: {row["6M"]}%</div>' +
                    f'<div style="flex:1; {colors[3]}; margin:0; padding:10px;">1Y: {row["1Y"]}%</div>' +
                    f'<div style="flex:1; {colors[4]}; margin:0; padding:10px;">5Y: {row["5Y"]}%</div>' +
                    '</div>', unsafe_allow_html=True
                )
                display_stock_details(row)

# Create and display data
display_stock_data_from_df(stock_list_df)
