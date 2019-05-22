"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.METALABELING_gen import MetaLabeling


class data_slice_info:
    def __init__(self, start_slice, slice_size, data_slice_shift_per_gen,
                 upper_barrier, lower_barrier, look_ahead):

        self.default_start_slice_index = start_slice

        self.start_index = start_slice
        self.stop_index = start_slice + slice_size

        self.slice_size = slice_size
        self.data_slice_shift_per_gen = data_slice_shift_per_gen

        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier
        self.look_ahead = look_ahead

    def gen_slice_metalabels(self, ticker):
        self.metalabels = MetaLabeling(ticker,
                                       self.upper_barrier, self.lower_barrier,
                                       self.look_ahead,
                                       self.start_index, self.stop_index)
        return

    def get_next_data_slice(self, ticker):
        # -- Determine new start/stop indexes
        self.start_index += self.slice_size
        self.stop_index += self.slice_size

        if self.stop_index >= 0:
            if self.start_index < 0:
                self.stop_index = 0

            else:
                # ------------------ Loop back to beginning of dataset if end of dataset is reached
                self.start_index = self.default_start_slice_index
                self.stop_index = self.default_start_slice_index + self.slice_size

        # -- Generate new metalabels
        self.gen_slice_metalabels(ticker)
        return

    def get_shifted_data_slice(self, ticker):
        # -- Determine new start/stop indexes
        self.start_index = self.start_index + self.data_slice_shift_per_gen
        self.stop_index = self.stop_index + self.data_slice_shift_per_gen

        if self.stop_index >= 0:
            if self.start_index < 0:
                self.stop_index = -1

            else:
                # ------------------ Loop back to beginning of dataset if end of dataset is reached
                self.start_index = self.default_start_slice_index
                self.stop_index = self.default_start_slice_index + self.slice_size

        print(self.start_index)
        print(self.stop_index)

        # -- Generate new metalabels
        self.gen_slice_metalabels(ticker)
        return

    def perform_trade_run(self, ticker):
        from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3
        from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Big_Data import BIGDATA
        from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data

        data = fetch_technical_data(ticker)

        analysis = mock()
        analysis.big_data = BIGDATA(data, self.start_index, self.stop_index)

        # TODO: Add open/close value selection
        analysis.big_data.buy_sell_labels = self.metalabels.close_values_metalabels
        tradebot = Tradebot_v3(analysis)
        self.metalabels_account = tradebot.account

        return


class mock:
    def __init__(self):
        return
