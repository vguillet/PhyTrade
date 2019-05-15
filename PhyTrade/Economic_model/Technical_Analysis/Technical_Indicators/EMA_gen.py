# TODO create EMA indicator class

"""
This script enables computing the EMA indicator

Victor Guillet
11/28/2018
"""


class EMA:
    def __init__(self, big_data, timeperiod_1=12, timeperiod_2=26):
        self.timeperiod_1 = timeperiod_1
        self.timeperiod_2 = timeperiod_2

        # -------------------------- SMA CALCULATION ---------------------------
        self.sma_1 = []
        self.sma_2 = []

        for i in range(len(big_data.data_slice)):

            # ------------------ Calculate close values falling in timeperiod_1 and 2
            timeperiod_1_close_values = []
            timeperiod_2_close_values = []

            for j in range(self.timeperiod_1):
                timeperiod_1_close_values.append(big_data.data_close_values[big_data.data_slice_start_ind + i - j])

            for j in range(self.timeperiod_2):
                timeperiod_2_close_values.append(big_data.data_close_values[big_data.data_slice_start_ind + i - j])

            # ------------------ Sum close values for timeperiod_1 and 2, and calc sma
            self.sma_1.append(sum(timeperiod_1_close_values)/len(timeperiod_1_close_values))
            self.sma_2.append(sum(timeperiod_2_close_values)/len(timeperiod_2_close_values))

        self.ema_1 = [self.sma_1[0]]
        self.ema_2 = [self.sma_2[0]]

        for i in range(len(big_data.data_slice)):
            # ------------------ Calculate the multiplier for weighting the EMA
            multiplier_1 = 2 / (self.timeperiod_1 + 1)
            multiplier_2 = 2 / (self.timeperiod_2 + 1)

            # ------------------ Calculate the EMA
            if 0 < i:
                self.ema_1.append(big_data.data_close_values[big_data.data_slice_start_ind + i] - self.ema_1[i-1]*multiplier_1 + self.ema_1[i-1])
                self.ema_2.append(big_data.data_close_values[big_data.data_slice_start_ind + i] - self.ema_2[i-1]*multiplier_2 + self.ema_2[i-1])

        # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):

        # ----------------- Trigger points determination
        sell_dates = []
        buy_dates = []

        # ema config can take two values, 0 for when ema_1 is higher than ema_2, and 2 for the other way around
        if self.ema_1[0] > self.ema_2[0]:
            ema_config = 0
        else:
            ema_config = 1

        for i in range(len(big_data.data_slice)):
            if ema_config == 0:
                if self.ema_2[i] > self.ema_1[i]:
                    sell_dates.append(big_data.data_slice_dates[i])
                    ema_config = 1
            else:
                if self.ema_1[i] > self.ema_2[i]:
                    buy_dates.append(big_data.data_slice_dates[i])
                    ema_config = 0

        self.sell_dates = sell_dates
        self.buy_dates = buy_dates

        # ----------------- Bear/Bullish continuous signal
        bb_signal = []

        for i in range(len(big_data.data_slice)):
            bb_signal.append((self.ema_1[i] - self.ema_2[i])/2)

        # Normalising ema bb signal values between -1 and 1
        from PhyTrade.Tools.MATH_tools import MATH

        bb_signal_normalised = MATH().normalise_minus_one_one(bb_signal)

        if include_triggers_in_bb_signal:
            for date in self.sell_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 1

            for date in self.buy_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 0

        self.bb_signal = bb_signal_normalised

    """




    """
    # ------------------------- PLOT SMA ----------------------------------

    def plot_ema(self, big_data, plot_ema_1=True, plot_ema_2=True, plot_trigger_signals=True):
        import matplotlib.pyplot as plt

        if plot_ema_1:
            plt.plot(big_data.data_slice_dates, self.ema_1, label="SMA "+str(self.timeperiod_1)+" days")          # Plot SMA_1

        if plot_ema_2:
            plt.plot(big_data.data_slice_dates, self.ema_2, label="SMA "+str(self.timeperiod_2)+" days")          # Plot SMA_2

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_SMA, label="Sell trigger")       # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_SMA, label="Buy trigger")          # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("SMA")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("SMI")




