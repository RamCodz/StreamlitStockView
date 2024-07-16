import pandas as pd
import yahoo_fin.stock_info as si
import datetime

# Function to get stock data using yahoo_fin
def get_stock_data(ticker, period):
    try:
        # Calculate the start date based on the period
        end_date = datetime.date.today()
        if period == "1y":
            start_date = end_date - datetime.timedelta(days=365)
        elif period == "6m":
            start_date = end_date - datetime.timedelta(days=182)
        elif period == "3m":
            start_date = end_date - datetime.timedelta(days=91)
        elif period == "1m":
            start_date = end_date - datetime.timedelta(days=30)
        else:
            raise ValueError("Unsupported period. Use '1y', '6m', '3m', or '1m'.")

        stock_data = si.get_data(ticker, start_date=start_date, end_date=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Function to filter stocks based on the criteria
def filter_stocks(tickers, period):
    filtered_stocks = []
    for ticker in tickers:
        stock_data = get_stock_data(ticker, period)
        if not stock_data.empty:
            # Calculate 1-year average price and volume
            one_year_avg_price = stock_data['close'].mean()
            one_year_avg_volume = stock_data['volume'].mean()

            # Calculate 5-day average price and volume
            five_day_avg_price = stock_data['close'].tail(5).mean()
            five_day_avg_volume = stock_data['volume'].tail(5).mean()

            # Check if the 5-day averages are greater than the 1-year averages
            if five_day_avg_price > one_year_avg_price and five_day_avg_volume > one_year_avg_volume:
                filtered_stocks.append(ticker)

    return filtered_stocks# Code to identify Early Cherries
