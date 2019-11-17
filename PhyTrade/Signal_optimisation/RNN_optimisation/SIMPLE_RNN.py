
################################################################################################################
"""

"""

# Built-in/Generic Imports
from __future__ import print_function
import sys

# Libs
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, RMSprop, Adam
from keras.utils import np_utils

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


# --> Set random seed for reproducibility
np.random.seed(1671)

# -------------------- Network and Training parameters --------------------
nb_epoch = 200
batch_size = 128
verbose = 1                 # Print settings
nb_classes = 10             # Nb of possible outputs
nb_hidden_neurons = 128
validation_split = 0.2      # How much data is reserved for validation
optimiser = RMSprop()
dropout = 0.3               # Dropout probability

# -------------------- Data collection and preparation --------------------
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

# -------------------- Model definition and compilation -------------------
# --> Create empty sequential model
model = Sequential()

# ----> Add model layers
# --> Densely connected layer 1
model.add(Dense(nb_hidden_neurons, input_shape=(reshaped,)))
# --> Activation function relu
model.add(Activation("relu"))
# --> Dropout
model.add(Dropout(dropout))

# --> Densely connected layer 2
model.add(Dense(nb_hidden_neurons))
# --> Activation function relu
model.add(Activation("relu"))
# --> Dropout
model.add(Dropout(dropout))

# --> Densely connected layer 3
model.add(Dense(nb_hidden_neurons))
# --> Activation function relu
model.add(Activation("relu"))
# --> Dropout
model.add(Dropout(dropout))

# --> Densely connected layer final
model.add(Dense(nb_classes))
# --> Single neuron layer with activation function softmax (generalization of the sigmoid function)
model.add(Activation("softmax"))    # Final stage is softmax
model.summary()

# ---> Model compilation
model.compile(loss="categorical_crossentropy", optimizer=optimiser, metrics=["accuracy"])

# -------------------- Model fitting --------------------------------------
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=nb_epoch, verbose=verbose, validation_split=validation_split)

# -------------------- Model evaluation -----------------------------------
score = model.evaluate(x_test, y_test, verbose=verbose)

print("Test score:", score[0])
print("Test accuracy:", score[1])

# ---> Plot training progress
# import matplotlib.pyplot as plt
#
# history_dic = history.history
# loss_values = history_dic["loss"]
# val_loss_values = history_dic["val_loss"]
#
# epochs = range(1, nb_epoch + 1)
#
# plt.plot(epochs, loss_values, "bo", label="Training loss")
# plt.plot(epochs, val_loss_values, "b", label="Validation loss")
# plt.title("Traininig and validation loss")
# plt.xlabel("Epochs")
# plt.ylabel("Loss")
# plt.legend()
# plt.show()
