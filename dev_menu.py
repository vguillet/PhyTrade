"""
This script is a prototype making use of the full PhyTrade library, as a mean of testing and optimizing

Victor Guillet
11/28/2018
"""

from Data_Collection_preparation.Quandl import pull_quandl_data
from Data_Collection_preparation.Big_Data import BIGDATA

from Indicators.RSI_gen import RSI
from Indicators.SMA_gen import SMA

from Tools.OC_gen import OC
from Tools.SPLINE_gen import SPLINE


# ========================= DATA COLLECTION INITIALISATION =======================
# Data Collection using Quandl
quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection
data = pull_quandl_data(quandl_ticker)      # Pull data from Quandl

print(data)
# ========================= ANALYSIS INITIALISATION ==============================
ticker = "AAPL"
data_slice_start_ind = -200
data_slice_stop_ind = len(data)-10


big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

# ------------------ Indicators initialisation
setattr(big_data, "rsi", RSI(big_data))     # Create RSI property
setattr(big_data, "sma", SMA(big_data))      # Create SMA property

# ------------------ Tools initialisation
oc = OC()
spline = SPLINE(big_data)


# ========================= DATA GENERATION AND PROCESSING =======================

# ------------------ Trigger value determination
oc.calc_trigger_values(big_data, big_data.rsi.sell_dates, big_data.rsi.buy_dates)

# ------------------ Signal processing
setattr(big_data, "signal_spline_rsi",
        spline.calc_signal_spline(big_data, big_data.rsi.bb_signal))

setattr(big_data, "signal_spline_oc_avg_gradient",
        spline.calc_signal_spline(big_data, big_data.oc_avg_gradient_bb_signal, smoothing_factor=4))

setattr(big_data, "signal_spline_sma",
        spline.calc_signal_spline(big_data, big_data.sma.bb_signal))

signals = [big_data.signal_spline_rsi, big_data.signal_spline_oc_avg_gradient, big_data.signal_spline_sma]
setattr(big_data, "signal_splines_combined", spline.combine_signal_splines(big_data, signals))

setattr(big_data, "signal_splines_weight_combined", spline.combine_weighted_signal_splines(big_data,
                                                                                           big_data.signal_spline_rsi,
                                                                                           big_data.signal_spline_oc_avg_gradient,
                                                                                           big_data.signal_spline_sma,
                                                                                           weight_1=1,
                                                                                           weight_2=1,
                                                                                           weight_3=2))
# ========================= SIGNAL PLOTS =========================================
import matplotlib.pyplot as plt


# ---------------------------------------------- Plot 1
# ------------------ Plot Open/Close prices
ax1 = plt.subplot(211)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot RSI
ax2 = plt.subplot(212, sharex=ax1)
big_data.rsi.plot_rsi_and_bounds(big_data)
plt.show()


# ---------------------------------------------- Plot 2
# ------------------ Plot Open/Close prices
ax3 = plt.subplot(211)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot SMA Signal
ax4 = plt.subplot(212, sharex=ax3)
big_data.sma.plot_sma(big_data, plot_trigger_signals=False)
plt.show()


# ---------------------------------------------- Plot 3
# ------------------ Plot Open/Close prices
ax5 = plt.subplot(211)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot bb signal(s)
ax6 = plt.subplot(212)
# spline.plot_signal_spline(big_data, big_data.signal_spline_rsi, label="RSI bb signal")
spline.plot_signal_spline(big_data, big_data.signal_spline_sma, label="SMA bb signal", color='r')
# spline.plot_signal_spline(big_data, big_data.signal_spline_oc_avg_gradient, label="OC gradient bb signal", color='m')

# spline.plot_signal_spline(big_data, big_data.signal_splines_combined, label="Combined bb signal", color='b')
spline.plot_signal_spline(big_data, big_data.signal_splines_weight_combined, label="Combined weighted bb signal", color='y')
plt.show()

print(big_data.__dict__.keys())
