import pandas as pd
import os
from datetime import datetime

# Define the folder where your outbound files are stored
outbound_folder = "path/to/Outbound"

# Function to read all the CSV files in the outbound folder
def read_files(folder):
    all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.csv')]
    data = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
    return data

# Read the data from all files
df = read_files(outbound_folder)

# Convert the date column to datetime (if it exists in your dataset)
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filter the data by report type ('C' and 'G')
df_c = df[df['report_type'] == 'C']
df_g = df[df['report_type'] == 'G']

# Count occurrences of each stock for both report types
stock_counts_c = df_c['stock_name'].value_counts()
stock_counts_g = df_g['stock_name'].value_counts()

# Combine the counts into one DataFrame
stock_counts = pd.DataFrame({
    'count_C': stock_counts_c,
    'count_G': stock_counts_g
}).fillna(0)

# Function to check if stock appeared continuously for 10 days
def find_continuous_stocks(df, threshold=10):
    continuous_stocks = []
    for stock in df['stock_name'].unique():
        stock_data = df[df['stock_name'] == stock].sort_values('date')
        consecutive_days = 0
        for i in range(1, len(stock_data)):
            if (stock_data['date'].iloc[i] - stock_data['date'].iloc[i-1]).days == 1:
                consecutive_days += 1
            else:
                consecutive_days = 0
            if consecutive_days >= threshold - 1:  # 10 days threshold
                continuous_stocks.append(stock)
                break
    return continuous_stocks

# Find stocks with continuous appearances for 10 days in each report type
continuous_c = find_continuous_stocks(df_c)
continuous_g = find_continuous_stocks(df_g)

# Combine the continuous stocks results
continuous_stocks = list(set(continuous_c + continuous_g))

# Display the results
print("Stock Counts by Report Type:")
print(stock_counts)
print(f"\nStocks with continuous appearances for 10 days: {continuous_stocks}")
