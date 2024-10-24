import yfinance as yf
import pandas as pd
import datetime

# Function to fetch stock data and analyze performance
def analyze_stocks(stock_symbols):
    results = []
    
    # Calculate dates
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    
    for symbol in stock_symbols:
        # Fetch historical data
        data = yf.download(symbol, start=start_date, end=end_date)
        
        if data.empty:
            continue
        
        # Calculate the percentage change over the last year
        year_start_price = data['Close'].iloc[0]
        year_end_price = data['Close'].iloc[-1]
        year_change = ((year_end_price - year_start_price) / year_start_price) * 100
        
        # Calculate the recent performance (last 30 days)
        recent_data = yf.download(symbol, start=end_date - datetime.timedelta(days=30), end=end_date)
        
        if recent_data.empty:
            continue
        
        recent_start_price = recent_data['Close'].iloc[0]
        recent_end_price = recent_data['Close'].iloc[-1]
        recent_change = ((recent_end_price - recent_start_price) / recent_start_price) * 100
        
        # Criteria for identifying underperformers that recently rallied
        if year_change < 0 and recent_change > 5:  # Adjust the thresholds as needed
            results.append({
                'Symbol': symbol,
                'Year Change (%)': year_change,
                'Recent Change (%)': recent_change
            })
    
    return results

# List of stock symbols to analyze
stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Add more symbols as needed
underperformers = analyze_stocks(stock_symbols)

# Display results
for stock in underperformers:
    print(stock)
