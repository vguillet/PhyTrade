
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

# Libs
import sys
import numpy as np

from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

# Own modules
from PhyTrade.Signal_optimisation.NN_optimisation.Tools.Fetch_NN_data import Fetch_NN_data
from PhyTrade.Signal_optimisation.NN_optimisation.Tools.ML_data_preparation_tools import ML_data_preparation_tools
from PhyTrade.Signal_optimisation.NN_optimisation.Tools.Keras_model_shell import Model_shell

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################
# --> Initiate tools
ml_tools = ML_data_preparation_tools()

# --> Set random seed for reproducibility
np.random.seed(1671)
print("\n")

# ================================= LSTM network settings ===========================================
main_ticker = "AAPL"

# --> Print settings
verbose = 1                     # Print settings

# --> Model settings
nb_epoch = 1000
nb_classes = 6                  # Nb of possible outputs
nb_hidden_neurons = 51
batch_size = None

validation_split = 0.2          # How much data is reserved for validation (percent)
train_test_split_value = 0.1    # How much data is used for testing

# optimiser = SGD()
optimiser = RMSprop(lr=0.0001, decay=0.0001/nb_epoch)
metrics = ['accuracy']
loss_function = 'categorical_crossentropy'

model_mode = "normal"
timesteps = 25                  # Number of timestep included in each batch
# timesteps = settings.market_settings.data_slice_size   # Number of timestep included in each batch

return_sequences = True


# ================================= Data collection and preparation ==================================
# ========================== Initialise tools and trackers
print("\n")

x_data, y_data = Fetch_NN_data().fetch_x_y(main_ticker, x_type="spline", y_type="signal")

# np.savetxt("x_data.csv", x_data, delimiter=",")
# x_data = np.genfromtxt("x_data.csv", delimiter=",")
#
# # # TODO: Remove
# y_data = x_data[:, 0]

# ================================= Model definition and compilation ================================
# --> Initiate model
model = Sequential()

# ========================== LSTM model
# --> Auto-shape data (trim/reshape/split) to compatible input
x_train, y_train, x_test, y_test, input_shape, batch_input_shape = \
    ml_tools.auto_shape_lstm_data(x_data, y_data, timesteps, train_test_split_value, return_sequences=return_sequences)

# --> Vanilla model
stateful = False
model.add(LSTM(64, return_sequences=True,
               input_shape=input_shape))

model.add(LSTM(64, return_sequences=True))
model.add(LSTM(64, return_sequences=True))
model.add(LSTM(32, return_sequences=True))
model.add(LSTM(32, return_sequences=return_sequences))  # Return sequence dictates whether y shape (2d/3d)


model.add(Dense(y_data.shape[1], activation='softmax'))         # Activation defines the format that the prediction will take


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


