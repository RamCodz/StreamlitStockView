import pandas as pd
from pathlib import Path
import yahoo_fin.stock_info as si
import datetime

def get_stock_data(ticker, period):
    try:
        end_date = datetime.date.today()
        if period == "5y":
            start_date = end_date - datetime.timedelta(days=1825)
        elif period == "1y":
            start_date = end_date - datetime.timedelta(days=365)
        elif period == "6m":
            start_date = end_date - datetime.timedelta(days=182)
        elif period == "3m":
            start_date = end_date - datetime.timedelta(days=91)
        elif period == "1m":
            start_date = end_date - datetime.timedelta(days=30)
        else:
            raise ValueError("Unsupported period. Use '1y', '6m', '3m', or '1m'.")

        # Fetch stock data from Yahoo Finance
        stock_data = si.get_data(ticker + ".BO", start_date=start_date, end_date=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def filter_stocks(df, period):
    filtered_rows = []
    try:
        for index, row in df.iterrows():
            ticker = row['Security Id']
            stock_data = get_stock_data(ticker, period)
            if not stock_data.empty:
                one_year_avg_price = stock_data['close'].mean()
                one_year_avg_volume = stock_data['volume'].mean()

                five_day_avg_price = stock_data['close'].tail(5).mean()
                five_day_avg_volume = stock_data['volume'].tail(5).mean()

                # Check if criteria are met
                if five_day_avg_price > one_year_avg_price and five_day_avg_volume > one_year_avg_volume:
                    filtered_rows.append(row)

        # Create a new DataFrame from filtered rows
        filtered_df = pd.DataFrame(filtered_rows)

    except Exception as e:
        print(f"Error filtering stocks: {e}")
        filtered_df = pd.DataFrame()  # Return an empty DataFrame on error

    return filtered_df
