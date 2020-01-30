
################################################################################################################
"""
Used for generating time series plots
"""

# Libs
import matplotlib.pyplot as plt
import pandas as pd

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class PLOT_tools:
    @staticmethod
    def plot_trade_process(data_slice,
                           trade_spline, upper_threshold_spline, lower_threshold_spline, trade_signal):
        """
        Generates a two part plot, with the opening/closing prices at the top,
        and the trading/indicator splines at the bottom

        :param data_slice:
        :param trade_spline:
        :param upper_threshold_spline:
        :param lower_threshold_spline:
        :param trade_signal:
        :param indicator_splines:
        :return:
        """
        plot_tools = PLOT_tools()

        fig = plt.figure(figsize=(10, 5), dpi=150)

        # ------------------ Plot Open/Close prices
        ax1 = plt.subplot(211)
        plot_tools.plot_oc_values(data_slice)
        plot_tools.plot_values_trigger(data_slice, trade_signal)
        plt.title("Trade process: " + data_slice.ticker + "        " + data_slice.start_date + " --> " + data_slice.stop_date)

        # ------------------ Plot bb signal(s)
        ax2 = plt.subplot(212)
        plot_tools.plot_spline(data_slice, trade_spline, color="y")
        plot_tools.plot_spline(data_slice, upper_threshold_spline)
        plot_tools.plot_spline(data_slice, lower_threshold_spline)
        plot_tools.plot_spline_trigger(data_slice, trade_spline, trade_signal)

        print("===============================================================================================", len(trade_spline), len(data_slice.sliced_data["Date"]))
        # --> Format resulting plot
        # ax1.get_shared_x_axes().join(ax1, ax2)
        # ax2.set_xticklabels([])

        plt.show()

    @staticmethod
    def plot_oc_values(data_slice, plot_close_values=True, plot_open_values=True):
        """
        :param data_slice: DATA_SLICE class instance
        :param plot_close_values: Plot close values
        :param plot_open_values:  Plot open values
        """

        datelist = list(pd.to_datetime(date) for date in data_slice.sliced_data["Date"])

        if plot_close_values:
            plt.plot(datelist, list(data_slice.sliced_data["Close"]),
                     linewidth=1, label="Close values")   # Plot closing value

        if plot_open_values:
            plt.plot(datelist, list(data_slice.sliced_data["Open"]),
                     linewidth=1, label="Open values")

        plt.title("Open and close values")
        plt.xlabel("Trade date")
        plt.ylabel("Value")

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=19)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=21)

    @staticmethod
    def plot_spline(data_slice, spline, label=None, color='g'):
        """
        Plot a spline against its corresponding dataslice
        """

        datelist = list(pd.to_datetime(date) for date in data_slice.sliced_data["Date"])

        if label is not None:
            plt.plot(datelist, spline, linewidth=1, label=label, c=color)
            plt.legend()
        else:
            plt.plot(datelist, spline, linewidth=1, c=color)

        plt.title("Splines")
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")

        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=19)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=21)

    @staticmethod
    def plot_spline_trigger(data_slice, trade_spline, trade_signal):
        """
        Plot inputted trigger values on spline plot
        """
        buy_spline_values = []
        buy_dates = []
        sell_spline_values = []
        sell_dates = []

        for i in range(len(trade_signal)):
            if trade_signal[i] == 1:
                sell_spline_values.append(trade_spline[i])
                sell_dates.append(list(data_slice.sliced_data["Date"])[i])

            elif trade_signal[i] == -1:
                buy_spline_values.append(trade_spline[i])
                buy_dates.append(list(data_slice.sliced_data["Date"])[i])

        plt.scatter(sell_dates, sell_spline_values, label="Sell trigger")
        plt.scatter(buy_dates, buy_spline_values, label="Buy trigger")

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=19)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=21)

    @staticmethod
    def plot_values_trigger(data_slice, trade_signal):
        """
        Plot inputted trigger values on open/close price plot
        """
        buy_values = []
        buy_dates = []
        sell_values = []
        sell_dates = []

        for i in range(len(trade_signal)):
            if trade_signal[i] == 1:
                sell_values.append(data_slice.sliced_data_selection[i])
                sell_dates.append(list(data_slice.sliced_data["Date"])[i])

            elif trade_signal[i] == -1:
                buy_values.append(data_slice.sliced_data_selection[i])
                buy_dates.append(list(data_slice.sliced_data["Date"])[i])

        plt.scatter(sell_dates, sell_values, label="Sell trigger")
        plt.scatter(buy_dates, buy_values, label="Buy trigger")

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=19)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=21)
