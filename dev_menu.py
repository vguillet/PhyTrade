# Data Collection using Quandl
from Data_Collection.Quandl import pull_quandl_data
from Indicators.RSI_gen import RSI
from Indicators.Open_close_value import plot_open_close_values

# -------------------------DATA COLLECTION AND SELECTION------------------------
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection

data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

data_slice = data[-200:]                    # Create data slice
print("Selected number of points for analysis:", len(data_slice))

# -------------------------INDICATORS CALCULATION-------------------------------
# --RSI
rsi = RSI(quandl_ticker, data_slice, data)
rsi.plot_rsi_and_bounds()

# --OPEN-CLOSE VALUES
plot_open_close_values(data_slice)


print("Run complete")

