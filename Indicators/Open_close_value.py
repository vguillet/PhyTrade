"""
This scripts enable plotting the opening and close value of stocks of a data slice
"""


def plot_open_close_values(data_slice):
    import matplotlib.pyplot as plt

    # Variable initialisation
    dates = list(data_slice.index.values)
    
    close_value_slice = []
    open_value_slice = []
    
    # Collect Open and close values in respective lists
    for index, row in data_slice.iterrows():
        # ...for the data slice
        close_value_slice.append(row['Close'])
        open_value_slice.append(row['Open'])

    plt.plot(dates, close_value_slice)
    plt.plot(dates, open_value_slice)
    plt.gcf().autofmt_xdate()
    plt.title("Open and close value of Apple stocks over time")
    plt.grid()
    plt.xlabel("Trade date")
    plt.ylabel("Value")
    plt.show()

