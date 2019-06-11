"""
This script enables computing the RSI indicator

Victor Guillet
11/28/2018
"""
import numpy as np


class RSI:
    def __init__(self, big_data, timeframe=14, standard_upper_threshold=70, standard_lower_threshold=30,
                 buffer_setting=0):
        """
        Generates an RSI indicator instance

        :param big_data: BIGDATA class instance
        :param timeframe: First Timeframe parameter to be used
        :param buffer_setting: 0: no buffer, 1: fixed value buffer, 2: variable value buffer
        :param standard_upper_threshold: Upper threshold for sell trigger points generation
        :param standard_lower_threshold: Lower threshold for buy trigger points generation
        """

        # --> RSI initialisation
        self.timeframe = timeframe
        self.buffer_setting = buffer_setting
        self.standard_upper_threshold = standard_upper_threshold
        self.standard_lower_threshold = standard_lower_threshold
        
        # --------------------------RSI CALCULATION---------------------------
        self.rsi_values = np.zeros(big_data.data_slice.slice_size)
        
        for i in range(big_data.data_slice.slice_size):
            # --> Adjust timeframe if necessary
            if len(big_data.data_slice.data[:big_data.data_slice.start_index]) < self.timeframe:
                self.timeframe = len(big_data.data_slice.data[big_data.data_slice.start_index:])

            # -- Collect open and close values falling in rsi_timeframe
            timeframe_open_values = np.zeros(self.timeframe)
            timeframe_close_values = np.zeros(self.timeframe)

            for j in range(self.timeframe):
                timeframe_open_values[j] = big_data.data_slice.data.iloc[big_data.data_slice.start_index + (i - j), 4]
                timeframe_close_values[j] = big_data.data_slice.data.iloc[big_data.data_slice.start_index + (i - j), 5]

            # -- Calculate gains and losses in timeframe
            # Calculate the net loss or gain for each date falling
            # in the data frame and store them in gains and loss lists
            gains = []
            losses = []
            for j in range(self.timeframe):
                net = timeframe_close_values[j] - timeframe_open_values[j]
                if net > 0:
                    gains.append(net)
                elif net < 0:
                    losses.append(net)
            
            # -- Calculate rs and rsi values for data_slice
            
            if gains:                                       # If gains != Null, calculate rsi_value, else rsi_value = 50
                avg_gain = sum(gains)/len(gains)
                if losses:                                  # If losses != Null, calculate rsi_value, else rsi_value = 50
                    avg_loss = sum(losses)/len(losses)
                    if avg_loss != 0:                       # If avg_loss != Null, calculate rsi_value, else rsi_value = 50
                        rs = avg_gain/avg_loss
                        current_rsi_value = 100-100/(1-rs)
                    else:
                        current_rsi_value = 50
                else:
                    current_rsi_value = 50
            else:
                current_rsi_value = 50

            self.rsi_values[i] = current_rsi_value
        
    # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer
        # TODO implement variable weighted buffer for rsi ??
        if self.buffer_setting == 0:
            rsi_buffer = 0

        elif self.buffer_setting == 1:
            rsi_buffer = 3

        elif self.buffer_setting == 2:
            rsi_buffer = 2

        else:
            rsi_buffer = 0
    # -------------------------DYNAMIC BOUND DEFINITION-------------------
        # Define initial upper and lower bounds
        self.upper_bound = np.zeros(big_data.data_slice.slice_size)
        self.lower_bound = np.zeros(big_data.data_slice.slice_size)

        self.upper_bound[:] = self.standard_lower_threshold
        self.lower_bound[:] = self.standard_upper_threshold

        # Define upper dynamic bound method
        freeze_trade_upper = False

        for i in range(big_data.data_slice.slice_size):
            if self.rsi_values[i] < self.standard_upper_threshold:
                freeze_trade_upper = False

            if self.rsi_values[i] > (self.standard_upper_threshold + rsi_buffer) and freeze_trade_upper is False:
                new_upper_bound = self.rsi_values[i] - rsi_buffer
                if new_upper_bound >= self.upper_bound[i-1]:
                    self.upper_bound[i] = new_upper_bound

                elif self.rsi_values[i] < self.upper_bound[i-1]:
                    freeze_trade_upper = True

                else:
                    self.upper_bound[i] = self.upper_bound[i-1]

        # Define lower dynamic bound method
        freeze_trade_lower = False

        for i in range(len(self.rsi_values)):
            if self.rsi_values[i] > self.standard_lower_threshold:
                freeze_trade_lower = False

            if self.rsi_values[i] < (self.standard_lower_threshold - rsi_buffer) and freeze_trade_lower is False:
                new_lower_bound = self.rsi_values[i] + rsi_buffer
                if new_lower_bound <= self.upper_bound[i-1]:
                    self.lower_bound[i] = new_lower_bound

                elif self.rsi_values[i] > self.lower_bound[i - 1]:
                    freeze_trade_lower = True

                else:
                    self.lower_bound[i] = self.lower_bound[i-1]

    """




    """
    # ===================== INDICATOR OUTPUT DETERMINATION ==============
    def get_output(self, big_data, include_triggers_in_bb_signal=False):
        """
        Generate RSI indicator output

        :param big_data: BIGDATA class instance
        :param include_triggers_in_bb_signal: Maximise/minimise bb signal when RSI crosses upper/lower bound
        """

        # -----------------Trigger points determination
        sell_dates = []
        buy_dates = []

        sell_rsi = []
        buy_rsi = []

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        # Defining indicator trigger for...
        for i in range(len(big_data.data_slice)):

            # ...upper bound
            if self.rsi_values[i] >= self.standard_upper_threshold and sell_trigger == 0:  # Initiate sell trigger
                sell_trigger = 1

            if self.rsi_values[i] <= self.upper_bound[i] and sell_trigger == 1:  # Trigger sell signal
                sell_dates.append(big_data.data_slice_dates[i])
                sell_rsi.append(self.rsi_values[i])

                sell_trigger = 2

            if self.rsi_values[i] < self.standard_upper_threshold and sell_trigger == 2:  # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if self.rsi_values[i] <= self.standard_lower_threshold and buy_trigger == 0:  # Initiate buy trigger
                buy_trigger = 1

            if self.rsi_values[i] >= self.lower_bound[i] and buy_trigger == 1:  # Trigger buy signal
                buy_dates.append(big_data.data_slice_dates[i])
                buy_rsi.append(self.rsi_values[i])

                buy_trigger = 2

            if self.rsi_values[i] > self.standard_lower_threshold and sell_trigger == 2:  # Reset trigger
                buy_trigger = 0

        self.sell_rsi = sell_rsi
        self.buy_rsi = buy_rsi

        self.sell_dates = sell_dates
        self.buy_dates = buy_dates

        # -----------------Bear/Bullish continuous signal
        from PhyTrade.Tools.MATH_tools import MATH_tools

        # Normalising rsi bb signal values between -1 and 1
        bb_signal_normalised = MATH_tools().normalise_minus_one_one(self.rsi_values)

        if include_triggers_in_bb_signal:
            for date in self.sell_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 1

            for date in self.buy_dates:
                bb_signal_normalised[big_data.data_slice_dates.index(date)] = 0

        self.bb_signal = bb_signal_normalised

    """




    """
    # -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------
    def plot_rsi(self, big_data, plot_rsi=True, plot_upper_bound=True, plot_lower_bound=True, plot_trigger_signals=True):
        """
        :param big_data: BIGDATA class instance
        :param plot_rsi: Plot RSI indicator
        :param plot_upper_bound: Include RSI upper bound in plot
        :param plot_lower_bound: Include RSI upper bound in plot
        :param plot_trigger_signals: Include RSI trigger signals in plot
        """

        import matplotlib.pyplot as plt

        if plot_rsi:
            plt.plot(big_data.data_slice_dates, self.rsi_values, linewidth=1, label="RSI values")    # Plot RSI

        if plot_upper_bound:
            plt.plot(big_data.data_slice_dates, self.upper_bound, linewidth=1, label="Upper bound")  # Plot upper bound

        if plot_lower_bound:
            plt.plot(big_data.data_slice_dates, self.lower_bound, linewidth=1, label="Lower bound")  # Plot lower bound

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_rsi, label="Sell trigger")           # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_rsi, label="Buy trigger")              # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("RSI")
        plt.legend()
        plt.xlabel("Trade date")
        plt.ylabel("RSI - %")


