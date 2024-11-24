import pandas as pd
from datetime import datetime, timedelta

def find_gems(calculated_ticker_dtls):    
    # Apply flags based on conditions and set to 'Y' or 'N' directly
    calculated_ticker_dtls['1W_FLG'] = (calculated_ticker_dtls['1W_value'] < -10).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['1M_FLG'] = (calculated_ticker_dtls['1M_value'] < -20).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['3M_FLG'] = (calculated_ticker_dtls['3M_value'] < -30).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['6M_FLG'] = (calculated_ticker_dtls['6M_value'] < -40).map({True: 'Y', False: 'N'})
    calculated_ticker_dtls['1Y_FLG'] = (calculated_ticker_dtls['1Y_value'] < -50).map({True: 'Y', False: 'N'})
  
    # Filter data based on the 1M_value and flags
    filtered_data = calculated_ticker_dtls[
        ((calculated_ticker_dtls['1W_FLG'] == 'Y') | (calculated_ticker_dtls['1M_FLG'] == 'Y') | (calculated_ticker_dtls['3M_FLG'] == 'Y'))
    ]
    filtered_data['Report'] = 'G'
    return filtered_data
