from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.DATA_SLICE_gen import data_slice


class PORTFOLIO_gen:
    def __init__(self, tickers, parameter_sets,
                 start_date, data_slice_size,
                 upper_barrier, lower_barrier, look_ahead):

        # ---- Initiate Portfolio parameters
        self.tickers = tickers
        self.parameter_sets = parameter_sets

        # ---- Generate data slices
        self.data_slices = []

        for ticker in tickers:
            self.data_slices.append(data_slice(ticker, start_date, data_slice_size, 0, upper_barrier, lower_barrier, look_ahead))

        # ---- Generate individuals and initial economic models
        self.individuals = []
        for i in range(len(self.tickers)):
            self.individuals.append(Individual(self.tickers[i], self.parameter_sets[i]))

        self.gen_economic_models()

    def get_next_data_slices(self):
        for i, individual in enumerate(self.individuals):
            individual.gen_economic_model(self.data_slices[i].get_next_data_slice())

    def gen_economic_models(self):
        for i, individual in enumerate(self.individuals):
            individual.gen_economic_model(self.data_slices[i])

    def perform_trade_run(self,
                          investment_settings=3, cash_in_settings=0,
                          initial_funds=1000,
                          initial_assets=0,
                          prev_stop_loss=0.85, max_stop_loss=0.75,
                          max_investment_per_trade=500,
                          run_metalabels=False,
                          prev_simple_investment_assets=None,
                          print_trade_process=False):

        for i in range(self.data_slices[0].slice_size):
            sell_orders = []
            hold_orders = []
            buy_orders = []

            for individual in self.individuals:

                if individual.analysis.big_data.Major_spline.trade_signal[i] == 1:
                    sell_orders.append(individual)
                elif individual.analysis.big_data.Major_spline.trade_signal[i] == 0:
                    hold_orders.append(individual)
                elif individual.analysis.big_data.Major_spline.trade_signal[i] == -1:
                    buy_orders.append(individual)

            order_lst = [sell_orders, buy_orders]

            for orders in order_lst:
                for j in range(1, len(orders)-1):
                    if abs(orders[j].analysis.big_data.Major_spline.spline[i]) > abs(orders[j-1].analysis.big_data.Major_spline.spline[i]):
                        orders[j], orders[j-1] = orders[j-1], orders[j]
                for j in range(len(orders)):
                    print("Order")
                    print(orders[j].analysis.big_data.Major_spline.spline[i])

