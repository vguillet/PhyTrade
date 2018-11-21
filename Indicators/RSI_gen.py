"""
The RSI indicator script is contained here
It is currently optimised for Quandl
"""


class RSI:
    @staticmethod
    def __init__(big_data):

        # --------------------------RSI CALCULATION---------------------------
        rsi_values = []
        
        for i in range(len(big_data.data_slice)):

            # ------------------Calculate open and close values falling in rsi_timeframe
            timeframe_open_values = []
            timeframe_close_values = []

            for j in range(big_data.rsi_timeframe):
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
            
        setattr(big_data, "rsi_values", rsi_values)
        
    # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer

        if big_data.rsi_buffer_setting == 0:
            big_data.buffer = 0

        elif big_data.rsi_buffer_setting == 1:
            big_data.buffer = 3

        elif big_data.rsi_buffer_setting == 2:
            big_data.buffer = 2
    
    # -------------------------DYNAMIC BOUND DEFINITION-------------------
        # Define initial upper and lower bounds
        upper_bound = [70]*len(big_data.data_slice_dates)
        lower_bound = [30]*len(big_data.data_slice_dates)
    
        # Define upper dynamic bound method
        for i in range(len(big_data.rsi_values)):
            if big_data.rsi_values[i] > (70 + big_data.buffer):
                new_upper_bound = big_data.rsi_values[i] - big_data.buffer
                if new_upper_bound >= upper_bound[i-1]:
                    upper_bound[i] = new_upper_bound
                else:
                    upper_bound[i] = upper_bound[i-1]
        setattr(big_data, "rsi_upper_bound", upper_bound)
        
        # Define lower dynamic bound method
        for i in range(len(big_data.rsi_values)):
            if big_data.rsi_values[i] < (30 - big_data.buffer):
                new_lower_bound = big_data.rsi_values[i] + big_data.buffer
                if new_lower_bound <= upper_bound[i-1]:
                    lower_bound[i] = new_lower_bound
                else:
                    lower_bound[i] = lower_bound[i-1]
        setattr(big_data, "rsi_lower_bound", lower_bound)

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
            if big_data.rsi_values[i] >= 70 and sell_trigger == 0:  # Initiate sell trigger
                sell_trigger = 1

            if big_data.rsi_values[i] <= upper_bound[i] and sell_trigger == 1:  # Trigger sell signal
                sell_count += 1
                sell_dates.append(big_data.data_slice_dates[i])
                sell_rsi.append(big_data.rsi_values[i])

                sell_trigger = 2

            if big_data.rsi_values[i] < 70 and sell_trigger == 2:  # Reset trigger
                sell_trigger = 0

            # ...lower bound
            if big_data.rsi_values[i] <= 30 and buy_trigger == 0:  # Initiate buy trigger
                buy_trigger = 1

            if big_data.rsi_values[i] >= lower_bound[i] and buy_trigger == 1:  # Trigger buy signal
                buy_count += 1
                buy_dates.append(big_data.data_slice_dates[i])
                buy_rsi.append(big_data.rsi_values[i])

                buy_trigger = 2

            if big_data.rsi_values[i] > 30 and sell_trigger == 2:  # Reset trigger
                buy_trigger = 0

        setattr(big_data, "rsi_sell_rsi", sell_rsi)
        setattr(big_data, "rsi_buy_rsi", buy_rsi)

        setattr(big_data, "rsi_sell_dates", sell_dates)
        setattr(big_data, "rsi_buy_dates", buy_dates)
        
        setattr(big_data, "rsi_sell_count", sell_count)
        setattr(big_data, "rsi_buy_count", buy_count)

        # -----------------Bear/Bullish continuous signal
        bb_signal = []

        for i in range(len(big_data.rsi_values)):
            bb_signal.append((big_data.rsi_values[i])/max(big_data.rsi_values)-1)

        for date in big_data.rsi_sell_dates:
            bb_signal[big_data.data_slice_dates.index(date)] = 1

        for date in big_data.rsi_buy_dates:
            bb_signal[big_data.data_slice_dates.index(date)] = 0
        
        setattr(big_data, "rsi_bb_signal", bb_signal)

    # ____________________________________________________________________
    # -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------

    @staticmethod
    def plot_rsi_and_bounds(big_data):
        import matplotlib.pyplot as plt

        plt.plot(big_data.data_slice_dates, big_data.rsi_upper_bound)   # Plot upper bound
        plt.plot(big_data.data_slice_dates, big_data.rsi_lower_bound)   # Plot lower bound

        plt.plot(big_data.data_slice_dates, big_data.rsi_values)        # Plot RSI

        plt.scatter(big_data.rsi_sell_dates, big_data.rsi_sell_rsi)         # Plot sell signals
        plt.scatter(big_data.rsi_buy_dates, big_data.rsi_buy_rsi)           # Plot buy signals

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("RSI")
        plt.xlabel("Trade date")
        plt.ylabel("RSI - %")
        # plt.show()

    @staticmethod
    def plot_rsi_signal(big_data):
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.interpolate import UnivariateSpline

        x = np.array(range(len(big_data.data_slice_dates)))
        y = np.array(big_data.rsi_bb_signal)

        rsi_bb_spl = UnivariateSpline(x, y)
        xs = np.linspace(0, 200, len(big_data.data_slice_dates)*5)
        rsi_bb_spl.set_smoothing_factor(0.7)

        plt.plot(xs, rsi_bb_spl(xs), 'g', lw=3)

        plt.plot(range(len(big_data.data_slice_dates)), big_data.rsi_bb_signal)            # Plot rsi continuous signal

        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.title("RSI signal")
        plt.xlabel("Trade date")
        plt.ylabel("Signal power")
        # plt.show()

