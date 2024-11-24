import pandas as pd
from datetime import datetime, timedelta

def find_cherries(calculated_ticker_dtls):
    # Create flags and handle None values directly
    calculated_ticker_dtls['1M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1W_value']) or pd.isna(row['1M_value']) else ('Y' if row['1W_value'] > row['1M_value'] else 'N'), axis=1)
    calculated_ticker_dtls['3M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1M_value']) or pd.isna(row['3M_value']) else ('Y' if row['1M_value'] > row['3M_value'] else 'N'), axis=1)
    calculated_ticker_dtls['6M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1M_value']) or pd.isna(row['6M_value']) else ('Y' if row['1M_value'] > row['6M_value'] else 'N'), axis=1)
    calculated_ticker_dtls['1Y_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1M_value']) or pd.isna(row['1Y_value']) else ('Y' if row['1M_value'] > row['1Y_value'] else 'N'), axis=1)
    calculated_ticker_dtls['5Y_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1M_value']) or pd.isna(row['5Y_value']) else ('Y' if row['1M_value'] > row['5Y_value'] else 'N'), axis=1)
    
    # Filter data based on the 1M_value and flags
    filtered_data = calculated_ticker_dtls[
        (calculated_ticker_dtls['1M_value'] >= 15) & 
        ((calculated_ticker_dtls['5Y_FLG'] == 'Y') | (calculated_ticker_dtls['1Y_FLG'] == 'Y'))
    ]
    filtered_data['Report'] = 'C'
    return filtered_data
