"""
Prototype 3

This prototype is based entirely on technical analysis, and is ment as a test for the genetic algorithm parameter
optimisation algorithm
Victor Guillet
12/14/2018
"""

from PhyTrade.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA

from PhyTrade.Technical_Analysis.Technical_Indicators.RSI_gen import RSI
from PhyTrade.Technical_Analysis.Technical_Indicators.SMA_gen import SMA

from PhyTrade.Technical_Analysis.Amplification_signals.Volume_gen import VOLUME
from PhyTrade.Technical_Analysis.Amplification_signals.Volatility_gen import VOLATILITY

from PhyTrade.Technical_Analysis.Data_Collection_preparation.MAJOR_SPLINE_gen import MAJOR_SPLINE
from PhyTrade.Tools.MATH_tools import MATH
from PhyTrade.Technical_Analysis.Tools.OC_tools import OC
from PhyTrade.Tools.SPLINE_tools import SPLINE

import pandas


class Prototype_3:
    def __init__(self, parameters, data_slice_info):

        # ========================= DATA COLLECTION INITIALISATION =======================
        ticker = 'AAPL'  # Ticker selected for Yahoo data collection
        # data = pull_yahoo_data(ticker)  # Pull data from Yahoo

        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Steffegium\Data\AAPL_Yahoo_data.csv".replace(
            '\\', '/')

        data = pandas.read_csv(path)

        # ========================= ANALYSIS INITIALISATION ==============================
        data_slice_start_ind = data_slice_info.start_index
        data_slice_stop_ind = data_slice_info.stop_index

        self.big_data = BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

        # ------------------ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)
        self.math_tools = MATH()

        # ------------------ Technical_Indicators initialisation
        # -- RSI initialisation
        self.big_data.rsi_1 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"]["rsi_1_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_1_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_1_standard_lower_threshold"])

        self.big_data.rsi_2 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"]["rsi_2_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_2_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_2_standard_lower_threshold"])

        self.big_data.rsi_3 = RSI(self.big_data,
                                  timeframe=parameters["timeframe"]["rsi_3_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_3_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_3_standard_lower_threshold"])

        # -- SMA initialisation
        self.big_data.sma_1 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"]["sma_1_timeperiod_1"],
                                  timeperiod_2=parameters["timeframe"]["sma_1_timeperiod_2"])

        self.big_data.sma_2 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"]["sma_2_timeperiod_1"],
                                  timeperiod_2=parameters["timeframe"]["sma_2_timeperiod_2"])

        self.big_data.sma_3 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframe"]["sma_3_timeperiod_1"],
                                  timeperiod_2=parameters["timeframe"]["sma_3_timeperiod_2"])

        # -- Volume initialisation
        self.big_data.volume = VOLUME(self.big_data,
                                      amplification_factor=parameters["amplification_factor"]["volume_amplification_factor"])

        # -- Volatility initialisation
        self.big_data.volatility = VOLATILITY(self.big_data,
                                              timeframe=parameters["timeframe"]["volatility_timeframe"],
                                              amplification_factor=parameters["amplification_factor"]["volatility_amplification_factor"])

        # ================================================================================
        """




        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ~~~~~~~~~~~~~~~~~~ Technical_Indicators output generation
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
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_1_spline_smoothing_factor"])

        self.big_data.spline_rsi_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_2_spline_smoothing_factor"])

        self.big_data.spline_rsi_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_3_spline_smoothing_factor"])

        # - SMA
        self.big_data.spline_sma_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_1_spline_smoothing_factor"])
        self.big_data.spline_sma_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_2_spline_smoothing_factor"])
        self.big_data.spline_sma_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_3_spline_smoothing_factor"])

        # - OC avg gradient
        self.big_data.spline_oc_avg_gradient = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.oc_avg_gradient_bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["oc_avg_gradient_spline_smoothing_factor"])

        # -- Generating amplification signals
        self.big_data.spline_volume = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"]["volume_spline_smoothing_factor"])

        self.big_data.spline_volatility = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volatility.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"]["volatility_spline_smoothing_factor"])

        # -- Tuning separate signals
        self.big_data.spline_sma_3 = self.spline_tools.flip_spline(self.big_data.spline_sma_3)

        # -- Adding signals together
        self.big_data.combined_spline = \
            self.spline_tools.combine_7_splines(self.big_data,
                                                self.big_data.spline_rsi_1,
                                                self.big_data.spline_rsi_2,
                                                self.big_data.spline_rsi_3,
                                                self.big_data.spline_sma_1,
                                                self.big_data.spline_sma_2,
                                                self.big_data.spline_sma_3,
                                                self.big_data.spline_oc_avg_gradient,
                                                weight_2=parameters["weights"]["rsi_1_spline_weight"],
                                                weight_3=parameters["weights"]["rsi_2_spline_weight"],
                                                weight_4=parameters["weights"]["rsi_3_spline_weight"],
                                                weight_5=parameters["weights"]["sma_1_spline_weight"],
                                                weight_6=parameters["weights"]["sma_2_spline_weight"],
                                                weight_7=parameters["weights"]["sma_3_spline_weight"],
                                                weight_1=parameters["weights"]["oc_avg_gradient_spline_weight"])

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
                                              standard_upper_threshold=parameters["major_spline_standard_upper_thresholds"]["major_spline_standard_upper_threshold"],
                                              standard_lower_threshold=parameters["major_spline_standard_lower_thresholds"]["major_spline_standard_lower_threshold"])

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
