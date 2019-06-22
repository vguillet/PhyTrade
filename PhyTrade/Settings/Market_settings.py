import json


class Market_settings:
    def gen_market_settings(self):
        # ---- Market settings
        self.tickers = ["AAPL", "INTC", "NVDA", "AMZN"]
        self.ticker = "AAPL"

        self.parameter_set = json.load(open(r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\EVOA_results\Parameter_sets\Run_6_AAPL.json".replace('\\', '/')))
        # self.parameter_set = None

        self.parameter_sets = []
        # self.parameter_sets.append(json.load(open(
        #     r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_AAPL.json".replace(
        #         '\\', '/'))))
        # self.parameter_sets.append(json.load(open(
        #     r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_NVDA.json".replace(
        #         '\\', '/'))))
        # self.parameter_sets.append(json.load(open(
        #     r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_INTC.json".replace(
        #         '\\', '/'))))
        # self.parameter_sets.append(json.load(open(
        #     r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results\Parameter_sets\Run_5_AMZN.json".replace(
        #         '\\', '/'))))

        self.price_selection = "Open"
        # ---- Date settings
        # TODO: Add slice size auto scaling according to generation count/cycle count and start/end date
        self.start_date = "2017-01-03"
        self.end_date = "2019-01-02"
        # self.end_date = None

        self.data_slice_size = 24
