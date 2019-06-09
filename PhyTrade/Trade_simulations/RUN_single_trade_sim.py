"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice

Input that still require manual input:
    - Metalabels settings
    - Investment settings
    - Stop-loss settings
"""

from SETTINGS import SETTINGS
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_tools import EVOA_tools


class RUN_single_trade_sim:
    def __init__(self):

        # ~~~~~~~~~~~~~~~~ Dev options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Fetch single_trade_sim settings
        settings = SETTINGS()
        settings.gen_single_trade_sim()

        # --> Simulation parameters
        eval_name = settings.simulation_name

        ticker = settings.ticker
        parameter_set = settings.parameter_set

        start_date = settings.start_date
        data_slice_size = settings.data_slice_size
        nb_data_slices = settings.nb_data_slices

        # --> Print parameters
        plot_signal = settings.plot_signal
        print_trade_process = settings.print_trade_process

        # --> Metalabeling settings
        self.run_metalabels = settings.run_metalabels         # Can be switched off for performance increase

        self.upper_barrier = settings.upper_barrier
        self.lower_barrier = settings.lower_barrier
        self.look_ahead = settings.look_ahead

        self.m_investment_settings = settings.m_investment_settings
        self.m_cash_in_settings = settings.m_cash_in_settings

        # --> Investment settings
        self.investment_settings = settings.investment_settings
        self.cash_in_settings = settings.cash_in_settings

        max_investment_per_trade_percent = settings.max_investment_per_trade_percent
        min_investment_per_trade_percent = settings.min_investment_per_trade_percent

        investment_per_trade_decay_function = settings.investment_per_trade_decay_function

        # --> Stop-loss settings
        max_prev_stop_loss = settings.max_prev_stop_loss
        min_prev_stop_loss = settings.min_prev_stop_loss

        prev_stop_loss_decay_function = settings.prev_stop_loss_decay_function

        max_max_stop_loss = settings.max_max_stop_loss
        min_max_stop_loss = settings.min_max_stop_loss

        max_stop_loss_decay_function = settings.max_stop_loss_decay_function

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # ---- Initiate run parameters
        self.ticker = ticker
        self.parameter_set = parameter_set

        self.nb_data_slices = nb_data_slices

        # ---- Initiate records
        self.results = Trade_simulation_results_gen(eval_name)

        # ===============================================================================
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Trade simulation \n")

        print("Evaluated ticker:", ticker)
        print("\nStart date:", start_date)
        print("Data slice size:", data_slice_size)
        print("Number of data slices processed:", nb_data_slices)
        print("\nStarting parameters:", parameter_set)

        print("\nInvestment_settings =", self.investment_settings)
        print("Cash-in settings =", self.cash_in_settings)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ TRADING SIMULATION ===============================

        # ---- Generate data slice
        self.data_slice = data_slice(self.ticker, start_date, data_slice_size, 0,
                                     self.upper_barrier, self.lower_barrier, self.look_ahead,
                                     data_looper=False)
        self.data_slice.gen_slice_metalabels()

        if self.run_metalabels is True:
            self.data_slice.perform_trade_run(investment_settings=self.m_investment_settings,
                                              cash_in_settings=self.m_cash_in_settings,
                                              print_trade_process=print_trade_process)
            self.results.metalabel_net_worth = self.data_slice.metalabels_account.net_worth_history

        # ---- Generate Individual
        self.individual = Individual(ticker=self.ticker, parameter_set=parameter_set)

        # ---- Perform initial evaluation
        self.individual.gen_economic_model(self.data_slice, plot_3=plot_signal)
        self.individual.perform_trade_run(self.data_slice,
                                          investment_settings=self.investment_settings, cash_in_settings=self.cash_in_settings,
                                          prev_stop_loss=max_prev_stop_loss, max_stop_loss=max_max_stop_loss,
                                          print_trade_process=print_trade_process)

        # --> Record slice trade history
        self.results.buy_count += self.individual.tradebot.buy_count
        self.results.sell_count += self.individual.tradebot.sell_count
        self.results.stop_loss_count += self.individual.tradebot.stop_loss_count

        self.results.profit.append((self.individual.account.net_worth_history[-1] - 1000)/1000*100)

        self.results.net_worth = self.individual.account.net_worth_history
        self.results.funds = self.individual.account.funds_history
        self.results.assets = self.individual.account.assets_history

        self.results.simple_investment = self.individual.account.simple_investment_net_worth

        # ---- Generate economic model and perform trade run for all data slices
        for i in range(nb_data_slices-1):
            print("================== Data slice", i+1, "==================")
            # --> Calc new data slice parameters
            self.data_slice.get_next_data_slice()

            print(self.data_slice.start_date, "-->", self.data_slice.stop_date)
            print("Net worth =", round(self.results.net_worth[-1]), "$; Simple investment worth=", self.results.simple_investment[-1])
            print("Buy count:", self.individual.tradebot.buy_count,
                  "; Sell count:", self.individual.tradebot.sell_count,
                  "; Stop loss count:", self.individual.tradebot.stop_loss_count)

            if self.data_slice.end_of_dataset is True:
                break

            # --> Throttle values
            self.prev_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                              max_prev_stop_loss, min_prev_stop_loss,
                                                              decay_function=prev_stop_loss_decay_function), 3)
            print("\nPrev stop loss", self.prev_stop_loss)

            self.max_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                             max_max_stop_loss, min_max_stop_loss,
                                                             decay_function=max_stop_loss_decay_function), 3)
            print("Max stop loss", self.max_stop_loss, "\n")

            self.max_investment_per_trade = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                        max_investment_per_trade_percent, min_investment_per_trade_percent,
                                                                        decay_function=investment_per_trade_decay_function), 3)
            print("Max investment per trade", self.max_investment_per_trade, "\n")

            # --> Process slice metalabels
            if self.run_metalabels is True:
                self.data_slice.perform_trade_run(investment_settings=self.m_investment_settings,
                                                  cash_in_settings=self.m_cash_in_settings,
                                                  initial_funds=self.individual.account.current_funds,
                                                  initial_assets=self.individual.account.current_assets,
                                                  prev_stop_loss=self.prev_stop_loss, max_stop_loss=self.max_stop_loss,
                                                  max_investment_per_trade=self.max_investment_per_trade*self.individual.account.net_worth_history[-1],
                                                  prev_simple_investment_assets=self.individual.account.simple_investment_assets,
                                                  print_trade_process=print_trade_process)
                self.results.metalabel_net_worth += self.data_slice.metalabels_account.net_worth_history

            # --> Process slice
            self.individual.gen_economic_model(self.data_slice, plot_3=plot_signal)
            self.individual.perform_trade_run(self.data_slice,
                                              investment_settings=self.investment_settings, cash_in_settings=self.cash_in_settings,
                                              initial_funds=self.individual.account.current_funds,
                                              initial_assets=self.individual.account.current_assets,
                                              prev_stop_loss=self.prev_stop_loss, max_stop_loss=self.max_stop_loss,
                                              max_investment_per_trade=self.max_investment_per_trade*self.individual.account.net_worth_history[-1],
                                              prev_simple_investment_assets=self.individual.account.simple_investment_assets,
                                              print_trade_process=print_trade_process)

            # --> Record slice trade history
            self.results.buy_count += self.individual.tradebot.buy_count
            self.results.sell_count += self.individual.tradebot.sell_count
            self.results.stop_loss_count += self.individual.tradebot.stop_loss_count

            self.results.profit.append((self.individual.account.net_worth_history[-1]-self.results.net_worth[-1])/self.results.net_worth[-1]*100)

            self.results.net_worth += self.individual.account.net_worth_history
            self.results.funds += self.individual.account.funds_history
            self.results.assets += self.individual.account.assets_history

            self.results.simple_investment += self.individual.account.simple_investment_net_worth

        # ---- Generate simulation summary
        self.results.ticker = self.ticker
        self.results.individual = self.individual
        self.parameter_set = self.parameter_set

        self.results.data_slice_start = self.data_slice.default_start_slice_index
        self.results.data_slice_size = self.data_slice.slice_size
        self.results.nb_data_slices = self.nb_data_slices

        self.results.total_data_points_processed = self.data_slice.slice_size*self.nb_data_slices

        self.results.gen_result_recap_file()
        self.results.plot_results(self.run_metalabels)

        print("-- Trade simulation completed --")
        print("Number of data points processed:", self.results.total_data_points_processed)


class Trade_simulation_results_gen:
    def __init__(self, run_label):
        self.run_label = "Trade_simulation_" + run_label

        self.ticker = None
        self.individual = None
        self.parameter_set = None

        self.data_slice_start = None
        self.data_slice_size = None
        self.nb_data_slices = None

        self.total_data_points_processed = None
        self.buy_count = 0
        self.sell_count = 0
        self.stop_loss_count = 0

        self.net_worth = None
        self.profit = []
        self.funds = None
        self.assets = None

        self.simple_investment = None
        self.metalabel_net_worth = None

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\RUN_trade_sim_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n-----------> Model settings:" + "\n")
        self.results_file.write("Ticker: " + str(self.individual.ticker) + "\n")
        self.results_file.write("\ndata_slice_start_index = " + str(self.data_slice_start) + "\n")
        self.results_file.write("data_slice_size = " + str(self.data_slice_size) + "\n")
        self.results_file.write("nb_data_slices = " + str(self.nb_data_slices) + "\n")
        self.results_file.write("Model parameters: " + str(self.parameter_set) + "\n")

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

