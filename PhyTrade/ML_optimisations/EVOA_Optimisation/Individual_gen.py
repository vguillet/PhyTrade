
class Individual:
    def __init__(self):
        from PhyTrade.ML_optimisations.EVOA_Optimisation.EVOA_random_gen import EVOA_random_gen

        ga_random = EVOA_random_gen()

        # ========================================================== RSI parameters:
        self.rsi_1_timeframe = ga_random.timeframe_random_gen()
        self.rsi_1_standard_upper_threshold = ga_random.rsi_upper_threshold_random_gen()
        self.rsi_1_standard_lower_threshold = ga_random.rsi_lower_threshold_random_gen()

        self.rsi_2_timeframe = ga_random.timeframe_random_gen()
        self.rsi_2_standard_upper_threshold = ga_random.rsi_upper_threshold_random_gen()
        self.rsi_2_standard_lower_threshold = ga_random.rsi_lower_threshold_random_gen()

        self.rsi_3_timeframe = ga_random.timeframe_random_gen()
        self.rsi_3_standard_upper_threshold = ga_random.rsi_upper_threshold_random_gen()
        self.rsi_3_standard_lower_threshold = ga_random.rsi_lower_threshold_random_gen()

        self.rsi_1_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.rsi_2_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.rsi_3_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.rsi_timeframes_dic = {"rsi_1_timeframe": self.rsi_1_timeframe,
                                   "rsi_2_timeframe": self.rsi_2_timeframe,
                                   "rsi_3_timeframe": self.rsi_3_timeframe}

        self.rsi_standard_upper_thresholds_dic = {"rsi_1_standard_upper_threshold": self.rsi_1_standard_upper_threshold,
                                                  "rsi_2_standard_upper_threshold": self.rsi_2_standard_upper_threshold,
                                                  "rsi_3_standard_upper_threshold": self.rsi_3_standard_upper_threshold}

        self.rsi_standard_lower_thresholds_dic = {"rsi_1_standard_lower_threshold": self.rsi_1_standard_lower_threshold,
                                                  "rsi_2_standard_lower_threshold": self.rsi_2_standard_lower_threshold,
                                                  "rsi_3_standard_lower_threshold": self.rsi_3_standard_lower_threshold}

        self.rsi_smoothing_factors_dic = {"rsi_1_spline_smoothing_factor": self.rsi_1_spline_smoothing_factor,
                                          "rsi_2_spline_smoothing_factor": self.rsi_2_spline_smoothing_factor,
                                          "rsi_3_spline_smoothing_factor": self.rsi_3_spline_smoothing_factor}

        # ========================================================== SMA parameters:
        self.sma_1_timeperiod_1 = ga_random.timeframe_random_gen()
        self.sma_1_timeperiod_2 = ga_random.timeframe_random_gen()

        self.sma_2_timeperiod_1 = ga_random.timeframe_random_gen()
        self.sma_2_timeperiod_2 = ga_random.timeframe_random_gen()

        self.sma_3_timeperiod_1 = ga_random.timeframe_random_gen()
        self.sma_3_timeperiod_2 = ga_random.timeframe_random_gen()

        self.sma_1_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.sma_2_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.sma_3_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.sma_timeframes_dic = {"sma_1_timeperiod_1": self.sma_1_timeperiod_1,
                                   "sma_2_timeperiod_1": self.sma_2_timeperiod_1,
                                   "sma_3_timeperiod_1": self.sma_3_timeperiod_1,
                                   "sma_1_timeperiod_2": self.sma_1_timeperiod_2,
                                   "sma_2_timeperiod_2": self.sma_2_timeperiod_2,
                                   "sma_3_timeperiod_2": self.sma_3_timeperiod_2}

        self.sma_smoothing_factors_dic = {"sma_1_spline_smoothing_factor": self.sma_1_spline_smoothing_factor,
                                          "sma_2_spline_smoothing_factor": self.sma_2_spline_smoothing_factor,
                                          "sma_3_spline_smoothing_factor": self.sma_3_spline_smoothing_factor}

        # ========================================================== OC parameters:
        self.oc_avg_gradient_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.oc_avg_gradient_spline_smoothing_factor_dic = \
            {"oc_avg_gradient_spline_smoothing_factor": self.oc_avg_gradient_spline_smoothing_factor}

        # ========================================================== Volume parameters:
        self.volume_amplification_factor = ga_random.amplification_factor_random_gen()
        self.volume_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.volume_amplification_factor_dic = \
            {"volume_amplification_factor": self.volume_amplification_factor}

        self.volume_spline_smoothing_factor_dic = \
            {"volume_spline_smoothing_factor": self.volume_spline_smoothing_factor}

        # ========================================================== Volatility parameters:
        self.volatility_timeframe = ga_random.timeframe_random_gen()
        self.volatility_amplification_factor = ga_random.amplification_factor_random_gen()
        self.volatility_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.volatility_timeframe_dic = \
            {"volatility_timeframe": self.volatility_timeframe}

        self.volatility_amplification_factor_dic = \
            {"volatility_amplification_factor": self.volatility_amplification_factor}

        self.volatility_spline_smoothing_factor_dic = \
            {"volatility_spline_smoothing_factor": self.volatility_spline_smoothing_factor}

        # ========================================================== Spline weights:
        self.rsi_1_spline_weight = ga_random.weight_random_gen()
        self.rsi_2_spline_weight = ga_random.weight_random_gen()
        self.rsi_3_spline_weight = ga_random.weight_random_gen()

        self.sma_1_spline_weight = ga_random.weight_random_gen()
        self.sma_2_spline_weight = ga_random.weight_random_gen()
        self.sma_3_spline_weight = ga_random.weight_random_gen()

        self.oc_avg_gradient_spline_weight = ga_random.weight_random_gen()

        # -- Labeling/Classifying parameter types
        self.spline_weights_dic = {"rsi_1_spline_weight": self.rsi_1_spline_weight,
                                   "rsi_2_spline_weight": self.rsi_2_spline_weight,
                                   "rsi_3_spline_weight": self.rsi_3_spline_weight,
                                   "sma_1_spline_weight": self.sma_1_spline_weight,
                                   "sma_2_spline_weight": self.sma_2_spline_weight,
                                   "sma_3_spline_weight": self.sma_3_spline_weight,
                                   "oc_avg_gradient_spline_weight": self.oc_avg_gradient_spline_weight}

        # ========================================================== Dynamic threshold values:
        self.major_spline_standard_upper_threshold = ga_random.major_spline_upper_threshold_random_gen()
        self.major_spline_standard_lower_threshold = ga_random.major_spline_lower_threshold_random_gen()

        # -- Labeling/Classifying parameter types
        self.major_spline_standard_upper_threshold_dic = \
            {"major_spline_standard_upper_threshold": self.major_spline_standard_upper_threshold}

        self.major_spline_standard_lower_threshold_dic = \
            {"major_spline_standard_lower_threshold": self.major_spline_standard_lower_threshold}

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Further parameter classification
        self.timeframes_dic = dict(self.rsi_timeframes_dic,
                                   **self.sma_timeframes_dic,
                                   **self.volatility_timeframe_dic)

        self.amplification_factor_dic = dict(self.volume_amplification_factor_dic,
                                             **self.volatility_amplification_factor_dic)

        self.smoothing_factors_dic = dict(self.rsi_smoothing_factors_dic,
                                          **self.sma_smoothing_factors_dic,
                                          **self.oc_avg_gradient_spline_smoothing_factor_dic,
                                          **self.volume_spline_smoothing_factor_dic,
                                          **self.volatility_spline_smoothing_factor_dic)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Creating parameter dictionary
        self.parameter_dictionary = {"timeframe": self.timeframes_dic,
                                     "rsi_standard_upper_thresholds": self.rsi_standard_upper_thresholds_dic,
                                     "rsi_standard_lower_thresholds": self.rsi_standard_lower_thresholds_dic,
                                     "smoothing_factors": self.smoothing_factors_dic,
                                     "amplification_factor": self.amplification_factor_dic,
                                     "weights": self.spline_weights_dic,
                                     "major_spline_standard_upper_thresholds": self.major_spline_standard_upper_threshold_dic,
                                     "major_spline_standard_lower_thresholds": self.major_spline_standard_lower_threshold_dic}

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Counting number of parameters
        self.nb_of_parameters = 0
        for i in self.parameter_dictionary:
            for j in range(len(self.parameter_dictionary[i])):
                self.nb_of_parameters += 1

    def gen_economic_model(self, data_slice_info, plot_3=False):
        from PhyTrade.Analysis_protocols_V.Prototype_3 import Prototype_3
        from PhyTrade.Analysis_protocols_V.Prototype_4 import Prototype_4

        self.analysis = Prototype_3(self.parameter_dictionary, data_slice_info)
        # self.analysis = Prototype_4(self.parameter_dictionary, data_slice_info)

        self.analysis.plot(plot_1=False, plot_2=False, plot_3=plot_3)

    def perform_trade_run(self):
        from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3

        tradebot = Tradebot_v3(self.analysis)

        self.account = tradebot.account
        # self.big_data = tradebot.analysis.big_data