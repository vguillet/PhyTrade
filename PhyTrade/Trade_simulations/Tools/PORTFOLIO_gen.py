from PhyTrade.Trade_simulations.Trading_bots.Tradebot_v5 import Tradebot_v5
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.DATA_SLICE_gen import data_slice


class PORTFOLIO_gen:
    def __init__(self, tickers, parameter_sets,
                 start_date, data_slice_size,
                 upper_barrier, lower_barrier, look_ahead):

        # ---- Initiate Portfolio parameters
        self.tickers = tickers
        self.content = {}
        for i in range(len(tickers)):
            self.create_content_entry(tickers[i], parameter_sets[i])

        # ---- Generate initial data slices
        for ticker in self.content.keys():
            self.content[ticker]["Data_slice"] = data_slice(ticker, start_date, data_slice_size, 0,
                                                            upper_barrier, lower_barrier, look_ahead)

        # ---- Generate initial economic models
        for ticker in self.content.keys():
            self.content[ticker]["Individual"].gen_economic_model(self.content[ticker]["Data_slice"])

        # ---- Initiate counters
        self.data_slice_length = self.content[self.tickers[0]]["Data_slice"].slice_size

    def get_next_data_slices_and_economic_models(self):
        for ticker in self.content.keys():
            # --> Get next data slice
            self.content[ticker]["Data_slice"].get_next_data_slice()

            # --> Gen next economic model
            self.content[ticker]["Individual"].gen_economic_model(self.content[ticker]["Data_slice"])

            # --> Update counter
            self.data_slice_length = self.content[self.tickers[0]]["Data_slice"].slice_size

    def perform_trade_run(self,
                          investment_settings=3, cash_in_settings=0,
                          initial_funds=1000,
                          initial_orders=0,
                          prev_stop_loss=0.85, max_stop_loss=0.75,
                          max_investment_per_trade=500,
                          run_metalabels=False,
                          prev_simple_investment_orders=None,
                          print_trade_process=False):

        tradebot = Tradebot_v5(initial_funds, initial_orders, prev_simple_investment_orders,
                               prev_stop_loss, max_stop_loss,
                               print_trade_process)

        # --> For every day in current data slice
        for i in range(self.data_slice_length):
            sell_orders = []
            hold_orders = []
            buy_orders = []

            # --> Classify tickers based on trade signal
            for ticker in self.content.keys():
                if self.content[ticker]["Individual"].analysis.big_data.Major_spline.trade_signal[i] == 1:
                    sell_orders.append(ticker)

                elif self.content[ticker]["Individual"].analysis.big_data.Major_spline.trade_signal[i] == 0:
                    hold_orders.append(ticker)

                elif self.content[ticker]["Individual"].analysis.big_data.Major_spline.trade_signal[i] == -1:
                    buy_orders.append(ticker)

            order_lst = [sell_orders, hold_orders, buy_orders]

            # TODO: finish order orders
            # --> Reorder tickers based on signal strength
            for orders in order_lst:
                for j in range(1, len(orders)-1):
                    if abs(self.content[self.content.keys()[-1]]["Individual"].analysis.big_data.Major_spline.spline[i]) > \
                            abs(orders[j-1].analysis.big_data.Major_spline.spline[i]):
                        orders[j], orders[j-1] = orders[j-1], orders[j]
                for j in range(len(orders)):
                    print("Order")
                    print(orders[j].analysis.big_data.Major_spline.spline[i])

    def create_content_entry(self, ticker, parameter_set):
        """
        Used to add ticker entry to portfolio content

        :param ticker: Traded ticker
        :param parameter_set: Parameter set
        """
        self.content[ticker] = {}
        self.content[ticker]["Individual"] = Individual(ticker, parameter_set)
        self.content[ticker]["Data_slice"] = None

