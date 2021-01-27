
##################################################################################################################
"""
Used to fetch or download technical data of a specific ticker

# TODO: Add self-updating data fetcher (update missing time series points)
"""

# Built-in/Generic Imports
import os

# Libs
import pandas

# Own modules
from PhyTrade.Data_Collection_preparation.Data_sources.Yahoo import pull_yahoo_data

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


def fetch_technical_data(ticker, source="Yahoo"):

    path = r"Data/Technical_data\**_" + source + "_data.csv".replace('\\', '/').replace('**', ticker)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        data = pandas.read_csv(path, index_col=0)

    # --> Else download data
    else:
        # ---> Pull data from source
        if source == "Yahoo":
            data = pull_yahoo_data(ticker)
        else:
            # TODO: Add technical data sources
            pass

        file_name = ticker + "_" + source + "_data.csv"

        # ------------------ Fill in missing values (weekends)
        # idx = pandas.date_range(data.index[0], data.index[-1])
        # data = data.reindex(idx)
        # data = data.fillna(method='ffill')

        data = data.reset_index()

        # ---> Save data to csv file
        path = r"Data/Technical_data".replace('\\', '/')
        full_file_name = path + '/' + file_name

        data.to_csv(full_file_name)

    return data
