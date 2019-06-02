from PhyTrade.Tools.INDIVIDUAL_gen import Individual


class PORTFOLIO_gen:
    def __init__(self, tickers, parameter_sets, data_slice):

        self.tickers = tickers
        self.parameter_sets = parameter_sets
        self.data_slice = data_slice

        self.individuals = []
        for i in range(len(self.tickers)):
            self.individuals.append(Individual(self.tickers[i], self.parameter_sets[i]))

    def gen_economic_models(self):
        for individual in self.individuals:
            individual.gen_economic_model(self.data_slice)

    def perform_trade_run(self,
                          investment_settings=3, cash_in_settings=0,
                          initial_funds=1000,
                          initial_assets=0,
                          prev_stop_loss=0.85, max_stop_loss=0.75,
                          max_investment_per_trade=500,
                          prev_simple_investment_assets=None,
                          print_trade_process=False):

        for i in range(len(self.data_slice.slice_size)):
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
                    print(orders[j].analysis.big_data.Major_spline.spline[i])

