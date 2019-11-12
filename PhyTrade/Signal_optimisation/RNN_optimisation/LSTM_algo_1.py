
################################################################################################################
"""

"""

# Libs
import pandas as pd
import numpy as np

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.DATA_SLICE_gen import gen_data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.Progress_bar_tool import Progress_bar
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################

# --> Fetch settings
settings = SETTINGS()
settings.market_settings.gen_market_settings()
loading_bar_data_preparation = Progress_bar(max_step=len(settings.market_settings.tickers)+1,
                                            label="Data Preparation",
                                            overwrite_setting=False)

# --> Fetch Metalabel spline to be used as Target
main_ticker = "TM"
path = r"Data\Splines\**_splines.csv".replace('\\', '/').replace('**', main_ticker)

target_data = pd.read_csv(path, index_col=0)["trade_spline"].values

loading_bar_data_preparation.update_progress()

# --> Generate trading spline for each ticker and append to respective row to form Training data
training_data = np.empty((len(settings.market_settings.tickers), pd.read_csv(path, index_col=0).shape[0]))


for i, ticker in enumerate(settings.market_settings.tickers):
    ticker_model_results = []
    individual = Individual(ticker, parameter_set=fetch_parameter_set(ticker, "06", "Short_term"))
    data_slice = gen_data_slice(ticker,
                                settings.market_settings.training_start_date,
                                settings.market_settings.data_slice_size,
                                0,
                                data_selection=settings.market_settings.price_selection,
                                end_date=settings.market_settings.testing_end_date)

    while data_slice.end_of_dataset is False:
        print(data_slice.start_date)
        print(data_slice.stop_date)
        individual.gen_economic_model(data_slice)
        ticker_model_results += list(individual.trade_spline)
        data_slice.get_next_data_slice()
        # loading_bar_data_preparation.update_activity()

    print(ticker_model_results)
    training_data[i, :] = ticker_model_results

    loading_bar_data_preparation.update_progress()

print("Target_data", target_data)
print("Training_data", training_data)
