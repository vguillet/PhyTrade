from PhyTrade.Tools.SPLINE_tools import SPLINE


class MAJOR_SPLINE:
    def __init__(self, big_data, upper_threshold, lower_threshold):
        """
        Used to stored all the data relevant to the final result of the model.
        It computes the buy and sell dates based on the inputted spline and upper/lower threshold

        :param big_data:  BIGDATA class instance
        :param upper_threshold: Upper threshold for sell trigger points generation
        :param lower_threshold: Lower threshold for buy trigger points generation
        """

        spline_tools = SPLINE(big_data)

        self.spline = big_data.combined_spline

        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

        # -- Calculating buy/sell dates
        self.trade_signal, self.trade_spline = \
            spline_tools.calc_trading_spline(big_data, self.spline, self.upper_threshold, self.lower_threshold)

        # --> Remove buffer data from final output
        self.spline = self.spline[big_data.buffer*big_data.spline_multiplication_coef:]
        self.upper_threshold = self.upper_threshold[big_data.buffer*big_data.spline_multiplication_coef:]
        self.lower_threshold = self.lower_threshold[big_data.buffer*big_data.spline_multiplication_coef:]

        self.trade_spline = self.trade_spline[big_data.buffer:]
        self.trade_signal = self.trade_signal[big_data.buffer:]

        big_data.data_slice.start_index += big_data.buffer
        big_data.data_slice.slice_size -= big_data.buffer

