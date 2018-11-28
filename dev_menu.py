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


# ========================= ANALYSIS INITIALISATION ==============================
ticker = "AAPL"
data_slice_start_ind = -400
data_slice_stop_ind = len(data)

big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

# ------------------ Indicators initialisation
setattr(big_data, "rsi", RSI(big_data))     # Create RSI property

setattr(big_data, "sma", SMA(big_data))      # Create SMA property

# ------------------ Tools initialisation
oc = OC()
spline = SPLINE(big_data)


# ========================= DATA GENERATION AND PROCESSING =======================
oc.calc_trigger_values(big_data, big_data.rsi.sell_dates, big_data.rsi.buy_dates)

# ------------------ Signal processing
setattr(big_data, "rsi_signal_spline",
        spline.calc_signal_spline(big_data, big_data.rsi.bb_signal))

setattr(big_data, "oc_avg_gradient_signal_spline",
        spline.calc_signal_spline(big_data, big_data.oc_avg_gradient_bb_signal, smoothing_factor=4))

signals = [big_data.rsi_signal_spline, big_data.oc_avg_gradient_signal_spline]
spline.combine_signal_splines(big_data, signals)


# ========================= SIGNAL PLOTS =========================================
import matplotlib.pyplot as plt

# ---------------------------------------------- Plot 1
# ------------------ Plot Open/Close prices
ax1 = plt.subplot(311)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot open close diff
ax2 = plt.subplot(312, sharex=ax1)
oc.plot_open_close_values_diff(big_data)

# ------------------ Plot RSI
ax3 = plt.subplot(313, sharex=ax1)
big_data.rsi.plot_rsi_and_bounds(big_data)
plt.show()


# ---------------------------------------------- Plot 2
# ------------------ Plot Open/Close prices
ax4 = plt.subplot(211)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot SMA Signal
ax5 = plt.subplot(212, sharex=ax4)
big_data.sma.plot_sma(big_data, plot_trigger_signals=False)
plt.show()


# ---------------------------------------------- Plot 3
# ------------------ Plot Open/Close prices
ax6 = plt.subplot(211)
oc.plot_open_close_values(big_data)
oc.plot_trigger_values(big_data)

# ------------------ Plot bb signal(s)
ax7 = plt.subplot(212)
spline.plot_signal_spline(big_data, big_data.rsi_signal_spline, label="RSI bb signal")
# spline.plot_signal_spline(big_data, big_data.oc_avg_gradient_signal_spline)
spline.plot_signal_spline(big_data, big_data.combined_signal_splines, label="Combined bb signal", color='b')
plt.show()

print(big_data.__dict__.keys())
