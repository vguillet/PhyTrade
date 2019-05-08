"""
This class contains the results_gen class, used to generate results form the various runs
"""

import time


class EVOA_results_gen:
    def __init__(self, individual, benchmark_fitness, benchmark_matrix, config, run_label, run_start_time, run_stop_time, total_data_points_processed):
        self.individual = individual

        self.benchmark_fitness = benchmark_fitness
        self.benchmark_matrix = benchmark_matrix

        self.config = config
        self.run_label = run_label

        self.run_start_time = run_start_time
        self.run_stop_time = run_stop_time

        self.total_data_points_processed = total_data_points_processed

    def gen_result_file(self):
        # -- Create results file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\PhyTrade\ML_optimisations\EVOA_Optimisation\EVOA_results".replace('\\', '/')
        full_file_name = path + '/' + self.run_label

        self.results_file = open(full_file_name + ".txt", "w+")

        print("Net worth:", self.individual.account.net_worth_history[-1])

        self.results_file.write("====================== " + self.run_label + " ======================\n")
        self.results_file.write("\n~~~~~~~~~~~ Run configuration recap: ~~~~~~~~~~~\n")

        self.results_file.write("-----------> EVO_algo main parameters:" + "\n")
        self.results_file.write("population_size = " + str(self.config.population_size) + "\n")
        self.results_file.write("nb_of_generations = " + str(self.config.nb_of_generations) + "\n\n")

        self.results_file.write("mutation_rate = " + str(self.config.mutation_rate) + "\n")
        self.results_file.write("nb_parents = " + str(self.config.nb_parents) + "\n")
        self.results_file.write("nb_random_ind = " + str(self.config.nb_random_ind) + "\n\n")

        self.results_file.write("exploitation_phase_len_percent = " + str(self.config.exploitation_phase_len_percent) + "\n\n")

        self.results_file.write("data_slice_start_index = " + str(self.config.data_slice_start_index) + "\n")
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
        # self.results_file.write("Start time:" + run_start_time.strftime('%X %x %Z') + "\n")
        self.results_file.write("End time: " + time.strftime('%X %x %Z') + "\n")
        self.results_file.write("Run time: " + str(round(self.run_stop_time - self.run_start_time, 3)) + "s\n\n")

        self.results_file.write("Average computing time per generation: "
                                + str(round((self.run_stop_time - self.run_start_time)/self.config.nb_of_generations, 3)) + "s\n\n")

        self.results_file.write("Number of data points processed: " + str(self.total_data_points_processed) + "\n")

        self.results_file.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        self.results_file.write("-----------> Benchmark results: \n")
        self.results_file.write("Fitness achieved: " + str(benchmark_fitness) + "\n")

        self.results_file.write(str() + "\n")
        self.results_file.close()

