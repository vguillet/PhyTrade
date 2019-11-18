
################################################################################################################
"""

"""

# Built-in/Generic Imports
import math
import sys

# Libs
import numpy as np

# Own modules
from PhyTrade.Tools.Colours_and_Fonts import cf

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

################################################################################################################


class ML_data_preparation_tools:
    @staticmethod
    def get_trimmed_data(x, y, timesteps):
        """
        Trim data to fit in even batches
        """
        data_trimmed = len(x) % timesteps

        return x[:-data_trimmed], y[:-data_trimmed]

    @staticmethod
    def get_reshaped_data(x, y, timesteps):
        """
        Reshape data to match batch_input_shape
        """

        # --> Split x and y into samples
        x_sample_lst = []
        y_sample_lst = []

        for i in range(0, len(x), timesteps):
            x_sample = x[i:i + timesteps]
            y_sample = y[i:i + timesteps]

            x_sample_lst.append(x_sample)
            y_sample_lst.append(y_sample)

        # --> Convert list of array into 3d array
        x_formatted = np.array(x_sample_lst)
        y_formatted = np.array(y_sample_lst)

        return x_formatted, y_formatted

    @staticmethod
    def get_train_test_split(x, y, split, timesteps, total_nb_batches):
        """
        Split data to train and test according to split
        """
        length_train_data = math.ceil(total_nb_batches*(1-split)*timesteps) + 1

        x_train = x[:length_train_data]
        y_train = y[:length_train_data]

        x_test = x[length_train_data:]
        y_test = y[length_train_data:]

        return x_train, y_train, x_test, y_test
