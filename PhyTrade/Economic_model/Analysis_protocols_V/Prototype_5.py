"""
This script contains the Prototype_5 class
This prototype is based entirely on technical analysis, and include new indicators, including:
    - EMA
    - LWMA

The following parameter_dictionary still require manual input:
    - spline interpolation coef
    - include trigger in signals (Technical_Indicators output generation)
    - buffer and buffer settings (Threshold determination)

Victor Guillet
12/14/2018
"""

from PhyTrade.Economic_model.Big_Data import BIGDATA
# ---> Import model settings
from SETTINGS import SETTINGS

# ---> Import indicators
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.RSI_gen import RSI
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.SMA_gen import SMA
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.EMA_gen import EMA
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.LWMA_gen import LWMA
from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.OC_AVG_GRADIENT_gen import OC_AVG_GRADIENT

# ---> Import amplification signals
from PhyTrade.Economic_model.Technical_Analysis.Amplification_signals.Volume_gen import VOLUME
from PhyTrade.Economic_model.Technical_Analysis.Amplification_signals.Volatility_gen import VOLATILITY

# ---> import general tools
from PhyTrade.Economic_model.MAJOR_SPLINE_gen import MAJOR_SPLINE
from PhyTrade.Tools.MATH_tools import MATH_tools
from PhyTrade.Economic_model.Technical_Analysis.Tools.OC_tools import OC
from PhyTrade.Tools.SPLINE_tools import SPLINE

import numpy as np
import sys


