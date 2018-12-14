"""
Prototype 3

This prototype is based entirely on technical analysis, and is ment as a test for the genetic algorithm parameter
optimisation algorithm
Victor Guillet
12/14/2018
"""

from PhyTrade.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA

from PhyTrade.Technical_Analysis.Indicators.RSI_gen import RSI
from PhyTrade.Technical_Analysis.Indicators.SMA_gen import SMA

from PhyTrade.Technical_Analysis.Amplification_signals.Volume_gen import VOLUME
from PhyTrade.Technical_Analysis.Amplification_signals.Volatility_gen import VOLATILITY

from PhyTrade.Technical_Analysis.Data_Collection_preparation.MAJOR_SPLINE_gen import MAJOR_SPLINE
from PhyTrade.Tools.MATH_tools import MATH
from PhyTrade.Technical_Analysis.Tools.OC_tools import OC
from PhyTrade.Technical_Analysis.Tools.SPLINE_tools import SPLINE

import pandas


class Prototype_3:
    def __init__(self, parameters):

        # ========================= DATA COLLECTION INITIALISATION =======================
        ticker = 'AAPL'  # Ticker selected for Yahoo data collection
        # data = pull_yahoo_data(ticker)  # Pull data from Yahoo

        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Steffegium\Data\AAPL_Yahoo_data.csv".replace(
            '\\', '/')

        data = pandas.read_csv(path)

        # ========================= ANALYSIS INITIALISATION ==============================
        data_slice_start_ind = -400
        data_slice_stop_ind = len(data)

        self.big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

        # ------------------ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)
        self.math_tools = MATH()

        # ------------------ Indicators initialisation
        # -- RSI initialisation
        self.big_data.rsi_1 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"][0],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"][0],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"][0])

        self.big_data.rsi_2 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"][1],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"][1],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"][1])

        self.big_data.rsi_3 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"][2],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"][2],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"][2])

        # -- SMA initialisation
        self.big_data.sma_1 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"][3],
                                  timeperiod_2=parameters["timeframe"][6])

        self.big_data.sma_2 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"][4],
                                  timeperiod_2=parameters["timeframe"][7])

        self.big_data.sma_3 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"][5],
                                  timeperiod_2=parameters["timeframe"][8])

        # -- Volume initialisation
        self.big_data.volume = VOLUME(self.big_data,
                                      amplification_factor=parameters["amplification_factor"][0])

        # -- Volatility initialisation
        self.big_data.volatility = VOLATILITY(self.big_data,
                                              timeframe=parameters["timeframe"][9],
                                              amplification_factor=parameters["amplification_factor"][1])

        # ================================================================================
        """




        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ~~~~~~~~~~~~~~~~~~ Indicators output generation
        # - RSI
        self.big_data.rsi_1.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.rsi_2.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.rsi_3.get_output(self.big_data, include_triggers_in_bb_signal=True)

        # - SMA
        self.big_data.sma_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_2.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_3.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # ~~~~~~~~~~~~~~~~~~ BB signals processing
        # -- Creating splines from signals
        # - RSI
        self.big_data.spline_rsi_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][0])

        self.big_data.spline_rsi_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][1])

        self.big_data.spline_rsi_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][2])

        # - SMA
        self.big_data.spline_sma_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][3])
        self.big_data.spline_sma_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][4])
        self.big_data.spline_sma_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][5])

        # - OC avg gradient
        self.big_data.spline_oc_avg_gradient = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.oc_avg_gradient_bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"][6])

        # -- Generating amplification signals
        self.big_data.spline_volatility = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volatility.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"][7])

        self.big_data.spline_volume = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"][8])

        # -- Tuning separate signals
        self.big_data.spline_sma_3 = self.spline_tools.flip_spline(self.big_data.spline_sma_3)

        # -- Adding signals together
        self.big_data.combined_spline = \
            self.spline_tools.combine_7_splines(self.big_data,
                                                self.big_data.spline_oc_avg_gradient,
                                                self.big_data.spline_rsi_1,
                                                self.big_data.spline_rsi_2,
                                                self.big_data.spline_rsi_3,
                                                self.big_data.spline_sma_1,
                                                self.big_data.spline_sma_2,
                                                self.big_data.spline_sma_3,
                                                weight_1=parameters["weights"][6],
                                                weight_2=parameters["weights"][0],
                                                weight_3=parameters["weights"][1],
                                                weight_4=parameters["weights"][2],
                                                weight_5=parameters["weights"][3],
                                                weight_6=parameters["weights"][4],
                                                weight_7=parameters["weights"][5])

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
            self.spline_tools.calc_thresholds(self.big_data, self.big_data.combined_spline,
                                              buffer=0.05, buffer_setting=1,
                                              standard_upper_threshold=0.45,
                                              standard_lower_threshold=-0.5)

        # -- Modulating threshold with SMA 3 value
        # upper_threshold = self.spline_tools.modulate_amplitude_spline(
        #         upper_threshold,  self.math_tools.amplify(
        #             self.math_tools.normalise_zero_one(self.big_data.spline_sma_3), 0.3))
        #
        # lower_threshold = self.spline_tools.modulate_amplitude_spline(
        #         lower_threshold,  self.math_tools.amplify(
        #             self.math_tools.normalise_zero_one(self.big_data.spline_sma_3), 0.3))

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

            self.spline_tools.plot_spline(
                self.big_data, self.big_data.Major_spline.upper_threshold, label="Upper threshold")
            self.spline_tools.plot_spline(
                self.big_data, self.big_data.Major_spline.lower_threshold, label="Lower threshold")

            self.spline_tools.plot_spline_trigger(
                self.big_data, self.big_data.Major_spline.spline, self.big_data.Major_spline.sell_dates,
                self.big_data.Major_spline.buy_dates)

            # self.spline_tools.plot_spline(self.big_data, self.big_data.spline_volume, label="Volume", color='k')
            # self.spline_tools.plot_spline(self.big_data, self.big_data.spline_volatility, label="Volatility", color='grey')
            plt.show()
