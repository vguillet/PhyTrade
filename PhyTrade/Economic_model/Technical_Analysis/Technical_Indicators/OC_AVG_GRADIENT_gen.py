
##################################################################################################################
"""
Used to compute the open close average gradient indicator.
"""

# Libs
import numpy as np

# Own modules
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class OC_AVG_GRADIENT(ABSTRACT_indicator):
    def __init__(self, big_data):
        # ------- Calculate value fluctuation for each point in data slice
        self.values_fluctuation = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):
            self.values_fluctuation[i] = big_data.data_slice.sliced_data.iloc[i, 5] - big_data.data_slice.sliced_data.iloc[i, 4]

        # -------Calculate open/close values gradient:
        self.close_values_gradient = np.gradient(big_data.data_slice.sliced_data["Close"])
        self.open_values_gradient = np.gradient(big_data.data_slice.sliced_data["Open"])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):

        # ----------------- Bear/Bullish continuous signal of dataset gradient
        from PhyTrade.Tools.MATH_tools import MATH_tools

        avg_gradient = np.zeros(big_data.data_slice.slice_size)

        # --> Obtaining the average gradient
        for i in range(big_data.data_slice.slice_size):
            avg_gradient[i] = (self.close_values_gradient[i] + self.open_values_gradient[i]) / 2

        # --> Normalising avg gradient values between -1 and 1
        # avg_gradient_bb_signal = MATH_tools().normalise_minus_one_one(avg_gradient)
        avg_gradient_bb_signal = MATH_tools().alignator_minus_one_one(avg_gradient, signal_max=10, signal_min=-10)

        self.bb_signal = avg_gradient_bb_signal
