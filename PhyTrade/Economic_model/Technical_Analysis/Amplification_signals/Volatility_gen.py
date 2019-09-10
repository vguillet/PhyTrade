
##################################################################################################################
"""
This script contains the Volatility class for all calculations relating to Volatility
"""

# Built-in/Generic Imports
import statistics as st

# Libs
import numpy as np

# Own modules
from PhyTrade.Tools.MATH_tools import MATH_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/12/2018'

##################################################################################################################


class VOLATILITY:
    def __init__(self, big_data, timeframe=10, amplification_factor=1):
        """
        Calculate and generates amp_coef list based on volatility to be used as an amplification signal

        :param big_data: BIGDATA class instance
        :param timeframe: Timeframe parameter to be used
        :param amplification_factor: Amplification factor of the signal
        """

        # --> VOLATILITY initialisation
        self.timeframe = timeframe

        # -------------------------- VOLATILITY CALCULATION --------------------
        self.volatility = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):
            # --> Adjust timeframe if necessary
            if len(big_data.data_slice.data[:big_data.data_slice.start_index]) < self.timeframe:
                self.timeframe = len(big_data.data_slice.data[:big_data.data_slice.start_index])

            timeframe_values = np.array(big_data.data_slice.data_selection[
                                        big_data.data_slice.start_index+i-self.timeframe+1:
                                        big_data.data_slice.start_index+i+1])[::-1]

            self.timeframe_std_dev = st.stdev(timeframe_values)

            annualised_volatility = self.timeframe_std_dev*np.sqrt(252/self.timeframe)

            self.volatility[i] = annualised_volatility

        # Normalising volatility signal values between 0 and 1
        self.amp_coef = MATH_tools().normalise_zero_one(self.volatility)

        # Amplifying volatility signal
        self.amp_coef = MATH_tools().amplify(self.amp_coef, amplification_factor)
