import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf  # Library to pull stock data

# Define the stocks you want to analyze
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Example stock tickers

# Define time periods for analysis
time_frames = {
    '1 Week': 5,   # 5 trading days
    '1 Month': 21, # Approx 21 trading days
    '3 Months': 63, # Approx 63 trading days
    '6 Months': 126, # Approx 126 trading days
    '1 Year': 252   # Approx 252 trading days
}

# Create an empty DataFrame to store percentage losses
percentage_loss = pd.DataFrame(index=stocks, columns=time_frames.keys())

# Fetch data and calculate percentage losses
for stock in stocks:
    data = yf.download(stock, period='1y')['Adj Close']
    
    for period, days in time_frames.items():
        try:
            recent_price = data.iloc[-1]  # Most recent closing price
            past_price = data.iloc[-days]  # Price 'days' days ago
            percent_change = ((recent_price - past_price) / past_price) * 100
            percentage_loss.loc[stock, period] = percent_change
        except IndexError:
            percentage_loss.loc[stock, period] = np.nan  # In case data is missing

# Convert values to negative to represent losses (optional)
percentage_loss = percentage_loss.apply(lambda x: -x)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(percentage_loss, annot=True, cmap='coolwarm', fmt=".2f",
            linewidths=0.5, cbar_kws={'label': 'Percentage Loss (%)'})
plt.title('Stock Percentage Loss Heatmap')
plt.xlabel('Time Frame')
plt.ylabel('Stock Ticker')
plt.show()
