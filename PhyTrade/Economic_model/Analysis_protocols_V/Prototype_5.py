"""
This script contains the Prototype_5 class
This prototype is based entirely on technical analysis, and include new indicators, including:
    - EMA
    - LWMA

The following parameters still require manual input:
    - include trigger in signals (Technical_Indicators output generation)
    - buffer and buffer settings (Threshold determination)

Victor Guillet
12/14/2018
"""

from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA

# ---> Import indicators
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.RSI_gen import RSI
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.SMA_gen import SMA
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.EMA_gen import EMA
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.LWMA_gen import LWMA

# ---> Import amplification signals
from PhyTrade.Economic_model.Technical_Analysis.Amplification_signals.Volume_gen import VOLUME
from PhyTrade.Economic_model.Technical_Analysis.Amplification_signals.Volatility_gen import VOLATILITY

# ---> import general tools
from PhyTrade.Economic_model.Technical_Analysis.Tools.MAJOR_SPLINE_gen import MAJOR_SPLINE
from PhyTrade.Tools.MATH_tools import MATH
from PhyTrade.Economic_model.Technical_Analysis.Tools.OC_tools import OC
from PhyTrade.Tools.SPLINE_tools import SPLINE


class Prototype_5:
    def __init__(self, parameters, data_slice_info, data):
        """
        Generate a model containing all coded indicators, process and generate bullish/bearish signals

        :param parameters: Dictionary of dictionaries containing the values for all the variables of each signal
        :param data_slice_info: data_slice_info class instance
        :param data: Pandas dataframe
        """

        # ========================= ANALYSIS INITIALISATION ==============================
        data_slice_start_ind = data_slice_info.start_index
        data_slice_stop_ind = data_slice_info.stop_index

        self.big_data = BIGDATA(data, data_slice_start_ind, data_slice_stop_ind)

        # ~~~~~~~~~~~~~~~~~~ Tools initialisation
        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)
        self.math_tools = MATH()

        # ~~~~~~~~~~~~~~~~~~ Technical_Indicators initialisation
        # -- RSI initialisation
        self.big_data.rsi_1 = RSI(self.big_data,
                                  timeframe=parameters["timeframes"]["rsi_1_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_1_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_1_standard_lower_threshold"])

        self.big_data.rsi_2 = RSI(self.big_data,
                                  timeframe=parameters["timeframes"]["rsi_2_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_2_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_2_standard_lower_threshold"])

        self.big_data.rsi_3 = RSI(self.big_data,
                                  timeframe=parameters["timeframes"]["rsi_3_timeframe"],
                                  standard_upper_threshold=parameters["rsi_standard_upper_thresholds"]["rsi_3_standard_upper_threshold"],
                                  standard_lower_threshold=parameters["rsi_standard_lower_thresholds"]["rsi_3_standard_lower_threshold"])

        # -- SMA initialisation
        self.big_data.sma_1 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["sma_1_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["sma_1_timeframe_2"])

        self.big_data.sma_2 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["sma_2_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["sma_2_timeframe_2"])

        self.big_data.sma_3 = SMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["sma_3_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["sma_3_timeframe_2"])

        # -- EMA initialisation
        self.big_data.ema_1 = EMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["ema_1_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["ema_1_timeframe_2"])

        self.big_data.ema_2 = EMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["ema_2_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["ema_2_timeframe_2"])

        self.big_data.ema_3 = EMA(self.big_data,
                                  timeperiod_1=parameters["timeframes"]["ema_3_timeframe_1"],
                                  timeperiod_2=parameters["timeframes"]["ema_3_timeframe_2"])

        # -- LWMA initialisation
        self.big_data.lwma_1 = LWMA(self.big_data,
                                    lookback_period=parameters["timeframes"]["lwma_1_timeframe"],
                                    max_weight=parameters["lwma_max_weights"]["lwma_1_max_weight"])

        self.big_data.lwma_2 = LWMA(self.big_data,
                                    lookback_period=parameters["timeframes"]["lwma_2_timeframe"],
                                    max_weight=parameters["lwma_max_weights"]["lwma_2_max_weight"])

        self.big_data.lwma_3 = LWMA(self.big_data,
                                    lookback_period=parameters["timeframes"]["lwma_3_timeframe"],
                                    max_weight=parameters["lwma_max_weights"]["lwma_3_max_weight"])

        # ~~~~~~~~~~~~~~~~~~ Amplification signal initialisation
        # -- Volume initialisation
        self.big_data.volume = VOLUME(self.big_data,
                                      amplification_factor=parameters["amplification_factor"]["volume_amplification_factor"])

        # -- Volatility initialisation
        self.big_data.volatility = VOLATILITY(self.big_data,
                                              timeframe=parameters["timeframes"]["volatility_timeframe"],
                                              amplification_factor=parameters["amplification_factor"]["volatility_amplification_factor"])

        # ================================================================================
        """




        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ~~~~~~~~~~~~~~~~~~ Technical_Indicators output generation
        # -- RSI
        self.big_data.rsi_1.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.rsi_2.get_output(self.big_data, include_triggers_in_bb_signal=True)
        self.big_data.rsi_3.get_output(self.big_data, include_triggers_in_bb_signal=True)

        # -- SMA
        self.big_data.sma_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_2.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.sma_3.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # -- EMA
        self.big_data.ema_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.ema_2.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.ema_3.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # -- LWMA
        self.big_data.lwma_1.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.lwma_2.get_output(self.big_data, include_triggers_in_bb_signal=False)
        self.big_data.lwma_3.get_output(self.big_data, include_triggers_in_bb_signal=False)

        # ~~~~~~~~~~~~~~~~~~ BB signals processing
        # ---> Creating splines from indicator signals
        # -- RSI
        self.big_data.spline_rsi_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_1_spline_smoothing_factor"])

        self.big_data.spline_rsi_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_2_spline_smoothing_factor"])

        self.big_data.spline_rsi_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.rsi_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["rsi_3_spline_smoothing_factor"])

        # -- SMA
        self.big_data.spline_sma_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_1_spline_smoothing_factor"])
        self.big_data.spline_sma_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_2_spline_smoothing_factor"])
        self.big_data.spline_sma_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.sma_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["sma_3_spline_smoothing_factor"])

        # -- EMA
        self.big_data.spline_ema_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.ema_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_1_spline_smoothing_factor"])
        self.big_data.spline_ema_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.ema_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_2_spline_smoothing_factor"])
        self.big_data.spline_ema_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.ema_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_3_spline_smoothing_factor"])

        # -- LWMA
        self.big_data.spline_lwma_1 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.lwma_1.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_1_spline_smoothing_factor"])
        self.big_data.spline_lwma_2 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.lwma_2.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_2_spline_smoothing_factor"])
        self.big_data.spline_lwma_3 = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.lwma_3.bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["ema_3_spline_smoothing_factor"])

        # -- OC avg gradient
        self.big_data.spline_oc_avg_gradient = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.oc_avg_gradient_bb_signal,
                                                    smoothing_factor=parameters["smoothing_factors"]["oc_avg_gradient_spline_smoothing_factor"])

        # ---> Generating amplification signals
        self.big_data.spline_volume = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"]["volume_spline_smoothing_factor"])

        self.big_data.spline_volatility = \
            self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volatility.amp_coef,
                                                    smoothing_factor=parameters["smoothing_factors"]["volatility_spline_smoothing_factor"])

        # ---> Tuning separate signals
        # TODO: Figure out a systematic way of flipping spline when necessary
        # self.big_data.spline_sma_1 = self.spline_tools.flip_spline(self.big_data.spline_sma_1)
        self.big_data.spline_sma_2 = self.spline_tools.flip_spline(self.big_data.spline_sma_2)
        self.big_data.spline_sma_3 = self.spline_tools.flip_spline(self.big_data.spline_sma_3)

        # self.big_data.spline_ema_1 = self.spline_tools.flip_spline(self.big_data.spline_ema_1)
        # self.big_data.spline_ema_2 = self.spline_tools.flip_spline(self.big_data.spline_ema_2)
        # self.big_data.spline_ema_3 = self.spline_tools.flip_spline(self.big_data.spline_ema_3)

        self.big_data.spline_lwma_1 = self.spline_tools.flip_spline(self.big_data.spline_lwma_1)
        self.big_data.spline_lwma_2 = self.spline_tools.flip_spline(self.big_data.spline_lwma_2)
        self.big_data.spline_lwma_3 = self.spline_tools.flip_spline(self.big_data.spline_lwma_3)

        # ---> Adding signals together
        self.big_data.combined_spline = \
            self.spline_tools.combine_splines(self.big_data,
                                              [self.big_data.spline_oc_avg_gradient,
                                               self.big_data.spline_rsi_1,
                                               self.big_data.spline_rsi_2,
                                               self.big_data.spline_rsi_3,
                                               self.big_data.spline_sma_1,
                                               self.big_data.spline_sma_2,
                                               self.big_data.spline_sma_3,
                                               self.big_data.spline_ema_1,
                                               self.big_data.spline_ema_2,
                                               self.big_data.spline_ema_3,
                                               self.big_data.spline_lwma_1,
                                               self.big_data.spline_lwma_2,
                                               self.big_data.spline_lwma_3],
                                              [parameters["weights"]["oc_avg_gradient_spline_weight"],
                                               parameters["weights"]["rsi_1_spline_weight"],
                                               parameters["weights"]["rsi_2_spline_weight"],
                                               parameters["weights"]["rsi_3_spline_weight"],
                                               parameters["weights"]["sma_1_spline_weight"],
                                               parameters["weights"]["sma_2_spline_weight"],
                                               parameters["weights"]["sma_3_spline_weight"],
                                               parameters["weights"]["ema_1_spline_weight"],
                                               parameters["weights"]["ema_2_spline_weight"],
                                               parameters["weights"]["ema_3_spline_weight"],
                                               parameters["weights"]["lwma_1_spline_weight"],
                                               parameters["weights"]["lwma_2_spline_weight"],
                                               parameters["weights"]["lwma_3_spline_weight"]])

        # ---> Tuning combined signal
        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volume, std_dev_max=3)

        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volatility, std_dev_max=3)

        self.big_data.combined_spline = self.math_tools.normalise_minus_one_one(self.big_data.combined_spline)

        # ~~~~~~~~~~~~~~~~~~ Threshold determination
        # ---> Creating dynamic thresholds
        upper_threshold, lower_threshold = \
            self.spline_tools.calc_thresholds(self.big_data, self.big_data.combined_spline,
                                              buffer=0.05, buffer_setting=1,
                                              standard_upper_threshold=parameters["major_spline_standard_upper_thresholds"]["major_spline_standard_upper_threshold"],
                                              standard_lower_threshold=parameters["major_spline_standard_lower_thresholds"]["major_spline_standard_lower_threshold"])

        # ---> Modulating threshold with SMA 3 value
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
        """
        :param plot_1: Plot Open/Close prices & RSI
        :param plot_2: Plot Open/Close prices & SMA
        :param plot_3: Plot Open/Close prices & Bullish/Bearish signal
        """
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
            # ---> RSI signals
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_rsi_1, label="RSI bb spline")
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_rsi_2, label="RSI bb spline")
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_rsi_3, label="RSI bb spline")

            # ---> OC gradient signals
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_oc_avg_gradient, label="OC gradient bb spline", color='m')

            # ---> SMA signals
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_1, label="SMA_1 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_2, label="SMA_2 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_sma_3, label="SMA_3 bb spline", color='r')

            # # ---> EMA signals
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_ema_1, label="EMA_1 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_ema_2, label="EMA_2 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_ema_3, label="EMA_3 bb spline", color='r')

            # ---> LWMA signals
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_lwma_1, label="LWMA_1 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_lwma_2, label="LWMA_2 bb spline", color='b')
            # self.spline_tools.plot_spline(
            #     self.big_data, self.big_data.spline_lwma_3, label="LWMA_3 bb spline", color='r')

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

            plt.legend()
            plt.show()

        return
