
################################################################################################################
"""
LSTM cross ticker deep learning optimiser, ment to correct a trading signal based on the activity of others
The x values are generated for all the involved tickers using the EVOA optimiser,
and the y by the metalabeling toolbox for the target ticker.

TODO: Make data stationary?
TODO: Standardise series data?
TODO: stattools
"""

# Built-in/Generic Imports
import sys
import math

# Libs
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

from keras.models import Sequential
from keras.layers import LSTM, Dense, RNN, Embedding, Dropout

# Own modules
from PhyTrade.Signal_optimisation.NN_optimisation.Tools.Fetch_NN_data import Fetch_NN_data
from PhyTrade.Signal_optimisation.NN_optimisation.Tools.ML_data_preparation_tools import ML_data_preparation_tools
from PhyTrade.Signal_optimisation.NN_optimisation.Models.Keras_model_shell import Model_shell

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################
# --> Set random seed for reproducibility
np.random.seed(1671)

# ================================= LSTM network settings ===========================================
main_ticker = "AAPL"

# --> Print settings
verbose = 1                     # Print settings

# --> Model settings
model_types = ["simple", "lstm"]
model_type = 0

nb_epoch = 1000
nb_classes = 6                  # Nb of possible outputs
nb_hidden_neurons = 11

validation_split = 0.2          # How much data is reserved for validation (percent)
train_test_split_value = 0.1    # How much data is used for testing

# optimiser = SGD()
optimiser = RMSprop(lr=0.00001)
metrics = ['accuracy']
loss_function = 'categorical_crossentropy'

# > Simple-specific settings
dropout = 0.3                   # Dropout probability
batch_size = 128

# > LSTM-specific settings
timesteps = 1   # Number of timestep included in each batch
# timesteps = settings.market_settings.data_slice_size   # Number of timestep included in each batch

return_sequences = False


# ================================= Data collection and preparation ==================================
# ========================== Initialise tools and trackers
print("\n")
ml_tools = ML_data_preparation_tools()

x_data, y_data = Fetch_NN_data().fetch_x_y(main_ticker, x_type="spline", y_type="signal")

# x_train, y_train, x_test, y_test = Fetch_NN_data().fetch_mnst_x_y()

# ================================= Model definition and compilation ================================
# --> Initiate model
model = Sequential()

# ========================== Simple model
if model_types[model_type] == "simple":
    # --> Auto-shape data to compatible input
    x_train, y_train, x_test, y_test, input_shape, batch_input_shape = \
        ml_tools.auto_shape_classification_data(x_data, y_data, train_test_split_value, shuffle=False)

    # --> Densely connected layer 1
    model.add(Dense(nb_hidden_neurons, activation="relu", input_shape=(x_train.shape[1],)))
    # # --> Dropout
    model.add(Dropout(dropout))
    #
    # # --> Densely connected layer 2
    model.add(Dense(nb_hidden_neurons, activation="relu"))
    # # --> Dropout
    model.add(Dropout(dropout))
    #
    # # --> Densely connected layer 3
    model.add(Dense(nb_hidden_neurons, activation="relu"))
    # # --> Dropout
    model.add(Dropout(dropout))

    # --> Densely connected layer final
    model.add(Dense(nb_classes, activation="softmax"))
    # --> Single neuron layer with activation function softmax (generalization of the sigmoid function)

"""
# ========================== LSTM model
elif model_types[model_type] == "lstm":
    # --> Auto-shape data (trim/reshape/split) to compatible input
    x_train, y_train, x_test, y_test, input_shape, batch_input_shape = \
        ml_tools.auto_shape_lstm_data(x_data, y_data, timesteps, train_test_split_value, return_sequences=return_sequences)

    if timesteps == 1:
        # --> Vanilla model
        stateful = False
        model.add(LSTM(x_data.shape[1], return_sequences=True, input_shape=input_shape))

    else:
        # --> Batch model
        stateful = True
        model.add(LSTM(x_data.shape[1], return_sequences=True, stateful=True, batch_input_shape=batch_input_shape))

    model.add(LSTM(32, return_sequences=True, stateful=stateful))
    model.add(LSTM(32, return_sequences=True, stateful=stateful))   # Return sequence dictates whether y shape (2d/3d), needs to be specified in auto_shape
    model.add(LSTM(32, return_sequences=return_sequences))          # Return sequence dictates whether y shape (2d/3d)
    model.add(Dense(y_data.shape[1], activation='softmax'))         # Activation defines the format that the prediction will take
"""

# ================================= Model definition and compilation ================================
# -->  Generate model
model = Model_shell(model,
                    x_train, y_train, x_test, y_test,
                    optimiser, metrics,
                    train_test_split=train_test_split_value)

# --> Fit model
model.fit_model(nb_epoch, batch_size=batch_size, validation_split=validation_split, verbose=verbose)

# --> Plot training progress
model.plot_training_progress()

# --> Evaluate model
model.evaluate_model(verbose=verbose)


