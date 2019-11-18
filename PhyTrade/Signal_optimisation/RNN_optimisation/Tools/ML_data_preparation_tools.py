
################################################################################################################
"""

"""

# Built-in/Generic Imports
import math
import sys

# Libs
import numpy as np

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

################################################################################################################


class ML_data_preparation_tools:
    @staticmethod
    def auto_shape_data(x_data, y_data, timesteps, train_test_split_value, return_sequences=False):
        """
        Auto-format data

        :param x_data: x data
        :param y_data: y data
        :param timesteps: Timesteps per batch
        :param train_test_split_value: train-test split value
        :param return_sequences: return sequence boolean (has to match second to last layer)

        :return: x_formatted, y_formatted, batch_input shape, input_shape
        """
        ml_tools = ML_data_preparation_tools()

        # --> Trim data to fit in even batches
        if timesteps > 1:
            x_data, y_data = ml_tools.get_trimmed_data(x_data, y_data, timesteps)

        # --> Reshape x data to batch_input_shape format
        if return_sequences:
            x_data = ml_tools.get_reshaped_data(x_data, timesteps)
            y_data = ml_tools.get_reshaped_data(y_data, timesteps)
        else:
            x_data = ml_tools.get_reshaped_data(x_data, timesteps)

        # --> Split data to test and train
        x_train, y_train, x_test, y_test = \
            ml_tools.get_train_test_split(x_data, y_data, train_test_split_value, timesteps, x_data.shape[0], return_sequences=True)

        # --> Determine batch_input_shape and input_shape
        batch_input_shape = x_train.shape
        input_shape = (batch_input_shape[1], batch_input_shape[2])  # (timesteps, data_dim)

        return x_train, y_train, x_test, y_test, batch_input_shape, input_shape

    @staticmethod
    def get_trimmed_data(x, y, timesteps):
        """
        Trim data to fit in even batches
        """
        data_trimmed = len(x) % timesteps

        return x[:-data_trimmed], y[:-data_trimmed]

    @staticmethod
    def get_reshaped_data(x, timesteps):
        """
        Reshape data to match batch_input_shape (batch_size, timesteps, data_dim)
        """

        # --> Split x into samples
        x_sample_lst = []

        for i in range(0, len(x), timesteps):
            x_sample = x[i:i + timesteps]
            x_sample_lst.append(x_sample)

        # --> Convert list of array into array
        x_formatted = np.array(x_sample_lst)

        return x_formatted

    @staticmethod
    def get_train_test_split(x, y, split, timesteps, total_nb_batches, return_sequences=False):
        """
        Split data to train and test according to split
        """
        print("======================>", total_nb_batches)
        length_train_data = math.ceil(total_nb_batches*(1-split)) + 1

        x_train = x[:length_train_data]
        x_test = x[length_train_data:]

        if return_sequences:
            y_train = y[:length_train_data]
            y_test = y[length_train_data:]
        else:
            y_train = y[:length_train_data*timesteps]
            y_test = y[length_train_data*timesteps:]

        return x_train, y_train, x_test, y_test
