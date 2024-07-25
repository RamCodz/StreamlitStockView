import pandas as pd
from datetime import datetime, timedelta
from Utils import globals
from Utils.debug import debug


def dbg(msg):
    debug("early_cherries-->" + str(msg))


def analyze_stock(ticker_data):
    dbg("in analyze_stock")
    dbg(ticker_data)
    ##ticker_data.index.name = 'Date'
    ##ticker_data = ticker_data.rename_axis('Date').reset_index()
    ##ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
    dbg("Column labels:" + ticker_data.columns)
    end_date = datetime.now()
    start_date_one_year = end_date - timedelta(days=365)
    start_date_one_week = end_date - timedelta(days=7)

    last_year_data = ticker_data[(ticker_data['Date'] >= start_date_one_year) & (ticker_data['Date'] <= end_date)]
    last_week_data = ticker_data[(ticker_data['Date'] >= start_date_one_week) & (ticker_data['Date'] <= end_date)]
    if last_year_data is not None and last_week_data is not None:
        # Calculate average closing prices
        avg_close_one_year = last_year_data['close'].mean()
        avg_close_last_week = last_week_data['close'].mean()

        avg_volume_one_year = last_year_data['volume'].mean()
        avg_volume_last_week = last_week_data['volume'].mean()

        dbg('avg_volume_one_year ' + str(avg_volume_one_year))
        dbg('avg_volume_last_week ' + str(avg_volume_last_week))

        dbg('avg_close_one_year ' + str(avg_close_one_year))
        dbg('avg_close_last_week ' + str(avg_close_last_week))

        # Check if last week's average closing price is greater than one-year average closing price
        if avg_close_one_year < avg_close_last_week and avg_volume_one_year < avg_volume_last_week:
            return True
    return False


def find_cherries(all_data, StockList):
    dbg("in find_cherries ")
    cherries_ticker_dtls = pd.DataFrame()
    DListLbl = ['Security Code', 'Issuer Name', 'Security Id', 'Security Name', 'Status', 'Group', 'Face Value',
                'ISIN No', 'Industry', 'Instrument', 'Sector Name', 'Industry New Name', 'Igroup Name',
                'ISubgroup Name']
    unique_tickers = all_data['ticker'].unique()
    for ticker in unique_tickers:
        dbg("ticker " + ticker)
        ticker_data = all_data[all_data['ticker'] == ticker]
        if analyze_stock(ticker_data):
            ticker_stklist_dtls = StockList[StockList['Security Id'] + '.NS' == ticker]
            dbg("ticker stocklist " + str(ticker_stklist_dtls))
            cherries_ticker_dtls = pd.concat([cherries_ticker_dtls, ticker_stklist_dtls])
    ##dbg("cherries list "+str(cherries_ticker_dtls))
    return cherries_ticker_dtls
# Filter stocks and print potential candidates
##filter_stocks()
