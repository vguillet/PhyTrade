"""
This script contains the Volatility class for all calculations relating to Volatility

Victor Guillet
11/12/2018
"""


class VOLATILITY:
    def __init__(self, big_data, timeframe=10):
        import numpy as np
        import statistics as st
        
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

        # Normalising volatility signal values between -1 and 1
        self.amp_coef = []

        for i in range(len(big_data.data_slice)):
            self.amp_coef.append(
                (self.volatility[i] - min(self.volatility)) / (max(self.volatility) - min(self.volatility)))

