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
                               signal_1, signal_2, signal_3, signal_4,
                               weight_1=1, weight_2=1, weight_3=1, weight_4=1):

        combined_signal_spline = []
        for i in range(big_data.spline_length):
            combined_signal_spline.append((signal_1[i]*weight_1 + signal_2[i]*weight_2
                                           + signal_3[i]*weight_3 + signal_4[i]*weight_4) /
                                          (weight_1+weight_2+weight_3+weight_4))

        return combined_signal_spline

    @staticmethod
    def shift_spline(signal, index_shift):

        shifted_signal = [0]*len(signal)

        if index_shift < 0:
            for i in range(len(signal) + index_shift):
                shifted_signal[i+index_shift] = signal[i]
        else:
            for i in range(len(signal) - index_shift):
                shifted_signal[i+index_shift] = signal[i]

        return shifted_signal

    @staticmethod
    def simple_increase_amplitude_spline(signal, coef):

        signal_amplified = []

        for i in signal:
            signal_amplified.append(i*coef)

        return signal_amplified

    @staticmethod
    def increase_amplitude_spline(signal, coef_signal):

        signal_amplified = []

        for i in range(len(signal)):
            signal_amplified.append(signal[i]*(1+abs(coef_signal[i])))

        # Normalising signal_amplified values between -1 and 1
        signal_amplified_normalised = []

        for i in range(len(signal_amplified)):
            signal_amplified_normalised.append((signal_amplified[i])/max(max(signal_amplified), -min(signal_amplified)))

        return signal_amplified_normalised

    @staticmethod
    def plot_spline(big_data, spline, label, color='g'):
        import matplotlib.pyplot as plt

        plt.plot(big_data.spline_xs, spline, 'g', linewidth=1, label=label, c=color)

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Spline signals")
        # plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")

    # =========================================================================================

    @staticmethod
    def calc_upper_threshold(big_data, signal, buffer_setting=0, standard_upper_threshold=0.5):

        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer

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
        for i in range(len(signal)):
            if signal[i] < standard_upper_threshold:
                freeze_trade = False

            if signal[i] > (standard_upper_threshold + spline_buffer) and freeze_trade is False:
                new_upper_threshold = signal[i] - spline_buffer
                if new_upper_threshold >= upper_threshold[i - 1]:
                    upper_threshold[i] = new_upper_threshold

                elif signal[i] < upper_threshold[i - 1]:
                    freeze_trade = True

                else:
                    upper_threshold[i] = upper_threshold[i - 1]

        return upper_threshold

    @staticmethod
    def calc_lower_threshold(big_data, signal, buffer_setting=0, standard_lower_threshold=-0.5):

        # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer

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
        for i in range(len(signal)):
            if signal[i] > standard_lower_threshold:
                freeze_trade = False

            if signal[i] < (standard_lower_threshold - spline_buffer) and freeze_trade is False:
                new_lower_threshold = signal[i] + spline_buffer
                if new_lower_threshold <= lower_threshold[i - 1]:
                    lower_threshold[i] = new_lower_threshold

                elif signal[i] > lower_threshold[i - 1]:
                    freeze_trade = True

                else:
                    lower_threshold[i] = lower_threshold[i - 1]
        return lower_threshold

    @staticmethod
    def calc_spline_trigger(big_data, signal):

        sell_dates = []
        buy_dates = []

        sell_spline = []
        buy_spline = []

        # Listing out point of spline which are date points
        dates_points = []

        for i in range(len(signal)):
            if i % 5 == 0:
                dates_points.append(i)

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        # Defining indicator trigger for...

        for i in dates_points:

            # ...upper bound
            if signal[i] >= big_data.spline_upper_threshold[i] and sell_trigger == 0:    # Initiate sell trigger
                sell_trigger = 1

            if signal[i] < big_data.spline_upper_threshold[i] and sell_trigger == 1:   # Initiate sell trigger
                sell_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                sell_spline.append(signal[i])

                sell_trigger = 2

            if signal[i] < big_data.spline_upper_threshold[i] and sell_trigger == 2:   # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if signal[i] <= big_data.spline_lower_threshold[i] and buy_trigger == 0:     # Initiate buy trigger
                buy_trigger = 1

            if signal[i] > big_data.spline_lower_threshold[i] and buy_trigger == 1:    # Initiate sell trigger
                buy_dates.append(big_data.data_slice_dates[dates_points.index(i)])
                buy_spline.append(signal[i])

                buy_trigger = 2

            if signal[i] > big_data.spline_lower_threshold[i] and buy_trigger == 2:    # Reset trigger
                buy_trigger = 0

        return sell_dates, buy_dates, sell_spline, buy_spline

    @staticmethod
    def plot_spline_trigger(sell_spline, buy_spline, signal):
            import matplotlib.pyplot as plt

            plt.scatter(signal.index(sell_spline[i] for i in range(len(sell_spline))), sell_spline, label="Sell trigger")
            plt.scatter(signal.index(buy_spline[i] for i in range(len(buy_spline))), buy_spline, label="Buy trigger")