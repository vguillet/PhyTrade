"""
Prototype 1

This prototype is based entirely on technical analysis, and is ment as a test for the spline toolbox and RSI, SMA and OC
indicators

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
from Technical_Analysis.Tools.Major_spline_gen import MAJOR_SPLINE

import numpy as np


class Prototype_1:
    def __init__(self):

        # ========================= DATA COLLECTION INITIALISATION =======================
        quandl_ticker = 'WIKI/AAPL'                 # Ticker selected for Quandl data collection
        data = pull_quandl_data(quandl_ticker)      # Pull data from Quand

        # ========================= ANALYSIS INITIALISATION ==============================
        ticker = "AAPL"
        data_slice_start_ind = -70
        data_slice_stop_ind = len(data)-10
    
        self.big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

        # ------------------ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)

        # ------------------ Indicators initialisation
        setattr(self.big_data, "rsi", RSI(self.big_data, timeframe=14))
        setattr(self.big_data, "sma_1", SMA(self.big_data, timeperiod_1=10, timeperiod_2=25))
        setattr(self.big_data, "sma_2", SMA(self.big_data, timeperiod_1=5, timeperiod_2=15))
    
        setattr(self.big_data, "volume", Volume(self.big_data))

        # ================================================================================
        """
        
        
        
        
        
        
        
        
        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ------------------ Indicators output generation
        self.big_data.rsi.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.sma_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_2.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # ------------------ BB signals processing
        # -- Creating splines from signals
        setattr(self.big_data, "spline_rsi",
                self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi.bb_signal, smoothing_factor=.3))
    
        setattr(self.big_data, "spline_oc_avg_gradient",
                self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.oc_avg_gradient_bb_signal, smoothing_factor=5))
    
        setattr(self.big_data, "spline_sma_1",
                self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_1.bb_signal, smoothing_factor=1))
        setattr(self.big_data, "spline_sma_2",
                self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_2.bb_signal, smoothing_factor=1))
    
        setattr(self.big_data, "spline_volume",
                self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef, smoothing_factor=0.5))
    
        # -- Adding signals together
        setattr(self.big_data, "combined_spline", self.spline_tools.combine_splines(self.big_data,
                                                                                    self.big_data.spline_rsi,
                                                                                    self.big_data.spline_oc_avg_gradient,
                                                                                    self.big_data.spline_sma_1,
                                                                                    self.big_data.spline_sma_2,
                                                                                    weight_1=1,
                                                                                    weight_2=3,
                                                                                    weight_3=4,
                                                                                    weight_4=3))

        # -- Tuning combined signal
        self.big_data.combined_spline = \
            self.spline_tools.increase_amplitude_spline(self.big_data.combined_spline, self.big_data.spline_volume)

        # -- Creating Major Spline
        setattr(self.big_data, "Major_spline",
                MAJOR_SPLINE(self.big_data, self.big_data.combined_spline, threshold_buffer_setting=1,
                             upper_threshold=0.45, lower_threshold=-0.45))

    # ================================================================================
    """








    """
    # ========================= SIGNAL PLOTS =========================================
    def plot(self, plot_1=True, plot_2=True, plot_3=True):

        import matplotlib.pyplot as plt

        # ---------------------------------------------- Plot 1
        if plot_1:
            # ------------------ Plot Open/Close prices
            ax1 = plt.subplot(211)
            self.oc_tools.plot_oc_values(self.big_data)
            # oc.plot_trigger_values(self.big_data)

            # ------------------ Plot RSI
            ax2 = plt.subplot(212, sharex=ax1)
            self.big_data.rsi.plot_rsi(self.big_data)
            plt.show()

        if plot_2:
            # ---------------------------------------------- Plot 2
            # ------------------ Plot Open/Close prices
            ax3 = plt.subplot(211)
            self.oc_tools.plot_oc_values(self.big_data)
            # oc.plot_trigger_values(self.big_data)

            # ------------------ Plot SMA Signal
            ax4 = plt.subplot(212, sharex=ax3)
            self.big_data.sma_1.plot_sma(self.big_data, plot_trigger_signals=False)
            plt.show()

        if plot_3:
            # ---------------------------------------------- Plot 3
            # ------------------ Plot Open/Close prices
            ax5 = plt.subplot(211)
            self.oc_tools.plot_oc_values(self.big_data)
            self.oc_tools.plot_trigger_values(
                self.big_data, self.big_data.Major_spline.sell_dates, self.big_data.Major_spline.buy_dates)

            # ------------------ Plot bb signal(s)
            ax6 = plt.subplot(212)
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_rsi, label="RSI bb spline")
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_oc_avg_gradient, label="OC gradient bb spline", color='m')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_1, label="SMA_1 bb spline", color='r')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_2, label="SMA_2 bb spline", color='b')
            #
            self.spline_tools.plot_spline(
                self.big_data, self.big_data.Major_spline.spline, label="Major spline", color='y')

            self.spline_tools. plot_spline(
                self.big_data, self.big_data.Major_spline.upper_threshold, label="Upper threshold")
            self.spline_tools. plot_spline(
                self.big_data, self.big_data.Major_spline.lower_threshold, label="Lower threshold")

            self.spline_tools.plot_spline_trigger(
                self.big_data, self.big_data.Major_spline.spline, self.big_data.Major_spline.sell_dates, self.big_data.Major_spline.buy_dates)
            # TODO fix spline trigger points plot

            # self.spline_tools.plot_spline(self.big_data, self.big_data.spline_volume, label="Volume", color='k')
            plt.show()
