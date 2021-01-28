
################################################################################################################
"""
Used for generating portfolio and storing portfolio information
"""

# Own modules
from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v5 import Tradebot_v5
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Data_Collection_preparation.Trading_dataslice import Trading_dataslice

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class PORTFOLIO_gen:
    def __init__(self, tickers, parameter_sets,
                 start_date, end_date, data_slice_size,
                 plot_eco_model_results=False):

        self.plot_eco_model_results = plot_eco_model_results

        # ---- Initiate Portfolio parameters
        self.tradebot = None
        self.tickers = tickers
        self.current_values = {}

        self.content = {}
        for i in range(len(tickers)):
            self.create_content_entry(tickers[i], parameter_sets[i])

        # ---- Generate initial data slices
        for ticker in self.content.keys():
            self.content[ticker]["Data_slice"] = Trading_dataslice(ticker, start_date, data_slice_size, 0, end_date=end_date)

        # ---- Generate initial economic models
        print("-- Generating initial economic models --")
        for ticker in self.content.keys():
            self.content[ticker]["Individual"].gen_economic_model(self.content[ticker]["Data_slice"],
                                                                  plot_eco_model_results=self.plot_eco_model_results)
            print(ticker, "model generated")
        print("")

        # ---- Initiate counters
        self.data_slice_length = self.content[self.tickers[0]]["Data_slice"].slice_size

    def get_next_data_slices_and_economic_models(self):
        print("-- Generating next data slices and economic models")
        for ticker in self.content.keys():
            # --> Get next data slice
            self.content[ticker]["Data_slice"].get_next_subslice()

            # --> Gen next economic model
            self.content[ticker]["Individual"].gen_economic_model(self.content[ticker]["Data_slice"],
                                                                  plot_eco_model_results=self.plot_eco_model_results)

            # --> Update counter
            print(ticker, "model generated")
        self.data_slice_length = self.content[self.tickers[0]]["Data_slice"].slice_size

    def perform_trade_run(self,
                          investment_settings=3, cash_in_settings=0,
                          initial_funds=1000,
                          initial_account_content={},
                          initial_account_simple_investment_content={},
                          account_prev_stop_loss=0.85, account_max_stop_loss=0.75,
                          ticker_prev_stop_loss=0.85,
                          max_investment_per_trade=50000,
                          print_trade_process=False):

        self.tradebot = Tradebot_v5(self.tickers,
                                    initial_funds=initial_funds,
                                    initial_account_content=initial_account_content,
                                    initial_account_simple_investment_content=initial_account_simple_investment_content,
                                    account_prev_stop_loss=account_prev_stop_loss, account_max_stop_loss=account_max_stop_loss,
                                    ticker_prev_stop_loss=ticker_prev_stop_loss,
                                    print_trade_process=print_trade_process)

        # --> For every day in current data slice
        for i in range(self.data_slice_length):
            # date = self.content[self.tickers[0]]["Data_slice"].data["index"][-self.content[self.tickers[0]]["Data_slice"].start_index + i + len(self.tickers[0]["Data_slice"].data["index"])]
            date = self.content[self.tickers[0]]["Data_slice"].subslice_data.iloc[i]['Date']

            # ---- Update account
            # --> Update current values
            for ticker in self.content.keys():
                self.current_values[ticker] = self.content[ticker]["Data_slice"].subslice_data_selection[i]

            # --> Update tradebot account
            self.tradebot.account.update_account(date, self.current_values)

            if print_trade_process:
                print("------------- Trade Date:", date, "-------------")

            sell_orders = []
            hold_orders = []
            buy_orders = []

            # --> Classify tickers based on trade signal
            for ticker in self.content.keys():
                if self.content[ticker]["Individual"].trade_signal[i] == 1:
                    sell_orders.append(ticker)

                elif self.content[ticker]["Individual"].trade_signal[i] == 0:
                    hold_orders.append(ticker)

                elif self.content[ticker]["Individual"].trade_signal[i] == -1:
                    buy_orders.append(ticker)

            order_lst = [sell_orders, hold_orders, buy_orders]

            # --> Reorder tickers based on signal strength
            for orders in order_lst:
                for k in range(len(orders)):
                    for j in range(1, len(orders)):
                        if abs(self.content[orders[j]]["Individual"].trade_spline[i]) > \
                                abs(self.content[orders[j-1]]["Individual"].trade_spline[i]):
                            orders[j], orders[j-1] = orders[j-1], orders[j]

            # --> Perform trade runs
            for orders in order_lst:
                if orders == buy_orders:
                    order_type = -1
                elif orders == hold_orders:
                    order_type = 0
                else:
                    order_type = 1

                for ticker in orders:
                    self.tradebot.perform_trade(ticker, order_type,
                                                investment_settings, max_investment_per_trade, cash_in_settings,
                                                self.content[ticker]["Individual"].trade_spline[i])

    def create_content_entry(self, ticker, parameter_set):
        """
        Used to add ticker entry to portfolio content

        :param ticker: Traded ticker
        :param parameter_set: Parameter set
        """
        # --> Create content entry
        self.content[ticker] = {}
        self.content[ticker]["Individual"] = Individual(ticker, parameter_set)
        self.content[ticker]["Data_slice"] = None

        # --> Create current_value entry
        self.current_values[ticker] = {}
