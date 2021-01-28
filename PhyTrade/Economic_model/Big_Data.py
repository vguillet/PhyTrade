
##################################################################################################################
"""
This script contains the BIGDATA class, necessary to collect and move around data in the model generation prototypes
"""

# Own modules
from PhyTrade.Tools.SPLINE_tools import SPLINE

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '11/28/2018'

##################################################################################################################


class BIGDATA:
    def __init__(self, data_slice):
        """
        Contains all the information relating to a specific analysis,
        modules can be called, and their instance attribute should be saved in the big_data instance
        (to enable attribute access anywhere inm the model).
        To compute specific attributes, run the corresponding Technical_Indicators/modules.
        The list of all options can be found in the PhyTrade Library file

        :param data_slice: DATA_SLICE class instance
        """
        self.buffer = 0
        self.data_slice = data_slice

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

    def gen_major_and_trade_results(self, big_data, upper_threshold, lower_threshold):
        """
        Used to stored all the data relevant to the final result of the model.
        It computes the buy and sell dates based on the inputted spline and upper/lower threshold

        :param big_data:  BIGDATA class instance
        :param upper_threshold: Upper threshold for sell trigger points generation
        :param lower_threshold: Lower threshold for buy trigger points generation
        """

        spline_tools = SPLINE(big_data=big_data)

        self.major_spline = big_data.combined_spline

        self.major_upper_threshold = upper_threshold
        self.major_lower_threshold = lower_threshold

        # -- Calculating buy/sell dates
        self.trade_signal, self.trade_spline, self.trade_upper_threshold, self.trade_lower_threshold = \
            spline_tools.calc_trading_spline(big_data=big_data,
                                             spline=self.major_spline,
                                             upper_threshold=self.major_upper_threshold,
                                             lower_threshold=self.major_lower_threshold)

        # --> Remove buffer data from final output
        self.major_spline = self.major_spline[big_data.buffer * big_data.spline_multiplication_coef:]
        self.major_upper_threshold = self.major_upper_threshold[big_data.buffer * big_data.spline_multiplication_coef:]
        self.major_lower_threshold = self.major_lower_threshold[big_data.buffer * big_data.spline_multiplication_coef:]

        self.trade_spline = self.trade_spline[big_data.buffer:]
        self.trade_signal = self.trade_signal[big_data.buffer:]
        self.trade_upper_threshold = self.trade_upper_threshold[big_data.buffer:]
        self.trade_lower_threshold = self.trade_lower_threshold[big_data.buffer:]

        big_data.data_slice.subslice_start_index += big_data.buffer
        big_data.data_slice.subslice_slice_size -= big_data.buffer

