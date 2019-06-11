from PhyTrade.Tools.SPLINE_tools import SPLINE
from PhyTrade.Economic_model.Technical_Analysis.Tools.OC_tools import OC


class MAJOR_SPLINE:
    def __init__(self, big_data, upper_threshold, lower_threshold):
        """
        Used to stored all the data relevant to the final result of the model.
        It computes the buy and sell dates based on the inputted spline and upper/lower threshold

        :param big_data:  BIGDATA class instance
        :param spline: Spline to be used as the major spline
        :param upper_threshold: Upper threshold for sell trigger points generation
        :param lower_threshold: Lower threshold for buy trigger points generation
        """

        oc_tools = OC()
        spline_tools = SPLINE(big_data)

        self.spline = big_data.combined_spline
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

        # -- Calculating buy/sell dates
        self.sell_dates, self.buy_dates, self.sell_spline, self.buy_spline = \
            spline_tools.calc_spline_trigger(big_data, self.spline, self.upper_threshold, self.lower_threshold)

        # -- Calculating buy/sell values
        self.sell_values, self.buy_values = \
            oc_tools.calc_trigger_values(big_data, self.sell_dates, self.buy_dates)

        # -- Generate trade signal and spline
        self.trade_signal = [0] * len(big_data.data_slice_dates)

        for i in self.sell_dates:
            self.trade_signal[big_data.data_slice_dates.index(i)] = 1
        for i in self.buy_dates:
            self.trade_signal[big_data.data_slice_dates.index(i)] = -1

        self.trade_spline = [self.spline[i] for i in range(0, len(self.spline), int(len(self.spline)/len(big_data.data_slice_dates)))]


