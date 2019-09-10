
##################################################################################################################
"""
Used for plotting the opening and close value of stocks of a data slice
"""

# Libs
import matplotlib.pyplot as plt

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class OC:
    @staticmethod
    def calc_trigger_values(big_data, sell_dates, buy_dates):
        """
        :param big_data: BIGDATA class instance
        :param sell_dates: Sell dates triggers
        :param buy_dates: Buy dates triggers
        :return:
        """

        sell_values = []
        buy_values = []

        for i in range(len(sell_dates)):
            sell_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(sell_dates[i])])

        for i in range(len(buy_dates)):
            buy_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(buy_dates[i])])

        return sell_values, buy_values

    @staticmethod
    def plot_oc_values(big_data, plot_close_values=True, plot_open_values=True):
        """
        :param big_data: BIGDATA class instance
        :param plot_close_values: Plot close values
        :param plot_open_values:  Plot open values
        """

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
    def plot_oc_values_diff(big_data):
        """
        Plot the difference in opening/closing prices

        :param big_data: BIGDATA class instance
        """

        plt.plot(big_data.data_slice_dates, big_data.values_fluctuation, linewidth=1, label="Values fluctuation")

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Open and close values fluctuation")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Value fluctuation")

    @staticmethod
    def plot_trigger_values(big_data, sell_dates, buy_dates):
        """
        Plot inputted trigger values on open/close price plot

        :param big_data: BIGDATA class instance
        :param sell_dates: Sell dates triggers
        :param buy_dates: Buy dates triggers
        """

        sell_values, buy_values = OC().calc_trigger_values(big_data, sell_dates, buy_dates)

        plt.scatter(sell_dates, sell_values, label="Sell triggers")   # Plot sell signals
        plt.scatter(buy_dates, buy_values, label="Buy triggers")      # Plot buy signals
        # plt.legend()
