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
        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 10

        # --> Investment settings
        self.investment_settings = 3
        self.cash_in_settings = 2

        self.initial_investment = 1000

        # Max --> Min
        max_investment_per_trade_percent = 0.1
        min_investment_per_trade_percent = 0.000001

        investment_per_trade_decay_function = 1

        # --> Stop-loss settings
        # Account
        # Max --> Min
        max_account_prev_stop_loss = 0.85
        min_account_prev_stop_loss = 0.98

        account_prev_stop_loss_decay_function = 1

        # Max --> Min
        max_account_max_stop_loss = 0.75
        min_account_max_stop_loss = 0.95

        account_max_stop_loss_decay_function = 1

        # Ticker
        # Max --> Min
        max_ticker_prev_stop_loss = 0.80
        min_ticker_prev_stop_loss = 0.98

        ticker_prev_stop_loss_decay_function = 1

        # Max --> Min
        max_ticker_max_stop_loss = 0.70
        min_ticker_max_stop_loss = 0.95

        ticker_max_stop_loss_decay_function = 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Initiate run parameters
        self.portfolio = PORTFOLIO_gen(tickers, parameter_sets,
                                       start_date, data_slice_size,
                                       self.upper_barrier, self.lower_barrier, self.look_ahead,
                                       plot_signal=plot_signal)

        self.nb_data_slices = nb_data_slices

        # ---- Current param setup
        # Finance
        self.current_funds = self.initial_investment
        self.current_account_content = {}
        self.current_account_simple_investments_content = {}

        self.current_max_investment_per_trade = max_investment_per_trade_percent

        # Account stop-losses
        self.current_account_prev_stop_loss = max_account_prev_stop_loss
        self.current_account_max_stop_loss = max_account_max_stop_loss

        # Ticker stop-losses
        self.current_ticker_prev_stop_loss = max_ticker_prev_stop_loss
        self.current_ticker_max_stop_loss = max_ticker_max_stop_loss

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
                                             initial_funds=self.current_funds,
                                             initial_account_content=self.current_account_content,
                                             initial_account_simple_investment_content=self.current_account_simple_investments_content,
                                             account_prev_stop_loss=self.current_account_prev_stop_loss,
                                             account_max_stop_loss=self.current_account_max_stop_loss,
                                             ticker_prev_stop_loss=self.current_ticker_prev_stop_loss,
                                             ticker_max_stop_loss=self.current_ticker_max_stop_loss,
                                             max_investment_per_trade=self.current_funds * self.current_max_investment_per_trade,
                                             print_trade_process=print_trade_process)

            # ---- Record slice trade history
            # --> Record trade actions
            self.results.buy_count += self.portfolio.tradebot.buy_count
            self.results.sell_count += self.portfolio.tradebot.sell_count
            self.results.stop_loss_count += self.portfolio.tradebot.stop_loss_count

            # --> Record finance
            self.results.funds += self.portfolio.tradebot.account.funds_history
            self.results.net_worth += self.portfolio.tradebot.account.net_worth_history
            self.results.assets_worth += self.portfolio.tradebot.account.asset_worth_history

            self.results.profit.append((self.portfolio.tradebot.account.net_worth_history[-1]-self.results.net_worth[-1])/self.results.net_worth[-1]*100)

            # --> Update current parameters
            self.current_funds = self.portfolio.tradebot.account.current_funds
            self.current_account_content = self.portfolio.tradebot.account.content
            self.current_account_simple_investments_content = self.portfolio.tradebot.account.simple_investment_content

            # --> Print Data slice results
            print("--------------------------------------------------")
            print("Buy count:", self.portfolio.tradebot.buy_count,
                  "; Sell count:", self.portfolio.tradebot.sell_count,
                  "; Stop loss count:", self.portfolio.tradebot.stop_loss_count, "\n")

            self.portfolio.tradebot.account.print_account_status()

            print("--------------------------------------------------")

            # ---- Calc next data slice parameters
            self.ref_data_slice.get_next_data_slice()
            if self.ref_data_slice.end_of_dataset is True:
                break

            # --> Throttle values
            # Account stop-losses
            self.current_account_prev_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                              max_account_prev_stop_loss, min_account_prev_stop_loss,
                                                                              decay_function=account_prev_stop_loss_decay_function), 3)

            self.current_account_max_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                             max_account_max_stop_loss, min_account_max_stop_loss,
                                                                             decay_function=account_max_stop_loss_decay_function), 3)

            # Ticker stop-losses
            self.current_ticker_prev_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                             max_ticker_prev_stop_loss, min_ticker_prev_stop_loss,
                                                                             decay_function=ticker_prev_stop_loss_decay_function), 3)

            self.current_ticker_max_stop_loss = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                            max_ticker_max_stop_loss, min_ticker_max_stop_loss,
                                                                            decay_function=ticker_max_stop_loss_decay_function), 3)

            # Max investment per trade
            self.current_max_investment_per_trade = round(EVOA_tools().throttle(i, self.nb_data_slices,
                                                                                max_investment_per_trade_percent,
                                                                                min_investment_per_trade_percent,
                                                                                decay_function=investment_per_trade_decay_function), 3)

            # --> Print throttled values
            print("Account:")
            print("Prev stop loss", self.current_account_prev_stop_loss)
            print("Max stop loss", self.current_account_max_stop_loss)

            print("\nTickers:")
            print("Prev stop loss", self.current_ticker_prev_stop_loss)
            print("Max stop loss", self.current_ticker_max_stop_loss)

            print("Max investment percentage per trade", self.current_max_investment_per_trade*100, "%\n")

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
        self.results.plot_results()

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
        self.assets_worth = []

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

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write(str() + "\n")

        self.results_file.close()

    def plot_results(self):
        import matplotlib.pyplot as plt

        plt.plot(self.net_worth, label="Net worth")
        plt.plot(self.funds, label="Funds")
        plt.plot(self.assets_worth, label="Assets worth")

        plt.grid()
        plt.legend()

        plt.show()
        return

