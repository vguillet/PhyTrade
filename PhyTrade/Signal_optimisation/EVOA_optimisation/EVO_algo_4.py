"""
This script contains the EVOA_optimiser class, which is a refactored and optimised version of EVO_algo3 tailored for multiprocessing
"""

from PhyTrade.Settings.Metalabeling_settings import Metalabeling_settings

from PhyTrade.Signal_optimisation.EVOA_optimisation.EVOA_prints import EVOA_prints

from PhyTrade.Signal_optimisation.EVOA_optimisation.Tools.EVOA_tools import EVOA_tools
from PhyTrade.Signal_optimisation.EVOA_optimisation.Tools.EVOA_results_gen import EVOA_results_gen
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.Progress_bar_tool import Progress_bar

import time


class EVOA_optimiser:
    def __init__(self, settings, ticker="AAPL"):
        # ======================== GA OPTIMISATION INITIALISATION =======================
        # ------------------ Tools and GA parameters initialisation
        settings.signal_training_settings.gen_evoa_settings()
        settings.metalabeling_settings.gen_metalabels_settings()

        prints = EVOA_prints(ticker, 4)

        # --> Disable all prints/plots in case of multiprocessing
        if settings.signal_training_settings.multiprocessing:
            settings.signal_training_settings.print_evoa_parameters_per_gen = False
            settings.signal_training_settings.print_evaluation_status = False
            settings.signal_training_settings.print_trade_process = False

            settings.signal_training_settings.plot_eco_model_results = False
            settings.signal_training_settings.plot_best_individual_eco_model_results = False

        # --> Initialise data slice for gen and metalabels
        self.data_slice = data_slice(ticker,
                                     settings.market_settings.start_date,
                                     settings.market_settings.data_slice_size,
                                     settings.signal_training_settings.data_slice_shift_per_gen,
                                     data_selection=settings.market_settings.price_selection,
                                     end_date=settings.market_settings.end_date,
                                     data_looper=settings.signal_training_settings.data_looper)

        self.data_slice.gen_slice_metalabels(settings.metalabeling_settings.upper_barrier, settings.metalabeling_settings.lower_barrier,
                                             settings.metalabeling_settings.look_ahead,
                                             settings.metalabeling_settings.metalabeling_setting)

        # --> Initialise tools and counters
        self.evoa_tools = EVOA_tools()
        self.data_slice_cycle_count = 0

        self.nb_parents = None
        self.nb_random_ind = None

        # --> Initialise records
        self.results = EVOA_results_gen(ticker)
        self.results.data_slice_start_index = self.data_slice.start_index

        self.results.run_start_time = time.time()

        # ========================= EVO OPTIMISATION PROCESS =============================
        prints.evoa_run_initialisation_recap()
        progress_bar = Progress_bar(settings.signal_training_settings.nb_of_generations, 50, label=ticker)

        # ------------------ Initialise population
        if settings.signal_training_settings.starting_parameters is None:
            self.population = self.evoa_tools.gen_initial_population(ticker, settings.signal_training_settings.population_size)
        else:
            self.population = self.evoa_tools.generate_offsprings(ticker,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  0,
                                                                  settings.signal_training_settings.population_size,
                                                                  [Individual(parameter_set=settings.signal_training_settings.starting_parameters)],
                                                                  settings.signal_training_settings.nb_random_ind,
                                                                  mutation_rate=settings.signal_training_settings.mutation_rate)
        prints.init_pop_success_msg()

        # ------------------ Run for # nb of generations:
        for gen in range(settings.signal_training_settings.nb_of_generations):
            generation_start_time = time.time()

            if gen == settings.signal_training_settings.nb_of_generations-settings.signal_training_settings.exploitation_phase_len-1:
                prints.exploration_phase_complete_msg()

            if gen != 0:
                # ------------------ Define the data slice to be used by the generation
                self.data_slice_cycle_count += 1
                if self.data_slice_cycle_count > settings.signal_training_settings.data_slice_cycle_count:
                    self.data_slice.get_shifted_data_slice()
                    self.data_slice.gen_slice_metalabels(settings.metalabeling_settings.upper_barrier, settings.metalabeling_settings.lower_barrier,
                                                         settings.metalabeling_settings.look_ahead,
                                                         settings.metalabeling_settings.metalabeling_setting)
                    self.data_slice_cycle_count = 1

                    if self.data_slice.end_of_dataset is True:
                        break

                prints.new_slice_info(self.data_slice, gen, self.data_slice_cycle_count)

                # ------------------ Determine new generation GA parameters
                prints.det_new_generation_param_msg()
                self.nb_parents, self.nb_parents_in_next_gen, self.nb_random_ind = \
                    self.evoa_tools.determine_evolving_gen_parameters(settings.signal_training_settings, gen, self.data_slice_cycle_count)

                if sum(self.fitness_evaluation) != 0:
                    # ------------------ Select individuals from previous generation
                    prints.select_ind_msg()
                    self.parents = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                          self.population,
                                                                          selection_method=settings.signal_training_settings.parents_selection_method,
                                                                          nb_parents=self.nb_parents)

                    # ------------------ Generate offsprings with mutations
                    prints.gen_offsprings_msg()
                    self.new_population = self.evoa_tools.generate_offsprings(ticker,
                                                                              gen,
                                                                              settings.signal_training_settings.nb_of_generations,
                                                                              self.data_slice_cycle_count,
                                                                              settings.signal_training_settings.data_slice_cycle_count,
                                                                              settings.signal_training_settings.mutation_decay_function,
                                                                              settings.signal_training_settings.population_size,
                                                                              self.parents, self.nb_parents_in_next_gen,
                                                                              self.nb_random_ind,
                                                                              mutation_rate=settings.signal_training_settings.mutation_rate)
                    prints.darwin_in_charge_msg()
                    self.population = self.new_population

            # ------------------ Evaluate population
            prints.eval_pop_msg()
            self.fitness_evaluation, _, self.net_worth = \
                self.evoa_tools.evaluate_population(self.population,
                                                    self.data_slice,
                                                    evaluation_setting=settings.signal_training_settings.evaluation_method,
                                                    max_worker_processes=settings.signal_training_settings.max_process_count,
                                                    multiprocessing=settings.signal_training_settings.multiprocessing,
                                                    print_evaluation_status=settings.signal_training_settings.print_evaluation_status,
                                                    plot_eco_model_results=settings.signal_training_settings.plot_eco_model_results)

            if settings.signal_training_settings.evaluation_method == 1 and sum(self.fitness_evaluation) == 0:
                prints.invalid_slice_msg()
                self.results.invalid_slice_count += 1
                self.data_slice_cycle_count = settings.signal_training_settings.data_slice_cycle_count

            else:
                # ------------------ Collect generation data
                if self.nb_parents is not None and self.nb_random_ind is not None:
                    self.results.nb_parents.append(self.nb_parents)
                    self.results.nb_random_ind.append(self.nb_random_ind)

                self.results.best_individual_fitness_per_gen.append(max(self.fitness_evaluation))
                self.results.avg_fitness_per_gen.append(sum(self.fitness_evaluation)/len(self.fitness_evaluation))
                # self.results.avg_fitness_per_gen.append(sum(self.fitness_evaluation[:-self.nb_random_ind])/len(self.fitness_evaluation[:-self.nb_random_ind]))

                self.results.best_individual_net_worth_per_gen.append(max(self.net_worth))
                self.results.avg_net_worth_per_gen.append(sum(self.net_worth) / len(self.net_worth))

                self.data_slice.perform_trade_run()
                self.results.data_slice_metalabel_pp.append(self.data_slice.metalabels_account.net_worth_history[-1])

                generation_end_time = time.time()

                # ------------------ Print generation info
                prints.generation_info(gen, generation_start_time, generation_end_time,
                                       self.results, self.net_worth, self.fitness_evaluation,
                                       self.population)

                progress_bar.update_progress_bar(gen)

                if settings.signal_training_settings.plot_best_individual_eco_model_results is True:
                    self.population[self.fitness_evaluation.index(max(self.fitness_evaluation))].gen_economic_model(
                        self.data_slice, plot_eco_model_results=True)

        # ===============================================================================
        total_data_points_processed = -self.results.data_slice_start_index + self.data_slice.stop_index
        prints.end_of_optimisation_msg(total_data_points_processed)
        self.results.total_data_points_processed = total_data_points_processed

        # ========================= EVOA OPTIMISATION RESULTS =============================
        self.results.run_stop_time = time.time()

        # Select best individual from final population
        if self.fitness_evaluation is None:
            self.fitness_evaluation = [1]

        self.best_individual = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                      self.population,
                                                                      selection_method=settings.signal_training_settings.parents_selection_method,
                                                                      nb_parents=1)[0]

        self.results.individual = self.best_individual
        self.results.gen_parameters_json()

        # # ------------------ Final results benchmarking
        # # -- Initialise benchmark data slice
        # self.benchmark_data_slice = data_slice(ticker,
        #                                        settings.benchmark_data_slice_start_date,
        #                                        settings.benchmark_data_slice_size,
        #                                        0)
        #
        # self.benchmark_data_slice.gen_slice_metalabels(settings.upper_barrier, settings.lower_barrier, settings.look_ahead,
        #                                                settings.metalabeling_setting)
        #
        # _, benchmark_confusion_matrix_analysis, _ = self.evoa_tools.evaluate_population([self.best_individual],
        #                                                                                 self.benchmark_data_slice,
        #                                                                                 evaluation_setting=settings.evaluation_method,
        #                                                                                 calculate_stats=True,
        #                                                                                 print_evaluation_status=False,
        #                                                                                 plot_eco_model_results=True)
        #
        # # --> Generate run results summary
        # self.results.benchmark_confusion_matrix_analysis = benchmark_confusion_matrix_analysis[0]
        # self.results.gen_stats()
        # self.results.gen_result_recap_file()
        # self.results.plot_results()

        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
