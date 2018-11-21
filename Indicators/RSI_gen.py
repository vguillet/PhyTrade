"""
This script enables computing the RSI indicator
It is currently optimised for Quandl data
"""


class RSI:
    def __init__(self, big_data, timeframe=14, buffer_setting=0):
        
        self.timeframe = timeframe
        self.buffer_setting = buffer_setting
        
        # --------------------------RSI CALCULATION---------------------------
        rsi_values = []
        
        for i in range(len(big_data.data_slice)):

            # ------------------Calculate open and close values falling in rsi_timeframe
            timeframe_open_values = []
            timeframe_close_values = []

            for j in range(self.timeframe):
                timeframe_open_values.append(big_data.data_open_values[big_data.data_slice_start_ind + (i - j)])
                timeframe_close_values.append(big_data.data_close_values[big_data.data_slice_start_ind + (i - j)])

            # ------------------ Calculate gains and losses in timeframe
            # Calculate the net loss or gain for each date falling
            # in the data frame and store them in gains and loss lists
            gains = []
            losses = []
            for j in range(len(timeframe_close_values)):
                net = timeframe_close_values[j] - timeframe_open_values[j]
                if net > 0:
                    gains.append(net)
                elif net < 0:
                    losses.append(net)
            
            # ------------------Calculate rs and rsi values for data_slice
            
            if gains:                       # If gains != Null, calculate rsi_value, else rsi_value = 50
                avg_gain = sum(gains)/len(gains)
                if losses:                  # If losses != Null, calculate rsi_value, else rsi_value = 50
                    avg_loss = sum(losses)/len(losses)
                    if not avg_loss == 0:   # If avg_loss != Null, calculate rsi_value, else rsi_value = 50
                        rs = avg_gain/avg_loss
                        current_rsi_value = 100-100/(1-rs)
                    else:
                        current_rsi_value = 50
                else:
                    current_rsi_value = 50
            else:
                current_rsi_value = 50

            rsi_values.append(current_rsi_value)
        
        self.rsi_values = rsi_values
        
    # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer

        if self.buffer_setting == 0:
            big_data.buffer = 0

        elif self.buffer_setting == 1:
            big_data.buffer = 3

        elif self.buffer_setting == 2:
            big_data.buffer = 2
    
    # -------------------------DYNAMIC BOUND DEFINITION-------------------
        # Define initial upper and lower bounds
        upper_bound = [70]*len(big_data.data_slice_dates)
        lower_bound = [30]*len(big_data.data_slice_dates)
    
        # Define upper dynamic bound method
        for i in range(len(self.rsi_values)):
            if self.rsi_values[i] > (70 + big_data.buffer):
                new_upper_bound = self.rsi_values[i] - big_data.buffer
                if new_upper_bound >= upper_bound[i-1]:
                    upper_bound[i] = new_upper_bound
                else:
                    upper_bound[i] = upper_bound[i-1]
        
        self.upper_bound = upper_bound
        
        # Define lower dynamic bound method
        for i in range(len(self.rsi_values)):
            if self.rsi_values[i] < (30 - big_data.buffer):
                new_lower_bound = self.rsi_values[i] + big_data.buffer
                if new_lower_bound <= upper_bound[i-1]:
                    lower_bound[i] = new_lower_bound
                else:
                    lower_bound[i] = lower_bound[i-1]
        self.lower_bound = lower_bound

    # ===================== INDICATOR OUTPUT DETERMINATION ==============
        # -----------------Trigger points determination
        # Indicator output
        sell_dates = []
        buy_dates = []
        
        buy_count = 0
        sell_count = 0
        
        sell_rsi = []
        buy_rsi = []

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        sell_trigger = 0
        buy_trigger = 0

        # Defining indicator trigger for...
        for i in range(len(big_data.data_slice)):

            # ...upper bound
            if self.rsi_values[i] >= 70 and sell_trigger == 0:  # Initiate sell trigger
                sell_trigger = 1

            if self.rsi_values[i] <= upper_bound[i] and sell_trigger == 1:  # Trigger sell signal
                sell_count += 1
                sell_dates.append(big_data.data_slice_dates[i])
                sell_rsi.append(self.rsi_values[i])

                sell_trigger = 2

            if self.rsi_values[i] < 70 and sell_trigger == 2:  # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if self.rsi_values[i] <= 30 and buy_trigger == 0:  # Initiate buy trigger
                buy_trigger = 1

            if self.rsi_values[i] >= lower_bound[i] and buy_trigger == 1:  # Trigger buy signal
                buy_count += 1
                buy_dates.append(big_data.data_slice_dates[i])
                buy_rsi.append(self.rsi_values[i])

                buy_trigger = 2

            if self.rsi_values[i] > 30 and sell_trigger == 2:  # Reset trigger
                buy_trigger = 0

        self.sell_rsi = sell_rsi
        self.buy_rsi = buy_rsi

        self.sell_dates = sell_dates
        self.buy_dates = buy_dates

        self.sell_trigger_count = sell_count
        self.buy_trigger_count = buy_count

        # -----------------Bear/Bullish continuous signal
        bb_signal = []

        # Normalising rsi values between -1 and 1
        for i in range(len(self.rsi_values)):
            bb_signal.append((self.rsi_values[i])/max(self.rsi_values)-1)

        for date in self.sell_dates:
            bb_signal[big_data.data_slice_dates.index(date)] = 1

        for date in self.buy_dates:
            bb_signal[big_data.data_slice_dates.index(date)] = 0
        
        self.bb_signal = bb_signal

    # ____________________________________________________________________
    # -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------

    def plot_rsi_and_bounds(self, big_data, plot_rsi=True, plot_upper_bound=True, plot_lower_bound=True, plot_trigger_signals=True):
        import matplotlib.pyplot as plt

        if plot_rsi:
            plt.plot(big_data.data_slice_dates, self.rsi_values)        # Plot RSI

        if plot_upper_bound:
            plt.plot(big_data.data_slice_dates, self.upper_bound)   # Plot upper bound

        if plot_lower_bound:
            plt.plot(big_data.data_slice_dates, self.lower_bound)   # Plot lower bound

        if plot_trigger_signals:
            plt.scatter(self.sell_dates, self.sell_rsi)     # Plot sell signals
            plt.scatter(self.buy_dates, self.buy_rsi)       # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("RSI")
        plt.xlabel("Trade date")
        plt.ylabel("RSI - %")


