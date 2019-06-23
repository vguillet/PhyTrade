from PhyTrade.Data_Collection_preparation.Fetch_parameter_set import fetch_parameter_set


class Market_settings:
    def gen_market_settings(self):
        # ---- Market settings
        # self.tickers = ["AAPL", "INTC", "NVDA", "AMZN"]
        self.tickers = ["AAPL"]

        self.ticker = "AAPL"

        self.parameter_set = fetch_parameter_set(self.ticker, 6)
        # self.parameter_set = None

        self.parameter_sets = []
        for ticker in self.tickers:
            self.parameter_sets.append(fetch_parameter_set(ticker, 6))

        self.price_selection = "Open"
        # ---- Date settings
        # TODO: Add slice size auto scaling according to generation count/cycle count and start/end date
        self.start_date = "2017-01-03"
        self.end_date = "2018-03-02"
        # self.end_date = None

        self.data_slice_size = 24