class Prototype_5:
    def __init__(self, parameter_dictionary, data_slice):
        """
        Generate a model containing all coded indicators, process and generate bullish/bearish signals

        :param parameter_dictionary: Dictionary of dictionaries containing the values for all the variables of each signal
        :param data_slice: data_slice class instance
        """

        # ========================= ANALYSIS INITIALISATION ==============================
        # --> Fetch model settings
        settings = SETTINGS()
        settings.gen_model_settings()

        # --> Initiate records
        self.big_data = BIGDATA(data_slice)

        # ~~~~~~~~~~~~~~~~~~ Tools initialisation
        self.big_data.spline_multiplication_coef = settings.spline_interpolation_factor

        self.oc_tools = OC()
        self.spline_tools = SPLINE(self.big_data)
        self.math_tools = MATH_tools()

        # ~~~~~~~~~~~~~~~~~~ Technical_Indicators initialisation
        # --> RSI initialisation
        self.big_data.content["indicators"]["rsi"] = []
        for i in range(parameter_dictionary["indicators_count"]["rsi"]):
            self.big_data.content["indicators"]["rsi"].append(RSI(self.big_data,
                    timeframe=parameter_dictionary["indicator_properties"]["timeframes"]["rsi_"+str(i)],
                    standard_upper_threshold=parameter_dictionary["indicator_properties"]["rsi_standard_upper_thresholds"]["rsi_" + str(i)],
                    standard_lower_threshold=parameter_dictionary["indicator_properties"]["rsi_standard_lower_thresholds"]["rsi_" + str(i)],
                    buffer_setting=settings.buffer_setting))

        # --> SMA initialisation
        self.big_data.content["indicators"]["sma"] = []
        for i in range(parameter_dictionary["indicators_count"]["sma"]):
            self.big_data.content["indicators"]["sma"].append(SMA(self.big_data,
                    timeperiod_1=parameter_dictionary["indicator_properties"]["timeframes"]["sma_"+str(i)+"_1"],
                    timeperiod_2=parameter_dictionary["indicator_properties"]["timeframes"]["sma_"+str(i)+"_2"]))

        # --> EMA initialisation
        self.big_data.content["indicators"]["ema"] = []
        for i in range(parameter_dictionary["indicators_count"]["ema"]):
            self.big_data.content["indicators"]["ema"].append(EMA(self.big_data,
                    timeperiod_1=parameter_dictionary["indicator_properties"]["timeframes"]["ema_"+str(i)+"_1"],
                    timeperiod_2=parameter_dictionary["indicator_properties"]["timeframes"]["ema_"+str(i)+"_2"]))

        # --> LWMA initialisation
        self.big_data.content["indicators"]["lwma"] = []
        for i in range(parameter_dictionary["indicators_count"]["lwma"]):
            self.big_data.content["indicators"]["lwma"].append(LWMA(self.big_data,
                    timeperiod=parameter_dictionary["indicator_properties"]["timeframes"]["lwma_"+str(i)]))

        # --> OC_AVG_GRADIENT initialisation
        self.big_data.content["indicators"]["oc_gradient"] = []
        for i in range(parameter_dictionary["indicators_count"]["oc_gradient"]):
            self.big_data.content["indicators"]["oc_gradient"].append(OC_AVG_GRADIENT(self.big_data))

        # ~~~~~~~~~~~~~~~~~~ Amplification signal initialisation
        # --> Volume initialisation
        self.big_data.volume = VOLUME(self.big_data,
                                      amplification_factor=parameter_dictionary["spline_property"]["amplification_factor"]["volume_0"])

        # --> Volatility initialisation
        self.big_data.volatility = VOLATILITY(self.big_data,
                                              timeframe=parameter_dictionary["indicator_properties"]["timeframes"]["volatility_0"],
                                              amplification_factor=parameter_dictionary["spline_property"]["amplification_factor"]["volatility_0"])

        # ================================================================================
        """




        """
        # ========================= DATA GENERATION AND PROCESSING =======================
        # ~~~~~~~~~~~~~~~~~~ Technical_Indicators output generation
        for indicator_type in parameter_dictionary["indicators_count"]:
            if parameter_dictionary["indicators_count"][indicator_type] != 0:
                for indicator in self.big_data.content["indicators"][indicator_type]:
                    indicator.get_output(self.big_data,
                                         include_triggers_in_bb_signal=getattr(settings,
                                                                               indicator_type + "_include_triggers_in_bb_signal"))

        # ~~~~~~~~~~~~~~~~~~ BB signals processing
        # --> Creating splines from indicator signals
        for indicator_type in parameter_dictionary["indicators_count"]:
            if parameter_dictionary["indicators_count"][indicator_type] != 0:
                self.big_data.content["splines"][indicator_type] = []
                for i in range(len(self.big_data.content["indicators"][indicator_type])):
                    self.big_data.content["splines"][indicator_type].append(
                        self.spline_tools.calc_signal_to_spline(self.big_data,
                                                                self.big_data.content["indicators"][indicator_type][i].bb_signal,
                                                                smoothing_factor=parameter_dictionary["spline_property"]
                                                                ["smoothing_factors"][indicator_type + "_" + str(i)]))

        # --> Generating amplification signals
        self.big_data.spline_volume = self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volume.amp_coef,
                                                                              smoothing_factor=parameter_dictionary["spline_property"]["smoothing_factors"]["volume_0"])

        self.big_data.spline_volatility = self.spline_tools.calc_signal_to_spline(self.big_data, self.big_data.volatility.amp_coef,
                                                                                  smoothing_factor=parameter_dictionary["spline_property"]["smoothing_factors"]["volatility_0"])

        # --> Tuning separate signals
        for indicator_type in parameter_dictionary["indicators_count"]:
            if parameter_dictionary["indicators_count"][indicator_type] != 0:
                for i in range(len(self.big_data.content["splines"][indicator_type])):
                    if parameter_dictionary["spline_property"]["flip"][indicator_type+"_"+str(i)] is True:
                        self.big_data.content["splines"][indicator_type][i] = \
                            self.spline_tools.flip_spline(self.big_data.content["splines"][indicator_type][i])
                        print("spline flipped")

        # --> Adding signals together
        # Creating signal array
        self.big_data.spline_array = np.zeros(shape=(sum(parameter_dictionary["indicators_count"].values), data_slice.slice_size))
        self.big_data.weights_array = np.zeros(shape=(sum(parameter_dictionary["indicators_count"].values), 1))

        counter = 0
        for indicator_type in self.big_data.content["splines"]:
            for i in range(len(self.big_data.content["splines"][indicator_type])):
                self.big_data.spline_array[counter] = self.big_data.content["splines"][indicator_type][i]
                self.big_data.weights_array[counter] = parameter_dictionary["spline_property"]["weights"][indicator_type+"_"+str(i)]
                counter += 1

        self.big_data.combined_spline = \
            self.spline_tools.combine_splines(self.big_data.spline_array,
                                              self.big_data.weights_array)

        # ---> Tuning combined signal
        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volume, std_dev_max=settings.volume_std_dev_max)

        self.big_data.combined_spline = \
            self.spline_tools.modulate_amplitude_spline(
                self.big_data.combined_spline, self.big_data.spline_volatility, std_dev_max=settings.volatility_std_dev_max)

        # print(self.big_data.combined_spline)
        # print(np.shape(self.big_data.combined_spline))

        self.big_data.combined_spline = self.math_tools.normalise_minus_one_one(self.big_data.combined_spline)

        # ~~~~~~~~~~~~~~~~~~ Threshold determination
        # ---> Creating dynamic thresholds
        upper_threshold, lower_threshold = \
            self.spline_tools.calc_thresholds(self.big_data, self.big_data.combined_spline,
                                              buffer=settings.buffer, buffer_setting=settings.buffer_setting,
                                              standard_upper_threshold=parameter_dictionary["major_spline_standard_upper_thresholds"]["major_spline_standard_upper_threshold"],
                                              standard_lower_threshold=parameter_dictionary["major_spline_standard_lower_thresholds"]["major_spline_standard_lower_threshold"])

        # ---> Modulating threshold with SMA 3 value
        # upper_threshold = self.spline_tools.modulate_amplitude_spline(
        #         upper_threshold,  self.math_tools.amplify(
        #             self.math_tools.normalise_zero_one(self.big_data.spline_sma_3), 0.3))
        #
        # lower_threshold = self.spline_tools.modulate_amplitude_spline(
        #         lower_threshold,  self.math_tools.amplify(
        #             self.math_tools.normalise_zero_one(self.big_data.spline_sma_3), 0.3))

        # ~~~~~~~~~~~~~~~~~~ Creating Major Spline/trigger values
        self.big_data.Major_spline = MAJOR_SPLINE(self.big_data,
                                                  upper_threshold, lower_threshold)

