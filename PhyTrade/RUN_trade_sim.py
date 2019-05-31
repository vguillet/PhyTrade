"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice
"""
from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info
from PhyTrade.ML_optimisation.EVOA_Optimisation.INDIVIDUAL_gen import Individual
from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Fetch_technical_data import fetch_technical_data

import numpy as np


class RUN_trade_sim:
    def __init__(self, eval_name,
                 parameter_set, ticker,
                 start_date, data_slice_size, nb_data_slices,
                 plot_signal=False,
                 print_trade_process=False):

        self.ticker = ticker
        self.parameter_set = parameter_set

        self.data_slice_size = data_slice_size
        self.nb_data_slices = nb_data_slices

        # ---- Find corresponding data index from date
        data = fetch_technical_data(ticker)

        self.data_slice_start = -len(data)+np.flatnonzero(data['index'] == start_date)[0]

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
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ TRADING SIMULATION ===============================

        # ---- Generate data slice
        self.data_slice = data_slice_info(self.data_slice_start, self.data_slice_size, 0, 20, -20, 0, data_looper=False)
        self.data_slice.gen_slice_metalabels(ticker)
        self.data_slice.perform_trade_run(self.ticker)

        # ---- Generate Individual
        self.individual = Individual(ticker=self.ticker, parameter_set=parameter_set)

        # ---- Perform initial evaluation
        self.individual.gen_economic_model(self.data_slice, plot_3=plot_signal)
        self.individual.perform_trade_run(investment_settings=3, cash_in_settings=0,
                                          max_investment_per_trade=5000,
                                          print_trade_process=print_trade_process)

        # --> Record slice trade history
        self.results.buy_count += len(self.individual.analysis.big_data.Major_spline.buy_dates)
        self.results.sell_count += len(self.individual.analysis.big_data.Major_spline.sell_dates)

        self.results.net_worth = self.individual.account.net_worth_history
        self.results.funds = self.individual.account.funds_history
        self.results.assets = self.individual.account.assets_history

        self.results.simple_investment = self.individual.account.simple_investment_net_worth

        # ---- Generate economic model and perform trade run
        for i in range(nb_data_slices-1):
            print("================== Data slice", i+1, "==================")
            self.data_slice.get_next_data_slice(self.ticker)
            print(data.iloc[self.data_slice.start_index]['index'], "-->", data.iloc[self.data_slice.stop_index]['index'])

            if self.data_slice.end_of_dataset is True:
                break

            self.individual.gen_economic_model(self.data_slice, plot_3=plot_signal)
            self.individual.perform_trade_run(investment_settings=3, cash_in_settings=0,
                                              initial_funds=self.individual.account.current_funds,
                                              initial_assets=self.individual.account.current_assets,
                                              max_investment_per_trade=5000,
                                              prev_simple_investment_assets=self.individual.account.simple_investment_assets,
                                              print_trade_process=print_trade_process)

            # --> Record slice trade history
            self.results.buy_count += len(self.individual.analysis.big_data.Major_spline.buy_dates)
            self.results.sell_count += len(self.individual.analysis.big_data.Major_spline.sell_dates)
            self.results.profit.append((self.individual.account.net_worth_history[-1]-self.results.net_worth[-1])/self.results.net_worth[-1]*100)

            self.results.net_worth += self.individual.account.net_worth_history
            self.results.funds += self.individual.account.funds_history
            self.results.assets += self.individual.account.assets_history

            self.results.simple_investment += self.individual.account.simple_investment_net_worth

        # ---- Generate simulation summary
        self.results.ticker = self.ticker
        self.results.individual = self.individual
        self.parameter_set = self.parameter_set

        self.results.data_slice_start = self.data_slice_start
        self.results.data_slice_size = self.data_slice_size
        self.results.nb_data_slices = self.nb_data_slices

        self.results.total_data_points_processed = self.data_slice_size*self.nb_data_slices

        self.results.gen_result_recap_file()
        self.results.plot_results()

        print("-- Trade simulation completed --")
        print("Number of data points processed:", self.results.total_data_points_processed)
        print(self.results.simple_investment[-1])


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

        self.net_worth = None
        self.profit = []
        self.funds = None
        self.assets = None

        self.simple_investment = []

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

    def plot_results(self):
        import matplotlib.pyplot as plt

        plt.plot(self.net_worth, label="Net worth")
        plt.plot(self.funds, label="Funds")
        plt.plot(self.assets, label="Assets")
        plt.plot(self.simple_investment, label="Simple investment")

        plt.grid()
        plt.legend()

        plt.show()
        return

