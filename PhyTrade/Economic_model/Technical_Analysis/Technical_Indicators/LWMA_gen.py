"""
This script enables computing the LWMA indicator. A linearly weighted moving average (LWMA) is a moving average calculation that more
heavily weights recent price data. The most recent price has the highest weighting, and each prior price has progressively less weight.
The weights drop in a linear fashion. LWMAs are quicker to react to price changes than simple moving averages (SMA) and exponential
moving averages (EMA).

Victor Guillet
11/28/2018
"""
import numpy as np


class LWMA:
    def __init__(self, big_data, lookback_period=10, max_weight=1):
        """
        Generates an LWMA indicator instance

        :param big_data: BIGDATA class
        :param lookback_period: Lookback period to be used, if larger than dataslice length, dataslice length is used
        :param max_weight: Weight given to current day value
        """

        self.lookback_period = lookback_period
        self.lwma = np.zeros(big_data.data_slice.slice_size)

        for i in range(big_data.data_slice.slice_size):

            # --> Adjust timeframe if necessary
            if len(big_data.data_slice.data[:big_data.data_slice.start_index]) < self.lookback_period:
                self.lookback_period = len(big_data.data_slice.data[:big_data.data_slice.start_index])

            # ------------------ Calculate values falling in timeperiod_1 and 2
            lookback_period_values = np.array(big_data.data_slice.data_selection[
                                              big_data.data_slice.start_index + i - self.lookback_period + 1:
                                              big_data.data_slice.start_index + i + 1])[::-1]

            # ---> Compute weights for each days based on max weight param and lookback period
            weights = np.zeros(big_data.data_slice.slice_size)

            for j in range(self.lookback_period):
                weights[j] = max_weight-(max_weight/self.lookback_period)*j
            # print(weights)
            weights = weights[::-1]

            # ---> Compute weighted daily values
            weighted_values = np.zeros(big_data.data_slice.slice_size)
            for j in range(self.lookback_period):
                weighted_values[j] = lookback_period_values[j]*weights[j]

            self.lwma[i] = sum(weighted_values)/sum(weights)

            # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        """
        Generate LWMA indicator output

        :param big_data: BIGDATA class instance
        :param include_triggers_in_bb_signal: Maximise/minimise bb signal when LWMAs crosses daily value
        """

        self.data_values = big_data.data_slice_close_values

        # ----------------- Trigger points determination
        sell_dates = []
        buy_dates = []

        # lwma config can take two values, 0 for when lwma is higher than the close value, and 1 for the other way around
        if self.lwma[0] > self.data_values[0]:
            lwma_config = 0
        else:
            lwma_config = 1

        for i in range(len(big_data.data_slice)):
            if lwma_config == 0:
                if self.data_values[i] > self.lwma[i]:
                    sell_dates.append(big_data.data_slice_dates[i])
                    lwma_config = 1
            else:
                if self.lwma[i] > self.data_values[i]:
                    buy_dates.append(big_data.data_slice_dates[i])
                    lwma_config = 0

        self.sell_dates = sell_dates
        self.buy_dates = buy_dates

        # ----------------- Bear/Bullish continuous signal
        bb_signal = []

        for i in range(len(big_data.data_slice)):
            bb_signal.append((self.lwma[i] - self.data_values[i]) / 2)

        # Normalising lwma bb signal values between -1 and 1
        from PhyTrade.Tools.MATH_tools import MATH_tools

        bb_signal_normalised = MATH_tools().normalise_minus_one_one(bb_signal)

        if include_triggers_in_bb_signal:
            for date in self.sell_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 1

            for date in self.buy_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 0

        self.bb_signal = bb_signal_normalised

    """




    """
    # ------------------------- PLOT LWMA ----------------------------------
    def plot_lwma(self, big_data, plot_lwma=True, plot_trigger_signals=True):
        """
        :param big_data: BIGDATA class instance
        :param plot_lwma: Plot LWMA indicator
        :param plot_trigger_signals: Include trigger signals in plot
        """

        import matplotlib.pyplot as plt

        if plot_lwma:
            plt.plot(big_data.data_slice_dates, self.lwma, label="LWMA " + str(self.lookback_period) + " days")  # Plot LWMA

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_SMA, label="Sell trigger")  # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_SMA, label="Buy trigger")  # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("LWMA")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("LWMA")



