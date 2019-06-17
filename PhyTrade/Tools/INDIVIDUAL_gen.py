from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_random_gen import EVOA_random_gen
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data
from SETTINGS import SETTINGS


class Individual:
    def __init__(self, ticker="AAPL", parameter_set=None):
        # ========================= DATA COLLECTION INITIALISATION =======================
        self.ticker = ticker
        self.data = fetch_technical_data(self.ticker)

        if parameter_set is None:
            settings = SETTINGS()
            settings.gen_individual_settings()
            self.gen_parameter_set(rsi_count=settings.rsi_count,
                                   sma_count=settings.sma_count,
                                   ema_count=settings.ema_count,
                                   lwma_count=settings.lwma_count,
                                   cci_count=settings.cci_count,
                                   eom_count=settings.eom_count)
        else:
            self.parameter_dictionary = parameter_set

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Counting number of parameters
        self.nb_of_parameters = 0
        for i in self.parameter_dictionary:
            for j in range(len(self.parameter_dictionary[i])):
                self.nb_of_parameters += 1

    def gen_economic_model(self, data_slice, plot_eco_model_results=False):
        from PhyTrade.Economic_model.Analysis_protocols.Prototype_5 import Prototype_5
        import matplotlib.pyplot as plt
        from PhyTrade.Tools.PLOT_tools import PLOT_tools

        self.analysis = Prototype_5(self.parameter_dictionary, data_slice)

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

    def gen_parameter_set(self, rsi_count=1, sma_count=1, ema_count=1, lwma_count=1, cci_count=1, eom_count=1):
        ga_random = EVOA_random_gen()
        self.parameter_dictionary = {"indicators_count": {},
                                     "spline_property": {"weights": {},
                                                         "smoothing_factors": {},
                                                         "amplification_factor": {},
                                                         "flip": {},
                                                         "major_spline_standard_upper_thresholds": {},
                                                         "major_spline_standard_lower_thresholds": {}},
                                     "indicator_properties": {"timeframes": {}}}

        # ========================================================== RSI parameters:
        self.parameter_dictionary["indicators_count"]["rsi"] = rsi_count

        if rsi_count != 0:
            self.parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"] = {}
            self.parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"] = {}

            for i in range(rsi_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["rsi_"+str(i)] = ga_random.timeframe_random_gen()
                self.parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"]["rsi_" + str(i)] = ga_random.rsi_upper_threshold_random_gen()
                self.parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"]["rsi_" + str(i)] = ga_random.rsi_lower_threshold_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["rsi_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["rsi_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["rsi_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== SMA parameters:
        self.parameter_dictionary["indicators_count"]["sma"] = sma_count

        if sma_count != 0:
            for i in range(sma_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["sma_"+str(i)+"_1"] = ga_random.timeframe_random_gen()
                self.parameter_dictionary["indicator_properties"]["timeframes"]["sma_"+str(i)+"_2"] = ga_random.timeframe_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["sma_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["sma_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["sma_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== EMA parameters:
        self.parameter_dictionary["indicators_count"]["ema"] = ema_count

        if ema_count != 0:
            for i in range(ema_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["ema_"+str(i)+"_1"] = ga_random.timeframe_random_gen()
                self.parameter_dictionary["indicator_properties"]["timeframes"]["ema_"+str(i)+"_2"] = ga_random.timeframe_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["ema_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["ema_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["ema_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== LWMA parameters:
        self.parameter_dictionary["indicators_count"]["lwma"] = lwma_count

        if lwma_count != 0:
            self.parameter_dictionary["indicator_properties"]["lwma_max_weights"] = {}

            for i in range(lwma_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["lwma_"+str(i)] = ga_random.timeframe_random_gen()
                self.parameter_dictionary["indicator_properties"]["lwma_max_weights"]["lwma_"+str(i)] = ga_random.lwma_max_weight_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["lwma_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["lwma_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["lwma_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== CCI parameters:
        self.parameter_dictionary["indicators_count"]["cci"] = cci_count

        if cci_count != 0:
            for i in range(cci_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["cci_"+str(i)] = ga_random.timeframe_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["cci_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["cci_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["cci_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== EOM parameters:
        self.parameter_dictionary["indicators_count"]["eom"] = eom_count

        if eom_count != 0:
            for i in range(eom_count):
                self.parameter_dictionary["indicator_properties"]["timeframes"]["eom_"+str(i)] = ga_random.timeframe_random_gen()

                self.parameter_dictionary["spline_property"]["smoothing_factors"]["eom_" + str(i)] = ga_random.smoothing_factor_random_gen()
                self.parameter_dictionary["spline_property"]["weights"]["eom_" + str(i)] = ga_random.weight_random_gen()
                self.parameter_dictionary["spline_property"]["flip"]["eom_" + str(i)] = ga_random.flip_random_gen()

        # ========================================================== OC parameters:
        self.parameter_dictionary["indicators_count"]["oc_gradient"] = 1

        self.parameter_dictionary["spline_property"]["smoothing_factors"]["oc_gradient_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_dictionary["spline_property"]["weights"]["oc_gradient_0"] = ga_random.weight_random_gen()
        self.parameter_dictionary["spline_property"]["flip"]["oc_gradient_0"] = ga_random.flip_random_gen()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Volume parameters:
        self.parameter_dictionary["spline_property"]["amplification_factor"]["volume_0"] = ga_random.amplification_factor_random_gen()
        self.parameter_dictionary["spline_property"]["smoothing_factors"]["volume_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_dictionary["spline_property"]["flip"]["volume_0"] = ga_random.flip_random_gen()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Volatility parameters:
        self.parameter_dictionary["indicator_properties"]["timeframes"]["volatility_0"] = ga_random.timeframe_random_gen()

        self.parameter_dictionary["spline_property"]["amplification_factor"]["volatility_0"] = ga_random.amplification_factor_random_gen()
        self.parameter_dictionary["spline_property"]["smoothing_factors"]["volatility_0"] = ga_random.smoothing_factor_random_gen()
        self.parameter_dictionary["spline_property"]["flip"]["volatility_0"] = ga_random.flip_random_gen()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Dynamic threshold values:
        self.parameter_dictionary["spline_property"]["major_spline_standard_upper_thresholds"] = ga_random.major_spline_upper_threshold_random_gen()
        self.parameter_dictionary["spline_property"]["major_spline_standard_lower_thresholds"] = ga_random.major_spline_lower_threshold_random_gen()

