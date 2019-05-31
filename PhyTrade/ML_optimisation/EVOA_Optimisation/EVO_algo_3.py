"""
This script contains the EVOA_optimiser class, which is a refactored and optimised version of EVO_algo2
"""

from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_tools import EVOA_tools
from PhyTrade.ML_optimisation.EVOA_Optimisation.EVOA_tools.EVOA_results_gen import EVOA_results_gen
from PhyTrade.ML_optimisation.EVOA_Optimisation.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info

import time
import sys


class EVOA_optimiser:
    def __init__(self, config, ticker="AAPL"):

        # ======================== GA OPTIMISATION INITIALISATION =======================
        # ------------------ Tools and GA parameters initialisation
        # -- Initialise data slice for gen and metalabels
        self.data_slice_info = data_slice_info(config.data_slice_start_index,
                                               config.data_slice_size,
                                               config.data_slice_shift_per_gen,
                                               config.upper_barrier,
                                               config.lower_barrier,
                                               config.look_ahead)
        self.data_slice_info.gen_slice_metalabels(ticker)

        # -- Initialise benchmark data slice
        self.benchmark_data_slice = data_slice_info(config.benchmark_data_slice_start,
                                                    config.benchmark_data_slice_size,
                                                    0,
                                                    config.upper_barrier,
                                                    config.lower_barrier,
                                                    config.look_ahead)
        self.benchmark_data_slice.gen_slice_metalabels(ticker)

        # -- Initialise tools and counters
        self.evoa_tools = EVOA_tools()
        self.data_slice_cycle_count = 0

        self.nb_parents = None
        self.nb_random_ind = None

        # -- Initialise records
        self.results = EVOA_results_gen(config, config.config_name, ticker)

        # ===============================================================================
        decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("EVOA_v3 \n")

        print("Evaluated ticker:", ticker)
        self.results.run_start_time = time.time()
        print("Start time:", time.strftime('%X %x %Z'), "\n")
        print("Estimated run time:", (config.nb_of_generations*config.population_size*0.80 + config.nb_of_generations * 0.45), "minutes\n")

        print("-- Settings selected --")
        print("Selected evaluation method:", config.evaluation_methods[config.evaluation_method])
        print("")
        print("Selected parent function:", config.decay_functions[config.parents_decay_function])
        print("Selected random individual function:", config.decay_functions[config.random_ind_decay_function])
        print("Selected mutation range function:", config.decay_functions[config.mutation_decay_function])
        print("")
        print("Configuration sheet:", config.config_name)
        print("Starting parameters:", config.starting_parameters)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ========================= EVO OPTIMISATION PROCESS =============================
        # ------------------ Initialise population
        if config.starting_parameters is None:
            self.population = self.evoa_tools.gen_initial_population(ticker, config.population_size)
        else:
            self.population = self.evoa_tools.generate_offsprings(ticker,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  0,
                                                                  config.population_size,
                                                                  [Individual(parameter_set=config.starting_parameters)],
                                                                  config.nb_random_ind,
                                                                  mutation_rate=config.mutation_rate)

        print("\n---------------> Initial population generated successfully")

        # ------------------ Run for # nb of generations:
        for gen in range(config.nb_of_generations+1):
            print("\n==================================== Generation", gen, "====================================")
            generation_start_time = time.time()

            if gen == config.nb_of_generations-config.exploitation_phase_len-1:
                print("-------------> Exploration phase completed, starting exploitation phase <-------------")

            if gen != 0:
                # ------------------ Define the data slice to be used by the generation
                self.data_slice_cycle_count += 1
                if self.data_slice_cycle_count > config.data_slice_cycle_count:
                    # data_slice_info.get_next_data_slice(ticker)
                    self.data_slice_info.get_shifted_data_slice(ticker)

                    self.data_slice_cycle_count = 1

                print("Data slice analysed:", self.data_slice_info.start_index, "-->", self.data_slice_info.stop_index)
                print("Data slice analysis cycle:", self.data_slice_cycle_count, "\n")

                # ------------------ Determine new generation GA parameters
                print("---------------> Determining new generation parameters")
                self.nb_parents, self.nb_random_ind = \
                    self.evoa_tools.determine_evolving_gen_parameters(gen,
                                                                      self.data_slice_cycle_count,
                                                                      config,
                                                                      print_evoa_parameters_per_gen=config.print_evoa_parameters_per_gen)

                if sum(self.fitness_evaluation) != 0:
                    # ------------------ Select individuals from previous generation
                    print("---------------> Selecting individuals from previous generation")
                    # -- Exit program if incorrect settings used
                    if config.parents_decay_function > 1:
                        print("Invalid evaluation method reference")
                        sys.exit()

                    if config.evaluation_method == 0:
                        self.parents = self.evoa_tools.select_from_population(self.net_worth,
                                                                              self.population,
                                                                              selection_method=config.parents_selection_method,
                                                                              nb_parents=self.nb_parents)

                    elif config.evaluation_method == 1:
                        self.parents = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                              self.population,
                                                                              selection_method=config.parents_selection_method,
                                                                              nb_parents=self.nb_parents)

                    # ------------------ Generate offsprings with mutations
                    print("---------------> Generating offsprings with mutations")
                    self.new_population = self.evoa_tools.generate_offsprings(ticker,
                                                                              gen,
                                                                              config.nb_of_generations,
                                                                              self.data_slice_cycle_count,
                                                                              config.data_slice_cycle_count,
                                                                              config.mutation_decay_function,
                                                                              config.population_size,
                                                                              self.parents,
                                                                              self.nb_random_ind,
                                                                              mutation_rate=config.mutation_rate)

                    print("\nParameter sets evolution completed (Darwin put in charge)")
                    print("Length new pop", len(self.new_population))

                    self.population = self.new_population

            # ------------------ Evaluate population
            self.fitness_evaluation, _, self.net_worth = self.evoa_tools.evaluate_population(self.population,
                                                                                             self.data_slice_info,
                                                                                             max_worker_processes=config.max_worker_processes,
                                                                                             print_evaluation_status=config.print_evaluation_status,
                                                                                             plot_3=config.plot_signal_triggers)

            if sum(self.fitness_evaluation) != 0:
                # ------------------ Collect generation data
                if self.nb_parents is not None and self.nb_random_ind is not None:
                    self.results.nb_parents.append(self.nb_parents)
                    self.results.nb_random_ind.append(self.nb_random_ind)

                self.results.best_individual_fitness_per_gen.append(max(self.fitness_evaluation))
                self.results.avg_fitness_per_gen.append(sum(self.fitness_evaluation)/len(self.fitness_evaluation))

                self.results.best_individual_net_worth_per_gen.append(max(self.net_worth))
                self.results.avg_net_worth_per_gen.append(sum(self.net_worth) / len(self.net_worth))

                self.data_slice_info.perform_trade_run(ticker)
                self.results.data_slice_metalabel_pp.append(self.data_slice_info.metalabels_account.net_worth_history[-1])

                # ------------------ Return generation info
                generation_end_time = time.time()
                print("\nTime elapsed:", generation_end_time-generation_start_time)
                print("\n-- Generation", gen + 1, "population evaluation completed --\n")
                print("Metalabel net worth from previous generation:", round(self.results.data_slice_metalabel_pp[-1], 3))
                print("\n")
                print("Best Individual fitness from previous generation:", round(max(self.fitness_evaluation), 3))
                print("Average fitness from previous generation:", round((sum(self.fitness_evaluation) / len(self.fitness_evaluation)), 3))
                print("\n")
                print("Best Individual net worth from previous generation:", round(max(self.net_worth), 3))
                print("Average net worth from previous generation:", round((sum(self.net_worth) / len(self.net_worth)), 3))
                print("\n")

            else:
                self.results.invalid_slice_count += 1
                self.data_slice_cycle_count = config.data_slice_cycle_count
                print("Data slice invalid for training, proceed to next data slice")

        # ===============================================================================
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("All data processed")
        total_data_points_processed = -config.data_slice_start_index + self.data_slice_info.stop_index
        print("Number of data points processed:", total_data_points_processed)
        print("Parameter optimisation completed")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.results.total_data_points_processed = total_data_points_processed
        # ========================= EVOA OPTIMISATION RESULTS =============================
        self.results.run_stop_time = time.time()
        print("\nEnd time:", time.strftime('%X %x %Z'), "\n")

        # ------------------ Final results benchmarking
        # Select best individual from final population
        if self.fitness_evaluation is None:
            self.fitness_evaluation = [1]

        self.best_individual = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                      self.population,
                                                                      selection_method=config.parents_selection_method,
                                                                      nb_parents=1)[0]

        _, benchmark_confusion_matrix_analysis, _ = self.evoa_tools.evaluate_population([self.best_individual],
                                                                                        self.benchmark_data_slice,
                                                                                        calculate_stats=True,
                                                                                        print_evaluation_status=False,
                                                                                        plot_3=True)

        # Generate run results summary
        self.results.individual = self.best_individual
        self.results.benchmark_confusion_matrix_analysis = benchmark_confusion_matrix_analysis[0]
        self.results.gen_stats()

        self.results.gen_result_recap_file()
        self.results.gen_parameters_json()
        self.results.plot_results()

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
