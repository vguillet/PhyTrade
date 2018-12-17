from PhyTrade.GA_optimisation.GA_tools import GA_tools
from PhyTrade.Tools.DATA_SLICE_gen import data_slice_info
import time


class GA_optimiser():
    def __init__(self,
                 population_size=10,
                 nb_of_generations=5,
                 mutation_rate=0.2,
                 nb_parents=4,
                 nb_random_ind=4,
                 data_slice_size=200):

        # ======================== GA OPTIMISATION INITIALISATION =======================
        self.data_slice_start_index = -7000
        parents_selection_method = 0

        max_worker_threads = 4
        # ------------------ Tools and GA parameters initialisation
        # -- Initialise population and generation parameters
        self.nb_of_generations = nb_of_generations
        self.population_size = population_size

        # -- Initialise population evolution parameters
        self.nb_parents = nb_parents
        self.nb_random_ind = nb_random_ind
        self.mutation_rate = mutation_rate

        # -- Initialise data slice
        self.data_slice_info = data_slice_info(self.data_slice_start_index, data_slice_size)

        # -- Initialise tools
        self.ga_tools = GA_tools()

        # -- Initialise records
        self.best_individual_per_gen = []

        # ===============================================================================
        """




        """
        # ======================== INITIATE OPTIMISATION ALGORITHM ======================

        generation_start_time = time.time()

        # ------------------ Initialise population
        self.population = self.ga_tools.gen_initial_population(self.population_size)

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("GA_v1 \n")
        optimisation_start_time = time.time()
        print("Start time:", time.strftime('%X %x %Z'))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
        print("\nData slice analysed:", self.data_slice_info.start_index, "-->", self.data_slice_info.stop_index, "\n")

        # ------------------ Evaluate initial population
        self.fitness_evaluation = self.ga_tools.evaluate_population(self.population,
                                                                    self.data_slice_info,
                                                                    max_worker_threads=max_worker_threads)

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
        for i in range(nb_of_generations):

            generation_start_time = time.time()

            print("\n==================== Generation", i + 1, "====================")

            # ------------------ Select individuals from current generation
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
            print("New population generated")

            self.population = self.new_population

            # ------------------ Define the data slice to be used by the generation
            self.data_slice_info.get_next_data_slice()

            if self.data_slice_info.stop_index >= 0:
                break

            print("\nData slice analysed:", self.data_slice_info.start_index, "-->", self.data_slice_info.stop_index)

            # ------------------ Evaluate new population
            self.fitness_evaluation = self.ga_tools.evaluate_population(self.population,
                                                                        self.data_slice_info,
                                                                        max_worker_threads=max_worker_threads)

            self.best_individual_per_gen.append(max(self.fitness_evaluation))

            print("\n-- Generation", i + 1, "population evaluation completed --")
            print("Max net achieved:", max(self.fitness_evaluation))
            print("Max profit achieved:", (max(self.fitness_evaluation)-1000)/10)

            generation_end_time = time.time()
            print("\nTime elapsed:", generation_end_time-generation_start_time)

        # ===============================================================================
        """




        """
        # ========================= GA OPTIMISATION RESULTS =============================
        print(self.best_individual_per_gen)

        optimisation_end_time = time.time()
        print("\nEnd time:", time.strftime('%X %x %Z'))
        print("Optimisation run time:", optimisation_end_time - optimisation_start_time)
        print("")

        import matplotlib.pyplot as plt

        plt.plot(range(len(self.best_individual_per_gen)), self.best_individual_per_gen)
        plt.show()














