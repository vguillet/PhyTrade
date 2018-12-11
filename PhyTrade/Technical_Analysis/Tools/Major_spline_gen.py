from PhyTrade.Technical_Analysis.Tools.SPLINE_tools import SPLINE
from PhyTrade.Technical_Analysis.Tools.OC_tools import OC


class MAJOR_SPLINE:
    def __init__(self, big_data, spline, threshold_buffer=0.05, threshold_buffer_setting=0,
                 upper_threshold=0.5, lower_threshold=-0.5):

        oc_tools = OC()
        spline_tools = SPLINE(big_data)

        self.spline = spline

        # -- Creating dynamic thresholds
        self.upper_threshold, self.lower_threshold = \
            spline_tools.calc_thresholds(big_data, spline,
                                         buffer=threshold_buffer,
                                         buffer_setting=threshold_buffer_setting,
                                         standard_upper_threshold=upper_threshold,
                                         standard_lower_threshold=lower_threshold)

        # -- Calculating buy/sell dates
        self.sell_dates, self.buy_dates, self.sell_spline, self.buy_spline = \
            spline_tools.calc_spline_trigger(big_data, spline, self.upper_threshold, self.lower_threshold)

        # -- Calculating buy/sell values
        self.sell_values, self.buy_values = \
            oc_tools.calc_trigger_values(big_data, self.sell_dates, self.buy_dates)

