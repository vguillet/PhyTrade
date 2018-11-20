"""
The RSI indicator script is contained here

"""

def rsi(ticker, data_slice, data):
    import matplotlib.pyplot as plt

# -------------------------DATA PREPROCESSING-------------------------
    # Plot parameter definition:
    timeframe = 25      # Define the time frame used
    rsi = []

    # Fetch the data from the dataframe
    dates = list(data_slice.index.values)
    close_price = []
    open_price = []

    close_price_slice = []
    open_price_slice = []

    # print("".join([ticker, ' - Close']))
    # assert "".join([ticker, ' - Close']) == 'WIKI/AAPL - Close'
    # return

    # Collect Open and close prices in respective lists
    for index, row in data_slice.iterrows():
        # ...for the data slice
        close_price_slice.append(row['Close'])
        open_price_slice.append(row['Open'])

    for index, row in data[-(len(data_slice)+timeframe):].iterrows():
        # ...for the whole dataset
        close_price.append(row['Close'])
        open_price.append(row['Open'])

    print("calculating RSI")

# --------------------------RSI CALCULATION---------------------------
    # Calculate for each date the RSI
    for i in range(len(close_price_slice)):

        timeframe_open_prices = []
        timeframe_close_prices = []

        # Store open and close prices falling in the time frame
        for j in range(timeframe):
                timeframe_open_prices.append(open_price[i - j])
                timeframe_close_prices.append(close_price[i - j])

        # Calculate the net loss or gain for each date falling in the data frame and store them in gains and loss lists
        gains = []
        losses = []
        for j in range(len(timeframe_close_prices)):
            net = timeframe_close_prices[j] - timeframe_open_prices[j]
            if net > 0:
                gains.append(net)
            elif net < 0:
                losses.append(net)

        if gains:                       # If gains != Null, calculate rsi, else rsi = 50
            avg_gain = sum(gains)/len(gains)
            if losses:                  # If losses != Null, calculate rsi, else rsi = 50
                avg_loss = sum(losses)/len(losses)
                if not avg_loss == 0:   # If avg_loss != Null, calculate rsi, else rsi = 50
                    rs = avg_gain/avg_loss
                    current_rsi = 100-100/(1-rs)
                else:
                    current_rsi = 50
            else:
                current_rsi = 50
        else:
            current_rsi = 50

        rsi.append(current_rsi)

        # print("timeframe_open_prices", timeframe_open_prices)
        # print("timeframe_close_prices", timeframe_close_prices)
        # print("Point:", i)
        # print("Gains:", gains)
        # print("losses", losses)
    print("RSI:", len(rsi))
    print("Dates:", len(dates))

# -------------------------WEIGHTED BUFFER DEFINITION-----------------
    buffer = 2

# -------------------------DYNAMIC BOUND DEFINITION-------------------
    # Define initial upper and lower bounds
    upper_bound = [70]*len(dates)
    lower_bound = [30]*len(dates)

    # Define upper dynamic bound method
    for i in range(len(rsi)):
        if rsi[i] > 70 and rsi[i] > (upper_bound[i] + buffer):
            new_upper_bound = rsi[i] - buffer
            if new_upper_bound >= upper_bound[i-1]:
                upper_bound[i] = new_upper_bound
            else:
                upper_bound[i] = upper_bound[i-1]

    # Define lower dynamic bound method
    for i in range(len(rsi)):
        if rsi[i] < 30 and rsi[i] < (upper_bound[i] + buffer):
            new_lower_bound = rsi[i] + buffer
            if new_lower_bound <= upper_bound[i-1]:
                upper_bound[i] = new_lower_bound
            else:
                upper_bound[i] = upper_bound[i-1]

# -------------------------PLOT RSI AND DYNAMIC BOUNDS----------------
    plt.plot(dates, upper_bound)
    plt.plot(dates, lower_bound)
    plt.plot(dates, rsi)
    plt.gcf().autofmt_xdate()
    plt.title("RSI of Apple stocks over time")
    plt.grid()
    plt.xlabel("Trade date")
    plt.ylabel("RSI - %")
    plt.figure(figsize=(70, 70))  # This increases resolution
    plt.show()

# -------------------------DETERMINE INDICATOR OUTPUT-----------------
    # Indicator output
    sellcount = 0
    buycount = 0

    sell_dates = []
    buy_dates = []

    # Buy and sell triggers can take three values, 0 for neutral, 1 for sell at next bound crossing and 2 for post-sell
    sell_trigger = 0
    buy_trigger = 0

    # Defining indicator trigger for...
    for i in range(len(dates)):
        # ...upper bound
        if rsi[i] > 70 and sell_trigger == 0:               # Initiate sell trigger
            sell_trigger = 1
        if rsi[i] < upper_bound[i] and sell_trigger == 1:   # Trigger sell signal
            sellcount += 1
            sell_dates.append(dates[i])
            sell_trigger = 2
        if rsi[i] < 70 and sell_trigger == 2:               # Reset trigger
            sell_trigger = 0

        # ...lower bound
        if rsi[i] < 30 and buy_trigger == 0:                # Initiate buy trigger
            buy_trigger = 1
        if rsi[i] > lower_bound[i] and buy_trigger == 1:    # Trigger buy signal
            buycount += 1
            buy_dates.append(dates[i])
            buy_trigger = 2
        if rsi[i] > 30 and sell_trigger == 2:               # Reset trigger
            buy_trigger = 0

    print("sellcount Db:", sellcount)
    print("buycount Db:", buycount)

    return rsi, sell_dates, buy_dates
