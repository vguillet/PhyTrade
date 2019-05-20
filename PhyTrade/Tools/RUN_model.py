"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice
"""
from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info
from PhyTrade.ML_optimisation.EVOA_Optimisation.INDIVIDUAL_gen import Individual
from PhyTrade.Economic_model.Analysis_protocols_V.Prototype_3 import Prototype_3
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_benchmark_tool import Confusion_matrix_analysis


class RUN_model:
    def __init__(self, eval_name,
                 parameter_set, ticker,
                 data_slice_start, data_slice_size, look_ahead):

        self.parameter_set = parameter_set

        self.ticker = ticker
        self.data_slice_start = data_slice_start
        self.data_slice_size = data_slice_size
        self.look_ahead = look_ahead

        # ===============================================================================
        decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("EVOA_parameter_evaluation \n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # ---- Generate data slice
        self.data_slice = data_slice_info(self.data_slice_start, self.data_slice_size, 0, 0, 0, self.look_ahead)

        # ---- Generate Individual
        self.individual = Individual(ticker=ticker, parameter_set=parameter_set)

        # ---- Generate economic model and perform trade run
        self.individual.gen_economic_model(self.data_slice, plot_3=True)
        self.individual.perform_trade_run()

        # ---- Generate evaluation summary
        self.results = EVAL_parameter_set_results_gen(eval_name)
        self.results.benchmark_confusion_matrix_analysis = Confusion_matrix_analysis(self.individual.analysis.big_data.Major_spline.trade_signal,
                                                                                     self.data_slice.metalabels.close_values_metalabels,
                                                                                     calculate_stats=True,
                                                                                     print_benchmark_results=False)

        self.results.individual = self.individual
        self.results.total_data_points_processed = self.data_slice_size
        self.results.look_ahead = self.look_ahead
        self.results.benchmark_data_slice_start = self.data_slice_start
        self.results.benchmark_data_slice_stop = self.data_slice_start + self.data_slice_size

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
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVAL_parameter_set_results".replace('\\', '/')
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

