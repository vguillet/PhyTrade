# Data Collection using Quandl
from Data_Collection.Quandl import pull_quandl_data
from Indicators.RSI_gen import rsi


quandl_ticker = 'WIKI/AAPL'           # ticker selected for Quandl data collection

data = pull_quandl_data(quandl_ticker)  # Pull data from Quandl

# print(data[0:5])

data_slice = data[-800:-200]               # Slice the data
print("Selected number of points for analysis:", len(data_slice))
# print(data_slice)
rsi, sell_dates_rsi, buy_dates_rsi = rsi(quandl_ticker, data_slice, data)

# Simple Indicator output
sellcount = 0
sell_trigger = True
buycount = 0
buy_trigger = True

for i in rsi:
    if i > 70 and sell_trigger is True:
        sellcount = sellcount + 1
        sell_trigger = False
    if i < 70 and sell_trigger is False:
        sell_trigger = True

    if i < 30 and buy_trigger is True:
        buycount = buycount + 1
        buy_trigger = False
    if i > 30 and buy_trigger is False:
        buy_trigger = True

print("sellcount:", sellcount)
print("buycount:", buycount)
