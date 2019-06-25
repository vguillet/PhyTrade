from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set
from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_sets
from Data.Company_data.Fetch_company_tickers import fetch_company_tickers
import sys


class Market_settings:
    def gen_market_settings(self):
        # ---- Market settings
        # --> Multi-ticker
        # self.tickers = fetch_company_tickers(0, 30)
        # for x in ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]:
        #     if x not in self.tickers:
        #         self.tickers.append(x)

        # self.tickers = ["AAPL", "INTC", "NVDA", "AMZN", "GOOGL", "MSFT", "FB", "CSCO", "ATVI", "ADSK"]
        self.tickers = ["AAPL"]

        # self.tickers, self.parameter_sets = fetch_parameter_sets(self.tickers, 6, "Short_term")

        self.price_selection = "Open"

        # ---- Date settings
        self.start_date = "2014-01-03"
        self.end_date = "2019-01-02"

        # self.start_date = "2019-01-02"
        # self.end_date = None

        self.data_slice_size = 253

        # ---- Broker settings
        self.min_transaction_cost = 1
        self.transaction_cost_per_share = 0.005
