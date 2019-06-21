"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""
from PhyTrade.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data
from PhyTrade.Backtesting.Metalabel_optimisation.METALABELS_gen import MetaLabeling

import numpy as np


class data_slice:
    def __init__(self, ticker, start_date, slice_size, data_slice_shift_per_gen,
                 data_selection="Open", end_date=None, data_looper=True):

        self.ticker = ticker
        self.data = fetch_technical_data(ticker)

        # ---- Data slice properties
        # --> Find corresponding starting data index from start date
        self.start_date = start_date
        self.start_index = -len(self.data)+np.flatnonzero(self.data['Date'] == self.start_date)[0]

        # --> Adjust slice size according to data available if necessary
        self.slice_size = slice_size

        if len(self.data[self.start_index:]) < self.slice_size:
            self.slice_size = -len(self.data[self.start_index:])
            print("Data slice size adjusted to:", self.slice_size)

        # --> Find corresponding stop data index
        self.stop_index = self.start_index + self.slice_size
        self.stop_date = self.data.iloc[self.stop_index]['Date']

        # ---- Generate special dataframes
        # --> Slice Pandas dataframe according to start/stop indexes
        self.sliced_data = self.data[self.start_index:self.stop_index]

        # --> List open/closed price according to selection
        self.selection = data_selection
        self.data_selection = list(self.data[self.selection])
        self.sliced_data_selection = list(self.sliced_data[self.selection])

        # ---- Default properties
        self.default_start_date = self.start_date
        self.default_start_index = self.start_index

        self.default_end_date = end_date
        if self.default_end_date is not None:
            self.default_end_index = -len(self.data)+np.flatnonzero(self.data['Date'] == self.default_end_date)[0]

        self.default_slice_size = slice_size
        self.data_slice_shift_per_gen = data_slice_shift_per_gen

        # ---- Data slice settings
        # --> Disable/enable  data looping
        self.data_looper = data_looper
        self.end_of_dataset = False

    def gen_slice_metalabels(self, upper_barrier, lower_barrier, look_ahead, metalabeling_setting=0):
        """
        Generate metalabels for a specific data slice. Only necessary to be ran when a
        dataslice instance is initiated.

        :param upper_barrier: Upper barrier to be used
        :param lower_barrier: Lower barrier to be used
        :param look_ahead: Look ahead to be used
        :param metalabeling_setting: Metalabeling method to be used
        """
        # --> Create mock data slice and add parameters and info
        mock_data_slice = address_sim()
        mock_data_slice.data_selection = self.data_selection
        mock_data_slice.sliced_data_selection = self.sliced_data_selection
        mock_data_slice.start_index = self.start_index
        mock_data_slice.stop_index = self.stop_index

        self.metalabels = MetaLabeling(upper_barrier, lower_barrier,
                                       look_ahead,
                                       mock_data_slice,
                                       metalabel_setting=metalabeling_setting).metalabels
        return

    def get_next_data_slice(self):
        # --> Determine new start/stop indexes
        self.start_index += self.slice_size
        self.start_date = self.data.iloc[self.start_index]['Date']

        self.stop_index += self.slice_size

        # --> Check for end of data
        self.check_end_data()

        # --> Determine start/stop date
        self.start_date = self.data.iloc[self.start_index]['Date']
        self.stop_date = self.data.iloc[self.stop_index]['Date']

        # --> Update slice data
        self.sliced_data = self.data[self.start_index:self.stop_index]
        self.sliced_data_selection = list(self.sliced_data[self.selection])

    def get_shifted_data_slice(self):
        # --> Determine new start/stop indexes
        self.start_index = self.start_index + self.data_slice_shift_per_gen
        self.start_date = self.data.iloc[self.start_index]['Date']

        self.stop_index = self.stop_index + self.data_slice_shift_per_gen

        # --> Check for end of data
        self.check_end_data()

        # --> Determine stop date
        self.start_date = self.data.iloc[self.start_index]['Date']
        self.stop_date = self.data.iloc[self.stop_index]['Date']

        # --> Update slice data
        self.sliced_data = self.data[self.start_index:self.stop_index]
        self.sliced_data_selection = list(self.sliced_data[self.selection])

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

        tradebot = Tradebot_v4(self.sliced_data_selection,
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

    # ========================================= Data slice tools =========================================
    def check_end_data(self):
        if self.default_end_date is None:
            if self.stop_index >= -1:
                if self.start_index < -1:
                    self.stop_index = -1
                    self.slice_size = abs(self.start_index)-1
                    return
                else:
                    if self.data_looper is True:
                        # --> Loop back to beginning of dataset if end of dataset is reached
                        self.slice_size = self.default_slice_size
                        self.start_index = self.default_start_index
                        self.stop_index = self.default_start_index + self.default_slice_size
                        return
                    else:
                        # --> Trigger End of dataset
                        self.end_of_dataset = True
                        print("End of dataset reached\n")
                        return
            else:
                return
        else:
            if self.stop_index > self.default_end_index:
                if self.start_index < self.default_end_index:
                    self.stop_index = self.default_end_index
                    self.slice_size = abs(self.start_index - self.stop_index)
                    return
                else:
                    if self.data_looper is True:
                        # --> Loop back to beginning of dataset if end of dataset is reached
                        self.slice_size = self.default_slice_size
                        self.start_index = self.default_start_index
                        self.stop_index = self.default_start_index + self.default_slice_size
                        return
                    else:
                        # --> Trigger End of dataset
                        self.end_of_dataset = True
                        print("End of dataset reached\n")
                        return
            else:
                return

    def __str__(self):
        return "Data slice: Ticker - " + self.ticker + ", Current start_date - " + self.start_date + ", Slice size: " + str(self.slice_size)


class address_sim:
    def __init__(self):
        pass