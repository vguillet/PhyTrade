from Data_Collection_preparation.Quandl import pull_quandl_data
from Indicators.RSI_gen import RSI
from Indicators.OC_values import *

import numpy as np
import matplotlib.pyplot as plt

# -------------------------DATA COLLECTION AND SELECTION------------------------
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection

data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

# Create data slice
data_start_ind = -600
data_stop_ind = -400

# data_start_ind = 0
# data_stop_ind = len(data)

print("Selected number of points for analysis:", data_stop_ind-data_start_ind)

# -------------------------INDICATORS CALCULATION-------------------------------
# --RSI
rsi = RSI(quandl_ticker, data, data_start_ind, data_stop_ind, timeframe=14, buffer_setting=1)


# -------------------------SIGNAL PLOTS-----------------------------------------
# ============================================== Plot 1
# ------------------Plot Open/Close prices
ax1 = plt.subplot(311)
plot_open_close_values(data, data_start_ind, data_stop_ind, rsi.sell_dates, rsi.buy_dates)

# ------------------Plot open close diff
ax2 = plt.subplot(312, sharex=ax1)
plot_open_close_values_diff(data, data_start_ind, data_stop_ind, rsi.sell_dates, rsi.buy_dates)

# ------------------Plot RSI
ax3 = plt.subplot(313, sharex=ax1)
rsi.plot_rsi_and_bounds()
plt.show()

# ============================================== Plot 2
# # ------------------Plot Open/Close prices
ax4 = plt.subplot(211)
plot_open_close_values(data, data_start_ind, data_stop_ind, rsi.sell_dates, rsi.buy_dates)

# ------------------Plot RSI Signal
ax5 = plt.subplot(212)
rsi.plot_rsi_signal()
plt.show()
