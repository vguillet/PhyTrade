from PhyTrade.GA_optimisation.GA_tools import GA_tools
import time

"""""
begin
    count = 0                                   \done
    initialize population                       \done
    evaluate population                         \done
    while not termination condition do
    begin
        count = count + 1
        select individuals for reproduction
        apply variation operators
        evaluate offspring
    end
end
"""""


class GA_optimiser():
    def __init__(self, population_size=10, nb_of_generations=5, mutation_rate=0.2, nb_parents=4, nb_random_ind=4):
        # ========================= GA OPTIMISATION INITIALISATION =======================
        self.nb_of_generations = nb_of_generations

        self.population_size = population_size
        self.nb_parents = nb_parents
        self.nb_random_ind = nb_random_ind
        self.mutation_rate = mutation_rate
        # ------------------ Tools and GA parameters initialisation
        self.ga_tools = GA_tools()
        self.best_individual_per_gen = []

        # ------------------ Initialise population
        self.population = self.ga_tools.gen_initial_population(self.population_size)

        print("~~~~~~~~~~~~~~~~~~~~~~")
        print("GA_v1")
        print("")
        time.ctime()  # 'Mon Oct 18 13:35:29 2010'
        print("Start time:", time.strftime('%X %x %Z'))
        print("~~~~~~~~~~~~~~~~~~~~~~")
        print("")

        # ------------------ Evaluate initial population
        self.fitness_evaluation = self.ga_tools.evaluate_population(self.population)

        self.best_individual_per_gen.append(max(self.fitness_evaluation))
        print("")
        print("Max net achieved:", max(self.fitness_evaluation))
        print("Max profit achieved:", (max(self.fitness_evaluation) - 1000) / 10)

        # ==============================================================================
        """




        """
        # ========================= GA OPTIMISATION PROCESS ==============================
        # Run for # nb of generations:
        for i in range(nb_of_generations):
            start = time.time()

            print("==================== Generation", i + 1, "====================")
            print("")
            # -- Throttle the number of parents according to the generation
            self.nb_parents = self.ga_tools.throttle(self.nb_parents, nb_of_generations, 0.1)
            print("Number of parents selected:", self.nb_parents)

            # -- Throttle the number of random individual according to the generation
            self.nb_random_ind = self.ga_tools.throttle(self.nb_random_ind, nb_of_generations, 0.2)
            print("Number of random individuals included:", self.nb_random_ind)

            # ------------------ Select individuals from current generation
            self.parents = self.ga_tools.select_from_population(self.fitness_evaluation,
                                                                self.population,
                                                                selection_method=0,
                                                                nb_parents=self.nb_parents)

            # ------------------ Generate offsprings with mutations
            self.new_population = self.ga_tools.generate_offsprings(self.population_size,
                                                                    self.nb_parents,
                                                                    self.parents,
                                                                    self.nb_random_ind,
                                                                    self.mutation_rate)

            print("")
            print("Parameter sets evolution completed (Darwin put in charge)")
            print("New population generated")
            print("")

            assert self.parents[0] == self.new_population[0]

            self.population = self.new_population

            # ------------------ Evaluate new population
            self.fitness_evaluation = self.ga_tools.evaluate_population(self.population)

            self.best_individual_per_gen.append(max(self.fitness_evaluation))
            print("")
            print("-- Generation", i + 1, "population evaluation completed --")
            print("Max net achieved:", max(self.fitness_evaluation))
            print("Max profit achieved:", (max(self.fitness_evaluation)-1000)/10)
            print("")
            end = time.time()
            print("Time elapsed:", end-start)
            print("")


        print(self.best_individual_per_gen)
        import matplotlib.pyplot as plt

        plt.plot(range(len(self.best_individual_per_gen)), self.best_individual_per_gen)
        plt.show()














