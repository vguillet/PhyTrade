"""
This script enables computing the SMA indicator
It is currently optimised for Quandl data
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

    # ____________________________________________________________________
    # -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------

    def plot_sma(self, big_data, plot_sma_1=True, plot_sma_2=True, plot_trigger_signals=True):
        import matplotlib.pyplot as plt

        if plot_sma_1:
            plt.plot(big_data.data_slice_dates, self.sma_1, label="SMA 1")          # Plot SMA_1

        if plot_sma_2:
            plt.plot(big_data.data_slice_dates, self.sma_2, label="SMA 2")          # Plot SMA_2

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_SMA, label="Sell trigger")       # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_SMA, label="Buy trigger")          # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("SMI")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("SMI")