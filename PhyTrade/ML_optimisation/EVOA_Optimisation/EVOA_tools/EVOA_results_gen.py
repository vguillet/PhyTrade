"""
This class contains the results_gen class, used to generate results form the various runs
"""

import time


class EVOA_results_gen:
    def __init__(self, config, run_label):
        self.config = config
        self.run_label = run_label

        self.individual = None

        self.benchmark_confusion_matrix_analysis = None

        self.run_start_time = None
        self.run_stop_time = None

        self.total_data_points_processed = None

    def gen_parameters_json(self):
        import json
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\PhyTrade\ML_optimisation\EVOA_Optimisation\EVOA_results".replace('\\', '/')
        file_name = path + '/' + self.run_label + ".csv"

        with open(file_name, 'w') as fout:
            json.dump(self.individual.parameter_dictionary, fout)
        print("Parameters recorded to ", file_name, " successfully")
        return

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\PhyTrade\ML_optimisation\EVOA_Optimisation\EVOA_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        print("Net worth:", self.individual.account.net_worth_history[-1])

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n~~~~~~~~~~~ Run configuration recap: ~~~~~~~~~~~\n")

        self.results_file.write("\nConfiguration file: " + self.config.config_name + "\n")

        self.results_file.write("\n-----------> EVO_algo main parameters:" + "\n")
        self.results_file.write("population_size = " + str(self.config.population_size) + "\n")
        self.results_file.write("nb_of_generations = " + str(self.config.nb_of_generations) + "\n")

        self.results_file.write("\nmutation_rate = " + str(self.config.mutation_rate) + "\n")
        self.results_file.write("nb_parents = " + str(self.config.nb_parents) + "\n")
        self.results_file.write("nb_random_ind = " + str(self.config.nb_random_ind) + "\n")

        self.results_file.write("\nexploitation_phase_len_percent = " + str(self.config.exploitation_phase_len_percent) + "\n")

        self.results_file.write("\ndata_slice_start_index = " + str(self.config.data_slice_start_index) + "\n")
        self.results_file.write("data_slice_size = " + str(self.config.data_slice_size) + "\n")
        self.results_file.write("data_slice_shift_per_gen = " + str(self.config.data_slice_shift_per_gen) + "\n")

        self.results_file.write("\n-----------> Metalabeling settings:" + "\n")
        self.results_file.write("upper_barrier = " + str(self.config.upper_barrier) + "\n")
        self.results_file.write("lower_barrier = " + str(self.config.lower_barrier) + "\n")
        self.results_file.write("look_ahead = " + str(self.config.look_ahead) + "\n")

        self.results_file.write("\n-----------> Benchmarking data slice settings:" + "\n")
        self.results_file.write("benchmark_data_slice_start = " + str(self.config.benchmark_data_slice_start) + "\n")
        self.results_file.write("benchmark_data_slice_stop = " + str(self.config.benchmark_data_slice_stop) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("-----------> Run stats: \n")
        # self.results_file.write("Start time:" + self.run_start_time.strftime('%X %x %Z') + "\n")
        self.results_file.write("End time: " + time.strftime('%X %x %Z') + "\n")
        self.results_file.write("Run time: " + str(round(self.run_stop_time - self.run_start_time, 3)) + "s\n")

        self.results_file.write("\nAverage computing time per generation: "
                                + str(round((self.run_stop_time - self.run_start_time)/self.config.nb_of_generations, 3)) + "s\n")

        self.results_file.write("\nNumber of data points processed: " + str(self.total_data_points_processed) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("-----------> Validation benchmark results: \n")
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

        print("EVOA run results summary successfully generated")
        self.results_file.close()

