
################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Libs
import pandas as pd
import numpy as np


from keras.optimizers import SGD
from keras.utils import np_utils

from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import OneHotEncoder

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.DATA_SLICE_gen import gen_data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.Progress_bar_tool import Progress_bar
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set
from PhyTrade.Signal_optimisation.RNN_optimisation.Models.Simple_LSTM import Simple_LSTM

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################

# --> Fetch settings
settings = SETTINGS()
settings.market_settings.gen_market_settings()

loading_bar_data_preparation = Progress_bar(max_step=len(settings.market_settings.tickers)+1,
                                            label="Data Preparation")

# ================================= LSTM network settings ===========================================
nb_epoch = 200
batch_size = 128
verbose = 1                 # Print settings
nb_classes = 20             # Nb of possible outputs
nb_hidden_neurons = 128

train_test_split = 0.1      # How much data is used for training and testing
validation_split = 0.2      # How much data is reserved for validation (percent)
dropout = 0.3               # Dropout probability

optimiser = SGD(lr=0.01)
loss_function = 'categorical_crossentropy'


# ================================= Data collection and preparation ==================================
# x_data --> y_data

# --> Fetch Metalabel spline to be used as y part of training data (target)
main_ticker = "AAPL"
path = r"Data\Splines\**_splines.csv".replace('\\', '/').replace('**', main_ticker)

y_data = pd.read_csv(path, index_col=0)["trade_spline"].values
loading_bar_data_preparation.update_progress()

# --> Generate trading spline for each ticker and append to respective row to form x part of training data
x_data = np.empty((len(settings.market_settings.tickers), pd.read_csv(path, index_col=0).shape[0]))


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
        individual.gen_economic_model(data_slice)
        ticker_model_results += list(individual.trade_spline)
        data_slice.get_next_data_slice(prints=False)
        loading_bar_data_preparation.update_activity()

    x_data[i, :] = ticker_model_results

    loading_bar_data_preparation.update_progress()

# --> Reshape data
y_data.shape = (len(y_data), 1)
x_data = x_data.T

# --> Round data
y_data = np.round(y_data, 1)
x_data = np.round(x_data, 1)

# --> Convert to float32 to enable GPU use
y_data = y_data.astype("float32")
x_data = x_data.astype("float32")

# --> One hot encoding
# target_data_encoded = OneHotEncoder(sparse=False).fit_transform(y_data)
# training_data_encoded = OneHotEncoder(sparse=False).fit_transform(x_data)

# print("Target_data", y_data)
# print("Training_data", x_data)

y_data = np_utils.to_categorical(y_data, nb_classes)

# ================================= Model definition and compilation ================================
input_shape = (x_data.shape[0], x_data.shape[1])
batch_input_shape = (x_data.shape[0]//batch_size, x_data.shape[0], x_data.shape[1])

# --> Generate model
model = Simple_LSTM(x_data, y_data, input_shape, batch_input_shape, nb_classes, optimiser, test_train_split=train_test_split)

# --> Fit model
model.fit_model(nb_epoch, batch_size, validation_split)

# --> Evaluate model
score = model.evaluate_model()

print("Test score:", score[0])
print("Test accuracy:", score[1])
