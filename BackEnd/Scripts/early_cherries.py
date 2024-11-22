import pandas as pd
from datetime import datetime, timedelta

def apply_flags(ticker_stklist_dtls):
    """Apply flags if one timeframe outperforms another."""
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1W_value'] > ticker_stklist_dtls['1M_value'], '1M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['3M_value'], '3M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['6M_value'], '6M_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['1Y_value'], '1Y_FLG'] = 'Y'
    ticker_stklist_dtls.loc[ticker_stklist_dtls['1M_value'] > ticker_stklist_dtls['5Y_value'], '5Y_FLG'] = 'Y'

def find_cherries(calculated_ticker_dtls, all_data):
    filtered_data_list = []

    for ticker in calculated_ticker_dtls['ticker'].unique():
        ticker_data = all_data[all_data['ticker'] == ticker]
        ticker_dtls = calculated_ticker_dtls[calculated_ticker_dtls['ticker'] == ticker]

        # Apply flags based on breakout conditions
        apply_flags(ticker_dtls)

        # Filter data based on the 1M_value and flags
        filtered_data = ticker_dtls[
            (ticker_dtls['1M_value'] >= 15) & 
            ((ticker_dtls['5Y_FLG'] == 'Y') | (ticker_dtls['1Y_FLG'] == 'Y'))
        ]
        filtered_data_list.append(filtered_data)

    return pd.concat(filtered_data_list, ignore_index=True)
