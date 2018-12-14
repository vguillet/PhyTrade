

class GA_tools:
    @staticmethod
    def gen_initial_population(population_size=10):
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst):
        from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3
        from PhyTrade.Tools.MATH_tools import MATH

        performance_lst = []
        for i in range(len(population_lst)):
            performance_lst.append(Tradebot_v3(population_lst[i]).account.net_worth_history[-1])
            print("Parameter set ", i+1, "evaluation completed")

        # performance_lst = MATH().normalise_zero_one(performance_lst)

        return performance_lst

    @staticmethod
    def select_from_population(fitness_evaluation, selection_method=0, number_of_selected_ind=3):

        # -- Determine fitness ratio
        fitness_ratios = []
        for i in range(len(fitness_evaluation)):
            fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

        # -- Select individuals
        selected_individuals = []

        if selection_method == 0:
            scanned_fitness_ratios = fitness_ratios

            for i in range(number_of_selected_ind):
                individual = max(scanned_fitness_ratios)
                selected_individuals.append(fitness_ratios.index(individual))

                scanned_fitness_ratios.remove(individual)

        return selected_individuals





















