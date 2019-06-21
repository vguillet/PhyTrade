"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice
"""
from Settings.Model_settings import Model_settings
from Settings.Metalabeling_settings import Metalabeling_settings

from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis


class RUN_model:
    def __init__(self):
        # ~~~~~~~~~~~~~~~~ Dev options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Fetch run_model settings
        model_settings = Model_settings()
        model_settings.gen_run_model_settings()

        print_trade_process = model_settings.print_trade_process

        eval_name = model_settings.evaluation_name
        ticker = model_settings.ticker
        parameter_set = model_settings.parameter_set

        start_date = model_settings.start_date
        data_slice_size = model_settings.data_slice_size

        # ---- Fetch metalabeling settings
        metalabels_settings = Metalabeling_settings()
        metalabels_settings.gen_metalabels_settings()

        metalabeling_setting = metalabels_settings.metalabeling_setting

        upper_barrier = metalabels_settings.upper_barrier
        lower_barrier = metalabels_settings
        look_ahead = metalabels_settings.look_ahead

        # ---- Initiate run parameters
        self.ticker = ticker
        self.parameter_set = parameter_set

        # ---- Generate data slice
        self.data_slice = data_slice(self.ticker, start_date, data_slice_size, 0, data_selection="Close")
        self.data_slice.gen_slice_metalabels(upper_barrier, lower_barrier, look_ahead,
                                             metalabeling_setting)
        self.data_slice.perform_trade_run()

        # ---- Generate Individual
        self.individual = Individual(ticker=ticker, parameter_set=parameter_set)

        # ===============================================================================
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Model generation\n")

        print("Evaluated ticker:", ticker)
        print("\nStart date:", self.data_slice.start_date)
        print("\nStop date:", self.data_slice.stop_date)
        print("Data slice size:", data_slice_size)

        print("\nStarting parameters:", parameter_set)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ ECONOMIC ANALYSIS ================================
        # ---- Generate economic model and perform trade run
        self.individual.gen_economic_model(self.data_slice, plot_eco_model_results=True)
        self.individual.perform_trade_run(self.data_slice, print_trade_process=print_trade_process)

        # ---- Generate evaluation summary
        self.results = EVAL_parameter_set_results_gen(eval_name)
        self.results.benchmark_confusion_matrix_analysis = \
            Confusion_matrix_analysis(self.individual.trade_signal,
                                      self.data_slice.metalabels,
                                      calculate_stats=True,
                                      print_benchmark_results=False)

        self.results.individual = self.individual
        self.results.total_data_points_processed = self.data_slice.slice_size
        self.results.look_ahead = look_ahead
        self.results.benchmark_data_slice_start = self.data_slice.start_index
        self.results.benchmark_data_slice_stop = self.data_slice.stop_index

        self.results.gen_result_recap_file()

        print("-- Parameter evaluation completed --")


class EVAL_parameter_set_results_gen:
    def __init__(self, run_label):
        self.run_label = "Evaluation_" + run_label
        self.individual = None
        self.benchmark_confusion_matrix_analysis = None
        self.total_data_points_processed = None
        self.look_ahead = None

        self.benchmark_data_slice_start = None
        self.benchmark_data_slice_stop = None

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\RUN_model_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n-----------> Model settings:" + "\n")
        self.results_file.write("Ticker: " + str(self.individual.ticker) + "\n")

        self.results_file.write("\n-----------> Metalabeling settings:" + "\n")
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
