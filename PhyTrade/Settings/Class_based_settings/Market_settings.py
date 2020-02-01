
##################################################################################################################
"""
Contains settings related to market, including tickers and dates
"""

# Own modules
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_sets
from Data.Company_data.Fetch_company_tickers import fetch_company_tickers
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set_labels_df import fetch_parameter_set_labels_df

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


class Market_settings:
    def gen_market_settings(self):
        # ---- Market settings
        # --> Fetch tickers
        current_tickers_df = fetch_parameter_set_labels_df(prints=False)

        # self.tickers = fetch_company_tickers(0, 60)
        # self.tickers = [x for x in self.tickers if x not in list(current_tickers_df[0].index)]

        # self.tickers = list(current_tickers_df[0].index)
        # self.tickers = ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]
        # self.tickers = ["AAPL", "GOOGL", "MSFT"]
        self.tickers = ["AAPL"]

        # --> Fetch parameter sets
        self.run_reference = 10
        self.term = "Short_term"
        self.tickers, self.parameter_sets = fetch_parameter_sets(self.tickers, str(self.run_reference), self.term)
        self.price_selection = "Open"

        # ---- Date settings
        # DATES provided must have an interval at least equal to slice size!
        # --> Training dates
        self.training_start_date = "2016-01-04"
        self.training_end_date = "2019-06-03"

        # --> Testing dates
        self.testing_start_date = "2019-06-03"
        self.testing_end_date = "2019-07-10"

        self.data_slice_size = 26

        # ---- Broker settings
        self.min_transaction_cost = 1
        self.transaction_cost_per_share = 0.005
