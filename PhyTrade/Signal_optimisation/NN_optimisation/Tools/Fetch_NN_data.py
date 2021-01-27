
################################################################################################################
"""
Fetch data for the NN block as specified in settings
"""

# Built-in/Generic Imports

# Libs
import pandas as pd
import numpy as np

from keras.utils import np_utils
from sklearn.preprocessing import OneHotEncoder

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.Trading_dataslice import Trading_dataslice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set
from PhyTrade.Tools.Progress_bar_tool import Progress_bar

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

################################################################################################################


class Fetch_NN_data:
    @staticmethod
    def fetch_x_y(main_ticker, x_type="spline", y_type="signal"):
        # --> Fetch settings
        settings = SETTINGS()
        settings.market_settings.gen_market_settings()
        loading_bar_data_preparation = Progress_bar(max_step=len(settings.market_settings.tickers) + 1,
                                                    label="Data Preparation",
                                                    overwrite_setting=True)

        if y_type == "spline":
            nb_classes = 20     # spline: -1.0, -0.9, [...], 0.9, 1.0
        else:
            nb_classes = 3      # signal: -1, 0, 1

        # ========================== Fetch data
        # --> Fetch y data (metalabel spline)
        path = r"Data\Splines\**_splines.csv".replace('\\', '/').replace('**', main_ticker)

        y_data = np.array(pd.read_csv(path, index_col=0)["trade_"+y_type].values)
        loading_bar_data_preparation.update_progress()

        # --> Generate x data (trading signal for each ticker and append to respective row)
        x_data = np.empty((len(settings.market_settings.tickers), y_data.shape[0]))

        for i, ticker in enumerate(settings.market_settings.tickers):
            ticker_model_results = []
            individual = Individual(ticker, parameter_set=fetch_parameter_set(ticker,
                                                                              settings.market_settings.run_reference,
                                                                              settings.market_settings.term))
            data_slice = Trading_dataslice(ticker,
                                           settings.market_settings.training_start_date,
                                           settings.market_settings.data_slice_size,
                                           0,
                                           price_data_selection=settings.market_settings.price_selection,
                                           end_date=settings.market_settings.testing_end_date)

            while data_slice.end_of_dataset is False:
                individual.gen_economic_model(data_slice)
                ticker_model_results += list(getattr(individual, "trade_"+x_type))
                data_slice.get_next_data_slice(prints=False)
                # loading_bar_data_preparation.update_activity()

            if len(ticker_model_results) > y_data.shape[0]:
                ticker_model_results = ticker_model_results[:y_data.shape[0]]

            x_data[i, :] = ticker_model_results

            loading_bar_data_preparation.update_progress()

        # x_data = np.empty((1))

        # ========================== Format data
        # --> Initial reshape data
        y_data.shape = (len(y_data), 1)
        x_data = x_data.T

        # --> Round data
        y_data = np.round(y_data, 1)
        x_data = np.round(x_data, 1)

        # --> Convert to float32 to enable GPU use
        y_data = y_data.astype("float32")
        x_data = x_data.astype("float32")

        # --> Convert y data to categorical
        y_data = np_utils.to_categorical(y_data, nb_classes)

        # --> One hot encoding (necessary to have one-hot-encoded y when using lstm)
        y_data = OneHotEncoder(sparse=False).fit_transform(y_data)

        print("\n\n_______________________________________________")
        print("--> Fetch data: success")
        print("x_data:\n", x_data)
        print("\ny_data:\n", y_data)

        return x_data, y_data

    @staticmethod
    def fetch_mnst_x_y():
        from keras.datasets import mnist
        nb_classes = 10  # Nb of possible outputs

        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        # x_train is 60000 rows of 28x28 values (60000 images of 28x28 pixels)
        # --> Reshape data to 60000x784
        reshaped = 784

        x_train = x_train.reshape(60000, reshaped)
        x_test = x_test.reshape(10000, reshaped)

        # --> Convert to float32 enable GPU use
        x_train = x_train.astype("float32")
        x_test = x_test.astype("float32")

        # --> Normalise between [0,1], the maximum intensity value being 255
        x_train /= 255
        x_test /= 255

        print(x_train.shape, "train samples")
        print(x_test.shape, "test samples")

        # --> Convert class vectors to binary class matrices, with a class for each possible output
        y_train = np_utils.to_categorical(y_train, nb_classes)
        y_test = np_utils.to_categorical(y_test, nb_classes)

        return x_train, y_train, x_test, y_test
