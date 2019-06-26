"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice
"""
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.Progress_bar_tool import Progress_bar

from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Signal_optimisation.EVOA_optimisation.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis

import math


class RUN_model:
    def __init__(self):
        # ~~~~~~~~~~~~~~~~ Dev options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        settings = SETTINGS()
        
        # ---- Fetch market settings
        settings.market_settings.gen_market_settings()

        ticker = settings.market_settings.tickers[0]
        parameter_set = settings.market_settings.parameter_sets[0]

        start_date = settings.market_settings.testing_start_date
        end_date = settings.market_settings.testing_end_date
        data_slice_size = settings.market_settings.data_slice_size

        # ---- Fetch run_model settings
        settings.model_settings.gen_run_model_settings()

        eval_name = settings.model_settings.evaluation_name
        print_trade_process = settings.model_settings.print_trade_process

        # ---- Fetch metalabeling settings
        settings.metalabeling_settings.gen_metalabels_settings()

        metalabeling_setting = settings.metalabeling_settings.metalabeling_setting
        upper_barrier = settings.metalabeling_settings.upper_barrier
        lower_barrier = settings.metalabeling_settings
        look_ahead = settings.metalabeling_settings.look_ahead

        # ---- Initiate run parameters
        self.ticker = ticker
        self.parameter_set = parameter_set

        self.results = EVAL_parameter_set_results_gen(self.ticker, eval_name)

        # ---- Generate data slice
        self.data_slice = data_slice(self.ticker, start_date, data_slice_size, 0, end_date=end_date)

        # ---- Generate Individual
        self.individual = Individual(ticker=ticker, parameter_set=parameter_set)

        # ===============================================================================
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Model generation\n")

        print("Evaluated ticker:", ticker)
        print("\nStart date:", self.data_slice.start_date)
        print("Stop date:", self.data_slice.stop_date)
        print("Data slice size:", data_slice_size)

        print("\nStarting parameters:", parameter_set)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ ECONOMIC ANALYSIS ================================
        # ---- Generate economic model and perform trade run
        progress_bar = Progress_bar(math.ceil(abs(self.data_slice.default_start_index-self.data_slice.default_end_index)/data_slice_size)+1,
                                    label="Model being generated")
        data_slice_count = 0
        while self.data_slice.end_of_dataset is not True:
            data_slice_count += 1

            self.individual.gen_economic_model(self.data_slice, plot_eco_model_results=False)
            self.individual.perform_trade_run(self.data_slice, print_trade_process=print_trade_process)

            self.data_slice.gen_slice_metalabels(upper_barrier, lower_barrier, look_ahead,
                                                 metalabeling_setting)
            self.data_slice.perform_trade_run()

            # --> Record results
            self.results.spline += list(self.individual.spline)
            self.results.trade_signal += list(self.individual.trade_signal)
            self.results.upper_threshold_spline += list(self.individual.analysis.big_data.Major_spline.upper_threshold)
            self.results.lower_threshold_spline += list(self.individual.analysis.big_data.Major_spline.lower_threshold)
            self.results.metalabels += list(self.data_slice.metalabels)

            # --> Generate next dataslice
            progress_bar.update_progress_bar(data_slice_count)
            self.data_slice.get_next_data_slice()

        # ---- Generate evaluation summary
        self.results.individual = self.individual
        self.results.benchmark_confusion_matrix_analysis = Confusion_matrix_analysis(self.results.trade_signal,
                                                                                     self.results.metalabels,
                                                                                     calculate_stats=True,
                                                                                     print_benchmark_results=False)

        self.results.upper_barrier = upper_barrier
        self.results.lower_barrier = lower_barrier
        self.results.look_ahead = look_ahead

        self.results.total_data_points_processed = abs(self.data_slice.default_start_index-self.data_slice.default_end_index)
        self.results.benchmark_data_slice_start = self.data_slice.default_start_date
        self.results.benchmark_data_slice_stop = self.data_slice.default_end_date

        self.results.gen_result_recap_file()

        print("-- Parameter evaluation completed --")
        self.results.plot_results()


class EVAL_parameter_set_results_gen:
    def __init__(self, ticker, run_label):
        self.run_label = "Evaluation_" + run_label

        self.ticker = ticker
        self.individual = None
        self.benchmark_confusion_matrix_analysis = None

        self.upper_barrier = None
        self.lower_barrier = None
        self.look_ahead = None

        self.spline = []
        self.trade_signal = []
        self.upper_threshold_spline = []
        self.lower_threshold_spline = []
        self.metalabels = []

        self.total_data_points_processed = None
        self.benchmark_data_slice_start = None
        self.benchmark_data_slice_stop = None

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\RUN_model_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n-----------> Model settings:" + "\n")
        self.results_file.write("Ticker: " + str(self.individual.ticker) + "\n")

        self.results_file.write("\n-----------> Metalabeling settings:" + "\n")
        self.results_file.write("upper_barrier = " + str(self.upper_barrier))
        self.results_file.write("lower_barrier = " + str(self.lower_barrier))
        self.results_file.write("look_ahead = " + str(self.look_ahead) + "\n")

        self.results_file.write("\n-----------> Benchmarking data slice settings:" + "\n")
        self.results_file.write("benchmark_data_slice_start = " + str(self.benchmark_data_slice_start) + "\n")
        self.results_file.write("benchmark_data_slice_stop = " + str(self.benchmark_data_slice_stop) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("\nNumber of data points processed: " + str(self.total_data_points_processed) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("-----------> Validation benchmark results: \n")
        self.results_file.write("---> Net worth: \n")
        self.results_file.write("Net worth achieved: " + str(self.individual.account.net_worth_history[-1]) + "\n")

        self.results_file.write("\n---> Fitness: \n")
        self.results_file.write("Fitness achieved: " + str(self.benchmark_confusion_matrix_analysis.overall_accuracy) + "\n")
        self.results_file.write("\nConfusion Matrix: \n" + self.benchmark_confusion_matrix_analysis.confusion_matrix.to_string() + "\n")

        self.results_file.write("\n-----------> Benchmark Confusion tables: \n")

        self.results_file.write("\nReference Confusion Table: \n" +
                                self.benchmark_confusion_matrix_analysis.confusion_table_ref.to_string() + "\n")

        self.results_file.write("\n-----------> Sell classification results: \n")
        self.results_file.write("\nSell Confusion Table: \n" +
                                self.benchmark_confusion_matrix_analysis.confusion_table_sell.to_string() + "\n\n")

        for key in self.benchmark_confusion_matrix_analysis.sell_stats:
            self.results_file.write(str(key) + " = " + str(round(self.benchmark_confusion_matrix_analysis.sell_stats[key], 3)) + "\n")

        self.results_file.write("\n-----------> Buy classification results: \n")
        self.results_file.write("\nBuy Confusion Table: \n" +
                                self.benchmark_confusion_matrix_analysis.confusion_table_buy.to_string() + "\n\n")

        for key in self.benchmark_confusion_matrix_analysis.buy_stats:
            self.results_file.write(str(key) + " = " + str(round(self.benchmark_confusion_matrix_analysis.buy_stats[key], 3)) + "\n")

        self.results_file.write("\n-----------> Hold classification results: \n")
        self.results_file.write("\nHold Confusion Table: \n" +
                                self.benchmark_confusion_matrix_analysis.confusion_table_hold.to_string() + "\n\n")

        for key in self.benchmark_confusion_matrix_analysis.hold_stats:
            self.results_file.write(str(key) + " = " + str(round(self.benchmark_confusion_matrix_analysis.hold_stats[key], 3)) + "\n")

        self.results_file.write(str() + "\n")

        self.results_file.close()
        return

    def plot_results(self):
        from PhyTrade.Tools.PLOT_tools import PLOT_tools
        print_data_slice = data_slice(self.ticker, self.benchmark_data_slice_start, self.total_data_points_processed, 0)
        PLOT_tools().plot_trade_process(print_data_slice,
                                        self.spline,
                                        self.upper_threshold_spline,
                                        self.lower_threshold_spline,
                                        self.trade_signal)
