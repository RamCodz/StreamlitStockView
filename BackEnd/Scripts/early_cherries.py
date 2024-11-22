import pandas as pd
from datetime import datetime, timedelta

def find_cherries(calculated_ticker_dtls):    
    # Apply flags based on conditions and set to 'Y' or 'N' directly
    calculated_ticker_dtls['1M_FLG'] = (calculated_ticker_dtls['1W_value'] > calculated_ticker_dtls['1M_value']).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['3M_FLG'] = (calculated_ticker_dtls['1M_value'] > calculated_ticker_dtls['3M_value']).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['6M_FLG'] = (calculated_ticker_dtls['1M_value'] > calculated_ticker_dtls['6M_value']).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['1Y_FLG'] = (calculated_ticker_dtls['1M_value'] > calculated_ticker_dtls['1Y_value']).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['5Y_FLG'] = (calculated_ticker_dtls['1M_value'] > calculated_ticker_dtls['5Y_value']).map({True: 'Y', False: 'N'})

    # Filter data based on the 1M_value and flags
    filtered_data = calculated_ticker_dtls[
        (calculated_ticker_dtls['1M_value'] >= 15) & 
        ((calculated_ticker_dtls['5Y_FLG'] == 'Y') | (calculated_ticker_dtls['1Y_FLG'] == 'Y'))
    ]

    return filtered_data
