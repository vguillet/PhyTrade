from Data_Collection.Quandl import pull_quandl_data
from Indicators.RSI_gen import RSI

import numpy as np
import matplotlib.pyplot as plt

# -------------------------DATA COLLECTION AND SELECTION------------------------
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection

data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

data_slice = data[-1000:]                    # Create data slice
print("Selected number of points for analysis:", len(data_slice))

# -------------------------INDICATORS CALCULATION-------------------------------
# --RSI
rsi = RSI(quandl_ticker, data_slice, data)


# -------------------------SIGNAL PLOTS-----------------------------------------
# Variable initialisation
dates = list(data_slice.index.values)

close_value_slice = []
open_value_slice = []

# Collect Open and close values in respective lists
for index, row in data_slice.iterrows():
    # ...for the data slice
    close_value_slice.append(row['Close'])
    open_value_slice.append(row['Open'])

# Signal plotting
# Plot
ax1 = plt.subplot(211)
plt.plot(dates, close_value_slice)
plt.plot(dates, open_value_slice)
plt.gcf().autofmt_xdate()
plt.title("Open and close values")
plt.grid()
plt.xlabel("Trade date")
plt.ylabel("Value")

# Plot RSI
ax2 = plt.subplot(212, sharex=ax1)
plt.plot(dates, rsi.upper_bound)
plt.plot(dates, rsi.lower_bound)
# plt.plot(dates, rsi.rsi_values)
plt.gcf().autofmt_xdate()
plt.title("RSI")
plt.grid()
plt.xlabel("Trade date")
plt.ylabel("RSI - %")
plt.show()
