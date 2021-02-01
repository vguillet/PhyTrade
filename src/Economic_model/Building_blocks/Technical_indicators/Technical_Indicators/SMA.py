
##################################################################################################################
"""
Used for computing the SMA indicator
"""

# Libs
import numpy as np

# Own modules
from src.Economic_model.Building_blocks.Technical_indicators.Technical_Indicators.Indicator_abc import Indicator_abc

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class SMA(Indicator_abc):
    def __init__(self, big_data, timeperiod_1=50, timeperiod_2=200):
        """
        Generates an SMA indicator instance

        :param big_data: BIGDATA class instance
        :param timeperiod_1: First Timeframe parameter to be used
        :param timeperiod_2: Second Timeframe parameter to be used
        """
        # --> SMA initialisation
        self.timeperiod_1 = timeperiod_1
        self.timeperiod_2 = timeperiod_2

        # -------------------------- SMA CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + max timeframe
        sma_df = big_data.data_slice.data[big_data.data_slice.subslice_start_index-max(self.timeperiod_1, timeperiod_2):
                                          big_data.data_slice.subslice_stop_index]

        sma_1 = sma_df[big_data.data_slice.price_data_selection].rolling(window=self.timeperiod_1, center=False).mean()
        sma_2 = sma_df[big_data.data_slice.price_data_selection].rolling(window=self.timeperiod_2, center=False).mean()

        self.sma_1 = np.array(sma_1.values[self.timeperiod_1:])
        self.sma_2 = np.array(sma_2.values[self.timeperiod_2:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        """
        Generate SMA indicator output

        :param big_data: BIGDATA class instance
        :param include_triggers_in_bb_signal: Maximise/minimise bb signal when SMAs cross
        """
        from src.Tools.Math_tools import Math_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = np.zeros(big_data.data_slice.subslice_size)

        for i in range(big_data.data_slice.subslice_size):
            self.bb_signal[i] = (self.sma_1[i] - self.sma_2[i])/2

        # --> Normalising sma bb signal values between -1 and 1
        # self.bb_signal = Math_tools().normalise_minus_one_one(self.bb_signal)
        self.bb_signal = Math_tools().alignator_minus_one_one(signal=self.bb_signal,
                                                              signal_max=15,
                                                              signal_min=-15)

        if include_triggers_in_bb_signal:
            # ----------------- Trigger points determination
            # sma config can take two values, 0 for when sma_1 is higher than sma_2, and 2 for the other way around
            if self.sma_1[0] > self.sma_2[0]:
                sma_config = 0
            else:
                sma_config = 1

            for i in range(big_data.data_slice.subslice_size):
                if sma_config == 0:
                    if self.sma_2[i] > self.sma_1[i]:
                        self.bb_signal[i] = 1
                        sma_config = 1
                else:
                    if self.sma_1[i] > self.sma_2[i]:
                        self.bb_signal[i] = -1
                        sma_config = 0
