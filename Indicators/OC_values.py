"""
This scripts enable plotting the opening and close value of stocks of a data slice
"""


def format_data(data, data_start_ind, data_stop_ind):
    # Variable initialisation
    data_slice = data[data_start_ind:data_stop_ind]
    dates = list(data_slice.index.values)

    close_value_slice = []
    open_value_slice = []

    # Collect Open and close values in respective lists
    for index, row in data_slice.iterrows():
        # ...for the data slice
        close_value_slice.append(row['Close'])
        open_value_slice.append(row['Open'])

    return dates, close_value_slice, open_value_slice


def plot_open_close_values(data, data_start_ind, data_stop_ind, sell_dates, buy_dates):
    import matplotlib.pyplot as plt

    # Initial data formatting
    dates, close_value_slice, open_value_slice = format_data(data, data_start_ind, data_stop_ind)

    # List sell and buy triggers
    sell_values = []
    buy_values = []

    for date in sell_dates:
        sell_values.append(close_value_slice[dates.index(date)])

    for date in buy_dates:
        buy_values.append(close_value_slice[dates.index(date)])

    plt.plot(dates, close_value_slice)      # Plot closing value
    plt.plot(dates, open_value_slice)       # Plot opening value

    plt.scatter(sell_dates, sell_values)  # Plot sell signals
    plt.scatter(buy_dates, buy_values)  # Plot buy signals

    plt.gcf().autofmt_xdate()
    plt.title("Open and close values")
    plt.grid()
    plt.xlabel("Trade date")
    plt.ylabel("Value")


def plot_open_close_values_diff(data, data_start_ind, data_stop_ind, sell_dates, buy_dates):
    import matplotlib.pyplot as plt

    # Initial data formatting
    dates, close_value_slice, open_value_slice = format_data(data, data_start_ind, data_stop_ind)

    # Calculate value fluctuation for each point
    value_fluctuation = []

    for i in range(len(dates)):
        value_fluctuation.append(close_value_slice[i] - open_value_slice[i])

    # List sell and buy triggers
    sell_values = []
    buy_values = []

    for date in sell_dates:
        sell_values.append(value_fluctuation[dates.index(date)])

    for date in buy_dates:
        buy_values.append(value_fluctuation[dates.index(date)])

    plt.plot(dates, value_fluctuation)      # Plot value fluctuation

    plt.scatter(sell_dates, sell_values)    # Plot sell signals
    plt.scatter(buy_dates, buy_values)      # Plot buy signals

    plt.gcf().autofmt_xdate()
    plt.title("Open and close values fluctuation")
    plt.grid()
    plt.xlabel("Trade date")
    plt.ylabel("Value fluctuation")
