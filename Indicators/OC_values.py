"""
This scripts enable plotting the opening and close value of stocks of a data slice
"""


class OC:
    def __init__(self, big_data):

        self.big_data = big_data
        import numpy as np

        # -------Calculate value fluctuation for each point
        values_fluctuation = []
        for i in range(len(big_data.data_slice)):
            values_fluctuation.append(big_data.close_values[i] - big_data.open_values[i])

        setattr(big_data, "data_slice_values_fluctuation", values_fluctuation)

        # -------Calculate open/close values gradient:

        close_values_gradient = np.gradient(big_data.close_values)
        open_values_gradient = np.gradient(big_data.open_values)

        setattr(big_data, "close_values_gradient", close_values_gradient)
        setattr(big_data, "open_values_gradient", open_values_gradient)

    def plot_open_close_values(self):
        import matplotlib.pyplot as plt

        plt.plot(self.big_data.data_slice_dates, self.big_data.close_values)                # Plot closing value
        plt.plot(self.big_data.data_slice_dates, self.big_data.open_values)                 # Plot opening value

        plt.scatter(self.big_data.rsi_sell_dates, self.big_data.rsi_sell_values)           # Plot sell signals
        plt.scatter(self.big_data.rsi_buy_dates, self.big_data.rsi_buy_values)             # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.title("Open and close values")
        plt.grid()
        plt.xlabel("Trade date")
        plt.ylabel("Value")

    def plot_open_close_values_diff(self):
        import matplotlib.pyplot as plt

        plt.plot(self.big_data.data_slice_dates, self.big_data.data_slice_values_fluctuation)      # Plot value fluctuation

        plt.scatter(self.big_data.rsi_sell_dates, self.big_data.sell_values)    # Plot sell signals
        plt.scatter(self.big_data.rsi_buy_dates, self.big_data.buy_values)      # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.title("Open and close values fluctuation")
        plt.grid()
        plt.xlabel("Trade date")
        plt.ylabel("Value fluctuation")
