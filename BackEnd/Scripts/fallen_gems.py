import pandas as pd
from datetime import datetime, timedelta

def find_gems(calculated_ticker_dtls):
    # Create flags and handle None values directly
    calculated_ticker_dtls['1W_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1W_value']) else ('Y' if row['1W_value'] > -10 else 'N'), axis=1)
    calculated_ticker_dtls['1M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1M_value']) else ('Y' if row['1M_value'] > -20 else 'N'), axis=1)
    calculated_ticker_dtls['3M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['3M_value']) else ('Y' if row['3M_value'] > -30 else 'N'), axis=1)
    calculated_ticker_dtls['6M_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['6M_value']) else ('Y' if row['6M_value'] > -40 else 'N'), axis=1)
    calculated_ticker_dtls['1Y_FLG'] = calculated_ticker_dtls.apply(lambda row: 'N' if pd.isna(row['1Y_value']) else ('Y' if row['1Y_value'] > -50 else 'N'), axis=1)

    # Filter data based on the 1W, 1M, and 3M flags
    filtered_data = calculated_ticker_dtls[
        (calculated_ticker_dtls['1W_FLG'] == 'Y') | (calculated_ticker_dtls['1M_FLG'] == 'Y') | (calculated_ticker_dtls['3M_FLG'] == 'Y')
    ]
    filtered_data['Report'] = 'G'
    return filtered_data
