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
    def __init__(self, population_size=10, nb_of_generations=5):
        # ========================= GA OPTIMISATION INITIALISATION =======================
        self.population_size = population_size

        # ------------------ Tools and GA parameters initialisation
        self.ga_tools = GA_tools()
        count = 0

        # ------------------ Initialise population
        self.population = self.ga_tools.gen_initial_population(self.population_size)

        print("Population initialised")
        # ==============================================================================
        """




        """
        # ========================= GA OPTIMISATION PROCESS ==============================
        # Run for # nb of generations:
        for i in range(nb_of_generations):
            print("==================== Generation", i+1, "====================")
            # ------------------ Evaluate population
            self.fitness_evaluation = self.ga_tools.evaluate_population(self.population)

            # ------------------ Select individuals from current generation
            self.selected_individuals = self.ga_tools.select_from_population(self.fitness_evaluation,
                                                                             selection_method=0,
                                                                             number_of_selected_ind=3)
            print(self.selected_individuals)
