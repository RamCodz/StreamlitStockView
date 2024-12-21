import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Streamlit page layout
st.set_page_config(page_title="Stock Report Analysis", layout="wide")

# Title
st.title("Stock Data Analysis Dashboard")

# Read the stock data CSV
df = read_files(outbound_folder)
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filter by report type and create a pivot table
df_c = df[df['report_type'] == 'C']
df_g = df[df['report_type'] == 'G']

# Count stock occurrences by date for each stock
stock_counts_c = df_c.groupby(['date', 'stock_name']).size().unstack(fill_value=0)
stock_counts_g = df_g.groupby(['date', 'stock_name']).size().unstack(fill_value=0)

# Interactive widgets
stock_name = st.selectbox("Select Stock Name", stock_counts_c.columns)
report_type = st.selectbox("Select Report Type", ["C", "G"])
start_date = st.date_input("Select Start Date", df['date'].min())
end_date = st.date_input("Select End Date", df['date'].max())

# Filter data based on selected inputs
filtered_df = df[(df['report_type'] == report_type) & (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Display the filtered data table
st.write(f"Showing {len(filtered_df)} records between {start_date} and {end_date}")
st.dataframe(filtered_df)

# 1. Scatter Plot: Stock Occurrences vs Date
st.header("Scatter Plot: Stock Occurrences vs Date")
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot for each stock in report type C
for stock in stock_counts_c.columns:
    ax.scatter(stock_counts_c.index, stock_counts_c[stock], label=f"{stock} - Report C", alpha=0.6)

# Scatter plot for each stock in report type G
for stock in stock_counts_g.columns:
    ax.scatter(stock_counts_g.index, stock_counts_g[stock], label=f"{stock} - Report G", alpha=0.6)

ax.set_title("Scatter Plot: Stock Occurrences vs Date")
ax.set_xlabel("Date")
ax.set_ylabel("Occurrences")
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# 2. Rolling Average Line Plot
st.header("Rolling Average of Stock Occurrences Over Time")
rolling_window = 7  # 7-day rolling average for smoothing
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate and plot the rolling average for each stock in report type C
for stock in stock_counts_c.columns:
    ax.plot(stock_counts_c.index, stock_counts_c[stock].rolling(window=rolling_window).mean(), label=f"{stock} - Report C (7-day avg)")

# Calculate and plot the rolling average for each stock in report type G
for stock in stock_counts_g.columns:
    ax.plot(stock_counts_g.index, stock_counts_g[stock].rolling(window=rolling_window).mean(), label=f"{stock} - Report G (7-day avg)")

ax.set_title("Rolling Average of Stock Occurrences Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("7-Day Rolling Average of Occurrences")
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# Optional: Add further visualizations like a heatmap, bar charts, etc., based on your preference
