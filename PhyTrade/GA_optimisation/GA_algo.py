from PhyTrade.GA_optimisation.GA_tools import GA_tools

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
    def __init__(self, population_size=10, nb_of_generations=5, mutation_rate=0.2):
        # ========================= GA OPTIMISATION INITIALISATION =======================
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        # ------------------ Tools and GA parameters initialisation
        self.ga_tools = GA_tools()

        # ------------------ Initialise population
        self.population = self.ga_tools.gen_initial_population(self.population_size)

        print("Population initialised")
        print(self.population[0].parameter_lsts)
        # ==============================================================================
        """




        """
        # ========================= GA OPTIMISATION PROCESS ==============================
        # Run for # nb of generations:
        for i in range(nb_of_generations):

            # ------------------ Evaluate population
            self.fitness_evaluation = self.ga_tools.evaluate_population(self.population)

            print("==================== Generation", i + 1, "====================")
            # ------------------ Select individuals from current generation
            self.parents = self.ga_tools.select_from_population(self.fitness_evaluation,
                                                                self.population,
                                                                selection_method=0,
                                                                number_of_selected_ind=3)
            print(self.parents)

            # ------------------ Generate offsprings with mutations
            self.new_population = self.ga_tools.generate_offsprings(self.parents, self.mutation_rate)














