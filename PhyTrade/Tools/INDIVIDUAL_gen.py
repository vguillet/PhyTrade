
################################################################################################################
"""
Used to generate individuals. Individuals contain a parameter set (either provided or generated)
and can generate economic model, and perform trade runs
"""

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Signal_optimisation.EVOA_optimisation.Tools.EVOA_random_gen import EVOA_random_gen
from PhyTrade.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data
from PhyTrade.Tools.GENERAL_tools import GENERAL_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Individual:
    def __init__(self, ticker="AAPL", parameter_set=None):
        # ========================= DATA COLLECTION INITIALISATION =======================
        self.ticker = ticker
        self.data = fetch_technical_data(self.ticker)
        settings = SETTINGS()
        settings.signal_training_settings.gen_evoa_settings()

        if parameter_set is None:
            settings.individual_settings.gen_individual_settings()
            self.gen_parameter_set(threshold_setting=settings.individual_settings.threshold_setting,
                                   buffer_setting=settings.individual_settings.buffer_setting,
                                   spline_interpolation_factor=settings.individual_settings.spline_interpolation_factor,
                                   rsi_count=settings.individual_settings.rsi_count,
                                   rsi_include_triggers_in_bb_signal=settings.individual_settings.rsi_include_triggers_in_bb_signal,
                                   rsi_buffer_setting=settings.individual_settings.rsi_buffer_setting,
                                   sma_count=settings.individual_settings.sma_count,
                                   sma_include_triggers_in_bb_signal=settings.individual_settings.sma_include_triggers_in_bb_signal,
                                   ema_count=settings.individual_settings.ema_count,
                                   ema_include_triggers_in_bb_signal=settings.individual_settings.ema_include_triggers_in_bb_signal,
                                   lwma_count=settings.individual_settings.lwma_count,
                                   lwma_include_triggers_in_bb_signal=settings.individual_settings.lwma_include_triggers_in_bb_signal,
                                   cci_count=settings.individual_settings.cci_count,
                                   cci_include_triggers_in_bb_signal=settings.individual_settings.cci_include_triggers_in_bb_signal,
                                   eom_count=settings.individual_settings.eom_count,
                                   eom_include_triggers_in_bb_signal=settings.individual_settings.eom_include_triggers_in_bb_signal,
                                   oc_include_triggers_in_bb_signal=settings.individual_settings.oc_gradient_include_triggers_in_bb_signal)
        else:
            self.parameter_set = parameter_set

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Counting number of parameters
        self.nb_of_parameters = GENERAL_tools().calc_nested_dic_item_count(self.parameter_set, settings.signal_training_settings.parameter_blacklist)

        for i in self.parameter_set:
            for j in range(len(self.parameter_set[i])):
                self.nb_of_parameters += 1

    def gen_economic_model(self, data_slice, plot_eco_model_results=False):
        from PhyTrade.Economic_model.Analysis_protocols.Prototype_5 import Prototype_5
        from PhyTrade.Tools.PLOT_tools import PLOT_tools

        self.analysis = Prototype_5(self.parameter_set, data_slice)

        self.spline = self.analysis.big_data.Major_spline.spline
        self.trade_spline = self.analysis.big_data.Major_spline.trade_spline
        self.trade_signal = self.analysis.big_data.Major_spline.trade_signal

        # analysis.plot(plot_1=False, plot_2=False, plot_3=plot_3)
        if plot_eco_model_results:
            PLOT_tools().plot_trade_process(data_slice, self.spline,
                                            self.analysis.big_data.Major_spline.upper_threshold,
                                            self.analysis.big_data.Major_spline.lower_threshold,
                                            self.trade_signal)

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

        self.tradebot = Tradebot_v4(data_slice.sliced_data_selection,
                                    self.trade_signal,
                                    self.trade_spline,
                                    investment_settings=investment_settings, cash_in_settings=cash_in_settings,
                                    initial_funds=initial_funds,
                                    initial_assets=initial_assets,
                                    prev_stop_loss=prev_stop_loss, max_stop_loss=max_stop_loss,
                                    max_investment_per_trade=max_investment_per_trade,
                                    prev_simple_investment_assets=prev_simple_investment_assets,
                                    print_trade_process=print_trade_process)

        self.account = self.tradebot.account
        # self.big_data = tradebot.analysis.big_data

    def gen_parameter_set(self,
                          threshold_setting=2,
                          buffer_setting=1,
                          spline_interpolation_factor=4,
                          rsi_count=1, rsi_include_triggers_in_bb_signal=False, rsi_buffer_setting=0,
                          sma_count=1, sma_include_triggers_in_bb_signal=False,
                          ema_count=1, ema_include_triggers_in_bb_signal=False,
                          lwma_count=1, lwma_include_triggers_in_bb_signal=False,
                          cci_count=1, cci_include_triggers_in_bb_signal=False,
                          eom_count=1, eom_include_triggers_in_bb_signal=False,
                          oc_include_triggers_in_bb_signal=False):

        ga_random = EVOA_random_gen()
        self.parameter_set = {"indicators_count": {},
                                     "spline_property": {"weights": {},
                                                         "smoothing_factors": {},
                                                         "amplification_factor": {},
                                                         "flip": {}},
                                     "indicator_properties": {"timeframes": {}},
                                     "general_settings": {"spline_interpolation_factor": spline_interpolation_factor,
                                                          "threshold_setting": threshold_setting,
                                                          "buffer_setting": buffer_setting,
                                                          "include_triggers_in_bb_signal":{}}}

        # ========================================================== RSI parameters:
        self.parameter_set["indicators_count"]["rsi"] = rsi_count

        if rsi_count != 0:
            self.parameter_set["indicator_properties"]["rsi_standard_upper_thresholds"] = {}
            self.parameter_set["indicator_properties"]["rsi_standard_lower_thresholds"] = {}

            for i in range(rsi_count):
                self.parameter_set["indicator_properties"]["timeframes"]["rsi_" + str(i)] = ga_random.timeframe_random_gen()
                self.parameter_set["indicator_properties"]["rsi_standard_upper_thresholds"]["rsi_" + str(i)] = ga_random.rsi_upper_threshold_random_gen()
                self.parameter_set["indicator_properties"]["rsi_standard_lower_thresholds"]["rsi_" + str(i)] = ga_random.rsi_lower_threshold_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["rsi_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["rsi_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["rsi_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["rsi"] = rsi_include_triggers_in_bb_signal
            self.parameter_set["general_settings"]["rsi_buffer_setting"] = rsi_buffer_setting

        # ========================================================== SMA parameters:
        self.parameter_set["indicators_count"]["sma"] = sma_count

        if sma_count != 0:
            for i in range(sma_count):
                self.parameter_set["indicator_properties"]["timeframes"]["sma_" + str(i) + "_1"] = ga_random.small_timeframe_random_gen()
                self.parameter_set["indicator_properties"]["timeframes"]["sma_" + str(i) + "_2"] = ga_random.large_timeframe_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["sma_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["sma_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["sma_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["sma"] = sma_include_triggers_in_bb_signal

        # ========================================================== EMA parameters:
        self.parameter_set["indicators_count"]["ema"] = ema_count

        if ema_count != 0:
            for i in range(ema_count):
                self.parameter_set["indicator_properties"]["timeframes"]["ema_" + str(i) + "_1"] = ga_random.small_timeframe_random_gen()
                self.parameter_set["indicator_properties"]["timeframes"]["ema_" + str(i) + "_2"] = ga_random.large_timeframe_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["ema_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["ema_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["ema_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["ema"] = ema_include_triggers_in_bb_signal

        # ========================================================== LWMA parameters:
        self.parameter_set["indicators_count"]["lwma"] = lwma_count

        if lwma_count != 0:
            self.parameter_set["indicator_properties"]["lwma_max_weights"] = {}

            for i in range(lwma_count):
                self.parameter_set["indicator_properties"]["timeframes"]["lwma_" + str(i)] = ga_random.timeframe_random_gen()
                self.parameter_set["indicator_properties"]["lwma_max_weights"]["lwma_" + str(i)] = ga_random.lwma_max_weight_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["lwma_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["lwma_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["lwma_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["lwma"] = lwma_include_triggers_in_bb_signal

        # ========================================================== CCI parameters:
        self.parameter_set["indicators_count"]["cci"] = cci_count

        if cci_count != 0:
            for i in range(cci_count):
                self.parameter_set["indicator_properties"]["timeframes"]["cci_" + str(i)] = ga_random.timeframe_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["cci_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["cci_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["cci_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["cci"] = cci_include_triggers_in_bb_signal

        # ========================================================== EOM parameters:
        self.parameter_set["indicators_count"]["eom"] = eom_count

        if eom_count != 0:
            for i in range(eom_count):
                self.parameter_set["indicator_properties"]["timeframes"]["eom_" + str(i)] = ga_random.timeframe_random_gen()

                self.parameter_set["spline_property"]["smoothing_factors"]["eom_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_set["spline_property"]["weights"]["eom_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_set["spline_property"]["flip"]["eom_" + str(i)] = ga_random.flip_random_gen()

            self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["eom"] = eom_include_triggers_in_bb_signal

        # ========================================================== OC parameters:
        self.parameter_set["indicators_count"]["oc_gradient"] = 1

        self.parameter_set["spline_property"]["smoothing_factors"]["oc_gradient_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_set["spline_property"]["weights"]["oc_gradient_0"] = ga_random.weight_random_gen()
        self.parameter_set["spline_property"]["flip"]["oc_gradient_0"] = ga_random.flip_random_gen()

        self.parameter_set["general_settings"]["include_triggers_in_bb_signal"]["oc_gradient"] = oc_include_triggers_in_bb_signal

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Volume parameters:
        self.parameter_set["spline_property"]["amplification_factor"]["volume_0"] = ga_random.amplification_factor_random_gen()
        self.parameter_set["spline_property"]["smoothing_factors"]["volume_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_set["spline_property"]["flip"]["volume_0"] = ga_random.flip_random_gen()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Volatility parameters:
        self.parameter_set["indicator_properties"]["timeframes"]["volatility_0"] = ga_random.timeframe_random_gen()

        self.parameter_set["spline_property"]["amplification_factor"]["volatility_0"] = ga_random.amplification_factor_random_gen()
        self.parameter_set["spline_property"]["smoothing_factors"]["volatility_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_set["spline_property"]["flip"]["volatility_0"] = ga_random.flip_random_gen()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Dynamic threshold parameters:
        self.parameter_set["spline_property"]["major_spline_standard_upper_thresholds"] = ga_random.major_spline_upper_threshold_random_gen()
        self.parameter_set["spline_property"]["major_spline_standard_lower_thresholds"] = ga_random.major_spline_lower_threshold_random_gen()
        self.parameter_set["indicator_properties"]["timeframes"]["threshold_timeframe"] = 20
