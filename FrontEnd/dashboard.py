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

# Count stock occurrences by date for each report type
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

# 1. Line Chart: Stock Occurrences Over Time
st.header("Stock Occurrences Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(stock_counts_c.index, stock_counts_c[stock_name], label="Report Type C", color='blue')
ax.plot(stock_counts_g.index, stock_counts_g[stock_name], label="Report Type G", color='orange')
ax.set_title(f"Occurrences of {stock_name} Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Occurrences")
ax.legend()
st.pyplot(fig)

# 2. Heatmap: Stock Appearances Over Time
st.header("Heatmap of Stock Appearances")
heatmap_data = df.groupby(['date', 'stock_name']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data.T, cmap='Blues', cbar_kws={'label': 'Occurrences'}, ax=ax)
plt.title("Heatmap of Stock Appearances Over Time")
st.pyplot(fig)

# 3. Bar Chart: Stock Occurrences by Report Type
st.header("Stock Occurrences by Report Type")
stock_counts_df = stock_counts_c.reset_index().melt(id_vars=['date'], var_name='Stock Name', value_name='Occurrences')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='date', y='Occurrences', hue='Stock Name', data=stock_counts_df, ax=ax)
plt.title("Stock Occurrences by Report Type C")
plt.xlabel("Date")
plt.ylabel("Occurrences")
st.pyplot(fig)

# Display the continuous stocks (appearing 10 days in a row)
st.header("Stocks Appearing Continuously for 10 Days")
st.write(f"Stocks that appeared continuously for 10 days (in either report type): {continuous_stocks}")
