
################################################################################################################
"""

"""

# Libs
import pandas as pd
import numpy as np

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


settings = SETTINGS()
settings.market_settings.gen_market_settings()

main_ticker = "AAPL"
path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Splines\**_splines".replace('\\', '/').replace('**', main_ticker)

data = np.zeros((len(settings.market_settings.tickers)+1, pd.read_csv(path, index_col=0).shape[0]))
data[-1] = pd.read_csv(path, index_col=0)["trade_spline"]
print(data)
print(pd.read_csv(path, index_col=0).shape[0])


for ticker in settings.market_settings.tickers:
    ticker_model_results = []
    individual = Individual(ticker, parameter_set=fetch_parameter_set(ticker, "06", "Short_term"))
    data_slice = data_slice(ticker,
                            settings.market_settings.training_start_date,
                            settings.market_settings.data_slice_size,
                            0, data_selection=settings.market_settings.price_selection,
                            end_date=settings.market_settings.training_end_date)

    while data_slice.end_of_dataset is False:
        individual.gen_economic_model(data_slice)
        ticker_model_results += list(individual.trade_spline)
        print(data_slice.start_date)
        print(data_slice.stop_date, "\n")
        data_slice.get_next_data_slice()

    print(ticker_model_results)
    print(len(ticker_model_results))



