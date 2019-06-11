"""
This script contains the Volatility class for all calculations relating to Volatility

Victor Guillet
11/12/2018
"""

from PhyTrade.Tools.MATH_tools import MATH_tools
import statistics as st
import numpy as np


class VOLATILITY:
    def __init__(self, big_data, timeframe=10, amplification_factor=1):
        """
        Calculate and generates amp_coef list based on volatility to be used as an amplification signal

        :param big_data: BIGDATA class instance
        :param timeframe: Timeframe parameter to be used
        :param amplification_factor: Amplification factor of the signal
        """

        self.timeframe = timeframe
        self.volatility = []

        for i in range(len(big_data.data_slice)):

            timeframe_close_values = []

            for j in range(self.timeframe):
                timeframe_close_values.append(big_data.data_close_values[big_data.data_slice_start_ind + (i - j)])

            self.timeframe_std_dev = st.stdev(timeframe_close_values)
            annualisation_factor = np.sqrt(252/self.timeframe)

            annualised_volatility = self.timeframe_std_dev*annualisation_factor

            self.volatility.append(annualised_volatility)

        # Normalising volatility signal values between 0 and 1
        self.amp_coef = MATH_tools().normalise_zero_one(self.volatility)

        # Amplifying volatility signal
        self.amp_coef = MATH_tools().amplify(self.amp_coef, amplification_factor)
