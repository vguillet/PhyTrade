
##################################################################################################################
"""
Contains settings related to market, including tickers and dates
"""

# Built-in/Generic Imports
import json

# Own modules
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_sets

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Market_settings:
    def gen_market_settings(self):
        market_settings = json.load(open(r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings\Current_settings\Market_settings_.json"))

        # ---- Market settings
        self.tickers = market_settings["tickers"]

        # --> Fetch parameter sets
        self.tickers, self.parameter_sets = fetch_parameter_sets(self.tickers, market_settings["reference_label"], market_settings["reference_term"])
        self.price_selection = market_settings["price_selection"]

        # ---- Date settings
        # --> Training dates
        self.training_start_date = market_settings["training_start_date"]
        self.training_end_date = market_settings["training_stop_date"]

        # --> Testing dates
        self.testing_start_date = market_settings["testing_start_date"]
        self.testing_end_date = market_settings["testing_stop_date"]

        self.data_slice_size = market_settings["data_slice_size"]

        # ---- Broker settings
        self.min_transaction_cost = market_settings["min_transaction_cost"]
        self.transaction_cost_per_share = market_settings["transaction_cost_per_share"]
