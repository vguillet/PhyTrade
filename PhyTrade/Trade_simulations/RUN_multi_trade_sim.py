"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice

Input that still require manual input:
    - Metalabels settings
    - Investment settings
    - Stop-loss settings
"""
from PhyTrade.Trade_simulations.Tools.PORTFOLIO_gen import PORTFOLIO_gen
from PhyTrade.ML_optimisation.EVOA_Optimisation.Tools.EVOA_tools import EVOA_tools
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
import sys


class RUN_trade_sim:
    def __init__(self, eval_name,
                 parameter_sets, tickers,
                 start_date, data_slice_size, nb_data_slices,
                 plot_signal=False,
                 print_trade_process=False):

        # ~~~~~~~~~~~~~~~~ Dev options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # --> Metalabeling settings
        self.run_metalabels = False         # Can be switched off for performance increase

        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 10

        self.m_investment_settings = 1
        self.m_cash_in_settings = 0

        # --> Investment settings
        self.investment_settings = 3
        self.cash_in_settings = 2

        self.initial_investment = 1000

        max_investment_per_trade_percent = 0.2
        min_investment_per_trade_percent = 0.01

        investment_per_trade_decay_function = 1

        # --> Stop-loss settings
        # Max --> Min
        max_prev_stop_loss = 0.85
        min_prev_stop_loss = 0.98

        prev_stop_loss_decay_function = 1

        # Max --> Min
        max_max_stop_loss = 0.75
        min_max_stop_loss = 0.95

        max_stop_loss_decay_function = 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Initiate run parameters
        self.portfolio = PORTFOLIO_gen(tickers, parameter_sets,
                                       start_date, data_slice_size,
                                       self.upper_barrier, self.lower_barrier, self.look_ahead)

        self.nb_data_slices = nb_data_slices

        # ---- Current param setup
        self.current_funds = self.initial_investment
        self.current_orders = []
        self.current_simple_investments_orders = []

        self.current_max_investment_per_trade = max_investment_per_trade_percent
        self.current_prev_stop_loss = max_prev_stop_loss
        self.current_max_stop_loss = max_max_stop_loss

        self.ref_data_slice = data_slice("AAPL", start_date, data_slice_size, 0, 0, 0, 0, False)

        # ---- Initiate records
        self.results = Trade_simulation_results_gen(eval_name)
        self.results.net_worth = [self.initial_investment]

        # ===============================================================================
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Multi ticker trade simulation \n")

        print("Evaluated tickers:", tickers)
        print("\nStart date:", start_date)
        print("Data slice size:", data_slice_size)
        print("Number of data slices processed:", nb_data_slices)
        print("\nStarting parameters:", parameter_sets)

        print("\nInvestment_settings =", self.investment_settings)
        print("Cash-in settings =", self.cash_in_settings)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ TRADING SIMULATION ===============================
        # ---- Generate economic model and perform trade run for all data slices
        for i in range(nb_data_slices-1):
            print("================== Data slice", i+1, "==================")
            print(self.ref_data_slice.start_date, "-->", self.ref_data_slice.stop_date)
            # --> Perform trade run
            self.portfolio.perform_trade_run(investment_settings=self.investment_settings, cash_in_settings=self.cash_in_settings,
                                             initial_funds=self.current_funds, initial_orders=self.current_orders,
                                             prev_stop_loss=self.current_prev_stop_loss, max_stop_loss=self.current_max_stop_loss,
                                             max_investment_per_trade=self.current_max_investment_per_trade,
                                             prev_simple_investment_orders=self.current_simple_investments_orders,
                                             print_trade_process=print_trade_process)
            sys.exit()
            # --> Record slice trade history
            self.results.buy_count += self.portfolio.tradebot.buy_count
            self.results.sell_count += self.portfolio.tradebot.sell_count
            self.results.stop_loss_count += self.portfolio.tradebot.stop_loss_count

            self.results.profit.append((self.portfolio.tradebot.account.net_worth_history[-1]-self.results.net_worth[-1])/self.results.net_worth[-1]*100)

            self.results.net_worth += self.portfolio.tradebot.account.net_worth_history
            self.results.funds += self.portfolio.tradebot.account.funds_history
            self.results.assets += self.portfolio.tradebot.account.assets_history

            # --> Update current parameters
            self.current_funds = self.portfolio.tradebot.account.current_funds

            self.current_orders = []
            self.current_simple_investments_orders = []
            for ticker in self.portfolio.tradebot.account.content.keys():
                self.current_orders.append(self.portfolio.tradebot.account.content[ticker]["Open_orders"])
                self.current_simple_investments_orders.append(self.portfolio.tradebot.account.simple_investment_orders[ticker]["Order"])

            assert len(self.current_orders) == self.portfolio.tradebot.account.current_order_count

            print("Net worth =", round(self.results.net_worth[-1]), "$")
            print("Buy count:", self.portfolio.tradebot.buy_count,
                  "; Sell count:", self.portfolio.tradebot.sell_count,
                  "; Stop loss count:", self.portfolio.tradebot.stop_loss_count)
            self.portfolio.tradebot.account.print_account_status()

            # ---- Calc next data slice parameters
            self.ref_data_slice.get_next_data_slice()
            if self.ref_data_slice.end_of_dataset is True:
                break

            # --> Throttle values
            self.current_prev_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                      max_prev_stop_loss, min_prev_stop_loss,
                                                                      decay_function=prev_stop_loss_decay_function), 3)
            print("\nPrev stop loss", self.current_prev_stop_loss)

            self.current_max_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                     max_max_stop_loss, min_max_stop_loss,
                                                                     decay_function=max_stop_loss_decay_function), 3)
            print("Max stop loss", self.current_max_stop_loss, "\n")

            self.current_max_investment_per_trade = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                                max_investment_per_trade_percent,
                                                                                min_investment_per_trade_percent,
                                                                                decay_function=investment_per_trade_decay_function), 3)
            print("Max investment per trade", self.current_max_investment_per_trade, "\n")

            # --> Update account
            self.portfolio.get_next_data_slices_and_economic_models()

        # ---- Generate simulation summary
        self.results.tickers = tickers
        self.parameter_sets = parameter_sets

        self.results.data_slice_start = start_date
        self.results.data_slice_size = data_slice_size
        self.results.nb_data_slices = nb_data_slices

        # TODO: Fixed total_datapoint count
        self.results.total_data_points_processed = data_slice_size*nb_data_slices

        self.results.gen_result_recap_file()
        self.results.plot_results(self.run_metalabels)

        print("-- Trade simulation completed --")
        print("Number of data points processed:", self.results.total_data_points_processed)


class Trade_simulation_results_gen:
    def __init__(self, run_label):
        self.run_label = "Trade_simulation_" + run_label

        self.tickers = None
        self.parameter_sets = None

        self.data_slice_start = None
        self.data_slice_size = None
        self.nb_data_slices = None

        self.total_data_points_processed = None
        self.buy_count = 0
        self.sell_count = 0
        self.stop_loss_count = 0

        self.net_worth = None
        self.profit = []
        self.funds = []
        self.assets = []

        self.metalabel_net_worth = None

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\RUN_trade_sim_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n-----------> Model settings:" + "\n")
        self.results_file.write("Tickers: " + str(self.tickers) + "\n")
        self.results_file.write("\ndata_slice_start_index = " + str(self.data_slice_start) + "\n")
        self.results_file.write("data_slice_size = " + str(self.data_slice_size) + "\n")
        self.results_file.write("nb_data_slices = " + str(self.nb_data_slices) + "\n")
        self.results_file.write("Model parameters: " + str(self.parameter_sets) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.results_file.write("-----------> Run stats: \n")
        self.results_file.write("\nNumber of data points processed: " + str(self.total_data_points_processed) + "\n")
        self.results_file.write("Buy trigger count: " + str(self.buy_count) + "\n")
        self.results_file.write("Sell trigger count: " + str(self.sell_count) + "\n")

        self.results_file.write("\nFinal net worth: " + str(round(self.net_worth[-1])) + "$\n")
        self.results_file.write("Average profit per gen: " + str(round(sum(self.profit)/len(self.profit))) + "%\n")
        self.results_file.write("Max profit achieved: " + str(round(max(self.profit))) + "%\n")
        if min(self.profit) >= 0:
            self.results_file.write("Min profit achieved: " + str(round(min(self.profit))) + "%\n")
        else:
            self.results_file.write("Max loss achieved: " + str(round(min(self.profit))) + "%\n")

        self.results_file.write("\nSimple investment final net worth: " + str(round(self.simple_investment[-1])) + "$\n")
        self.results_file.write("Simple investment profit: " + str(round((self.simple_investment[-1]-1000)/1000*100)) + "%\n")

        self.results_file.write(
            "\n Net worth difference trading strategy vs simple investment: " + str(round(self.net_worth[-1]-self.simple_investment[-1])) + "$\n")
        self.results_file.write(
            "% Net worth difference trading strategy vs simple investment: " + str(round((self.net_worth[-1] - self.simple_investment[-1])/self.simple_investment[-1]*100)) + "%\n")
        # self.results_file.write("" + "\n")
        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write(str() + "\n")

        self.results_file.close()

    def plot_results(self, run_metalabels):
        import matplotlib.pyplot as plt

        plt.plot(self.net_worth, label="Net worth")
        plt.plot(self.funds, label="Funds")
        plt.plot(self.assets, label="Assets")
        plt.plot(self.simple_investment, label="Simple investment NW")

        if run_metalabels:
            plt.plot(self.metalabel_net_worth, label="Metalabels NW")

        plt.grid()
        plt.legend()

        plt.show()
        return

