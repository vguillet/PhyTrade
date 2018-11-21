"""
This script contains tools for smoothing out signals, using interpolation and splines
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

        setattr(big_data, "combined_signal_splines", combined_signal_spline)

    @staticmethod
    def plot_signal_spline(big_data, spline):
        import matplotlib.pyplot as plt

        plt.plot(big_data.spline_xs, spline, 'g', lw=3)

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("Spline signals")
        plt.xlabel("Trade date")
        plt.ylabel("Signal power")
