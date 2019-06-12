
"""
This script contains the BIGDATA class, necessary to collect and move around data in the model generation prototypes

Victor Guillet
11/28/2018
"""

import numpy as np


class BIGDATA:
    def __init__(self, data_slice):
        """
        Contains all the information relating to a specific analysis,
        modules can be called, and their instance attribute should be saved in the big_data instance
        (to enable attribute access anywhere inm the model).
        To compute specific attributes, run the corresponding Technical_Indicators/modules.
        The list of all options can be found in the PhyTrade Library file

        :param data_slice: DATA_SLICE class instance
        """

        self.data_slice = data_slice

        self.sell_trigger_values = []
        self.buy_trigger_values = []

        self.sell_trigger_dates = []
        self.buy_trigger_dates = []

        # ------- Calculate value fluctuation for each point in data slice
        self.values_fluctuation = np.zeros(self.data_slice.slice_size)

        for i in range(self.data_slice.slice_size):
            self.values_fluctuation[i] = self.data_slice.sliced_data.iloc[i, 5] - self.data_slice.sliced_data.iloc[i, 4]

        # -------Calculate open/close values gradient:
        self.close_values_gradient = np.gradient(self.data_slice.sliced_data["Close"])
        self.open_values_gradient = np.gradient(self.data_slice.sliced_data["Open"])

        # -----------------Bear/Bullish continuous signal of dataset gradient
        from PhyTrade.Tools.MATH_tools import MATH_tools

        avg_gradient = np.zeros(self.data_slice.slice_size)

        # Obtaining the average gradient
        for i in range(self.data_slice.slice_size):
            avg_gradient[i] = (self.close_values_gradient[i] + self.open_values_gradient[i]) / 2

        # Normalising avg gradient values between -1 and 1
        avg_gradient_bb_signal = MATH_tools().normalise_minus_one_one(avg_gradient)

        self.oc_avg_gradient_bb_signal = avg_gradient_bb_signal
