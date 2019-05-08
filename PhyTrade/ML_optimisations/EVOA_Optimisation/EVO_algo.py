from PhyTrade.ML_optimisation.GA_Optimisation.GA_tools.GA_tools import GA_tools
from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info

import time


class GA_optimiser():
    def __init__(self,
                 population_size=10,
                 nb_of_generations=5,

                 mutation_rate=0.2,
                 nb_parents=4,
                 nb_random_ind=3,

                 exploitation_phase_len=3,

                 data_slice_start_index=-7000,
                 data_slice_size=200,
                 data_slice_shift_per_gen=100):

        # ======================== GA OPTIMISATION INITIALISATION =======================
        # ------------------ User settings
        # -- Print parameters
        print_ga_parameters_per_gen = True
        print_evaluation_status = True

        plot_signal_triggers = False

        # -- Generations settings
        decay_functions = ["Fixed value", "Linear decay", "Exponential decay", "Logarithmic decay"]

        parents_decay_function = 1
        random_ind_decay_function = 1

        parents_selection_method = 0

        max_worker_threads = 4

        # -- Metalabels settings:
        upper_barrier = 20
        lower_barrier = -20
        look_ahead = 10

        # ------------------ Tools and GA parameters initialisation
        # -- Initialise population and generation parameters
        self.nb_of_generations = nb_of_generations
        self.population_size = population_size

        # -- Initialise population evolution parameters
        self.initial_nb_parents = nb_parents
        self.nb_parents = nb_parents

        self.initial_nb_random_ind = nb_random_ind
        self.nb_random_ind = nb_random_ind

        self.mutation_rate = mutation_rate

        # -- Initialise data slice for gen and metalabels
        self.data_slice_info = data_slice_info(data_slice_start_index,
                                               data_slice_size,
                                               data_slice_shift_per_gen,
                                               upper_barrier,
                                               lower_barrier,
                                               look_ahead)

        # -- Initialise benchmark data slice
        self.benchmark_data_slice = data_slice_info(-453, 252, 0, upper_barrier, lower_barrier, look_ahead)

        # -- Initialise tools
        self.ga_tools = GA_tools()

        # -- Initialise records
        self.best_individual_per_gen = []

        # ===============================================================================
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("GA_v2 \n")
        optimisation_start_time = time.time()
        print("Start time:", time.strftime('%X %x %Z'), "\n")
        print("-- Settings selected --")
        print("Selected parent function:", decay_functions[parents_decay_function])
        print("Selected random individual function:", decay_functions[random_ind_decay_function])
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ======================== GA INITIAL POPULATION GENERATION =====================
        print("\n==================== INITIAL GENERATION ========================")
        generation_start_time = time.time()

        # ------------------ Initialise population
        print("\nData slice analysed:", self.data_slice_info.start_index, "-->", self.data_slice_info.stop_index, "\n")
        self.population = self.ga_tools.gen_initial_population(self.population_size)

        # ------------------ Evaluate initial population
        self.fitness_evaluation = self.ga_tools.evaluate_population(self.population,
                                                                    self.data_slice_info,
                                                                    max_worker_threads=max_worker_threads,
                                                                    print_evaluation_status=print_evaluation_status,
                                                                    plot_3=plot_signal_triggers)

        self.best_individual_per_gen.append(max(self.fitness_evaluation))

        print("\nMax net achieved:", max(self.fitness_evaluation))
        print("Max profit achieved:", (max(self.fitness_evaluation) - 1000) / 10)

        generation_end_time = time.time()
        print("\nTime elapsed:", generation_end_time - generation_start_time)

        # ===============================================================================
        """




        """
        # ========================= GA OPTIMISATION PROCESS =============================
        # Run for # nb of generations:
        for gen in range(nb_of_generations):

            print("\n==================== Generation", gen + 1, "====================")
            generation_start_time = time.time()

            # ------------------ Determine new generation GA parameters
            self.data_slice_info, self.nb_parents, self.nb_random_ind = \
                self.ga_tools.determine_evolving_gen_parameters(self.data_slice_info,
                                                                gen,
                                                                self.nb_of_generations-exploitation_phase_len,
                                                                self.initial_nb_parents,
                                                                self.initial_nb_random_ind,
                                                                parents_decay_function=parents_decay_function,
                                                                random_ind_decay_function=random_ind_decay_function,
                                                                print_ga_parameters_per_gen=print_ga_parameters_per_gen)

            # ------------------ Select individuals from previous generation
            self.parents = self.ga_tools.select_from_population(self.fitness_evaluation,
                                                                self.population,
                                                                selection_method=parents_selection_method,
                                                                nb_parents=self.nb_parents)

            # ------------------ Generate offsprings with mutations
            self.new_population = self.ga_tools.generate_offsprings(self.population_size,
                                                                    self.nb_parents,
                                                                    self.parents,
                                                                    self.nb_random_ind,
                                                                    self.mutation_rate)

            print("\nParameter sets evolution completed (Darwin put in charge)")
            print("New population generated\n")

            self.population = self.new_population

            # ------------------ Evaluate new population
            self.fitness_evaluation = self.ga_tools.evaluate_population(self.population,
                                                                        self.data_slice_info,
                                                                        max_worker_threads=max_worker_threads,
                                                                        print_evaluation_status=print_evaluation_status,
                                                                        plot_3=plot_signal_triggers)

            self.best_individual_per_gen.append(max(self.fitness_evaluation))

            generation_end_time = time.time()

            print("\n-- Generation", gen + 1, "population evaluation completed --")
            print("Max net achieved:", max(self.fitness_evaluation))
            print("Max profit achieved:", (max(self.fitness_evaluation)-1000)/10)
            print("\nTime elapsed:", generation_end_time-generation_start_time)

            if self.data_slice_info.stop_index >= 0:
                break

        # ===============================================================================
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("All data processed")
        print("Number of data points processed:")
        print("Parameter optimisation completed")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # ========================= GA OPTIMISATION RESULTS =============================
        self.best_individual = self.ga_tools.select_from_population(self.fitness_evaluation,
                                                                    self.population,
                                                                    selection_method=parents_selection_method,
                                                                    nb_parents=1)[0]
        # ------------------ Results benchmarking
        print("\n-- Results benchmarking --")
        self.best_individual.perform_trade_run(self.benchmark_data_slice, plot_3=True)
        print("Net worth:", self.best_individual.account.net_worth_history[-1])

        # self.best_individual.save_parameters_to_csv()

        print("\n-- RUN SUMMARY: --")
        optimisation_end_time = time.time()
        print("\nEnd time:", time.strftime('%X %x %Z'))
        print("Optimisation run time:", optimisation_end_time - optimisation_start_time)
        print("")

        import matplotlib.pyplot as plt

        plt.plot(range(len(self.best_individual_per_gen)), self.best_individual_per_gen)
        plt.show()














