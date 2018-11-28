"""
This scripts enable plotting the opening and close value of stocks of a data slice

Victor Guillet
11/28/2018
"""


class OC:
    @staticmethod
    def calc_trigger_values(big_data, sell_dates, buy_dates):

        sell_values = []
        buy_values = []

        for i in range(len(sell_dates)):
            sell_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(sell_dates[i])])

        for i in range(len(buy_dates)):
            buy_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(buy_dates[i])])

        big_data.sell_trigger_dates.append(sell_dates)
        big_data.buy_trigger_dates.append(buy_dates)

        big_data.sell_trigger_values.append(sell_values)
        big_data.buy_trigger_values.append(buy_values)

    @staticmethod
    def plot_open_close_values(big_data, plot_close_values=True, plot_open_values=True):
        import matplotlib.pyplot as plt

        if plot_close_values:
            plt.plot(big_data.data_slice_dates, big_data.data_slice_close_values, linewidth=1, label="Close values")   # Plot closing value

        if plot_open_values:
            plt.plot(big_data.data_slice_dates, big_data.data_slice_open_values, linewidth=1, label="Open values")     # Plot opening value

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Open and close values")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Value")

    @staticmethod
    def plot_open_close_values_diff(big_data):
        import matplotlib.pyplot as plt

        plt.plot(big_data.data_slice_dates, big_data.values_fluctuation, linewidth=1, label="Values fluctuation")

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Open and close values fluctuation")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Value fluctuation")

    @staticmethod
    def plot_trigger_values(big_data):
        import matplotlib.pyplot as plt

        plt.scatter(big_data.sell_trigger_dates, big_data.sell_trigger_values, label="Sell triggers")   # Plot sell signals
        plt.scatter(big_data.buy_trigger_dates, big_data.buy_trigger_values, label="Buy triggers")      # Plot buy signals
        plt.legend()
