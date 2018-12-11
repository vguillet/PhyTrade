from PhyTrade.Technical_Analysis.Tools.SPLINE_tools import SPLINE
from PhyTrade.Technical_Analysis.Tools.OC_tools import OC


class MAJOR_SPLINE:
    def __init__(self, big_data, spline, upper_threshold, lower_threshold):

        oc_tools = OC()
        spline_tools = SPLINE(big_data)

        self.spline = spline
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

        # -- Calculating buy/sell dates
        self.sell_dates, self.buy_dates, self.sell_spline, self.buy_spline = \
            spline_tools.calc_spline_trigger(big_data, spline, self.upper_threshold, self.lower_threshold)

        # -- Calculating buy/sell values
        self.sell_values, self.buy_values = \
            oc_tools.calc_trigger_values(big_data, self.sell_dates, self.buy_dates)

