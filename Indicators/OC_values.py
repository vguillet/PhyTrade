"""
This scripts enable plotting the opening and close value of stocks of a data slice
"""


class OC:
    @staticmethod
    def __init__(big_data):
        import numpy as np

        # -------Compute the values matching the trigger sell/buy dates

        rsi_sell_values = []
        rsi_buy_values = []

        for i in range(len(big_data.rsi_sell_dates)):
            rsi_sell_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(big_data.rsi_sell_dates[i])])

        for i in range(len(big_data.rsi_buy_dates)):
            rsi_buy_values.append(
                big_data.data_slice_close_values[big_data.data_slice_dates.index(big_data.rsi_buy_dates[i])])

        setattr(big_data, "rsi_sell_values", rsi_sell_values)
        setattr(big_data, "rsi_buy_values", rsi_buy_values)

        # -------Calculate value fluctuation for each point

        values_fluctuation = []
        for i in range(len(big_data.data_slice)):
            values_fluctuation.append(big_data.data_slice_close_values[i] - big_data.data_slice_open_values[i])

        setattr(big_data, "values_fluctuation", values_fluctuation)

        # -------Calculate open/close values gradient:

        close_values_gradient = np.gradient(big_data.data_slice_close_values)
        open_values_gradient = np.gradient(big_data.data_slice_open_values)

        setattr(big_data, "close_values_gradient", close_values_gradient)
        setattr(big_data, "open_values_gradient", open_values_gradient)

    # ===================== INDICATOR OUTPUT DETERMINATION ==============
        # -----------------Bear/Bullish continuous signal
        avg_gradient = []
        avg_gradient_bb_signal = []

        # Obtaining the average gradient
        for i in range(len(big_data.data_slice)):
            avg_gradient.append(
                (big_data.close_values_gradient[i]+big_data.open_values_gradient[i])/2)

        # Normalising avg gradient values between -1 and 1
        for i in range(len(avg_gradient)):
            avg_gradient_bb_signal.append(-((avg_gradient[i]) / (max(max(avg_gradient), -min(avg_gradient)))))

        setattr(big_data, "oc_avg_gradient_bb_signal", avg_gradient_bb_signal)

    @staticmethod
    def plot_open_close_values(big_data):
        import matplotlib.pyplot as plt

        plt.plot(big_data.data_slice_dates, big_data.data_slice_close_values)               # Plot closing value
        plt.plot(big_data.data_slice_dates, big_data.data_slice_open_values)                # Plot opening value

        plt.scatter(big_data.rsi_sell_dates, big_data.rsi_sell_values)           # Plot sell signals
        plt.scatter(big_data.rsi_buy_dates, big_data.rsi_buy_values)             # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.title("Open and close values")
        plt.grid()
        plt.xlabel("Trade date")
        plt.ylabel("Value")

    @staticmethod
    def plot_open_close_values_diff(big_data):
        import matplotlib.pyplot as plt

        plt.plot(big_data.data_slice_dates, big_data.values_fluctuation)        # Plot value fluctuation

        plt.gcf().autofmt_xdate()
        plt.title("Open and close values fluctuation")
        plt.grid()
        plt.xlabel("Trade date")
        plt.ylabel("Value fluctuation")
