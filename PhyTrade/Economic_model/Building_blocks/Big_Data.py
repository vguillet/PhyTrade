
##################################################################################################################
"""
This script contains the BIGDATA class, necessary to collect and move around data in the model generation prototypes
"""

# Own modules
from PhyTrade.Tools.SPLINE_tools import Spline_tools

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class BIGDATA:
    def __init__(self, data_slice, parameter_dictionary):
        """
        Contains all the information relating to a specific analysis,
        modules can be called, and their instance attribute should be saved in the big_data instance
        (to enable attribute access anywhere inm the model).
        To compute specific attributes, run the corresponding Technical_Indicators/modules.
        The list of all options can be found in the PhyTrade Library file

        :param data_slice: DATA_SLICE class instance
        :param parameter_dictionary: The parameter dictionary used for this model
        """

        self.buffer = 0
        self.data_slice = data_slice
        self.spline_multiplication_coef = parameter_dictionary["general_settings"]["spline_interpolation_factor"]

        # --> Apply buffer to data slice
        self.data_slice.start_index -= self.buffer
        self.data_slice.slice_size += self.buffer

        self.sell_trigger_values = []
        self.buy_trigger_values = []

        self.sell_trigger_dates = []
        self.buy_trigger_dates = []

        self.content = {"indicators": {},
                        "indicator_splines": {},
                        "trading_indicator_splines": {}}

    def gen_major_and_trade_results(self, upper_threshold, lower_threshold):
        """
        Used to stored all the data relevant to the final result of the model.
        It computes the buy and sell dates based on the inputted spline and upper/lower threshold

        :param upper_threshold: Upper threshold for sell trigger points generation
        :param lower_threshold: Lower threshold for buy trigger points generation
        """

        spline_tools = Spline_tools(big_data=self)

        self.major_upper_threshold = upper_threshold
        self.major_lower_threshold = lower_threshold

        # -- Calculating buy/sell dates
        self.trade_signal, self.trade_spline, self.trade_upper_threshold, self.trade_lower_threshold = \
            spline_tools.calc_trading_spline(big_data=self,
                                             spline=self.major_spline,
                                             upper_threshold=self.major_upper_threshold,
                                             lower_threshold=self.major_lower_threshold)

        # --> Remove buffer data from final output
        self.major_spline = self.major_spline[self.buffer * self.spline_multiplication_coef:]
        self.major_upper_threshold = self.major_upper_threshold[self.buffer * self.spline_multiplication_coef:]
        self.major_lower_threshold = self.major_lower_threshold[self.buffer * self.spline_multiplication_coef:]

        self.trade_spline = self.trade_spline[self.buffer:]
        self.trade_signal = self.trade_signal[self.buffer:]
        self.trade_upper_threshold = self.trade_upper_threshold[self.buffer:]
        self.trade_lower_threshold = self.trade_lower_threshold[self.buffer:]

        self.data_slice.subslice_start_index += self.buffer
        self.data_slice.subslice_slice_size -= self.buffer

