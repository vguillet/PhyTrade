"""
This script contains tools for smoothing out and adding up signals, using interpolation and splines

Victor Guillet
11/28/2018
"""


class SPLINE:
    @staticmethod
    def __init__(big_data):
        import numpy as np

        x = np.array(range(len(big_data.data_slice_dates)))
        xs = np.linspace(0, len(big_data.data_slice_dates), len(big_data.data_slice_dates) * 5)

        setattr(big_data, "spline_x", x)
        setattr(big_data, "spline_xs", xs)

    @staticmethod
    def calc_signal_to_spline(big_data, signal, smoothing_factor=0.7):
        import numpy as np
        from scipy.interpolate import UnivariateSpline

        y = np.array(signal)

        spline_x = UnivariateSpline(big_data.spline_x, y)
        spline_x.set_smoothing_factor(smoothing_factor)

        spline = spline_x(big_data.spline_xs)

        # Limiting the magnitude of the signal when it reaches values above 1 or below -1
        for i in range(len(spline)):
            if spline[i] > 1:
                spline[i] = 1

            if spline[i] < -1:
                spline[i] = -1

        setattr(big_data, "spline_length", len(spline))

        return spline

    @staticmethod
    def combine_5_splines(big_data,
                          spline_1, spline_2, spline_3, spline_4, spline_5,
                          weight_1=1, weight_2=1, weight_3=1, weight_4=1, weight_5=1):

        combined_splines = []
        for i in range(big_data.spline_length):
            combined_splines.append((spline_1[i]*weight_1 + spline_2[i]*weight_2
                                     + spline_3[i]*weight_3 + spline_4[i]*weight_4
                                     + spline_5[i]*weight_5) /
                                    (weight_1+weight_2+weight_3+weight_4+weight_5))

        return combined_splines

    @staticmethod
    def combine_7_splines(big_data,
                          spline_1, spline_2, spline_3, spline_4, spline_5, spline_6, spline_7,
                          weight_1=1, weight_2=1, weight_3=1, weight_4=1, weight_5=1, weight_6=1, weight_7=1):

        combined_splines = []
        for i in range(big_data.spline_length):
            combined_splines.append((spline_1[i]*weight_1 + spline_2[i]*weight_2
                                     + spline_3[i]*weight_3 + spline_4[i]*weight_4
                                     + spline_5[i]*weight_5 + spline_6[i]*weight_6
                                     + spline_7[i]*weight_7) /
                                    (weight_1+weight_2+weight_3+weight_4+weight_5+weight_6+weight_7))

        return combined_splines

    @staticmethod
    def shift_spline(spline, index_shift):

        # Shifts a spline by index_shift

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

        # Limiting the magnitude of the signal when it reaches values above a certain number of standard deviation
        coef_spline_standard_dev = statistics.stdev(coef_spline)
        coef_spline_mean = statistics.mean(coef_spline)

        for i in range(len(coef_spline)):
            if coef_spline[i] > 0 and coef_spline[i] - coef_spline_mean > std_dev_max * coef_spline_standard_dev:
                coef_spline[i] = coef_spline_mean + std_dev_max * coef_spline_standard_dev

            if coef_spline[i] < 0 and abs(coef_spline[i]) + coef_spline_mean > std_dev_max * coef_spline_standard_dev:
                coef_spline[i] = coef_spline_mean - std_dev_max * coef_spline_standard_dev

        # Modulating spline
        spline_modulated = []
        for i in range(len(spline)):
            spline_modulated.append(spline[i]*(1+abs(coef_spline[i])))

        return spline_modulated         # Note that the spline modulated still requires being normalised

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
        from PhyTrade.Technical_Analysis.Data_Collection_preparation.Google_trends import pull_google_trends_data
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
        upper_threshold = [standard_upper_threshold]*len(big_data.spline_xs)
        freeze_trade = False
        # ---- Define upper dynamic bound method
        for i in range(len(spline)):
            if spline[i] < standard_upper_threshold:
                freeze_trade = False

            if spline[i] > (standard_upper_threshold + (buffer * spline_buffer[i])) and freeze_trade is False:
                new_upper_threshold = spline[i] - (buffer * spline_buffer[i])
                if new_upper_threshold >= upper_threshold[i - 1]:
                    upper_threshold[i] = new_upper_threshold

                elif spline[i] < upper_threshold[i - 1]:
                    freeze_trade = True

                else:
                    upper_threshold[i] = upper_threshold[i - 1]

        lower_threshold = [standard_lower_threshold]*len(big_data.spline_xs)
        freeze_trade = False

        # ---- Define upper dynamic bound method
        for i in range(len(spline)):
            if spline[i] > standard_lower_threshold:
                freeze_trade = False

            if spline[i] < (standard_lower_threshold - (buffer * spline_buffer[i])) and freeze_trade is False:
                new_lower_threshold = spline[i] + (buffer * spline_buffer[i])
                if new_lower_threshold <= lower_threshold[i - 1]:
                    lower_threshold[i] = new_lower_threshold

                elif spline[i] > lower_threshold[i - 1]:
                    freeze_trade = True

                else:
                    lower_threshold[i] = lower_threshold[i - 1]
        return upper_threshold, lower_threshold

    @staticmethod
    def calc_spline_trigger(big_data, spline, upper_threshold, lower_threshold):

        sell_dates = []
        buy_dates = []

        sell_spline = []
        buy_spline = []

        # Listing out point of spline which are date points
        dates_points = []

        for i in range(0, len(big_data.spline_xs)):
            if i % 5 == 0:
                dates_points.append(i)

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        # Defining indicator trigger for...
        for i in dates_points:

            # ...upper bound
            if spline[i] >= upper_threshold[i] and sell_trigger == 0:    # Initiate sell trigger
                sell_trigger = 1

            if spline[i] <= max(list(upper_threshold[i-j] for j in range(10))) and sell_trigger == 1:   # Initiate sell trigger
                sell_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                sell_spline.append(spline[i])
                sell_trigger = 2

            if spline[i] <= min(upper_threshold) and sell_trigger == 2:   # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if spline[i] <= lower_threshold[i] and buy_trigger == 0:     # Initiate buy trigger
                buy_trigger = 1

            if spline[i] >= min(list(lower_threshold[i-j] for j in range(10))) and buy_trigger == 1:    # Initiate sell trigger
                buy_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                buy_spline.append(spline[i])
                buy_trigger = 2

            if spline[i] >= max(lower_threshold) and buy_trigger == 2:    # Reset trigger
                buy_trigger = 0

        return sell_dates, buy_dates, sell_spline, buy_spline

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
