"""
This script enables computing the EMA indicator. An exponential moving average (EMA) is a type of moving average (MA) that places a greater
weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted
moving average. An exponentially weighted moving average reacts more significantly to recent price changes than
a simple moving average (SMA), which applies an equal weight to all observations in the period.

Victor Guillet
11/28/2018
"""
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator
import numpy as np


class EMA(ABSTRACT_indicator):
    def __init__(self, big_data, timeperiod_1=12, timeperiod_2=26):
        """
        Generates an EMA indicator instance

        :param big_data: BIGDATA class instance
        :param timeperiod_1: First Timeframe parameter to be used
        :param timeperiod_2: Second Timeframe parameter to be used
        """
        # --> EMA initialisation
        self.timeperiod_1 = timeperiod_1
        self.timeperiod_2 = timeperiod_2

        # -------------------------- EMA CALCULATION ---------------------------
        # --> Slice data to obtain Data falling in data slice + max timeframe
        ewma_df = big_data.data_slice.data[big_data.data_slice.start_index-max(self.timeperiod_1, timeperiod_2):big_data.data_slice.stop_index]

        # TODO: Check whether adjust should be True or False
        ema_1 = ewma_df[big_data.data_slice.selection].ewm(span=self.timeperiod_1, min_periods=0, adjust=True, ignore_na=False).mean()
        ema_2 = ewma_df[big_data.data_slice.selection].ewm(span=self.timeperiod_2, min_periods=0, adjust=True, ignore_na=False).mean()

        self.ema_1 = np.array(ema_1.values[self.timeperiod_1:])
        self.ema_2 = np.array(ema_2.values[self.timeperiod_2:])

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        """
        Generate EMA indicator output

        :param big_data: BIGDATA class instance
        :param include_triggers_in_bb_signal: Maximise/minimise bb signal when EMAs cross
        """
        from PhyTrade.Tools.MATH_tools import MATH_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):
            self.bb_signal[i] = (self.ema_1[i] - self.ema_2[i])/2

        # --> Normalising ema bb signal values between -1 and 1
        # self.bb_signal = MATH_tools().normalise_minus_one_one(self.bb_signal)
        self.bb_signal = MATH_tools().alignator_minus_one_one(self.bb_signal, signal_max=15, signal_min=-15)

        if include_triggers_in_bb_signal:
            # ----------------- Trigger points determination
            # ema config can take two values, 0 for when ema_1 is higher than ema_2, and 2 for the other way around
            if self.ema_1[0] > self.ema_2[0]:
                ema_config = 0
            else:
                ema_config = 1

            for i in range(big_data.data_slice.slice_size):
                if ema_config == 0:
                    if self.ema_2[i] > self.ema_1[i]:
                        self.bb_signal[i] = 1
                        ema_config = 1
                else:
                    if self.ema_1[i] > self.ema_2[i]:
                        self.bb_signal[i] = -1
                        ema_config = 0
