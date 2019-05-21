import pandas_datareader as pdr
from datetime import datetime


# TODO: Automate start date_time of wanted data
def pull_yahoo_data(ticker):
    """
    Download financial data from Yahoo for a specific ticker

    :param ticker: Desired ticker
    :return: Pandas dataframe
    """
    i = datetime.now()
    data = pdr.get_data_yahoo(symbols=ticker, start=datetime(1990, 1, 1), end=datetime(i.year, i.month, i.day))

    print("--Yahoo! Finance data pulled successfully--")
    print("Number of points pulled:", len(data), "for", ticker)
    print("-------------------------------------------")

    return data
