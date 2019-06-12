"""
This script contains tools for smoothing out and adding up signals, using interpolation and splines

Victor Guillet
11/28/2018
"""
import numpy as np


class SPLINE:
    @staticmethod
    def __init__(big_data):

        x = np.array(range(big_data.data_slice.slice_size))
        xs = np.linspace(0, big_data.data_slice.slice_size, big_data.data_slice.slice_size * big_data.spline_multiplication_coef)

        setattr(big_data, "spline_x", x)
        setattr(big_data, "spline_xs", xs)

    @staticmethod
    def calc_signal_to_spline(big_data, signal, smoothing_factor=0.7):
        from scipy.interpolate import UnivariateSpline

        y = signal
        spline_x = UnivariateSpline(big_data.spline_x, y)
        spline_x.set_smoothing_factor(smoothing_factor)

        spline = spline_x(big_data.spline_xs)

        # Limiting the magnitude of the signal when it reaches values above 1 or below -1
        for i in range(len(spline)):
            if spline[i] > 1:
                spline[i] = 1

            if spline[i] < -1:
                spline[i] = -1

        return spline

    @staticmethod
    def combine_splines(spline_array, weights_array):
        # --> Multiply each spline by its respective weight
        combined_splines = spline_array * weights_array

        # --> Sum all weighted splines into a single one
        combined_splines = combined_splines.sum(axis=0)

        return combined_splines

    @staticmethod
    def shift_spline(spline, index_shift):

        # --> Shifts a spline by index_shift

        shifted_spline = [0]*len(spline)

        if index_shift < 0:
            for i in range(len(spline) + index_shift):
                shifted_spline[i+index_shift] = spline[i]
        else:
            for i in range(len(spline) - index_shift):
                shifted_spline[i+index_shift] = spline[i]

        return shifted_spline

    @staticmethod
    def modulate_amplitude_spline(spline, coef_spline, std_dev_max=5):
        import statistics

        # --> Limiting the magnitude of the signal when it reaches values above a certain number of standard deviation
        coef_spline_standard_dev = statistics.stdev(coef_spline)
        coef_spline_mean = statistics.mean(coef_spline)

        for i in range(len(coef_spline)):
            if coef_spline[i] > 0 and coef_spline[i] - coef_spline_mean > std_dev_max * coef_spline_standard_dev:
                coef_spline[i] = coef_spline_mean + std_dev_max * coef_spline_standard_dev
                continue

            if coef_spline[i] < 0 and abs(coef_spline[i]) + coef_spline_mean > std_dev_max * coef_spline_standard_dev:
                coef_spline[i] = coef_spline_mean - std_dev_max * coef_spline_standard_dev
                continue

        # --> Obtaining absolute and add one
        coef_spline = np.absolute(coef_spline) + 1

        # --> Modulating spline
        spline_modulated = spline * coef_spline

        return spline_modulated         # Modulated spline still requires being normalised

    @staticmethod
    def flip_spline(spline):
        flipped_spline = [-x for x in spline]

        return flipped_spline

    @staticmethod
    def plot_spline(big_data, spline, label, color='g'):
        import matplotlib.pyplot as plt

        plt.plot(big_data.spline_xs, spline, 'g', linewidth=1, label=label, c=color)

        plt.grid()
        plt.title("Splines")
        # plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")
        """




        """
    @staticmethod
    def calc_thresholds(big_data, spline, buffer=0.05, buffer_setting=0,
                        standard_upper_threshold=0.5, standard_lower_threshold=-0.5):
        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Google_trends import pull_google_trends_data
        import pandas as pd

        """        
        Buffer settings:
              - 0: no buffer
              - 1: fixed value buffer
              - 2: variable value buffer
        """

        # TODO decide whether to keep google trends-modulated buffer size?

        if buffer_setting == 0:
            buffer = 0.0000001
            spline_buffer = [1]*len(big_data.spline_xs)

        elif buffer_setting == 1:
            spline_buffer = [1]*len(big_data.spline_xs)

        elif buffer_setting == 2:

            # ---- Obtaining timeframe to be used for fetching google trends data
            start_date = str(pd.to_datetime(big_data.data_slice_dates[0]).date())
            end_date = str(
                pd.to_datetime(big_data.data_slice_dates[len(big_data.data_slice_dates) - 1]).date())

            timeframe = start_date + " " + end_date

            google_trends_data = pull_google_trends_data(["Apple"], cat=7, timeframe=timeframe, gprop="news")

            google_trends_lst = []
            for index, row in google_trends_data.iterrows():
                google_trends_lst.append(row['Apple'])

            # ---- Normalising the list obtained
            google_trends_lst_normalised = []
            for i in range(len(big_data.data_slice)):
                google_trends_lst_normalised.append((google_trends_lst[i]) / max(google_trends_lst))

            spline_buffer_lst = SPLINE(big_data).calc_signal_to_spline(
                big_data, google_trends_lst_normalised, smoothing_factor=0)

            for i in range(len(spline_buffer_lst)):
                round(i, 4)
                if spline_buffer_lst[i] < 0:
                    spline_buffer_lst[i] = 0

            # ---- Normalising spline_buffer obtained
            spline_buffer_normalised = []
            for i in range(len(spline_buffer_lst)):
                spline_buffer_normalised.append((spline_buffer_lst[i])/max(spline_buffer_lst))

            spline_buffer = spline_buffer_normalised

        # -------------------------DYNAMIC BOUND DEFINITION-------------------
        # ---- Define upper dynamic bound method
        upper_threshold = [standard_upper_threshold]*len(big_data.spline_xs)
        max_prev = 1
        freeze_trade = False
        for i in range(len(spline)):
            if spline[i] < standard_upper_threshold:
                freeze_trade = False

            if spline[i] > (standard_upper_threshold + (buffer * spline_buffer[i])) and freeze_trade is False or spline[i] > max_prev:
                new_upper_threshold = spline[i] - (buffer * spline_buffer[i])
                if new_upper_threshold >= upper_threshold[i - 1]:
                    upper_threshold[i] = new_upper_threshold

                elif spline[i] < upper_threshold[i - 1]:
                    max_prev = spline[i]
                    freeze_trade = True

                else:
                    max_prev = spline[i]
                    upper_threshold[i] = upper_threshold[i - 1]

        # ---- Define lower dynamic bound method
        lower_threshold = [standard_lower_threshold]*len(big_data.spline_xs)
        min_prev = -1
        freeze_trade = False
        for i in range(len(spline)):
            if spline[i] > standard_lower_threshold:
                freeze_trade = False

            if spline[i] < (standard_lower_threshold - (buffer * spline_buffer[i])) and freeze_trade is False or spline[i] < min_prev:
                new_lower_threshold = spline[i] + (buffer * spline_buffer[i])
                if new_lower_threshold <= lower_threshold[i - 1]:
                    lower_threshold[i] = new_lower_threshold

                elif spline[i] > lower_threshold[i - 1]:
                    min_prev = spline[i]
                    freeze_trade = True

                else:
                    min_prev = spline[i]
                    lower_threshold[i] = lower_threshold[i - 1]

        return upper_threshold, lower_threshold

    @staticmethod
    def calc_trading_spline(big_data, spline, upper_threshold, lower_threshold):

        trade_signal = np.zeros(big_data.data_slice.slice_size)

        # Listing out point of spline which are date points
        trade_spline = []

        for i in range(0, len(spline)):
            if i % int(int(len(big_data.spline_xs)/big_data.data_slice.slice_size)) == 0:
                trade_spline.append(spline[i])

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        max_prev = None
        min_prev = None

        # Defining indicator trigger for...
        for i in range(big_data.data_slice.slice_size):
            # ...upper bound
            if trade_spline[i] >= upper_threshold[i] and sell_trigger == 0:    # Initiate sell trigger
                sell_trigger = 1

            if max_prev is not None:        # Re-initiate sell trigger if signal increase past previous max
                if trade_spline[i] > max_prev:
                    sell_trigger = 1
                    max_prev = None

            if trade_spline[i] <= max(list(upper_threshold[i-j] for j in range(10))) and sell_trigger == 1:   # Initiate sell trigger
                trade_signal[i] = 1
                max_prev = trade_spline[i]
                sell_trigger = 2

            if trade_spline[i] <= min(upper_threshold) and sell_trigger == 2:   # Reset trigger
                max_prev = None
                sell_trigger = 0

            # ...lower bound
            if trade_spline[i] <= lower_threshold[i] and buy_trigger == 0:     # Initiate buy trigger
                buy_trigger = 1

            if min_prev is not None:        # Re-initiate buy trigger if signal decrease past previous min
                if trade_spline[i] < min_prev:
                    buy_trigger = 1
                    min_prev = None

            if trade_spline[i] >= min(list(lower_threshold[i-j] for j in range(10))) and buy_trigger == 1:    # Initiate sell trigger
                trade_signal[i] = -1
                min_prev = trade_spline[i]
                buy_trigger = 2

            if trade_spline[i] >= max(lower_threshold) and buy_trigger == 2:    # Reset trigger
                min_prev = None
                buy_trigger = 0

        return trade_signal, trade_spline

    @staticmethod
    def plot_spline_trigger(big_data,  spline, sell_dates, buy_dates):
        import matplotlib.pyplot as plt

        # Listing out point of spline which are date points
        dates_points = []

        for i in range(len(big_data.spline_xs)):
            if i % 5 == 0:
                dates_points.append(i)

        sell_spline_values = []
        sell_spline_dates = []

        for i in sell_dates:
            sell_spline_values.append(spline[dates_points[big_data.data_slice_dates.index(i)]])
            sell_spline_dates.append(dates_points[big_data.data_slice_dates.index(i)]/5)

        buy_spline_values = []
        buy_spline_dates = []
        for i in buy_dates:
            buy_spline_values.append(spline[dates_points[big_data.data_slice_dates.index(i)]])
            buy_spline_dates.append(dates_points[big_data.data_slice_dates.index(i)]/5)

        plt.scatter(sell_spline_dates,  sell_spline_values, label="Sell trigger")
        plt.scatter(buy_spline_dates, buy_spline_values, label="Buy trigger")
