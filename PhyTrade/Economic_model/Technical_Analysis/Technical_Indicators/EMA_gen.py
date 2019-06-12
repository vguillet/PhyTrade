"""
This script enables computing the EMA indicator. An exponential moving average (EMA) is a type of moving average (MA) that places a greater
weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted
moving average. An exponentially weighted moving average reacts more significantly to recent price changes than
a simple moving average (SMA), which applies an equal weight to all observations in the period.

Victor Guillet
11/28/2018
"""
import numpy as np


class EMA:
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
        self.ema_1 = np.zeros(big_data.data_slice.slice_size)
        self.ema_2 = np.zeros(big_data.data_slice.slice_size)

        # --> SMA CALCULATION
        self.sma_1 = np.zeros(big_data.data_slice.slice_size)
        self.sma_2 = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):

            # --> Adjust timeframe if necessary
            if len(big_data.data_slice.data[:big_data.data_slice.start_index]) < self.timeperiod_1:
                self.timeperiod_1 = len(big_data.data_slice.data[:big_data.data_slice.start_index])

            if len(big_data.data_slice.data[:big_data.data_slice.start_index]) < self.timeperiod_2:
                self.timeperiod_2 = len(big_data.data_slice.data[:big_data.data_slice.start_index])

            # ------------------ Calculate values falling in timeperiod_1 and 2
            timeperiod_1_close_values = np.array(big_data.data_slice.data_selection[
                                                 big_data.data_slice.start_index+i-self.timeperiod_1+1:
                                                 big_data.data_slice.start_index+i+1])[::-1]

            timeperiod_2_close_values = np.array(big_data.data_slice.data_selection[
                                                 big_data.data_slice.start_index+i-self.timeperiod_2+1:
                                                 big_data.data_slice.start_index+i+1])[::-1]

            # ------------------ Sum close values for timeperiod_1 and 2, and calc sma
            self.sma_1[i] = sum(timeperiod_1_close_values)/len(timeperiod_1_close_values)
            self.sma_2[i] = sum(timeperiod_2_close_values)/len(timeperiod_2_close_values)

        self.ema_1[0] = self.sma_1[0]
        self.ema_2[0] = self.sma_2[0]

        # ------------------ Calculate the multiplier for weighting the EMA
        multiplier_1 = 2 / (self.timeperiod_1 + 1)
        multiplier_2 = 2 / (self.timeperiod_2 + 1)

        for i in range(1, big_data.data_slice.slice_size):
            # ------------------ Calculate the EMA
            self.ema_1[i] = big_data.data_slice.data_selection[big_data.data_slice.start_index + i] - self.ema_1[i-1]*multiplier_1 + self.ema_1[i-1]
            self.ema_2[i] = big_data.data_slice.data_selection[big_data.data_slice.start_index + i] - self.ema_2[i-1]*multiplier_2 + self.ema_2[i-1]

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

        # Normalising ema bb signal values between -1 and 1
            self.bb_signal = MATH_tools().normalise_minus_one_one(self.bb_signal)

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

    """




    """
    # ------------------------- PLOT SMA ----------------------------------
    def plot_ema(self, big_data, plot_ema_1=True, plot_ema_2=True, plot_trigger_signals=True):
        """
        :param big_data: BIGDATA class instance
        :param plot_ema_1: Plot EMA indicator based on timeperiod_1
        :param plot_ema_2: Plot EMA indicator based on timeperiod_2
        :param plot_trigger_signals: Include trigger signals in plot
        """

        import matplotlib.pyplot as plt

        if plot_ema_1:
            plt.plot(big_data.data_slice_dates, self.ema_1, label="EMA "+str(self.timeperiod_1)+" days")          # Plot SMA_1

        if plot_ema_2:
            plt.plot(big_data.data_slice_dates, self.ema_2, label="EMA "+str(self.timeperiod_2)+" days")          # Plot SMA_2

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_EMA, label="Sell trigger")       # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_EMA, label="Buy trigger")          # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("EMA")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("EMA")




