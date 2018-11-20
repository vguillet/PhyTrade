"""
This script contains the tests for the RSI_gen script
"""
import pytest


@pytest.fixture()
def data():
    from Data_Collection.Quandl import pull_quandl_data

    quandl_ticker = 'WIKI/AAPL'  # ticker selected for Quandl data collection
    data = pull_quandl_data(quandl_ticker)  # Pull data from Quandl
    return data, quandl_ticker


def test_dynamic_boundary(data):
    from Indicators.RSI_gen import RSI

    # Pull data
    data, quandl_ticker = data

    # Slice data
    data_slice = data[-800:-200]

    # Initiate RSI instance
    rsi_inst = RSI(quandl_ticker, data_slice, data, buffer_setting=0)
    rsi = rsi_inst.rsi_values

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

    assert sell_trigger == rsi_inst.sell_trigger
    assert buy_trigger == rsi_inst.buy_trigger
