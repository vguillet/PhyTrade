"""
This class contains the results_gen class, used to generate results form the various runs
"""

import time
from PhyTrade.Tools.MATH_tools import MATH


class EVOA_results_gen:
    def __init__(self, config, run_label):
        self.config = config
        self.run_label = run_label

        self.individual = None

        self.benchmark_confusion_matrix_analysis = None

        self.run_start_time = None
        self.run_stop_time = None

        self.total_data_points_processed = None

        self.best_individual_fitness_per_gen = []
        self.avg_fitness_per_gen = []

        self.best_individual_net_worth_per_gen = []
        self.avg_net_worth_per_gen = []

        self.data_slice_metalabel_pp = []

    def gen_stats(self):
        # ------------ Generating further informations
        # -------- Determine best fit lines
        # --> For average fitness
        a_avg_f, b_avg_f = MATH().best_fit(range(len(self.avg_fitness_per_gen)), self.avg_fitness_per_gen)
        self.gradient_bestfit_avg_f = b_avg_f
        self.yfit_avg_f = [a_avg_f + b_avg_f * xi for xi in range(len(self.avg_fitness_per_gen))]

        # --> For best fitness individual
        a_best_f, b_best_f = MATH().best_fit(range(len(self.best_individual_fitness_per_gen)), self.best_individual_fitness_per_gen)
        self.gradient_bestfit_best_f = b_best_f
        self.yfit_best_f = [a_best_f + b_best_f * xi for xi in range(len(self.avg_fitness_per_gen))]

        # --> For average net worth
        a_avg_nw, b_avg_nw = MATH().best_fit(range(len(self.avg_net_worth_per_gen)), self.avg_net_worth_per_gen)
        self.gradient_bestfit_avg_nw = b_avg_nw
        self.yfit_avg_nw = [a_avg_nw + b_avg_nw * xi for xi in range(len(self.avg_net_worth_per_gen))]

        # --> FOr best net worth individual
        a_best_nw, b_best_nw = MATH().best_fit(range(len(self.best_individual_net_worth_per_gen)), self.best_individual_net_worth_per_gen)
        self.gradient_bestfit_best_nw = b_best_nw
        self.yfit_best_nw = [a_best_nw + b_best_nw * xi for xi in range(len(self.best_individual_net_worth_per_gen))]


    def gen_parameters_json(self):
        import json
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results".replace('\\', '/')
        file_name = path + '/' + self.run_label + ".json"

        with open(file_name, 'w') as fout:
            json.dump(self.individual.parameter_dictionary, fout)
        print("Parameters recorded to ", file_name, " successfully")
        return

    def gen_result_recap_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\EVOA_results".replace('\\', '/')
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

        self.results_file.write("\nexploitation_phase_len_percent = " + str(self.config.exploitation_phase_len_percent*100) + "\n")

        self.results_file.write("\ndata_slice_start_index = " + str(self.config.data_slice_start_index) + "\n")
        self.results_file.write("data_slice_size = " + str(self.config.data_slice_size) + "\n")
        self.results_file.write("data_slice_shift_per_gen = " + str(self.config.data_slice_shift_per_gen) + "\n")

        self.results_file.write("\n-----------> Generations settings:" + "\n")
        self.results_file.write("Evaluation method: " + self.config.evaluation_methods[self.config.evaluation_method] + "\n")

        self.results_file.write("\nParents # decay function: " + self.config.decay_functions[self.config.parents_decay_function] + "\n")
        self.results_file.write("Random individual # decay function: " + self.config.decay_functions[self.config.parents_decay_function] + "\n")

        self.results_file.write("data_slice_size = " + str(self.config.data_slice_size) + "\n")

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

        self.results_file.write("\n-----------> Fitness results:" + "\n")
        self.results_file.write("Max average fitness achieved: " + str(max(self.avg_fitness_per_gen)) + "\n")
        self.results_file.write("Max individual fitness achieved: " + str(max(self.best_individual_fitness_per_gen)) + "\n")

        self.results_file.write("\nAverage fitness best fit line gradient achieved: " + str(self.gradient_bestfit_avg_f) + "\n")
        self.results_file.write("Individual fitness best fit line gradient achieved: " + str(self.gradient_bestfit_best_f) + "\n")

        self.results_file.write("\n-----------> Net Worth results:" + "\n")
        self.results_file.write("Max average net worth achieved: " + str(max(self.avg_net_worth_per_gen)) + "\n")
        self.results_file.write("Max individual net worth achieved: " + str(max(self.best_individual_net_worth_per_gen)) + "\n")

        self.results_file.write("\nAverage net worth best fit line gradient achieved: " + str(self.gradient_bestfit_avg_nw) + "\n")
        self.results_file.write("Individual net worth best fit line gradient achieved: " + str(self.gradient_bestfit_best_nw) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("-----------> Validation benchmark results: \n")
        self.results_file.write("Fitness achieved: " + str(self.benchmark_confusion_matrix_analysis.overall_accuracy) + "\n")
        self.results_file.write("Fitness achieved bs: " + str(self.benchmark_confusion_matrix_analysis.overall_accuracy_bs) + "\n")

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
        return

    def plot_results(self):
        import matplotlib.pyplot as plt

        # --> Fitness plot
        plt.plot(range(len(self.avg_fitness_per_gen)), self.avg_fitness_per_gen, label="Average fitness per gen")
        plt.plot(range(len(self.avg_fitness_per_gen)), self.yfit_avg_f, "k", dashes=[6, 2])

        plt.plot(range(len(self.best_individual_fitness_per_gen)), self.best_individual_fitness_per_gen, label="Best individual fitness per gen")
        plt.plot(range(len(self.best_individual_fitness_per_gen)), self.yfit_best_f, "k", dashes=[6, 2])

        plt.ylabel("Fitness %")
        plt.xlabel("Generation #")
        plt.legend()
        plt.grid()

        plt.show()

        # --> Net Worth plot
        plt.plot(range(len(self.avg_net_worth_per_gen)), self.avg_net_worth_per_gen, label="Average net worth per gen")
        plt.plot(range(len(self.avg_net_worth_per_gen)), self.yfit_avg_nw, "k", dashes=[6, 2])

        plt.plot(range(len(self.best_individual_net_worth_per_gen)), self.best_individual_net_worth_per_gen, label="Best individual net worth per gen")
        plt.plot(range(len(self.best_individual_net_worth_per_gen)), self.yfit_best_nw, "k", dashes=[6, 2])

        plt.ylabel("Net worth $")
        plt.xlabel("Generation #")
        plt.legend()
        plt.grid()

        plt.show()


