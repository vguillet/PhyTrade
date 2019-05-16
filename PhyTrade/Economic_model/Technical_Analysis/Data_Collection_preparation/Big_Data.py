"""
This script contains the BIGDATA class, necessary to collect and move around data in the model generation prototypes

Victor Guillet
11/28/2018
"""

import numpy as np


class BIGDATA:
    def __init__(self, data, data_slice_start_ind=0, data_slice_stop_ind=200):
        """
        Contains all the information relating to a specific analysis,
        modules can be called, and their instance attribute should be saved in the big_data instance
        (to enable attribute access anywhere inm the model).
        To compute specific attributes, run the corresponding Technical_Indicators/modules.
        The list of all options can be found in the PhyTrade Library file

        :param data: Pandas dataframe
        :param data_slice_start_ind: Start index of processed data slice
        :param data_slice_stop_ind: Stop index of processed data slice
        """

        self.data = data
        self.dates = list(self.data.index.values)

        self.data_slice_start_ind = data_slice_start_ind
        self.data_slice_stop_ind = data_slice_stop_ind
        self.data_slice = data[data_slice_start_ind:data_slice_stop_ind]
        self.data_slice_dates = list(self.data_slice.index.values)

        self.sell_trigger_values = []
        self.buy_trigger_values = []

        self.sell_trigger_dates = []
        self.buy_trigger_dates = []

        self.buy_sell_labels = None

        # --------------------- List close/open values
        # ... in data
        self.data_open_values = []
        self.data_close_values = []

        for index, row in self.data.iterrows():
            self.data_close_values.append(row['Close'])
            self.data_open_values.append(row['Open'])

        # ... in data slice
        self.data_slice_open_values = []
        self.data_slice_close_values = []

        for index, row in self.data_slice.iterrows():
            self.data_slice_close_values.append(row['Close'])
            self.data_slice_open_values.append(row['Open'])

        # --------------------- List Volume values
        # ... in data slice
        self.volume = []
        for index, row in self.data_slice.iterrows():
            self.volume.append(row['Volume'])

        # ------- Calculate value fluctuation for each point in data slice
        values_fluctuation = []
        for i in range(len(self.data_slice)):
            values_fluctuation.append(self.data_slice_close_values[i] - self.data_slice_open_values[i])

        self.values_fluctuation = values_fluctuation

        # -------Calculate open/close values gradient:
        close_values_gradient = np.gradient(self.data_slice_close_values)
        open_values_gradient = np.gradient(self.data_slice_open_values)

        self.close_values_gradient = close_values_gradient
        self.open_values_gradient = open_values_gradient

        # -----------------Bear/Bullish continuous signal of dataset gradient
        from PhyTrade.Tools.MATH_tools import MATH

        avg_gradient = []

        # Obtaining the average gradient
        for i in range(len(self.data_slice)):
            avg_gradient.append(
                (self.close_values_gradient[i] + self.open_values_gradient[i]) / 2)

        # Normalising avg gradient values between -1 and 1
        avg_gradient_bb_signal = MATH().normalise_minus_one_one(avg_gradient)

        self.oc_avg_gradient_bb_signal = avg_gradient_bb_signal
