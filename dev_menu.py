from Data_Collection_preparation.Quandl import pull_quandl_data
from Data_Collection_preparation.Big_Data import BIGDATA
from Indicators.RSI_gen import RSI
from Indicators.OC_values import *

import numpy as np
import matplotlib.pyplot as plt

# -------------------------DATA COLLECTION AND SELECTION------------------------
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection
data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

# ---------Analysis definition
ticker = "AAPL"

data_slice_start_ind = -600
data_slice_stop_ind = -400
timeframe_rsi = 14
rsi_buffer_setting = 0

big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind,
                   timeframe_rsi=timeframe_rsi, rsi_buffer_setting=rsi_buffer_setting)

rsi = RSI(big_data)
oc = OC(big_data)

print(len(big_data.data_slice_dates))

# -------------------------SIGNAL PLOTS-----------------------------------------
# ============================================== Plot 1
# ------------------Plot Open/Close prices
ax1 = plt.subplot(311)
oc.plot_open_close_values(big_data)

# ------------------Plot open close diff
ax2 = plt.subplot(312, sharex=ax1)
oc.plot_open_close_values_diff(big_data)

# ------------------Plot RSI
ax3 = plt.subplot(313, sharex=ax1)
rsi.plot_rsi_and_bounds(big_data)
plt.show()

# ============================================== Plot 2
# # ------------------Plot Open/Close prices
ax4 = plt.subplot(211)
oc.plot_open_close_values(big_data)

# ------------------Plot RSI Signal
ax5 = plt.subplot(212)
rsi.plot_rsi_signal(big_data)
plt.show()
