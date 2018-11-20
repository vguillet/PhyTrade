from Data_Collection.Quandl import pull_quandl_data
from Indicators.RSI_gen import RSI
from Indicators.OC_values import plot_open_close_values

import numpy as np
import matplotlib.pyplot as plt

# -------------------------DATA COLLECTION AND SELECTION------------------------
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection

data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

# Create data slice
data_start_ind = -800
data_stop_ind = -400

# data_start_ind = 0
# data_stop_ind = len(data)

print("Selected number of points for analysis:", data_stop_ind-data_start_ind)

# -------------------------INDICATORS CALCULATION-------------------------------
# --RSI
rsi = RSI(quandl_ticker, data, data_start_ind, data_stop_ind, buffer_setting=1)


# -------------------------SIGNAL PLOTS-----------------------------------------
# Signal plotting
# ------------------Plot Open/Close prices
ax1 = plt.subplot(211)
plot_open_close_values(data, data_start_ind, data_stop_ind, rsi.sell_dates, rsi.buy_dates)

# ------------------Plot RSI
ax2 = plt.subplot(212, sharex=ax1)
rsi.plot_rsi_and_bounds()
plt.show()
