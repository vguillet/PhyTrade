
##################################################################################################################
"""
Contains the EVAL_parameter_set class, to be used for direct evaluation of a set of parameters over a specific data slice
"""

# Built-in/Generic Imports
import math

# Own modules
from PhyTrade.Settings.SETTINGS import SETTINGS
from PhyTrade.Tools.Progress_bar_tool import Progress_bar

from PhyTrade.Building_blocks.Trading_dataslice import Trading_dataslice
from PhyTrade.Building_blocks.Individual import Individual
from PhyTrade.Signal_optimisation.EVO_algorithm.Tools.EVOA_benchmark_tool import Confusion_matrix_analysis

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


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
        subslice_size = settings.market_settings.subslice_size

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

        # ---- Fetch individual settings
        settings.individual_settings.gen_individual_settings()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ---- Initiate run parameters
        self.ticker = ticker
        self.parameter_set = parameter_set

        self.results = EVAL_parameter_set_results_gen(ticker=self.ticker,
                                                      run_label=eval_name)

        # ---- Generate data slice
        self.data_slice = Trading_dataslice(ticker=self.ticker,
                                            start_date=start_date,
                                            subslice_size=subslice_size,
                                            subslice_shift_per_step=0,
                                            end_date=end_date)

        # ---- Generate Individual
        self.individual = Individual(parameter_set=parameter_set)

        # ===============================================================================
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Model generation\n")

        print("Evaluated ticker:", ticker)
        print("\nStart date:", self.data_slice.subslice_start_date)
        print("Stop date:", self.data_slice.subslice_stop_date)
        print("Data slice size:", subslice_size)

        print("\nStarting parameters:", parameter_set)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ============================ ECONOMIC ANALYSIS ================================
        # ---- Generate economic model and perform trade run
        progress_bar = Progress_bar(math.ceil(abs(self.data_slice.start_index-self.data_slice.end_index)/subslice_size)+1, label="Model being generated")
        data_slice_count = 0
        while self.data_slice.end_of_dataset is not True:
            data_slice_count += 1

            self.individual.gen_economic_model(data_slice=self.data_slice,
                                               plot_eco_model_results=False)

            self.individual.perform_trade_run(data_slice=self.data_slice,
                                              print_trade_process=print_trade_process)

            self.data_slice.gen_subslice_metalabels(upper_barrier=upper_barrier,
                                                    lower_barrier=lower_barrier,
                                                    look_ahead=look_ahead,
                                                    metalabeling_setting=metalabeling_setting)

            self.data_slice.perform_metatrade_run()

            # --> Record results
            self.results.trade_spline += list(self.individual.analysis.trade_spline)
            self.results.trade_signal += list(self.individual.analysis.trade_signal)
            self.results.trade_upper_threshold += list(self.individual.analysis.trade_upper_threshold)
            self.results.trade_lower_threshold += list(self.individual.analysis.trade_lower_threshold)
            self.results.metalabels += list(self.data_slice.metalabels)

            # --> Generate next dataslice
            progress_bar.update_progress(data_slice_count)
            self.data_slice.get_next_subslice()

        # ---- Generate evaluation summary
        self.results.individual = self.individual
        self.results.benchmark_confusion_matrix_analysis = Confusion_matrix_analysis(model_predictions=self.results.trade_signal,
                                                                                     metalabels=self.results.metalabels,
                                                                                     calculate_stats=True,
                                                                                     print_benchmark_results=False)

        self.results.upper_barrier = upper_barrier
        self.results.lower_barrier = lower_barrier
        self.results.look_ahead = look_ahead

        self.results.total_data_points_processed = abs(self.data_slice.start_index-self.data_slice.end_index)

        self.results.benchmark_data_slice_start = self.data_slice.start_date
        self.results.benchmark_data_slice_stop = self.data_slice.end_date

        self.results.gen_result_recap_file()

        print("-- Parameter evaluation completed --")

        if settings.model_settings.plot_eco_model_results:
            self.results.plot_results(settings=settings,
                                      big_data=self.individual.analysis)


class EVAL_parameter_set_results_gen:
    def __init__(self, ticker, run_label):
        self.run_label = "Evaluation_" + run_label

        self.ticker = ticker
        self.individual = None
        self.benchmark_confusion_matrix_analysis = None

        self.upper_barrier = None
        self.lower_barrier = None
        self.look_ahead = None

        self.trade_spline = []
        self.trade_signal = []
        self.trade_upper_threshold = []
        self.trade_lower_threshold = []
        self.metalabels = []

        self.total_data_points_processed = None
        self.benchmark_data_slice_start = None
        self.benchmark_data_slice_stop = None

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"Data\RUN_model_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n-----------> Model settings:" + "\n")
        self.results_file.write("Ticker: " + str(self.ticker) + "\n")

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

    def plot_results(self, settings, big_data):
        from PhyTrade.Tools.Plot_tools import Plot_tools

        # --> Creating plotting dataslice with subslice the size of the total data count processed
        plot_data_slice = Trading_dataslice(ticker=self.ticker,
                                            start_date=self.benchmark_data_slice_start,
                                            subslice_size=self.total_data_points_processed,
                                            subslice_shift_per_step=0)

        Plot_tools().plot_trade_process(settings=settings,
                                        data_slice=plot_data_slice,
                                        trade_spline=self.trade_spline,
                                        trade_upper_threshold=self.trade_upper_threshold,
                                        trade_lower_threshold=self.trade_lower_threshold,
                                        trade_signal=self.trade_signal,
                                        trading_indicators=big_data.content["trading_indicator_splines"])
