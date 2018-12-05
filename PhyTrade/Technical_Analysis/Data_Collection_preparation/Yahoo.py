import pandas_datareader as pdr
from datetime import datetime


def pull_yahoo_data(ticker):
    i = datetime.now()
    data = pdr.get_data_yahoo(symbols=ticker, start=datetime(2000, 1, 1), end=datetime(i.year, i.month, i.day))

    print("--Yahoo! Finance data pulled successfully--")
    print("Number of points pulled:", len(data))
    print("-------------------------------------------")

    return data
