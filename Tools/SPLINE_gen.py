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
    def combine_signal_splines(big_data, signals):

        combined_signal_spline = []
        for i in range(big_data.spline_length):
            combined_signal_spline.append(sum(signals[j][i] for j in range(len(signals)))/len(signals))

        return combined_signal_spline

    @staticmethod
    def combine_weighted_signal_splines(big_data,
                                        signal_1, signal_2, signal_3,
                                        weight_1=1, weight_2=1, weight_3=1):

        combined_signal_spline = []
        for i in range(big_data.spline_length):
            combined_signal_spline.append((signal_1[i]*weight_1 + signal_2[i]*weight_2 + signal_3[i]*weight_3) /
                                          (weight_1+weight_2+weight_3))

        return combined_signal_spline

    @staticmethod
    def plot_signal_spline(big_data, spline, label, color='g'):
        import matplotlib.pyplot as plt

        plt.plot(big_data.spline_xs, spline, 'g', linewidth=1, label=label, c=color)

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Spline signals")
        # plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")

    @staticmethod
    def calc_upper_threshold(big_data):

        upper_threshold = [0.6]*len(big_data.spline_xs)

        return upper_threshold

    @staticmethod
    def calc_lower_threshold(big_data):

        lower_threshold = [-0.6]*len(big_data.spline_xs)

        return lower_threshold

