"""
This scripts enable plotting the opening and close value of stocks of a data slice
"""


def plot_open_close_values(data, data_start_ind, data_stop_ind, sell_dates, buy_dates):
    import matplotlib.pyplot as plt

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

    # List sell and buy triggers
    sell_values = []
    buy_values = []

    for date in sell_dates:
        sell_values.append(close_value_slice[dates.index(date)])

    for date in buy_dates:
        buy_values.append(open_value_slice[dates.index(date)])

    plt.plot(dates, close_value_slice)      # Plot closing value
    plt.plot(dates, open_value_slice)       # Plot opening value

    plt.scatter(sell_dates, sell_values)  # Plot sell signals
    plt.scatter(buy_dates, buy_values)  # Plot buy signals

    plt.gcf().autofmt_xdate()
    plt.title("Open and close values")
    plt.grid()
    plt.xlabel("Trade date")
    plt.ylabel("Value")


