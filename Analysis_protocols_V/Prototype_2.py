"""
Prototype 2

This prototype is based entirely on technical analysis, and is ment as a test for the spline toolbox and RSI, SMA and OC
indicators

Victor Guillet
11/28/2018
"""

from PhyTrade.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA
from PhyTrade.Technical_Analysis.Data_Collection_preparation.Yahoo import pull_yahoo_data

from PhyTrade.Technical_Analysis.Indicators.RSI_gen import RSI
from PhyTrade.Technical_Analysis.Indicators.SMA_gen import SMA

from PhyTrade.Technical_Analysis.Amplification_signals.Volume_gen import VOLUME
from PhyTrade.Technical_Analysis.Amplification_signals.Volatility_gen import VOLATILITY

from PhyTrade.Technical_Analysis.Tools.Major_spline_gen import MAJOR_SPLINE
from PhyTrade.Technical_Analysis.Tools.MATH_tools import MATH
from PhyTrade.Technical_Analysis.Tools.OC_tools import OC
from PhyTrade.Technical_Analysis.Tools.SPLINE_tools import SPLINE


class Prototype_2:
    def __init__(self):

        # ========================= DATA COLLECTION INITIALISATION =======================
        ticker = 'AAPL'                     # Ticker selected for Yahoo data collection
        data = pull_yahoo_data(ticker)      # Pull data from Yahoo

        # ========================= ANALYSIS INITIALISATION ==============================
        data_slice_start_ind = -200
        data_slice_stop_ind = len(data)

        self.big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

        # ------------------ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)
        self.math_tools = MATH()

        # ------------------ Indicators initialisation
        self.big_data.rsi = RSI(self.big_data, timeframe=14)
        self.big_data.sma_1 = SMA(self.big_data, timeperiod_1=5, timeperiod_2=15)
        self.big_data.sma_2 = SMA(self.big_data, timeperiod_1=10, timeperiod_2=25)
        self.big_data.sma_3 = SMA(self.big_data, timeperiod_1=20, timeperiod_2=45)

        self.big_data.volume = VOLUME(self.big_data, amplification_factor=1.2)
        self.big_data.volatility = VOLATILITY(self.big_data, timeframe=15, amplification_factor=1.2)

        # ================================================================================
        """
        
        
        
        
        
        
        
        
        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ~~~~~~~~~~~~~~~~~~ Indicators output generation
        self.big_data.rsi.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.sma_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_2.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_3.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # ~~~~~~~~~~~~~~~~~~ BB signals processing
        # -- Creating splines from signals
        self.big_data.spline_rsi = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi.bb_signal, smoothing_factor=.3)

        self.big_data.spline_oc_avg_gradient = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.oc_avg_gradient_bb_signal, smoothing_factor=1)

        self.big_data.spline_sma_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_1.bb_signal, smoothing_factor=1)
        self.big_data.spline_sma_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_2.bb_signal, smoothing_factor=1)
        self.big_data.spline_sma_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_3.bb_signal, smoothing_factor=1)

        # -- Generating amplification signals
        self.big_data.spline_volume = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef, smoothing_factor=0.5)

        self.big_data.spline_volatility = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volatility.amp_coef, smoothing_factor=0.5)

        # -- Tuning separate signals
        self.big_data.spline_sma_3 = self.spline_tools.flip_spline(self.big_data.spline_sma_3)

        # -- Adding signals together
        self.big_data.combined_spline = \
            self.spline_tools.combine_splines(self.big_data,
                                              self.big_data.spline_rsi,
                                              self.big_data.spline_oc_avg_gradient,
                                              self.big_data.spline_sma_1,
                                              self.big_data.spline_sma_2,
                                              self.big_data.spline_sma_3,
                                              weight_1=6,
                                              weight_2=1,
                                              weight_3=3,
                                              weight_4=3,
                                              weight_5=3)

        # -- Tuning combined signal
        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volume, std_dev_max=3)

        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volatility, std_dev_max=3)

        self.big_data.combined_spline = self.math_tools.normalise_minus_one_one(self.big_data.combined_spline)

        # ~~~~~~~~~~~~~~~~~~ Threshold determination
        # -- Creating dynamic thresholds
        upper_threshold, lower_threshold = \
            self.big_data.combined_spline.calc_thresholds(self.big_data, self.big_data.combined_spline,
                                                          buffer=0.05, buffer_setting=0,
                                                          standard_upper_threshold=0.6,
                                                          standard_lower_threshold=0.6)

        # -- Modulating threshold with SMA 3 value
        self.big_data.upper_threshold = \
            self.spline_tools.modulate_amplitude_spline(
                upper_threshold,  self.math_tools.amplify(
                    self.math_tools.normalise_zero_one(self.big_data.spline_sma_3), 1))

        # ~~~~~~~~~~~~~~~~~~ Creating Major Spline/trigger values
        self.big_data.Major_spline = MAJOR_SPLINE(self.big_data, self.big_data.combined_spline,
                                                  upper_threshold, lower_threshold)

    # ================================================================================
    """








    """
    # ========================= SIGNAL PLOTS =========================================
    def plot(self, plot_1=True, plot_2=True, plot_3=True):
        import matplotlib.pyplot as plt

        if plot_1:
            # ---------------------------------------------- Plot 1
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
            #     self.big_data, self.big_data.spline_sma_1, label="SMA_1 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_2, label="SMA_2 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_3, label="SMA_3 bb spline", color='r')

            self.spline_tools.plot_spline(
                self.big_data, self.big_data.Major_spline.spline, label="Major spline", color='y')

            self.spline_tools. plot_spline(
                self.big_data, self.big_data.Major_spline.upper_threshold, label="Upper threshold")
            self.spline_tools. plot_spline(
                self.big_data, self.big_data.Major_spline.lower_threshold, label="Lower threshold")

            self.spline_tools.plot_spline_trigger(
                self.big_data, self.big_data.Major_spline.spline, self.big_data.Major_spline.sell_dates, self.big_data.Major_spline.buy_dates)

            # self.spline_tools.plot_spline(self.big_data, self.big_data.spline_volume, label="Volume", color='k')
            # self.spline_tools.plot_spline(self.big_data, self.big_data.spline_volatility, label="Volatility", color='grey')
            plt.show()
