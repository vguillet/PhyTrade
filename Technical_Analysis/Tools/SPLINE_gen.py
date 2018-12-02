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
    def calc_signal_spline(big_data, signal, smoothing_factor=0.7):
        import numpy as np
        from scipy.interpolate import UnivariateSpline

        y = np.array(signal)

        spline = UnivariateSpline(big_data.spline_x, y)
        spline.set_smoothing_factor(smoothing_factor)

        setattr(big_data, "spline_length", len(spline(big_data.spline_xs)))

        return spline(big_data.spline_xs)

    @staticmethod
    def combine_splines(big_data,
                        spline_1, spline_2, spline_3, spline_4,
                        weight_1=1, weight_2=1, weight_3=1, weight_4=1):

        combined_splines = []
        for i in range(big_data.spline_length):
            combined_splines.append((spline_1[i]*weight_1 + spline_2[i]*weight_2
                                           + spline_3[i]*weight_3 + spline_4[i]*weight_4) /
                                          (weight_1+weight_2+weight_3+weight_4))

        return combined_splines

    @staticmethod
    def shift_spline(spline, index_shift):

        shifted_spline = [0]*len(spline)

        if index_shift < 0:
            for i in range(len(spline) + index_shift):
                shifted_spline[i+index_shift] = spline[i]
        else:
            for i in range(len(spline) - index_shift):
                shifted_spline[i+index_shift] = spline[i]

        return shifted_spline

    @staticmethod
    def simple_increase_amplitude_spline(spline, coef):

        spline_amplified = []

        for i in spline:
            spline_amplified.append(i*coef)

        return spline_amplified

    @staticmethod
    def increase_amplitude_spline(spline, coef_spline):

        spline_amplified = []

        for i in range(len(spline)):
            spline_amplified.append(spline[i]*(1+abs(coef_spline[i])))

        # Normalising spline_amplified values between -1 and 1
        spline_amplified_normalised = []

        for i in range(len(spline_amplified)):
            spline_amplified_normalised.append((spline_amplified[i])/max(max(spline_amplified), -min(spline_amplified)))

        return spline_amplified_normalised

    @staticmethod
    def plot_spline(big_data, spline, label, color='g'):
        import matplotlib.pyplot as plt

        plt.plot(big_data.spline_xs, spline, 'g', linewidth=1, label=label, c=color)

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Splines")
        # plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")

    # =========================================================================================

    @staticmethod
    def calc_upper_threshold(big_data, spline, buffer_setting=0, standard_upper_threshold=0.5):
        # TODO combine calc_upper and calc_lower functions?
        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer
        # TODO implement variable weighted buffer

        if buffer_setting == 0:
            spline_buffer = 0

        elif buffer_setting == 1:
            spline_buffer = 0.05

        elif buffer_setting == 2:
            spline_buffer = 2

        # -------------------------DYNAMIC BOUND DEFINITION-------------------

        upper_threshold = [standard_upper_threshold]*len(big_data.spline_xs)
        
        freeze_trade = False
        
        # Define upper dynamic bound method
        for i in range(len(spline)):
            if spline[i] < standard_upper_threshold:
                freeze_trade = False

            if spline[i] > (standard_upper_threshold + spline_buffer) and freeze_trade is False:
                new_upper_threshold = spline[i] - spline_buffer
                if new_upper_threshold >= upper_threshold[i - 1]:
                    upper_threshold[i] = new_upper_threshold

                elif spline[i] < upper_threshold[i - 1]:
                    freeze_trade = True

                else:
                    upper_threshold[i] = upper_threshold[i - 1]

        return upper_threshold

    @staticmethod
    def calc_lower_threshold(big_data, spline, buffer_setting=0, standard_lower_threshold=-0.5):

        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer
        # TODO implement variable weighted buffer

        if buffer_setting == 0:
            spline_buffer = 0

        elif buffer_setting == 1:
            spline_buffer = 0.05

        elif buffer_setting == 2:
            spline_buffer = 2

        # -------------------------DYNAMIC BOUND DEFINITION-------------------
        lower_threshold = [standard_lower_threshold]*len(big_data.spline_xs)

        freeze_trade = False

        # Define upper dynamic bound method
        for i in range(len(spline)):
            if spline[i] > standard_lower_threshold:
                freeze_trade = False

            if spline[i] < (standard_lower_threshold - spline_buffer) and freeze_trade is False:
                new_lower_threshold = spline[i] + spline_buffer
                if new_lower_threshold <= lower_threshold[i - 1]:
                    lower_threshold[i] = new_lower_threshold

                elif spline[i] > lower_threshold[i - 1]:
                    freeze_trade = True

                else:
                    lower_threshold[i] = lower_threshold[i - 1]
        return lower_threshold

    @staticmethod
    def calc_spline_trigger(big_data, spline):
        # TODO fix calc_spline_trigger
        sell_dates = []
        buy_dates = []

        sell_spline = []
        buy_spline = []

        # Listing out point of spline which are date points
        dates_points = []

        for i in range(len(spline)):
            if i % 5 == 0:
                dates_points.append(i)

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        # Defining indicator trigger for...

        for i in dates_points:

            # ...upper bound
            if spline[i] >= big_data.spline_upper_threshold[i] and sell_trigger == 0:    # Initiate sell trigger
                sell_trigger = 1

            if spline[i] < big_data.spline_upper_threshold[i] and sell_trigger == 1:   # Initiate sell trigger
                sell_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                sell_spline.append(spline[i])

                sell_trigger = 2

            if spline[i] < big_data.spline_upper_threshold[i] and sell_trigger == 2:   # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if spline[i] <= big_data.spline_lower_threshold[i] and buy_trigger == 0:     # Initiate buy trigger
                buy_trigger = 1

            if spline[i] > big_data.spline_lower_threshold[i] and buy_trigger == 1:    # Initiate sell trigger
                buy_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                buy_spline.append(spline[i])

                buy_trigger = 2

            if spline[i] > big_data.spline_lower_threshold[i] and buy_trigger == 2:    # Reset trigger
                buy_trigger = 0

        return sell_dates, buy_dates, sell_spline, buy_spline

    @staticmethod
    def plot_spline_trigger(sell_spline, buy_spline, spline):
            import matplotlib.pyplot as plt

            plt.scatter(spline.index(sell_spline[i] for i in range(len(sell_spline))), sell_spline, label="Sell trigger")
            plt.scatter(spline.index(buy_spline[i] for i in range(len(buy_spline))), buy_spline, label="Buy trigger")
