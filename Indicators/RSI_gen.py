"""
The RSI indicator script is contained here
It is currently optimised for Quandl
"""


class RSI:
    def __init__(self, ticker, data_slice, data, timeframe=25, buffer_setting=0):
        """
        :param ticker: Ticker of requested company/product
        :param data_slice: Data slice to analyse
        :param data: Full dataset
        :param timeframe:
        :param buffer_setting: 0: no buffer, 1: fixed value buffer, 2: variable value buffer
        """
        self.ticker = ticker
        self.data_slice = data_slice
        self.data = data

    # -------------------------DATA PRE-PROCESSING------------------------
        self.timeframe = timeframe
        self.rsi_values = []
        # Fetch the data from the dataframe
        self.dates = list(self.data_slice.index.values)

        # Variable initialisation
        close_price = []
        open_price = []

        close_price_slice = []
        open_price_slice = []

        # Collect Open and close prices in respective lists
        for index, row in self.data_slice.iterrows():
            # ...for the data slice
            close_price_slice.append(row['Close'])
            open_price_slice.append(row['Open'])

        for index, row in self.data[-(len(self.data_slice) + self.timeframe):].iterrows():
            # ...for the whole dataset
            close_price.append(row['Close'])
            open_price.append(row['Open'])

    # --------------------------RSI CALCULATION---------------------------
        # Calculate for each date the RSI
        for i in range(len(close_price_slice)):
    
            timeframe_open_prices = []
            timeframe_close_prices = []
    
            # Store open and close prices falling in the time frame
            for j in range(self.timeframe):
                    timeframe_open_prices.append(open_price[i - j])
                    timeframe_close_prices.append(close_price[i - j])
    
            # Calculate the net loss or gain for each date falling 
            # in the data frame and store them in gains and loss lists
            gains = []
            losses = []
            for j in range(len(timeframe_close_prices)):
                net = timeframe_close_prices[j] - timeframe_open_prices[j]
                if net > 0:
                    gains.append(net)
                elif net < 0:
                    losses.append(net)
    
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
    
            self.rsi_values.append(current_rsi_value)
    
            # print("timeframe_open_prices", timeframe_open_prices)
            # print("timeframe_close_prices", timeframe_close_prices)
            # print("Point:", i)
            # print("Gains:", gains)
            # print("losses", losses)
            
        # print("RSI:", len(self.rsi_values))
        # print("Dates:", len(self.dates))
    
    # -------------------------WEIGHTED BUFFER DEFINITION-----------------
        # Buffer settings:
        #       - 0: no buffer
        #       - 1: fixed value buffer
        #       - 2: variable value buffer

        if buffer_setting == 0:
            self.buffer = 0

        elif buffer_setting == 1:
            self.buffer = 2

        elif buffer_setting == 2:
            self.buffer = 2
    
    # -------------------------DYNAMIC BOUND DEFINITION-------------------
        # Define initial upper and lower bounds
        upper_bound = [70]*len(self.dates)
        lower_bound = [30]*len(self.dates)
    
        # Define upper dynamic bound method
        for i in range(len(self.rsi_values)):
            if self.rsi_values[i] > (70 + self.buffer):
                new_upper_bound = self.rsi_values[i] - self.buffer
                if new_upper_bound >= upper_bound[i-1]:
                    upper_bound[i] = new_upper_bound
                else:
                    upper_bound[i] = upper_bound[i-1]
    
        # Define lower dynamic bound method
        for i in range(len(self.rsi_values)):
            if self.rsi_values[i] < (30 - self.buffer):
                new_lower_bound = self.rsi_values[i] + self.buffer
                if new_lower_bound <= upper_bound[i-1]:
                    lower_bound[i] = new_lower_bound
                else:
                    lower_bound[i] = lower_bound[i-1]

    # ===================== INDICATOR OUTPUT DETERMINATION ==============
        # Indicator output
        sellcount = 0
        buycount = 0

        self.sell_dates = []
        self.buy_dates = []

        # Buy and sell triggers can take three values:
        # 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
        self.sell_trigger = 0
        self.buy_trigger = 0

        # Defining indicator trigger for...
        for i in range(len(self.dates)):
            # ...upper bound
            if self.rsi_values[i] >= 70 and self.sell_trigger == 0:  # Initiate sell trigger
                self.sell_trigger = 1
            if self.rsi_values[i] <= upper_bound[i] and self.sell_trigger == 1:  # Trigger sell signal
                sellcount += 1
                self.sell_dates.append(self.dates[i])
                self.sell_trigger = 2
            if self.rsi_values[i] < 70 and self.sell_trigger == 2:  # Reset trigger
                self.sell_trigger = 0

            # ...lower bound
            if self.rsi_values[i] <= 30 and self.buy_trigger == 0:  # Initiate buy trigger
                self.buy_trigger = 1
            if self.rsi_values[i] >= lower_bound[i] and self.buy_trigger == 1:  # Trigger buy signal
                buycount += 1
                self.buy_dates.append(self.dates[i])
                self.buy_trigger = 2
            if self.rsi_values[i] > 30 and self.sell_trigger == 2:  # Reset trigger
                self.buy_trigger = 0

        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

        # print("sellcount Db:", sellcount)
        # print("buycount Db:", buycount)

    # ____________________________________________________________________
    # -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------
    def plot_rsi_and_bounds(self):
        import matplotlib.pyplot as plt
        plt.plot(self.dates, self.upper_bound)
        plt.plot(self.dates, self.lower_bound)
        plt.plot(self.dates, self.rsi_values)
        plt.gcf().autofmt_xdate()
        plt.title("RSI of Apple stocks over time")
        plt.grid()
        plt.xlabel("Trade date")
        plt.ylabel("RSI - %")
        plt.show()
        



