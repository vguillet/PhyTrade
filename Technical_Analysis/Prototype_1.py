"""
This script is a prototype making use of the full PhyTrade library, as a mean of testing and optimizing.
The code is uncommented and messy as it is meant for personal experimentation

Victor Guillet
11/28/2018
"""

from Technical_Analysis.Data_Collection_preparation.Quandl import pull_quandl_data
from Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA

from Technical_Analysis.Indicators.RSI_gen import RSI
from Technical_Analysis.Indicators.SMA_gen import SMA
from Technical_Analysis.Indicators.Volume_gen import Volume

from Technical_Analysis.Tools.OC_gen import OC
from Technical_Analysis.Tools.SPLINE_gen import SPLINE

import numpy as np

# ========================= DATA COLLECTION INITIALISATION =======================
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection
data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

# print(data)
# ========================= ANALYSIS INITIALISATION ==============================
ticker = "AAPL"
data_slice_start_ind = -250
data_slice_stop_ind = len(data)-10


big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

# ------------------ Indicators initialisation
setattr(big_data, "rsi", RSI(big_data, timeframe=14))
setattr(big_data, "sma_1", SMA(big_data, timeperiod_1=10, timeperiod_2=25))
setattr(big_data, "sma_2", SMA(big_data, timeperiod_1=5, timeperiod_2=15))

setattr(big_data, "volume", Volume(big_data))

# ------------------ Tools initialisation
oc = OC()
spline = SPLINE(big_data)


# ========================= DATA GENERATION AND PROCESSING =======================
# ------------------ Indicators output generation
big_data.rsi.get_output(big_data, include_triggers_in_bb_signal=True)
big_data.sma_1.get_output(big_data, include_triggers_in_bb_signal=False)
big_data.sma_2.get_output(big_data, include_triggers_in_bb_signal=False)

# ------------------ Trigger value determination
# oc.calc_trigger_values(big_data, big_data.rsi.sell_dates, big_data.rsi.buy_dates)

oc.calc_trigger_values(big_data, big_data.sma_1.sell_dates, big_data.sma_1.buy_dates)
oc.calc_trigger_values(big_data, big_data.sma_2.sell_dates, big_data.sma_2.buy_dates)

print(big_data.sell_trigger_values)
print(big_data.sell_trigger_dates)

print(big_data.buy_trigger_values)
print(big_data.buy_trigger_dates)

# ------------------ BB signals processing

# -- Creating thresholds
setattr(big_data, "signal_spline_upper_threshold", spline.calc_upper_threshold(big_data))
setattr(big_data, "signal_spline_lower_threshold", spline.calc_lower_threshold(big_data))

# -- Creating signals
setattr(big_data, "signal_spline_rsi",
        spline.calc_signal_spline(big_data, big_data.rsi.bb_signal, smoothing_factor=.3))

setattr(big_data, "signal_spline_oc_avg_gradient",
        spline.calc_signal_spline(big_data, big_data.oc_avg_gradient_bb_signal, smoothing_factor=5))


setattr(big_data, "signal_spline_sma_1",
        spline.calc_signal_spline(big_data, big_data.sma_1.bb_signal, smoothing_factor=1))
setattr(big_data, "signal_spline_sma_2",
        spline.calc_signal_spline(big_data, big_data.sma_2.bb_signal, smoothing_factor=1))

setattr(big_data, "signal_spline_volume",
        spline.calc_signal_spline(big_data, big_data.volume.amp_coef, smoothing_factor=0.5))

# -- Tuning separate signals
# big_data.signal_spline_oc_avg_gradient = spline.shift_signal(big_data.signal_spline_oc_avg_gradient, 15)


# -- Adding signals together
setattr(big_data, "signal_splines_combined", spline.combine_signal_splines(big_data,
                                                                           big_data.signal_spline_rsi,
                                                                           big_data.signal_spline_oc_avg_gradient,
                                                                           big_data.signal_spline_sma_1,
                                                                           big_data.signal_spline_sma_2,
                                                                           weight_1=1,
                                                                           weight_2=3,
                                                                           weight_3=4,
                                                                           weight_4=3))

# -- Tuning combined signal
big_data.signal_splines_combined = \
    spline.increase_amplitude_signal(big_data.signal_splines_combined, big_data.signal_spline_volume)

"""
# -- Obtaining trigger value from master signal
trigger_sell_lst = []
trigger_buy_lst = []

for i in range(len(big_data.signal_splines_combined)):
    if big_data.signal_splines_combined[i] > big_data.signal_spline_upper_threshold[i]:
        trigger_sell_lst.append(big_data.signal_splines_combined[i])

for i in range(len(big_data.signal_splines_combined)):
    if big_data.signal_splines_combined[i] < big_data.signal_spline_lower_threshold[i]:
        trigger_buy_lst.append(big_data.signal_splines_combined[i])
"""

# ========================= SIGNAL PLOTS =========================================
import matplotlib.pyplot as plt


# ---------------------------------------------- Plot 1
# ------------------ Plot Open/Close prices
ax1 = plt.subplot(211)
oc.plot_open_close_values(big_data)
# oc.plot_trigger_values(big_data)

# ------------------ Plot RSI
ax2 = plt.subplot(212, sharex=ax1)
big_data.rsi.plot_rsi_and_bounds(big_data)
plt.show()


# ---------------------------------------------- Plot 2
# ------------------ Plot Open/Close prices
ax3 = plt.subplot(211)
oc.plot_open_close_values(big_data)
# oc.plot_trigger_values(big_data)

# ------------------ Plot SMA Signal
ax4 = plt.subplot(212, sharex=ax3)
big_data.sma_1.plot_sma(big_data, plot_trigger_signals=False)
plt.show()


# ---------------------------------------------- Plot 3
# ------------------ Plot Open/Close prices
ax5 = plt.subplot(211)
oc.plot_open_close_values(big_data)
# oc.plot_trigger_values(big_data)

# ------------------ Plot bb signal(s)
ax6 = plt.subplot(212)
spline.plot_signal_spline(big_data, big_data.signal_spline_rsi, label="RSI bb signal")
spline.plot_signal_spline(big_data, big_data.signal_spline_oc_avg_gradient, label="OC gradient bb signal", color='m')
spline.plot_signal_spline(big_data, big_data.signal_spline_sma_1, label="SMA_1 bb signal", color='r')
spline.plot_signal_spline(big_data, big_data.signal_spline_sma_2, label="SMA_2 bb signal", color='b')

spline.plot_signal_spline(big_data, big_data.signal_splines_combined, label="Combined weighted bb signal", color='y')

spline. plot_signal_spline(big_data, big_data.signal_spline_upper_threshold, label="Upper threshold")
spline. plot_signal_spline(big_data, big_data.signal_spline_lower_threshold, label="Lower threshold")

spline. plot_signal_spline(big_data, big_data.signal_spline_volume, label="Volume", color='k')
plt.show()

# print(big_data.__dict__.keys())
