import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data creation with returns
def create_sample_data():
    data = {
        "Security Id": ["RELIANCE.BO", "TCS.BO", "INFY.BO", "HDFC.BO"],
        "Security Name": ["Reliance", "TCS", "Infosys", "HDFC"],
        "Sector Name": ["Energy", "IT", "IT", "Finance"],
        "Industry": ["Oil & Gas", "Software", "Software", "Banking"],
        "Variation": [5, 3, -2, 4],
        "Report": ["C", "C", "C", "C"],
        "Break Out": ["5Y", "1Y", "6M", "3M"],
        "1M": [2.5, 1.8, -1.2, 2.1],
        "3M": [5.5, 3.4, -2.1, 4.3],
        "6M": [12.5, 8.2, -4.6, 10.7],
        "1Y": [25.6, 18.9, -8.3, 22.4],
        "5Y": [50.3, 37.8, -16.2, 47.1]
    }
    return pd.DataFrame(data)

# Using sample data for testing
stock_list_df = create_sample_data()

# Create heatmap
def create_heatmap(returns_df):
    fig = px.imshow(
        returns_df[["Security Name", "1M", "3M", "6M", "1Y", "5Y"]].set_index('Security Name').T,
        labels=dict(x="Stock", y="Period", color="Return (%)"),
        x=returns_df['Security Name'],
        y=["1M", "3M", "6M", "1Y", "5Y"],
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(title="Stock Returns Heatmap")
    st.plotly_chart(fig)

create_heatmap(stock_list_df)

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
                # Mock data for the stock price and volume change
                dates = pd.date_range(start="2020-01-01", periods=100)
                stock_data = pd.DataFrame({
                    "Date": dates,
                    "Close": pd.Series(range(100)) + pd.np.random.randn(100).cumsum(),
                    "Volume": pd.Series(range(1000, 1100)) + pd.np.random.randint(1, 10, size=100)
                }).set_index("Date")
                
                if not stock_data.empty:
                    # Plotting the stock price and volume change over time using Plotly
                    fig = go.Figure()

                    # Add trace for Close Price
                    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price', yaxis='y', marker=dict(color='blue')))

                    # Add trace for Volume Change
                    fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Volume Change', yaxis='y2', marker=dict(color='orange')))

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
