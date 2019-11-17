
################################################################################################################
"""

"""

# Built-in/Generic Imports

# Libs
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

################################################################################################################


class Simple_LSTM:
    def __init__(self,
                 x, y,
                 input_shape,
                 batch_input_shape,
                 nb_classes,
                 optimiser,
                 test_train_split=0.1,
                 loss_function='categorical_crossentropy'):
        """
        Compile the model

        :param x: x data
        :param y: y data (target)

        :param input_shape: The shape of a sample (time_steps, data_dim)
        :param batch_input_shape: Size of the batch (batch_size, nb_time_steps, data_dim)
        :param nb_classes: Number of different classes present
        :param optimiser: Optimiser to be used
        :param test_train_split: Data split to be used for training and testing
        """
        # --> Split data to train and test sets
        assert(len(x) == len(y))

        self.x_train, self.y_train, self.x_test, self.y_test = self.__get_train_test_split(x, y, test_train_split)
        print("\n\n_______________________________________________")
        print("-->", self.x_train.shape, "training samples")
        print("-->", self.x_test.shape, "testing samples")
        print("_______________________________________________")

        # --> Initiate model
        self.model = Sequential()

        # --> Add model layers
        # LSTM layer 1
        # self.model.add(LSTM(64, stateful=True, return_sequences=True, input_shape=input_shape))
        self.model.add(LSTM(64, stateful=True, return_sequences=True, batch_input_shape=batch_input_shape))

        # LSTM layer 2
        self.model.add(LSTM(32))

        # Densely connected layer (final)
        self.model.add(Dense(nb_classes, activation='softmax'))
        self.model.summary()

        # --> Compile model
        self.model.compile(loss=loss_function, optimizer=optimiser, metrics=['accuracy'])

    def fit_model(self, nb_epoch, batch_size, validation_split=0.2, verbose=1):
        """
        Fit the model

        :param nb_epoch: Number of epoch
        :param batch_size: Size of batches per epoch
        :param verbose: Specifies verbosity mode(0 = silent, 1= progress bar, 2 = one line per epoch)
        :param validation_split: How much data is reserved for validation
        """
        self.model.fit(self.x_train,
                       self.y_train,
                       batch_size=batch_size,
                       epochs=nb_epoch,
                       validation_split=validation_split,
                       verbose=verbose)

    def fit_generator_model(self, nb_epoch, batch_size, verbose=1):
        """
        Fit the model using fit generator

        :param nb_epoch: Number of epoch
        :param batch_size: Size of batches per epoch
        :param verbose: Specifies verbosity mode(0 = silent, 1= progress bar, 2 = one line per epoch)
        """
        # TODO: Fix fit_generator
        self.model.fit_generator(self.__data_generator(self.x_train, self.y_train),
                                 validation_data=self.__data_generator(self.x_test, self.y_test),
                                 validation_steps=self.x_test.shape[0] // batch_size,
                                 epochs=nb_epoch,
                                 steps_per_epoch=self.x_train.shape[0] // batch_size,
                                 verbose=verbose)

    def evaluate_model(self, verbose=1):
        """
        Evaluate the model

        :param verbose: Specifies verbosity mode(0 = silent, 1= progress bar, 2 = one line per epoch)
        :return: Score
        """
        return self.model.evaluate(self.x_test, self.y_test, verbose=verbose)

    @staticmethod
    def __get_train_test_split(x, y, split):
        length_train_data = int(len(x) * (1 - split))

        x_train = x[:length_train_data]
        y_train = y[:length_train_data]

        x_test = x[length_train_data:]
        y_test = y[length_train_data:]

        return x_train, y_train, x_test, y_test

    @staticmethod
    def __data_generator(x, y):
        # TODO: 50??
        for dt in range(len(x)):
            yield np.reshape(x[dt], (1, 50, 2)), np.reshape(y[dt], (1, 3))

