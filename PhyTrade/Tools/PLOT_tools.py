import matplotlib.pyplot as plt


class PLOT_tools:
    @staticmethod
    def plot_trade_process(data_slice, spline, upper_threshold_spline, lower_threshold_spline, trade_signal):
        plot_tools = PLOT_tools()
        # ------------------ Plot Open/Close prices
        ax1 = plt.subplot(211)
        plot_tools.plot_oc_values(data_slice)
        plot_tools.plot_values_trigger(data_slice, trade_signal)

        # ------------------ Plot bb signal(s)
        ax2 = plt.subplot(212)
        plot_tools.plot_spline(spline, color="y")
        plot_tools.plot_spline(upper_threshold_spline, label="Upper threshold")
        plot_tools.plot_spline(lower_threshold_spline, label="Lower threshold")
        plot_tools.plot_spline_trigger(spline, trade_signal)

        plt.show()

    @staticmethod
    def plot_oc_values(data_slice, plot_close_values=True, plot_open_values=True):
        """
        :param data_slice: DATA_SLICE class instance
        :param plot_close_values: Plot close values
        :param plot_open_values:  Plot open values
        """

        if plot_close_values:
            plt.plot(list(data_slice.sliced_data["Date"]), list(data_slice.sliced_data["Close"]),
                     linewidth=1, label="Close values")   # Plot closing value

        if plot_open_values:
            plt.plot(list(data_slice.sliced_data["Date"]), list(data_slice.sliced_data["Open"]),
                     linewidth=1, label="Open values")

        plt.gcf().autofmt_xdate()
        plt.title("Open and close values")
        plt.xlabel("Trade date")
        plt.ylabel("Value")

        plt.legend()
        plt.grid()

    @staticmethod
    def plot_spline(spline, label=" ", color='g'):

        plt.plot(range(len(spline)), spline, linewidth=1, label=label, c=color)

        plt.title("Splines")
        plt.xlabel("Trade date")
        plt.ylabel("Buy <-- Signal power --> Sell")

        plt.legend()
        plt.grid()

    @staticmethod
    def plot_spline_trigger(spline, trade_signal):
        buy_spline_values = []
        buy_index = []
        sell_spline_values = []
        sell_index = []

        spline_multiplication_coef = int(len(spline)/len(trade_signal))

        for i in range(len(trade_signal)):
            if trade_signal[i] == 1:
                sell_spline_values.append(spline[i*spline_multiplication_coef])
                sell_index.append(i*spline_multiplication_coef)

            elif trade_signal[i] == -1:
                buy_spline_values.append(spline[i*spline_multiplication_coef])
                buy_index.append(i*spline_multiplication_coef)

        plt.scatter(sell_index,  sell_spline_values, label="Sell trigger")
        plt.scatter(buy_index, buy_spline_values, label="Buy trigger")

        plt.legend()
        plt.grid()

    @staticmethod
    def plot_values_trigger(data_slice, trade_signal):
        """
        Plot inputted trigger values on open/close price plot
        """
        buy_values = []
        buy_date = []
        sell_values = []
        sell_date = []

        for i in range(len(trade_signal)):
            if trade_signal[i] == 1:
                sell_values.append(data_slice.sliced_data_selection[i])
                sell_date.append(list(data_slice.sliced_data["Date"])[i])

            elif trade_signal[i] == -1:
                buy_values.append(data_slice.sliced_data_selection[i])
                buy_date.append(list(data_slice.sliced_data["Date"])[i])

        plt.scatter(sell_date,  sell_values, label="Sell trigger")
        plt.scatter(buy_date, buy_values, label="Buy trigger")

        plt.legend()
        plt.grid()

