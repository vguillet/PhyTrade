"""
This script contains the EVOA_optimiser class, which is a refactored and optimised version of EVO_algo2
"""

from SETTINGS import SETTINGS
from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_tools import EVOA_tools
from PhyTrade.ML_optimisation.EVOA_optimisation.Tools.EVOA_results_gen import EVOA_results_gen
from PhyTrade.Tools.INDIVIDUAL_gen import Individual
from PhyTrade.Tools.DATA_SLICE_gen import data_slice

import time


class EVOA_optimiser:
    def __init__(self, ticker="AAPL"):
        # ======================== GA OPTIMISATION INITIALISATION =======================
        # ------------------ Tools and GA parameters initialisation
        settings = SETTINGS()
        settings.gen_evoa_settings()

        # -- Initialise data slice for gen and metalabels
        self.data_slice = data_slice(ticker,
                                     settings.data_slice_start_date,
                                     settings.data_slice_size,
                                     settings.data_slice_shift_per_gen,
                                     end_date=settings.end_date,
                                     data_looper=settings.data_looper)

        self.data_slice.gen_slice_metalabels(settings.upper_barrier, settings.lower_barrier, settings.look_ahead,
                                             settings.metalabeling_setting)

        # -- Initialise tools and counters
        self.evoa_tools = EVOA_tools()
        self.data_slice_cycle_count = 0

        self.nb_parents = None
        self.nb_random_ind = None

        # -- Initialise records
        self.results = EVOA_results_gen(ticker)
        self.results.data_slice_start_index = self.data_slice.start_index

        # ===============================================================================
        # decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("EVOA_v3 \n")

        print("Evaluated ticker:", ticker)
        self.results.run_start_time = time.time()
        print("Start time:", time.strftime('%X %x %Z'), "\n")

        print("-- Settings selected --")
        print("Selected evaluation method:", settings.evaluation_methods[settings.evaluation_method])
        print("Selected metalabeling method:", settings.metalabeling_settings[settings.metalabeling_setting])
        print("")
        print("Selected parent function:", settings.decay_functions[settings.parents_decay_function])
        print("Selected random individual function:", settings.decay_functions[settings.random_ind_decay_function])
        print("Selected mutation range function:", settings.decay_functions[settings.mutation_decay_function])
        print("")
        print("Configuration sheet:", settings.config_name)
        print("Starting parameters:", settings.starting_parameters)
        print("")
        if settings.starting_parameters is None:
            print("Indicators tuned: -> RSI:", settings.rsi_count)
            print("                  -> SMA:", settings.sma_count)
            print("                  -> EMA:", settings.ema_count)
            print("                  -> LWMA:", settings.lwma_count)
            print("                  -> CCI:", settings.cci_count)
            print("                  -> EVM:", settings.eom_count)
            print("                  -> OC gradient:", 1)

        else:
            print("Indicators tuned: -> RSI:", settings.starting_parameters["indicators_count"]["rsi"])
            print("                  -> SMA:", settings.starting_parameters["indicators_count"]["sma"])
            print("                  -> EMA:", settings.starting_parameters["indicators_count"]["ema"])
            print("                  -> LWMA:", settings.starting_parameters["indicators_count"]["lwma"])
            print("                  -> CCI:", settings.starting_parameters["indicators_count"]["cci"])
            print("                  -> EVM:", settings.starting_parameters["indicators_count"]["eom"])
            print("                  -> OC gradient:", 1)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ========================= EVO OPTIMISATION PROCESS =============================

        # ------------------ Initialise population
        if settings.starting_parameters is None:
            self.population = self.evoa_tools.gen_initial_population(ticker, settings.population_size)
        else:
            self.population = self.evoa_tools.generate_offsprings(ticker,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  1,
                                                                  0,
                                                                  settings.population_size,
                                                                  [Individual(parameter_set=settings.starting_parameters)],
                                                                  settings.nb_random_ind,
                                                                  mutation_rate=settings.mutation_rate)

        print("\n---------------> Initial population generated successfully")

        # ------------------ Run for # nb of generations:
        for gen in range(settings.nb_of_generations+1):
            generation_start_time = time.time()

            if gen == settings.nb_of_generations-settings.exploitation_phase_len-1:
                print("-------------> Exploration phase completed, starting exploitation phase <-------------")

            if gen != 0:
                # ------------------ Define the data slice to be used by the generation
                self.data_slice_cycle_count += 1
                if self.data_slice_cycle_count > settings.data_slice_cycle_count:
                    self.data_slice.get_shifted_data_slice()
                    self.data_slice.gen_slice_metalabels(settings.upper_barrier, settings.lower_barrier, settings.look_ahead,
                                                         settings.metalabeling_setting)
                    self.data_slice_cycle_count = 1

                    if self.data_slice.end_of_dataset is True:
                        break
                print("\n================================= Generation", gen, "=================================")
                print("Data slice analysed:", self.data_slice.start_date, "-->", self.data_slice.stop_date)
                print("Data slice analysed:", self.data_slice.start_index, "-->", self.data_slice.stop_index)
                print("Data slice analysis cycle:", self.data_slice_cycle_count, "\n")

                # ------------------ Determine new generation GA parameters
                print("---------------> Determining new generation parameters")
                self.nb_parents, self.nb_random_ind = \
                    self.evoa_tools.determine_evolving_gen_parameters(gen,
                                                                      self.data_slice_cycle_count)

                if sum(self.fitness_evaluation) != 0:
                    # ------------------ Select individuals from previous generation
                    print("---------------> Selecting individuals from previous generation")
                    self.parents = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                          self.population,
                                                                          selection_method=settings.parents_selection_method,
                                                                          nb_parents=self.nb_parents)

                    # ------------------ Generate offsprings with mutations
                    print("---------------> Generating offsprings with mutations")
                    self.new_population = self.evoa_tools.generate_offsprings(ticker,
                                                                              gen,
                                                                              settings.nb_of_generations,
                                                                              self.data_slice_cycle_count,
                                                                              settings.data_slice_cycle_count,
                                                                              settings.mutation_decay_function,
                                                                              settings.population_size,
                                                                              self.parents,
                                                                              self.nb_random_ind,
                                                                              mutation_rate=settings.mutation_rate)

                    print("\nParameter sets evolution completed (Darwin put in charge)\n")
                    # print("Length new pop", len(self.new_population), "\n")

                    self.population = self.new_population

            # ------------------ Evaluate population
            print("---------------> Evaluating population")
            self.fitness_evaluation, _, self.net_worth = \
                self.evoa_tools.evaluate_population(self.population,
                                                    self.data_slice,
                                                    evaluation_setting=settings.evaluation_method,
                                                    max_worker_processes=settings.max_worker_processes,
                                                    print_evaluation_status=settings.print_evaluation_status,
                                                    plot_eco_model_results=settings.plot_eco_model_results)

            if settings.evaluation_method == 1 and sum(self.fitness_evaluation) == 0:
                self.results.invalid_slice_count += 1
                self.data_slice_cycle_count = settings.data_slice_cycle_count
                print("Data slice invalid for training, proceed to next data slice")

            else:
                # ------------------ Collect generation data
                if self.nb_parents is not None and self.nb_random_ind is not None:
                    self.results.nb_parents.append(self.nb_parents)
                    self.results.nb_random_ind.append(self.nb_random_ind)

                self.results.best_individual_fitness_per_gen.append(max(self.fitness_evaluation))
                self.results.avg_fitness_per_gen.append(sum(self.fitness_evaluation)/len(self.fitness_evaluation))

                self.results.best_individual_net_worth_per_gen.append(max(self.net_worth))
                self.results.avg_net_worth_per_gen.append(sum(self.net_worth) / len(self.net_worth))

                self.data_slice.perform_trade_run()
                self.results.data_slice_metalabel_pp.append(self.data_slice.metalabels_account.net_worth_history[-1])

                # ------------------ Print generation info
                generation_end_time = time.time()
                print("\n-- Generation", gen + 1, "population evaluation completed --")
                print("Total generation Run time:", round(generation_end_time-generation_start_time, 3), "s")

                print("\nMetalabel net worth:", round(self.results.data_slice_metalabel_pp[-1], 3))
                print("Average net worth:", round((sum(self.net_worth) / len(self.net_worth)), 3))

                print("\n-> Best individual:")
                index_best_individual = self.fitness_evaluation.index(max(self.fitness_evaluation))

                print("Net worth:", round(self.net_worth[index_best_individual], 3))
                print("Transaction count:", self.population[index_best_individual].tradebot.buy_count +
                      self.population[index_best_individual].tradebot.sell_count)
                print("Buy count:", self.population[index_best_individual].tradebot.buy_count)
                print("Sell count:", self.population[index_best_individual].tradebot.sell_count)

                print("\nBest Individual fitness:", round(max(self.fitness_evaluation), 3))
                print("Average fitness:", round((sum(self.fitness_evaluation) / len(self.fitness_evaluation)), 3), "\n")

                if settings.plot_best_individual_eco_model_results is True:
                    self.population[index_best_individual].gen_economic_model(self.data_slice, plot_eco_model_results=True)

        # ===============================================================================
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("All data processed")
        total_data_points_processed = -self.results.data_slice_start_index + self.data_slice.stop_index
        print("Number of data points processed:", total_data_points_processed)
        print("Parameter optimisation completed")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.results.total_data_points_processed = total_data_points_processed
        # ========================= EVOA OPTIMISATION RESULTS =============================
        self.results.run_stop_time = time.time()
        print("\nEnd time:", time.strftime('%X %x %Z'), "\n")

        # Select best individual from final population
        if self.fitness_evaluation is None:
            self.fitness_evaluation = [1]

        self.best_individual = self.evoa_tools.select_from_population(self.fitness_evaluation,
                                                                      self.population,
                                                                      selection_method=settings.parents_selection_method,
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

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
