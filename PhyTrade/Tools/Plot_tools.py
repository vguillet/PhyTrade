
################################################################################################################
"""
Used for generating time series plots
"""

# Libs
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mpl_dates

import pandas as pd

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Plot_tools:
    @staticmethod
    def plot_trade_process(settings,
                           data_slice,
                           trade_spline, trade_upper_threshold, trade_lower_threshold, trade_signal,
                           trading_indicators):
        """
        Generates a two part plot, with the opening/closing prices at the top,
        and the trading/indicator splines at the bottom

        :param settings:
        :param data_slice:
        :param trade_spline:
        :param trade_upper_threshold:
        :param trade_lower_threshold:
        :param trade_signal:
        :param trading_indicators:
        """

        # --> Gathering print settings
        print_indicators_settings = {"rsi": settings.individual_settings.print_rsi,
                                     "sma": settings.individual_settings.print_sma,
                                     "ema": settings.individual_settings.print_ema,
                                     "lwma": settings.individual_settings.print_lwma,
                                     "cci": settings.individual_settings.print_cci,
                                     "eom": settings.individual_settings.print_eom,
                                     "oc_gradient": settings.individual_settings.print_oc_gradient}

        plot_tools = Plot_tools()
        datelist = list(date for date in data_slice.subslice_data["Date"])

        fig = plt.figure(figsize=(14, 10), dpi=150)
        fig.tight_layout()
        gs1 = gridspec.GridSpec(2, 1, height_ratios=[5, 2], bottom=0.5, hspace=0.00, figure=fig)
        gs2 = gridspec.GridSpec(1, 1, height_ratios=[2], top=0.45, figure=fig)

        # ------------------ Plot Open/Close prices
        ax1 = fig.add_subplot(gs1[0, 0])
        # plot_tools.plot_candlesticks(data_slice)

        plot_tools.plot_oc_values(data_slice=data_slice)

        plot_tools.plot_values_trigger(data_slice=data_slice,
                                       trade_signal=trade_signal)

        plt.title("Trade process: " + data_slice.ticker + "        " + str(data_slice.subslice_start_date) + " --> " + str(data_slice.subslice_stop_date))
        plt.xlabel("")

        # ------------------ Plot Volume
        ax2 = fig.add_subplot(gs1[1, 0], sharex=ax1)
        # ax2 = fig.add_subplot(gs1[1, 0])

        plot_tools.plot_volume(data_slice=data_slice)
        plt.xlabel("")

        # --> Formatting obtained plot
        ax1.get_xaxis().set_ticklabels([])
        ax2.get_xaxis().set_ticklabels([])

        plt.xlim(datelist[0], datelist[-1])

        # ------------------ Plot bb signal(s)
        ax3 = fig.add_subplot(gs2[0, 0])

        # --> Plot BB signal
        plot_tools.plot_spline(data_slice=data_slice,
                               spline=trade_spline,
                               type="Trading",
                               color="y",
                               line_thickness=2,
                               label="BB signal")

        # --> Plot Thresholds
        plot_tools.plot_spline(data_slice=data_slice,
                               spline=trade_upper_threshold,
                               type="Trading",
                               label="Thresholds")

        plot_tools.plot_spline(data_slice=data_slice,
                               spline=trade_lower_threshold,
                               type="Trading")

        # --> Plot trigger points and highlight sections
        plot_tools.plot_spline_trigger(data_slice=data_slice,
                                       trade_spline=trade_spline,
                                       trade_signal=trade_signal)

        # plot_tools.plot_spline_highlight(data_slice, trade_signal, trade_upper_threshold, trade_lower_threshold)

        # --> Plot trading indicators splines
        for indicator_type in trading_indicators.keys():
            if print_indicators_settings[indicator_type] is True:
                for trading_indicator_spline in trading_indicators[indicator_type]:
                    plot_tools.plot_spline(data_slice=data_slice,
                                           spline=trading_indicator_spline,
                                           type="Trading",
                                           color="k")

        # --> Formatting obtained plot
        plt.xlim(datelist[0], datelist[-1])
        plt.gcf().autofmt_xdate()

        plt.show()

        # plot_tools.plot_candlesticks(data_slice)

    @staticmethod
    def plot_candlesticks(data_slice):
        # --> Plot candlesticks
        # import mplfinance as mpf
        #
        # ohlc = data_slice.subslice_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        # ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        # ohlc = ohlc.set_index('Date')
        # mpf.plot(ohlc, type='candlestick', volume=False)

        import matplotlib as mpl
        import matplotlib.pyplot as plt

        # TODO: Fix candlestick chart

        # ---- Function to draw candlestick
        def draw_candlestick(axis, index, data, color_up, color_down):

            # Check if stock closed higher or not
            if data['Close'] > data['Open']:
                color = color_up
            else:
                color = color_down

            # Plot the candle wick
            axis.plot([index, index], [data['Low'], data['High']], linewidth=1.5, color='black',
                      solid_capstyle='round', zorder=2)

            # Draw the candle body
            rect = mpl.patches.Rectangle((index - 0.25, data['Open']), 0.5, (data['Close'] - data['Open']),
                                         facecolor=color, edgecolor='black', linewidth=1.5, zorder=3)

            # Add candle body to the axis
            axis.add_patch(rect)

            # Return modified axis
            return axis

        # General plot parameters
        mpl.rcParams['font.family'] = 'Avenir'
        mpl.rcParams['font.size'] = 18

        mpl.rcParams['axes.linewidth'] = 0
        mpl.rcParams['axes.facecolor'] = '#ededed'

        mpl.rcParams['xtick.major.size'] = 0
        mpl.rcParams['xtick.major.pad'] = 10
        mpl.rcParams['ytick.major.size'] = 0
        mpl.rcParams['ytick.major.pad'] = 10

        # Create figure and axes
        fig = plt.figure(figsize=(10, 5), facecolor='white')
        ax = fig.add_subplot(111)

        # Grid lines
        ax.grid(linestyle='-', linewidth=2, color='white', zorder=1)

        # Draw candlesticks
        for day in range(data_slice.subslice_size):
            ax = draw_candlestick(axis=ax,
                                  index=day,
                                  data=data_slice.subslice_data.iloc[day],
                                  color_up='#ff4500',
                                  color_down='#800080')

        # Append ticker symbol
        ax.text(0, 1.05, data_slice.ticker, va='baseline', ha='left', size=30, transform=ax.transAxes)

    @staticmethod
    def plot_oc_values(data_slice, plot_close_values=True, plot_open_values=True):
        """
        :param data_slice: DATA_SLICE class instance
        :param plot_close_values: Plot close values
        :param plot_open_values:  Plot open values
        """

        # ---> Calculating boilinger bands
        window = 20

        # datelist = list(pd.to_datetime(date) for date in data_slice.subslice_data["Date"])

        # --> Plot close values and boilinger bands
        if plot_close_values:
            plt.plot_date(data_slice.subslice_data["Date"], list(data_slice.subslice_data["Close"]), "-", linewidth=2, label="Close values", color="#1f77b4")   # Plot closing value
            plt.plot_date(data_slice.subslice_data["Date"], data_slice.subslice_data["close_upper_band"], "r--", linewidth=1, color="#1f77b4")
            plt.plot_date(data_slice.subslice_data["Date"], data_slice.subslice_data["close_lower_band"], "r--", linewidth=1, color="#1f77b4")

        # --> Plot open values and boilinger bands
        if plot_open_values:
            plt.plot_date(data_slice.subslice_data["Date"], list(data_slice.subslice_data["Open"]), "-", linewidth=2, label="Open values", color="#FFA500")
            plt.plot_date(data_slice.subslice_data["Date"], data_slice.subslice_data["open_upper_band"], "r--", linewidth=1, color="#FFA500")
            plt.plot_date(data_slice.subslice_data["Date"], data_slice.subslice_data["open_lower_band"], "r--", linewidth=1, color="#FFA500")

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

        plt.bar(data_slice.subslice_data["Date"], data_slice.subslice_data["Volume"], zorder=5)

        plt.xlabel("Trade date")
        plt.ylabel("Volume")

        plt.gcf().autofmt_xdate()

        plt.minorticks_on()
        plt.grid(which='minor', color='#e5e5e5', linestyle=':', zorder=3)
        plt.grid(which='major', color='#d1cfcf', linestyle='--', zorder=4)

    @staticmethod
    def plot_spline(data_slice, spline, type=None, label=None, color='g', line_thickness=1):
        """
        Plot a spline against its corresponding dataslice
        """

        if type is None:
            if label is not None:
                plt.plot(range(len(spline)), spline, linewidth=line_thickness, label=label, c=color)
                plt.legend()
            else:
                plt.plot(range(len(spline)), spline, linewidth=line_thickness, c=color)

            plt.xlabel("Time")

        if type == "Trading":
            if label is not None:
                plt.plot(data_slice.subslice_data["Date"], spline, linewidth=line_thickness, label=label, c=color)
                plt.legend()
            else:
                plt.plot(data_slice.subslice_data["Date"], spline, linewidth=line_thickness, c=color)

            plt.xlabel("Trade date")
            plt.gcf().autofmt_xdate()

        plt.ylabel("Buy <-- Signal strength --> Sell")

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
                sell_dates.append(data_slice.subslice_data["Date"].iloc[i])
                # sell_dates.append(i)

            elif trade_signal[i] == -1:
                buy_spline_values.append(trade_spline[i])
                buy_dates.append(data_slice.subslice_data["Date"].iloc[i])
                # buy_dates.append(i)

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
