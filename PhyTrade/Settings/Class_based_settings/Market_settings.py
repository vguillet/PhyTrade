
##################################################################################################################
"""
Contains settings related to market, including tickers and dates
"""

# Own modules
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_sets
from Data.Company_data.Fetch_company_tickers import fetch_company_tickers

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Market_settings:
    def gen_market_settings(self):
        # ---- Market settings
        # --> Fetch tickers
        self.tickers = fetch_company_tickers(0, 100)
        for x in self.tickers:
            if x in ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]:
                self.tickers.remove(x)

        # for x in ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]:
        #     if x not in self.tickers:
        #         self.tickers.append(x)

        # self.tickers = ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]
        # self.tickers = ["AAPL", "GOOGL", "MSFT"]
        # self.tickers = ["AAPL"]

        # --> Fetch parameter sets
        # self.tickers, self.parameter_sets = fetch_parameter_sets(self.tickers, "10", "Short_term")
        self.price_selection = "Open"

        # ---- Date settings
        # DATES provided must have an interval at least equal to slice size!
        # --> Training dates
        self.training_start_date = "2016-01-04"
        self.training_end_date = "2019-06-03"

        # --> Testing dates
        self.testing_start_date = "2019-06-03"
        self.testing_end_date = "2019-07-10"

        self.data_slice_size = 25

        # ---- Broker settings
        self.min_transaction_cost = 1
        self.transaction_cost_per_share = 0.005
