
################################################################################################################
"""
This script contains the data_slice class used by the EVOA Optimisation. The slice itself contains
information about the slice analysed, including the starting and stopping index, along with the metalabels generated
"""
# Built-in/Generic Imports
import sys

# Libs

# Own modules
from PhyTrade.Data_Collection_preparation.Tools.Fetch_technical_data import fetch_technical_data
from PhyTrade.Data_Collection_preparation.TS_dataslice import TS_dataslice
from PhyTrade.Backtesting.Metalabeling.Metalabels import MetaLabels

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class Trading_dataslice(TS_dataslice):
    def __init__(self, ticker,
                 start_date,
                 subslice_size, subslice_shift_per_step,
                 price_data_selection="Close", end_date=None, data_looper=False):
        """
        Trading_dataslice is build around the TS_dataslice parent.
        Instances contain all the data related to a ticker in a given date/time interval

        :param ticker:
        :param start_date:
        :param subslice_size:
        :param subslice_shift_per_step:
        :param price_data_selection:
        :param end_date:
        :param data_looper:
        """
        self.ticker = ticker
        self.price_data_selection = price_data_selection
        self.metalabels = None
        self.metalabels_account = None

        # ---- Generating TS_dataslice
        super().__init__(data=fetch_technical_data(ticker),
                         subslice_size=subslice_size,
                         subslice_shift_per_step=subslice_shift_per_step,
                         start_date=start_date,
                         end_date=end_date,
                         data_looper=data_looper)

        # TODO: Clean up/move boilinger bands calc
        # --> Calculate boilinger bands
        window = 20

        self.data["close_MA"] = self.data["Close"].rolling(window=window).mean()
        self.data["close_SD"] = self.data["Close"].rolling(window=window).std()
        self.data["close_upper_band"] = self.data["close_MA"] + 2 * self.data["close_SD"]
        self.data["close_lower_band"] = self.data["close_MA"] - 2 * self.data["close_SD"]

        self.data["open_MA"] = self.data["Open"].rolling(window=window).mean()
        self.data["open_SD"] = self.data["Open"].rolling(window=window).std()
        self.data["open_upper_band"] = self.data["open_MA"] + 2 * self.data["open_SD"]
        self.data["open_lower_band"] = self.data["open_MA"] - 2 * self.data["open_SD"]

    @property
    def data_selection(self):
        return list(self.data[self.price_data_selection])

    @property
    def subslice_data_selection(self):
        return list(self.subslice_data[self.price_data_selection])

    def gen_subslice_metalabels(self, upper_barrier, lower_barrier, look_ahead, metalabeling_setting=0):
        """
        Generate metalabels for current subslice. Only necessary to be ran when a
        dataslice instance is initiated.

        :param upper_barrier: Upper barrier to be used
        :param lower_barrier: Lower barrier to be used
        :param look_ahead: Look ahead to be used
        :param metalabeling_setting: Metalabeling method to be used
        """
        # --> Create mock data slice and add parameters and info to feed to metalabel generator
        mock_data_slice = address_sim()
        mock_data_slice.data_selection = self.data_selection
        mock_data_slice.sliced_data_selection = self.subslice_data_selection
        mock_data_slice.subslice_start_index = self.subslice_start_index
        mock_data_slice.subslice_stop_index = self.subslice_stop_index

        self.metalabels = MetaLabels(upper_barrier, lower_barrier,
                                     look_ahead,
                                     mock_data_slice,
                                     metalabel_setting=metalabeling_setting).metalabels
        return

    def perform_metatrade_run(self,
                              investment_settings=1, cash_in_settings=0,
                              initial_funds=1000,
                              initial_assets=0,
                              prev_stop_loss=0.85, max_stop_loss=0.75,
                              max_investment_per_trade=500,
                              prev_simple_investment_assets=None,
                              print_trade_process=False):
        """
        Performs a trade run using the metalabels as trading signal

        :param investment_settings:
        :param cash_in_settings:
        :param initial_funds:
        :param initial_assets:
        :param prev_stop_loss:
        :param max_stop_loss:
        :param max_investment_per_trade:
        :param prev_simple_investment_assets:
        :param print_trade_process:
        :return:
        """

        if self.metalabels is None:
            sys.exit("Data slice metalabels inexistent, run gen_subslice_metalabels before perform_metatrade_run")

        from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v4 import Tradebot_v4

        tradebot = Tradebot_v4(daily_values=self.subslice_data_selection,
                               trade_signal=self.metalabels,
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
        return "Data slice: Ticker - " + self.ticker + ", Current start_date - " + self.start_date + ", Slice size: " + str(self.subslice_size)


class address_sim:
    def __init__(self):
        pass
