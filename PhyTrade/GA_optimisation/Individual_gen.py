
class Individual:
    def __init__(self):
        import random
        from PhyTrade.GA_optimisation.GA_random_gen import GA_random_gen

        self.ga_random = GA_random_gen()

        # ========================================================== RSI parameters:
        self.rsi_1_timeframe = self.ga_random.timeframe_gen()
        self.rsi_1_standard_upper_threshold = random.randint(51, 100)
        self.rsi_1_standard_lower_threshold = random.randint(1, 49)

        self.rsi_2_timeframe = self.ga_random.timeframe_gen()
        self.rsi_2_standard_upper_threshold = random.randint(51, 100)
        self.rsi_2_standard_lower_threshold = random.randint(1, 49)

        self.rsi_3_timeframe = self.ga_random.timeframe_gen()
        self.rsi_3_standard_upper_threshold = random.randint(51, 100)
        self.rsi_3_standard_lower_threshold = random.randint(1, 49)

        self.rsi_1_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()
        self.rsi_2_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()
        self.rsi_3_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()

        self.rsi_parameters_lst = [self.rsi_1_timeframe,
                                   self.rsi_1_standard_upper_threshold,
                                   self.rsi_1_standard_lower_threshold,
                                   self.rsi_2_timeframe,
                                   self.rsi_2_standard_upper_threshold,
                                   self.rsi_2_standard_lower_threshold,
                                   self.rsi_3_timeframe,
                                   self.rsi_3_standard_upper_threshold,
                                   self.rsi_3_standard_lower_threshold,
                                   self.rsi_1_spline_smoothing_factor,
                                   self.rsi_2_spline_smoothing_factor,
                                   self.rsi_3_spline_smoothing_factor]

        # -- Classifying parameter types
        self.rsi_timeframes_lst = [self.rsi_1_timeframe,
                                   self.rsi_2_timeframe,
                                   self.rsi_3_timeframe]

        self.rsi_standard_upper_thresholds_lst = [self.rsi_1_standard_upper_threshold,
                                                  self.rsi_2_standard_upper_threshold,
                                                  self.rsi_3_standard_upper_threshold]

        self.rsi_standard_lower_thresholds_lst = [self.rsi_1_standard_lower_threshold,
                                                  self.rsi_2_standard_lower_threshold,
                                                  self.rsi_3_standard_lower_threshold]

        self.rsi_smoothing_factors_lst = [self.rsi_1_spline_smoothing_factor,
                                          self.rsi_2_spline_smoothing_factor,
                                          self.rsi_3_spline_smoothing_factor]

        # ========================================================== SMA parameters:
        self.sma_1_timeperiod_1 = self.ga_random.timeframe_gen()
        self.sma_1_timeperiod_2 = self.ga_random.timeframe_gen()

        self.sma_2_timeperiod_1 = self.ga_random.timeframe_gen()
        self.sma_2_timeperiod_2 = self.ga_random.timeframe_gen()

        self.sma_3_timeperiod_1 = self.ga_random.timeframe_gen()
        self.sma_3_timeperiod_2 = self.ga_random.timeframe_gen()

        self.sma_1_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()
        self.sma_2_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()
        self.sma_3_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()

        self.sma_parameters_lst = [self.sma_1_timeperiod_1,
                                   self.sma_1_timeperiod_2,
                                   self.sma_2_timeperiod_1,
                                   self.sma_2_timeperiod_2,
                                   self.sma_3_timeperiod_1,
                                   self.sma_3_timeperiod_2,
                                   self.sma_1_spline_smoothing_factor,
                                   self.sma_2_spline_smoothing_factor,
                                   self.sma_3_spline_smoothing_factor]

        # -- Classifying parameter types
        self.sma_timeframes_lst = [self.sma_1_timeperiod_1,
                                   self.sma_2_timeperiod_1,
                                   self.sma_3_timeperiod_1,
                                   self.sma_1_timeperiod_2,
                                   self.sma_2_timeperiod_2,
                                   self.sma_3_timeperiod_2]

        self.sma_smoothing_factors_lst = [self.sma_1_spline_smoothing_factor,
                                          self.sma_2_spline_smoothing_factor,
                                          self.sma_3_spline_smoothing_factor]

        # ========================================================== OC parameters:
        self.oc_avg_gradient_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()

        # ========================================================== Volume parameters:
        self.volume_amplification_factor = self.ga_random.amplification_factor_gen()
        self.volume_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()

        self.volume_parameters_lst = [self.volume_amplification_factor,
                                      self.volume_spline_smoothing_factor]

        # ========================================================== Volatility parameters:
        self.volatility_timeframe = self.ga_random.timeframe_gen()
        self.volatility_amplification_factor = self.ga_random.amplification_factor_gen()
        self.volatility_spline_smoothing_factor = self.ga_random.smoothing_factor_gen()

        self.volatility_parameters_lst = [self.volatility_timeframe,
                                          self.volatility_amplification_factor,
                                          self.volatility_spline_smoothing_factor]

        # ========================================================== Spline weights:
        self.rsi_1_spline_weight = self.ga_random.weight_gen()
        self.rsi_2_spline_weight = self.ga_random.weight_gen()
        self.rsi_3_spline_weight = self.ga_random.weight_gen()

        self.sma_1_spline_weight = self.ga_random.weight_gen()
        self.sma_2_spline_weight = self.ga_random.weight_gen()
        self.sma_3_spline_weight = self.ga_random.weight_gen()

        self.oc_avg_gradient_spline_weight = self.ga_random.weight_gen()

        self.spline_weights_lst = [self.rsi_1_spline_weight,
                            self.rsi_2_spline_weight,
                            self.rsi_3_spline_weight,
                            self.sma_1_spline_weight,
                            self.sma_2_spline_weight,
                            self.sma_3_spline_weight,
                            self.oc_avg_gradient_spline_weight]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Individual properties
        self.nb_of_parameters = len(self.rsi_parameters_lst) \
                                + len(self.sma_parameters_lst) \
                                + len(self.volume_parameters_lst) \
                                + len(self.volatility_parameters_lst) \
                                + len(self.spline_weights_lst) + 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Further parameter classification
        self.timeframes_lst = self.rsi_timeframes_lst \
                              + self.sma_timeframes_lst \
                              + [self.volatility_timeframe]

        self.rsi_standard_upper_thresholds_lst = self.rsi_standard_upper_thresholds_lst
        self.rsi_standard_lower_thresholds_lst = self.rsi_standard_lower_thresholds_lst

        self.smoothing_factors_lst = self.rsi_smoothing_factors_lst \
                                     + self.sma_smoothing_factors_lst \
                                     + [self.oc_avg_gradient_spline_smoothing_factor] \
                                     + [self.volatility_spline_smoothing_factor] \
                                     + [self.volume_spline_smoothing_factor]

        self.amplification_factor_lst = [self.volume_amplification_factor] \
                                        + [self.volatility_amplification_factor]

        self.list_combined = self.timeframes_lst \
                             + self.rsi_standard_upper_thresholds_lst \
                             + self.rsi_standard_lower_thresholds_lst \
                             + self.smoothing_factors_lst \
                             + self.amplification_factor_lst \
                             + self.spline_weights_lst

        assert len(self.list_combined) == self.nb_of_parameters

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Creating parameter dictionary
        self.parameter_dictionary = {"timeframe": self.timeframes_lst,
                                     "rsi_standard_upper_thresholds": self.rsi_standard_upper_thresholds_lst,
                                     "rsi_standard_lower_thresholds": self.rsi_standard_lower_thresholds_lst,
                                     "smoothing_factors": self.smoothing_factors_lst,
                                     "self.amplification_factor": self.amplification_factor_lst,
                                     "weights": self.spline_weights_lst}


