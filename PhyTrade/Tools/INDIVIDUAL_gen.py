from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_random_gen import EVOA_random_gen
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data


class Individual:
    def __init__(self, ticker="AAPL", parameter_set=None):
        # ========================= DATA COLLECTION INITIALISATION =======================
        self.ticker = ticker
        self.data = fetch_technical_data(self.ticker)

        if parameter_set is None:
            self.gen_parameter_set()
        else:
            self.parameter_dictionary = parameter_set

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Counting number of parameters
        self.nb_of_parameters = 0
        for i in self.parameter_dictionary:
            for j in range(len(self.parameter_dictionary[i])):
                self.nb_of_parameters += 1

    def gen_economic_model(self, data_slice, plot_3=False):
        from PhyTrade.Economic_model.Analysis_protocols_V.Prototype_5 import Prototype_5

        self.analysis = Prototype_5(self.parameter_dictionary, data_slice, self.data)

        self.analysis.plot(plot_1=False, plot_2=False, plot_3=plot_3)

    def perform_trade_run(self,
                          data_slice,
                          investment_settings=3, cash_in_settings=0,
                          initial_funds=1000,
                          initial_assets=0,
                          prev_stop_loss=0.85, max_stop_loss=0.75,
                          max_investment_per_trade=500,
                          prev_simple_investment_assets=None,
                          print_trade_process=False):

        from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4

        self.tradebot = Tradebot_v4(data_slice.data_slice_selection,
                                    self.analysis.big_data.Major_spline.trade_signal,
                                    self.analysis.big_data.Major_spline.trade_spline,
                                    investment_settings=investment_settings, cash_in_settings=cash_in_settings,
                                    initial_funds=initial_funds,
                                    initial_assets=initial_assets,
                                    prev_stop_loss=prev_stop_loss, max_stop_loss=max_stop_loss,
                                    max_investment_per_trade=max_investment_per_trade,
                                    prev_simple_investment_assets=prev_simple_investment_assets,
                                    print_trade_process=print_trade_process)

        self.account = self.tradebot.account
        # self.big_data = tradebot.analysis.big_data

    def gen_parameter_set(self):
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
        self.sma_1_timeframe_1 = ga_random.timeframe_random_gen()
        self.sma_1_timeframe_2 = ga_random.timeframe_random_gen()

        self.sma_2_timeframe_1 = ga_random.timeframe_random_gen()
        self.sma_2_timeframe_2 = ga_random.timeframe_random_gen()

        self.sma_3_timeframe_1 = ga_random.timeframe_random_gen()
        self.sma_3_timeframe_2 = ga_random.timeframe_random_gen()

        self.sma_1_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.sma_2_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.sma_3_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.sma_timeframes_dic = {"sma_1_timeframe_1": self.sma_1_timeframe_1,
                                   "sma_2_timeframe_1": self.sma_2_timeframe_1,
                                   "sma_3_timeframe_1": self.sma_3_timeframe_1,
                                   "sma_1_timeframe_2": self.sma_1_timeframe_2,
                                   "sma_2_timeframe_2": self.sma_2_timeframe_2,
                                   "sma_3_timeframe_2": self.sma_3_timeframe_2}

        self.sma_smoothing_factors_dic = {"sma_1_spline_smoothing_factor": self.sma_1_spline_smoothing_factor,
                                          "sma_2_spline_smoothing_factor": self.sma_2_spline_smoothing_factor,
                                          "sma_3_spline_smoothing_factor": self.sma_3_spline_smoothing_factor}

        # ========================================================== EMA parameters:
        self.ema_1_timeframe_1 = ga_random.timeframe_random_gen()
        self.ema_1_timeframe_2 = ga_random.timeframe_random_gen()

        self.ema_2_timeframe_1 = ga_random.timeframe_random_gen()
        self.ema_2_timeframe_2 = ga_random.timeframe_random_gen()

        self.ema_3_timeframe_1 = ga_random.timeframe_random_gen()
        self.ema_3_timeframe_2 = ga_random.timeframe_random_gen()

        self.ema_1_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.ema_2_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.ema_3_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.ema_timeframes_dic = {"ema_1_timeframe_1": self.ema_1_timeframe_1,
                                   "ema_2_timeframe_1": self.ema_2_timeframe_1,
                                   "ema_3_timeframe_1": self.ema_3_timeframe_1,
                                   "ema_1_timeframe_2": self.ema_1_timeframe_2,
                                   "ema_2_timeframe_2": self.ema_2_timeframe_2,
                                   "ema_3_timeframe_2": self.ema_3_timeframe_2}

        self.ema_smoothing_factors_dic = {"ema_1_spline_smoothing_factor": self.ema_1_spline_smoothing_factor,
                                          "ema_2_spline_smoothing_factor": self.ema_2_spline_smoothing_factor,
                                          "ema_3_spline_smoothing_factor": self.ema_3_spline_smoothing_factor}

        # ========================================================== LWMA parameters:
        self.lwma_1_timeframe = ga_random.timeframe_random_gen()
        self.lwma_1_max_weight = ga_random.lwma_max_weight_random_gen()

        self.lwma_2_timeframe = ga_random.timeframe_random_gen()
        self.lwma_2_max_weight = ga_random.lwma_max_weight_random_gen()

        self.lwma_3_timeframe = ga_random.timeframe_random_gen()
        self.lwma_3_max_weight = ga_random.lwma_max_weight_random_gen()

        self.lwma_1_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.lwma_2_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()
        self.lwma_3_spline_smoothing_factor = ga_random.smoothing_factor_random_gen()

        # -- Labeling/Classifying parameter types
        self.lwma_timeframes_dic = {"lwma_1_timeframe": self.lwma_1_timeframe,
                                    "lwma_2_timeframe": self.lwma_2_timeframe,
                                    "lwma_3_timeframe": self.lwma_3_timeframe}

        self.lwma_max_weights_dic = {"lwma_1_max_weight": self.lwma_1_max_weight,
                                     "lwma_2_max_weight": self.lwma_2_max_weight,
                                     "lwma_3_max_weight": self.lwma_3_max_weight}

        self.lwma_smoothing_factors_dic = {"lwma_1_spline_smoothing_factor": self.lwma_1_spline_smoothing_factor,
                                           "lwma_2_spline_smoothing_factor": self.lwma_2_spline_smoothing_factor,
                                           "lwma_3_spline_smoothing_factor": self.lwma_3_spline_smoothing_factor}

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

        self.ema_1_spline_weight = ga_random.weight_random_gen()
        self.ema_2_spline_weight = ga_random.weight_random_gen()
        self.ema_3_spline_weight = ga_random.weight_random_gen()

        self.lwma_1_spline_weight = ga_random.weight_random_gen()
        self.lwma_2_spline_weight = ga_random.weight_random_gen()
        self.lwma_3_spline_weight = ga_random.weight_random_gen()

        self.oc_avg_gradient_spline_weight = ga_random.weight_random_gen()

        # -- Labeling/Classifying parameter types
        self.spline_weights_dic = {"rsi_1_spline_weight": self.rsi_1_spline_weight,
                                   "rsi_2_spline_weight": self.rsi_2_spline_weight,
                                   "rsi_3_spline_weight": self.rsi_3_spline_weight,
                                   "sma_1_spline_weight": self.sma_1_spline_weight,
                                   "sma_2_spline_weight": self.sma_2_spline_weight,
                                   "sma_3_spline_weight": self.sma_3_spline_weight,
                                   "ema_1_spline_weight": self.ema_1_spline_weight,
                                   "ema_2_spline_weight": self.ema_2_spline_weight,
                                   "ema_3_spline_weight": self.ema_3_spline_weight,
                                   "lwma_1_spline_weight": self.ema_1_spline_weight,
                                   "lwma_2_spline_weight": self.ema_2_spline_weight,
                                   "lwma_3_spline_weight": self.ema_3_spline_weight,
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
                                   **self.ema_timeframes_dic,
                                   **self.lwma_timeframes_dic,
                                   **self.volatility_timeframe_dic)

        self.amplification_factors_dic = dict(self.volume_amplification_factor_dic,
                                              **self.volatility_amplification_factor_dic)

        self.smoothing_factors_dic = dict(self.rsi_smoothing_factors_dic,
                                          **self.sma_smoothing_factors_dic,
                                          **self.ema_smoothing_factors_dic,
                                          **self.lwma_smoothing_factors_dic,
                                          **self.oc_avg_gradient_spline_smoothing_factor_dic,
                                          **self.volume_spline_smoothing_factor_dic,
                                          **self.volatility_spline_smoothing_factor_dic)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Creating parameter dictionary
        self.parameter_dictionary = {"timeframes": self.timeframes_dic,
                                     "rsi_standard_upper_thresholds": self.rsi_standard_upper_thresholds_dic,
                                     "rsi_standard_lower_thresholds": self.rsi_standard_lower_thresholds_dic,
                                     "smoothing_factors": self.smoothing_factors_dic,
                                     "amplification_factor": self.amplification_factors_dic,
                                     "weights": self.spline_weights_dic,
                                     "lwma_max_weights": self.lwma_max_weights_dic,
                                     "major_spline_standard_upper_thresholds": self.major_spline_standard_upper_threshold_dic,
                                     "major_spline_standard_lower_thresholds": self.major_spline_standard_lower_threshold_dic}
