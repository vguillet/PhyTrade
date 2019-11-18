
################################################################################################################
"""
LSTM cross ticker deep learning optimiser, ment to correct a trading signal based on the activity of others
The x values are generated for all the involved tickers using the EVOA optimiser,
and the y by the metalabeling toolbox for the target ticker.

TODO: Make data stationary?
TODO: Standardise series data?
"""

# Built-in/Generic Imports
import sys
import math

# Libs
import pandas as pd
import numpy as np


from keras.optimizers import SGD
from keras.utils import np_utils

from keras.models import Sequential
from keras.layers import LSTM, Dense

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.DATA_SLICE_gen import gen_data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.Progress_bar_tool import Progress_bar
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set

from PhyTrade.Signal_optimisation.RNN_optimisation.Models.Keras_model_shell import Model_shell
from PhyTrade.Signal_optimisation.RNN_optimisation.Tools.ML_data_preparation_tools import ML_data_preparation_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################
ml_tools = ML_data_preparation_tools()

# --> Fetch settings
settings = SETTINGS()
settings.market_settings.gen_market_settings()

print("\n")
loading_bar_data_preparation = Progress_bar(max_step=len(settings.market_settings.tickers)+1,
                                            label="Data Preparation")

# ================================= LSTM network settings ===========================================
nb_epoch = 1000

# timesteps = settings.market_settings.data_slice_size   # Number of timestep included in each batch
timesteps = 1   # Number of timestep included in each batch

nb_classes = 20             # Nb of possible outputs

verbose = 1                 # Print settings

train_test_split_value = 0.1      # How much data is used for training and testing
validation_split = 0.2      # How much data is reserved for validation (percent)
dropout = 0.3               # Dropout probability

optimiser = SGD(lr=0.01)
metrics = ['accuracy']
loss_function = 'categorical_crossentropy'


# ================================= Data collection and preparation ==================================
# ========================== Fetch data
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

# --> One hot encoding
# target_data_encoded = OneHotEncoder(sparse=False).fit_transform(y_data)
# training_data_encoded = OneHotEncoder(sparse=False).fit_transform(x_data)

# --> Convert y data to categorical
y_data = np_utils.to_categorical(y_data, nb_classes)

# --> Run auto_shape_data (trim/reshape/split)
x_train, y_train, x_test, y_test, batch_input_shape, input_shape = \
    ml_tools.auto_shape_data(x_data, y_data, timesteps, train_test_split_value, return_sequences=False)


# ================================= Model definition and compilation ================================
# --> Initiate model
model = Sequential()

if timesteps != 1:
    # ==========================> Vanilla model
    # LSTM layer 1
    model.add(LSTM(32, return_sequences=True, stateful=True, batch_input_shape=batch_input_shape))

    # LSTM layer 2
    model.add(LSTM(32, return_sequences=True, stateful=True))

    # LSTM layer 3
    model.add(LSTM(32, return_sequences=True, stateful=True))   # Return sequence dictates whether y shape (2d/3d), needs to be specified in auto_shape

else:
    # ==========================> Batch_model
    # LSTM layer 1
    model.add(LSTM(32, return_sequences=True, input_shape=input_shape))

    # LSTM layer 2
    model.add(LSTM(32, return_sequences=True))

    # LSTM layer 3
    model.add(LSTM(32))                          # Return sequence dictates whether y shape (2d/3d)

# Densely connected layer (final)
model.add(Dense(nb_classes, activation='softmax'))          # Activation defines the format that the prediction will take


# ==========================  Generate model
model = Model_shell(model,
                    x_train, y_train, x_test, y_test,
                    nb_classes,
                    optimiser, metrics,
                    input_shape=input_shape,
                    batch_input_shape=batch_input_shape,
                    train_test_split=train_test_split_value)

# --> Fit model
model.fit_model(nb_epoch, validation_split)

# --> Plot training progress
model.plot_training_progress()

# --> Evaluate model
model.evaluate_model()


