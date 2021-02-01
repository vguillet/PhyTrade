
################################################################################################################
"""
This script contains tools for smoothing out and adding up signals, using interpolation and splines
"""

# Built-in/Generic Imports
import statistics
import sys

# Libs
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

# Own modules


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

################################################################################################################


class Spline_tools:
    @staticmethod
    def __init__(big_data):

        x = np.array(range(big_data.data_slice.subslice_size))
        xs = np.linspace(0, big_data.data_slice.subslice_size, big_data.data_slice.subslice_size * big_data.spline_multiplication_coef)

        setattr(big_data, "spline_x", x)
        setattr(big_data, "spline_xs", xs)

    @staticmethod
    def calc_signal_to_spline(big_data, signal, smoothing_factor=0.7):

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

        flipped_spline = np.zeros(len(spline))
        for i in range(len(spline)):
            flipped_spline[i] = -spline[i]

        return flipped_spline

    @staticmethod
    def calc_thresholds(big_data, spline, buffer=0.05,
                        standard_upper_threshold=0.5, standard_lower_threshold=-0.5,
                        bband_timeframe=15,
                        threshold_setting=1, buffer_setting=0):
        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        from src.Data_Collection_preparation.Data_sources.Google_trends import pull_google_trends_data
        from src.Tools.Math_tools import Math_tools

        """        
        Buffer settings:
              - 0: no buffer
              - 1: fixed value buffer
              - 2: variable value buffer (google trends)
        """

        # TODO decide whether to keep google trends-modulated buffer size?

        if buffer_setting == 0:
            buffer = 0.0000001
            spline_buffer = [1]*len(big_data.spline_xs)

        elif buffer_setting == 1:
            spline_buffer = [1]*len(big_data.spline_xs)

        elif buffer_setting == 2:

            # ---- Obtaining timeframe to be used for fetching google trends data
            start_date = big_data.data_slice.start_date
            end_date = big_data.data_slice.end_date

            timeframe = start_date + " " + end_date

            google_trends_data = pull_google_trends_data([big_data.data_slice.ticker], cat=7, timeframe=timeframe, gprop="news")

            google_trends_lst = []
            for index, row in google_trends_data.iterrows():
                google_trends_lst.append(row[big_data.data_slice.ticker])

            # ---- Normalising the list obtained
            google_trends_lst_normalised = []
            for i in range(len(big_data.data_slice)):
                google_trends_lst_normalised.append((google_trends_lst[i]) / max(google_trends_lst))

            spline_buffer_lst = Spline_tools(big_data).calc_signal_to_spline(big_data, google_trends_lst_normalised, smoothing_factor=0)

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
        if threshold_setting == 0:
            upper_threshold = [standard_upper_threshold]*len(big_data.spline_xs)
            lower_threshold = [standard_lower_threshold] * len(big_data.spline_xs)

        elif threshold_setting == 1:
            bbands_df = big_data.data_slice.data[big_data.data_slice.subslice_start_index - bband_timeframe:big_data.data_slice.subslice_stop_index]
            mean_avg = bbands_df[big_data.data_slice.price_data_selection].rolling(window=bband_timeframe).mean()
            standard_dev = bbands_df[big_data.data_slice.price_data_selection].rolling(window=bband_timeframe).std()

            upper_band = np.array(mean_avg + (2 * standard_dev))[bband_timeframe:]
            lower_band = np.array(mean_avg - (2 * standard_dev))[bband_timeframe:]

            # --> Normalise thresholds between -1 and 1
            upper_band_normalised = Math_tools().normalise_minus_one_one(upper_band)
            lower_band_normalised = Math_tools().normalise_minus_one_one(lower_band)

            # upper_band_normalised = Math_tools().alignator_minus_one_one(upper_band, signal_max=200, signal_min=100)
            # lower_band_normalised = Math_tools().alignator_minus_one_one(lower_band, signal_max=200, signal_min=100)

            upper_band_spline = Spline_tools(big_data).calc_signal_to_spline(big_data, upper_band_normalised)
            lower_band_spline = Spline_tools(big_data).calc_signal_to_spline(big_data, lower_band_normalised)

            difference_band_spline = abs(upper_band_spline-lower_band_spline)

            upper_threshold = standard_upper_threshold + standard_upper_threshold*0.5*difference_band_spline
            lower_threshold = standard_lower_threshold - standard_upper_threshold*0.5*difference_band_spline

        elif threshold_setting == 2:
            bbands_df = big_data.data_slice.data[big_data.data_slice.subslice_start_index - bband_timeframe:big_data.data_slice.subslice_stop_index]
            mean_avg = bbands_df[big_data.data_slice.price_data_selection].rolling(window=bband_timeframe).mean()
            standard_dev = bbands_df[big_data.data_slice.price_data_selection].rolling(window=bband_timeframe).std()

            upper_band = np.array(mean_avg + (2 * standard_dev))
            lower_band = np.array(mean_avg - (2 * standard_dev))

            upper_band_price_diff = (upper_band-np.array(bbands_df[big_data.data_slice.price_data_selection]))[bband_timeframe:]
            lower_band_price_diff = (np.array(bbands_df[big_data.data_slice.price_data_selection])-lower_band)[bband_timeframe:]

            # --> Normalise thresholds between -1 and 1
            upper_band_price_diff_normalised = Math_tools().normalise_minus_one_one(upper_band_price_diff)
            lower_band_price_diff_normalised = Math_tools().normalise_minus_one_one(lower_band_price_diff)

            # upper_band_price_diff_normalised = Math_tools().alignator_minus_one_one(upper_band_price_diff, signal_max=2.5, signal_min=-2.5)
            # lower_band_price_diff_normalised = Math_tools().alignator_minus_one_one(lower_band_price_diff, signal_max=2.5, signal_min=-2.5)

            upper_band_price_diff_spline = Spline_tools(big_data).calc_signal_to_spline(big_data, upper_band_price_diff_normalised)
            lower_band_price_diff_spline = Spline_tools(big_data).calc_signal_to_spline(big_data, lower_band_price_diff_normalised)

            upper_threshold = standard_upper_threshold + standard_upper_threshold*0.5*upper_band_price_diff_spline
            lower_threshold = standard_lower_threshold - standard_upper_threshold*0.5*lower_band_price_diff_spline

        else:
            sys.exit("Invalid threshold setting selected")

        # ---- Define upper dynamic bound method
        max_prev = 1
        freeze_trade = False
        for i in range(len(spline)):
            # --> If spline is below upper threshold
            if spline[i] < upper_threshold[i]:
                max_prev = 1
                freeze_trade = False

            # --> If spline is above upper threshold and no trade has been performed recently
            if spline[i] > (upper_threshold[i] + (buffer * spline_buffer[i])) and freeze_trade is False or spline[i] > max_prev:
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
        min_prev = -1
        freeze_trade = False
        for i in range(len(spline)):
            if spline[i] > lower_threshold[i]:
                min_prev = -1
                freeze_trade = False

            if spline[i] < (lower_threshold[i] - (buffer * spline_buffer[i])) and freeze_trade is False or spline[i] < min_prev:
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
        # Listing out point of spline which are date points
        trade_spline = []
        trade_upper_threshold = []
        trade_lower_threshold = []

        for i in range(0, len(spline), big_data.spline_multiplication_coef):
            trade_spline.append(spline[i])
            trade_upper_threshold.append(upper_threshold[i])
            trade_lower_threshold.append(lower_threshold[i])

        trade_signal = np.zeros(len(trade_spline))
        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        max_prev = None
        min_prev = None

        back_range = 1

        # Defining indicator trigger for...
        for i in range(big_data.data_slice.subslice_size):
            # print("Sell: ({0})  {1:.3f} | {2:.3f} | {3:.3f}  ({4}) :Buy".format(sell_trigger, round(trade_upper_threshold[i], 3), round(trade_spline[i], 3), round(trade_lower_threshold[i], 3), round(buy_trigger)))

            if sell_trigger == 1 or buy_trigger == 1:
                back_range += 1

            if trade_spline[i] > 0:
                # ...upper bound
                if trade_spline[i] >= trade_upper_threshold[i] and sell_trigger == 0:    # Initiate sell trigger
                    sell_trigger = 1
                    continue

                if trade_spline[i] <= max(list(trade_upper_threshold[i-j] for j in range(back_range))) and sell_trigger == 1:   # Initiate sell trigger
                    trade_signal[i] = 1
                    max_prev = trade_spline[i]
                    sell_trigger = 2

                    back_range = 1
                    continue

                if trade_spline[i] <= trade_upper_threshold[i] and sell_trigger == 2:   # Reset trigger
                    max_prev = None
                    sell_trigger = 0
                    continue

                if max_prev is not None:  # Re-initiate sell trigger if signal increase past previous max
                    if trade_spline[i] > max_prev and sell_trigger == 2:
                        sell_trigger = 1
                        max_prev = None

            else:
                # ...lower bound
                if trade_spline[i] <= trade_lower_threshold[i] and buy_trigger == 0:     # Initiate buy trigger
                    buy_trigger = 1
                    continue

                if trade_spline[i] >= min(list(trade_lower_threshold[i-j] for j in range(back_range))) and buy_trigger == 1:    # Initiate sell trigger
                    trade_signal[i] = -1
                    min_prev = trade_spline[i]
                    buy_trigger = 2

                    back_range = 1
                    continue

                if trade_spline[i] >= trade_lower_threshold[i] and buy_trigger == 2:    # Reset trigger
                    min_prev = None
                    buy_trigger = 0
                    continue

                if min_prev is not None:        # Re-initiate buy trigger if signal decrease past previous min
                    if trade_spline[i] < min_prev and buy_trigger == 2:
                        buy_trigger = 1
                        min_prev = None

        if buy_trigger == 1:
            trade_signal[-1] = -1

        if sell_trigger == 1:
            trade_signal[-1] = 1

        return trade_signal, trade_spline, trade_upper_threshold, trade_lower_threshold

    @staticmethod
    def calc_trading_indicator(big_data, spline):
        # Listing out point of spline which are date points
        trade_spline = []

        for i in range(0, len(spline), big_data.spline_multiplication_coef):
            trade_spline.append(spline[i])

        return trade_spline