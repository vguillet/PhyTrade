"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data
from PhyTrade.ML_optimisation.Metalabel_optimisation.METALABELING_gen import MetaLabeling

import numpy as np


class data_slice:
    def __init__(self, ticker, start_date, slice_size, data_slice_shift_per_gen,
                 upper_barrier, lower_barrier, look_ahead,
                 data_selection="Open", data_looper=True):

        self.ticker = ticker
        self.data = fetch_technical_data(ticker)

        # ---- Data slice properties
        # --> Find corresponding starting data index from start date
        self.start_date = start_date
        self.start_index = -len(self.data)+np.flatnonzero(self.data['index'] == self.start_date)[0]

        # --> Find corresponding stop data index
        self.slice_size = slice_size
        self.stop_index = self.start_index + self.slice_size
        self.stop_date = self.data.iloc[self.stop_index]['index']

        self.sliced_data = self.data[self.start_index:self.stop_index]

        self.data_slice_shift_per_gen = data_slice_shift_per_gen

        # ---- Record default properties
        self.default_start_slice_date = self.start_date
        self.default_start_slice_index = self.start_index
        self.default_slice_size = slice_size

        # ---- Metalabels properties
        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier

        self.look_ahead = look_ahead

        # ---- Data slice settings
        # --> Disable/enable  data looping
        self.data_looper = data_looper
        self.end_of_dataset = False

        # --> List open/closed price to be used by tradebot
        self.selection = data_selection
        self.data_selection = list(self.data[self.selection])
        self.data_slice_selection = list(self.sliced_data[self.selection])

    def gen_slice_metalabels(self):
        """
        Generate metalabels for a specific data slice. Only necessary to be ran when a
        dataslice instance is initiated.
        """
        # --> Create mock data slice and add parameters and info
        mock_data_slice = address_sim()
        mock_data_slice.data_selection = self.data_selection
        mock_data_slice.data_slice_selection = self.data_slice_selection
        mock_data_slice.start_index = self.start_index
        mock_data_slice.stop_index = self.stop_index

        self.metalabels = MetaLabeling(self.upper_barrier, self.lower_barrier,
                                       self.look_ahead,
                                       mock_data_slice,
                                       metalabel_setting=0).metalabels
        return

    def get_next_data_slice(self):
        # --> Determine new start/stop indexes
        self.start_index += self.slice_size
        self.start_date = self.data.iloc[self.start_index]['index']

        self.stop_index += self.slice_size
        self.stop_date = self.data.iloc[self.stop_index]['index']

        if self.stop_index >= 0:
            if self.start_index < 0:
                self.stop_index = -1
                self.slice_size = abs(self.start_index+self.stop_index)

            else:
                if self.data_looper is True:
                    # --> Loop back to beginning of dataset if end of dataset is reached
                    self.slice_size = self.default_slice_size
                    self.start_index = self.default_start_slice_index
                    self.stop_index = self.default_start_slice_index + self.default_slice_size
                else:
                    # --> Trigger End of dataset
                    self.end_of_dataset = True
                    print("End of dataset reached\n")
                    return

        # --> Update slice data
        self.sliced_data = self.data[self.start_index:self.stop_index]
        self.data_slice_selection = list(self.sliced_data[self.selection])

        # --> Generate new metalabels
        self.gen_slice_metalabels()
        return

    def get_shifted_data_slice(self):
        # --> Determine new start/stop indexes
        self.start_index = self.start_index + self.data_slice_shift_per_gen
        self.start_date = self.data.iloc[self.start_index]['index']

        self.stop_index = self.stop_index + self.data_slice_shift_per_gen
        self.stop_date = self.data.iloc[self.stop_index]['index']

        if self.stop_index >= 0:
            if self.start_index < 0:
                self.stop_index = -1

            else:
                if self.data_looper is True:
                    # ------------------ Loop back to beginning of dataset if end of dataset is reached
                    self.start_index = self.default_start_slice_index
                    self.stop_index = self.default_start_slice_index + self.slice_size
                else:
                    # ------------------ Trigger End of dataset
                    self.end_of_dataset = True
                    print("End of dataset reached\n")
                    return

        # --> Update slice data
        self.sliced_data = self.data[self.start_index:self.stop_index]
        self.data_slice_selection = list(self.sliced_data[self.selection])

        # --> Generate new metalabels
        self.gen_slice_metalabels()
        return

    def perform_trade_run(self,
                          investment_settings=1, cash_in_settings=0,
                          initial_funds=1000,
                          initial_assets=0,
                          prev_stop_loss=0.85, max_stop_loss=0.75,
                          max_investment_per_trade=500,
                          prev_simple_investment_assets=None,
                          print_trade_process=False):

        from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4

        self.trade_signal = self.metalabels

        tradebot = Tradebot_v4(self.data_slice_selection,
                               self.trade_signal,
                               investment_settings=investment_settings, cash_in_settings=cash_in_settings,
                               initial_funds=initial_funds,
                               initial_assets=initial_assets,
                               prev_stop_loss=prev_stop_loss, max_stop_loss=max_stop_loss,
                               max_investment_per_trade=max_investment_per_trade,
                               prev_simple_investment_assets=prev_simple_investment_assets,
                               print_trade_process=print_trade_process)

        self.metalabels_account = tradebot.account
        return

    def __str__(self):
        return "Data slice: Ticker - " + self.ticker + ", Current start_date - " + self.start_date + ", Slice size: " + str(self.slice_size)

class address_sim:
    def __init__(self):
        pass