"""
This script enables computing the SMA indicator
It is currently optimised for Quandl data

Victor Guillet
11/28/2018
"""


class SMA:
    def __init__(self, big_data, timeperiod_1=50, timeperiod_2=200):
        self.timeperiod_1 = timeperiod_1
        self.timeperiod_2 = timeperiod_2

        # --------------------------SMA CALCULATION---------------------------
        self.sma_1 = []
        self.sma_2 = []

        for i in range(len(big_data.data_slice)):

            # ------------------Calculate close values falling in timeperiod_1 and 2
            timeperiod_1_close_values = []
            timeperiod_2_close_values = []

            for j in range(self.timeperiod_1):
                timeperiod_1_close_values.append(big_data.data_open_values[big_data.data_slice_start_ind + i - j])

            for j in range(self.timeperiod_2):
                timeperiod_2_close_values.append(big_data.data_open_values[big_data.data_slice_start_ind + i - j])

            # ------------------Sum close values for timeperiod_1 and 2

            self.sma_1.append(sum(timeperiod_1_close_values)/len(timeperiod_1_close_values))
            self.sma_2.append(sum(timeperiod_2_close_values)/len(timeperiod_2_close_values))

        # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):

        # -----------------Trigger points determination
        sell_dates = []
        buy_dates = []

        # sma config can take two values, 0 for when sma_1 is higher than sma_2, and 2 for the other way around
        if self.sma_1[0] > self.sma_2[0]:
            sma_config = 0
        else:
            sma_config = 1

        for i in range(len(big_data.data_slice)):
            if sma_config == 0:
                if self.sma_2[i] > self.sma_1[i]:
                    sell_dates.append(big_data.data_slice_dates[i])
                    sma_config = 1
            else:
                if self.sma_1[i] > self.sma_2[i]:
                    buy_dates.append(big_data.data_slice_dates[i])
                    sma_config = 0

        self.sell_dates = sell_dates
        self.buy_dates = buy_dates

        # -----------------Bear/Bullish continuous signal
        bb_signal = []

        for i in range(len(big_data.data_slice)):
            bb_signal.append((self.sma_1[i] - self.sma_2[i])/2)

        # Normalising sma bb signal values between -1 and 1
        from PhyTrade.Technical_Analysis.Tools.MATH_tools import MATH

        bb_signal_normalised = MATH().normalise_minus_one_one(bb_signal)

        if include_triggers_in_bb_signal:
            for date in self.sell_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 1

            for date in self.buy_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 0

        self.bb_signal = bb_signal_normalised

    """








    """
    # -------------------------PLOT SMA ----------------------------------

    def plot_sma(self, big_data, plot_sma_1=True, plot_sma_2=True, plot_trigger_signals=True):
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
        plt.ylabel("SMI")
