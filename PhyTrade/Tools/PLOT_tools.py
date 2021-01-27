
################################################################################################################
"""
Used for generating time series plots
"""

# Libs
import matplotlib.pyplot as plt
from matplotlib import gridspec
import pandas as pd

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class PLOT_tools:
    @staticmethod
    def plot_trade_process(data_slice,
                           trade_spline, trade_upper_threshold, trade_lower_threshold, trade_signal,
                           trading_indicators, print_indicators_settings):
        """
        Generates a two part plot, with the opening/closing prices at the top,
        and the trading/indicator splines at the bottom

        :param data_slice:
        :param trade_spline:
        :param trade_upper_threshold:
        :param trade_lower_threshold:
        :param trade_signal:
        :param trading_indicators:
        :param print_indicators_settings:
        """

        plot_tools = PLOT_tools()
        datelist = list(pd.to_datetime(date) for date in data_slice.subslice_data["Date"])

        fig = plt.figure(figsize=(14, 10), dpi=150)
        fig.tight_layout()
        gs1 = gridspec.GridSpec(2, 1, height_ratios=[5, 2], bottom=0.5, hspace=0.00, figure=fig)
        gs2 = gridspec.GridSpec(1, 1, height_ratios=[2], top=0.45, figure=fig)

        # ------------------ Plot Open/Close prices
        ax1 = fig.add_subplot(gs1[0, 0])
        plot_tools.plot_oc_values(data_slice)
        plot_tools.plot_values_trigger(data_slice, trade_signal)
        plt.title("Trade process: " + data_slice.ticker + "        " + data_slice.subslice_start_date + " --> " + data_slice.subslice_stop_date)
        plt.xlabel("")

        # ------------------ Plot Volume
        ax2 = fig.add_subplot(gs1[1, 0], sharex=ax1)
        plot_tools.plot_volume(data_slice)
        plt.xlabel("")

        # --> Formatting obtained plot
        ax1.get_xaxis().set_ticklabels([])
        ax2.get_xaxis().set_ticklabels([])

        plt.xlim(datelist[0], datelist[-1])

        # ------------------ Plot bb signal(s)
        ax3 = fig.add_subplot(gs2[0, 0])
        # --> Plot BB signal
        plot_tools.plot_spline(data_slice, trade_spline, color="y", line_thickness=2, label="BB signal")

        # --> Plot Thresholds
        plot_tools.plot_spline(data_slice, trade_upper_threshold, label="Thresholds")
        plot_tools.plot_spline(data_slice, trade_lower_threshold)

        # --> Plot trigger points and highlight sections
        plot_tools.plot_spline_trigger(data_slice, trade_spline, trade_signal)
        # plot_tools.plot_spline_highlight(data_slice, trade_signal, trade_upper_threshold, trade_lower_threshold)

        # --> Plot trading indicators splines
        for indicator_type in trading_indicators.keys():
            if print_indicators_settings[indicator_type] is True:
                for trading_indicator_spline in trading_indicators[indicator_type]:
                    plot_tools.plot_spline(data_slice, trading_indicator_spline, color="k")

        # --> Formatting obtained plot
        plt.xlim(datelist[0], datelist[-1])
        plt.gcf().autofmt_xdate()

        plt.show()

        # plot_tools.plot_candlesticks(data_slice)

    @staticmethod
    def plot_candlesticks(data_slice):
        # --> Plot candlesticks
        import mplfinance as mpf

        ohlc = data_slice.subslice_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        ohlc = ohlc.set_index('Date')
        mpf.plot(ohlc, type='candle', volume=True)

    @staticmethod
    def plot_oc_values(data_slice, plot_close_values=True, plot_open_values=True):
        """
        :param data_slice: DATA_SLICE class instance
        :param plot_close_values: Plot close values
        :param plot_open_values:  Plot open values
        """

        # ---> Calculating boilinger bands
        window = 20

        datelist = list(pd.to_datetime(date) for date in data_slice.subslice_data["Date"])

        # --> Plot close values and boilinger bands
        if plot_close_values:
            plt.plot(datelist, list(data_slice.subslice_data["Close"]),
                     linewidth=2, label="Close values", color="#1f77b4")   # Plot closing value
            plt.plot(datelist, data_slice.subslice_data["close_upper_band"], "r--", linewidth=1, color="#1f77b4")
            plt.plot(datelist, data_slice.subslice_data["close_lower_band"], "r--", linewidth=1, color="#1f77b4")

        # --> Plot open values and boilinger bands
        if plot_open_values:
            plt.plot(datelist, list(data_slice.subslice_data["Open"]),
                     linewidth=2, label="Open values", color="#FFA500")
            plt.plot(datelist, data_slice.subslice_data["open_upper_band"], "r--", linewidth=1, color="#FFA500")
            plt.plot(datelist, data_slice.subslice_data["open_lower_band"], "r--", linewidth=1, color="#FFA500")

        plt.title("Open and close values")
        plt.xlabel("Trade date")
        plt.ylabel("Price")

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)

    @staticmethod
    def plot_volume(data_slice):

        datelist = list(pd.to_datetime(date) for date in data_slice.subslice_data["Date"])

        plt.bar(datelist, data_slice.subslice_data["Volume"], zorder=5)

        plt.xlabel("Trade date")
        plt.ylabel("Volume")

        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)

    @staticmethod
    def plot_spline(data_slice, spline, label=None, color='g', line_thickness=1):
        """
        Plot a spline against its corresponding dataslice
        """

        datelist = list(pd.to_datetime(date) for date in data_slice.subslice_data["Date"])

        if label is not None:
            plt.plot(datelist, spline, linewidth=line_thickness, label=label, c=color)
            plt.legend()
        else:
            plt.plot(datelist, spline, linewidth=line_thickness, c=color)

        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal strength --> Sell")

        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)

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
                sell_dates.append(list(data_slice.subslice_data["Date"])[i])

            elif trade_signal[i] == -1:
                buy_spline_values.append(trade_spline[i])
                buy_dates.append(list(data_slice.subslice_data["Date"])[i])

        plt.scatter(sell_dates, sell_spline_values, label="Sell trigger", zorder=6)
        plt.scatter(buy_dates, buy_spline_values, label="Buy trigger", zorder=6)

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)

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
                sell_values.append(data_slice.subslice_data_selection[i])
                sell_dates.append(list(data_slice.subslice_data["Date"])[i])

            elif trade_signal[i] == -1:
                buy_values.append(data_slice.subslice_data_selection[i])
                buy_dates.append(list(data_slice.subslice_data["Date"])[i])

        plt.scatter(sell_dates, sell_values, label="Sell trigger", zorder=6)
        plt.scatter(buy_dates, buy_values, label="Buy trigger", zorder=6)

        plt.legend()
        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)
