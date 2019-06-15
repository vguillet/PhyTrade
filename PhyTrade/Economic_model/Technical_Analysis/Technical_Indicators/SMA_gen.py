"""
This script enables computing the SMA indicator

Victor Guillet
11/28/2018
"""
import numpy as np
import pandas as pd


class SMA:
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
        sma_df = big_data.data_slice.data[big_data.data_slice.start_index-max(self.timeperiod_1, timeperiod_2):big_data.data_slice.stop_index]

        sma_1 = pd.rolling_mean(sma_df[big_data.data_slice.selection], window=self.timeperiod_1)
        sma_2 = pd.rolling_mean(sma_df[big_data.data_slice.selection], window=self.timeperiod_2)

        self.sma_1 = sma_1.values[self.timeperiod_1:]
        self.sma_2 = sma_2.values[self.timeperiod_2:]

        # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        """
        Generate SMA indicator output

        :param big_data: BIGDATA class instance
        :param include_triggers_in_bb_signal: Maximise/minimise bb signal when SMAs cross
        """
        from PhyTrade.Tools.MATH_tools import MATH_tools

        # ----------------- Bear/Bullish continuous signal
        self.bb_signal = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):
            self.bb_signal[i] = (self.sma_1[i] - self.sma_2[i])/2

        # Normalising sma bb signal values between -1 and 1
        self.bb_signal = MATH_tools().normalise_minus_one_one(self.bb_signal)

        if include_triggers_in_bb_signal:
            # ----------------- Trigger points determination
            # sma config can take two values, 0 for when sma_1 is higher than sma_2, and 2 for the other way around
            if self.sma_1[0] > self.sma_2[0]:
                sma_config = 0
            else:
                sma_config = 1

            for i in range(big_data.data_slice.slice_size):
                if sma_config == 0:
                    if self.sma_2[i] > self.sma_1[i]:
                        self.bb_signal[i] = 1
                        sma_config = 1
                else:
                    if self.sma_1[i] > self.sma_2[i]:
                        self.bb_signal[i] = -1
                        sma_config = 0

    """




    """
    # ------------------------- PLOT SMA ----------------------------------
    def plot_sma(self, big_data, plot_sma_1=True, plot_sma_2=True, plot_trigger_signals=True):
        """
        :param big_data: BIGDATA class instance
        :param plot_sma_1: Plot SMA indicator based on timeperiod_1
        :param plot_sma_2: Plot SMA indicator based on timeperiod_2
        :param plot_trigger_signals: Include trigger signals in plot
        """

        import matplotlib.pyplot as plt

        if plot_sma_1:
            plt.plot(big_data.data_slice_dates, self.sma_1, label="SMA "+str(self.timeperiod_1)+" days")          # Plot SMA_1

        if plot_sma_2:
            plt.plot(big_data.data_slice_dates, self.sma_2, label="SMA "+str(self.timeperiod_2)+" days")          # Plot SMA_2

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_SMA, label="Sell trigger")       # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_SMA, label="Buy trigger")          # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("SMA")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("SMA")
