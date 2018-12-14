

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

        performance_lst = []
        for i in range(len(population_lst)):
            performance_lst.append(Tradebot_v3(population_lst[i].parameter_dictionary).account.net_worth_history[-1])
            print("Parameter set", i+1, "evaluation completed")

        # performance_lst = MATH().normalise_zero_one(performance_lst)

        return performance_lst

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, number_of_selected_ind=3):

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
                selected_individuals.append(population[fitness_ratios.index(individual)])

                scanned_fitness_ratios.remove(individual)

        return selected_individuals

    @staticmethod
    def generate_offsprings(population_size, parents, mutation_rate=0.2):
        from PhyTrade.GA_optimisation.GA_random_gen import GA_random_gen
        import random

        ga_random_gen = GA_random_gen

        nb_of_parameters_to_mutate = round(parents[0].nb_of_parameters * mutation_rate)

        new_population = []
        for i in parents:
            new_population.append(i)

        for i in range(population_size-len(parents)):
            offspring = random.choice(parents)
            for j in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                if parameter_type_to_modify == "timeframe":
                    parameter = offspring.parameter_dictionary["timeframe"].index(
                        random.choice(offspring.parameter_dictionary["timeframe"]))

                    offspring.parameter_dictionary["timeframe"][parameter] = \
                        ga_random_gen.timeframe_gen()
                
                elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
                    parameter = offspring.parameter_dictionary["rsi_standard_upper_thresholds"].index(
                        random.choice(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen()
                
                elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
                    parameter = offspring.parameter_dictionary["rsi_standard_lower_thresholds"].index(
                        random.choice(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen()

                elif parameter_type_to_modify == "smoothing_factors":
                    parameter = offspring.parameter_dictionary["smoothing_factors"].index(
                        random.choice(offspring.parameter_dictionary["smoothing_factors"]))

                    offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                        ga_random_gen.timeframe_gen()

                elif parameter_type_to_modify == "amplification_factor":
                    parameter = offspring.parameter_dictionary["amplification_factor"].index(
                        random.choice(offspring.parameter_dictionary["amplification_factor"]))

                    offspring.parameter_dictionary["amplification_factor"][parameter] = \
                        ga_random_gen.timeframe_gen()

                elif parameter_type_to_modify == "weights":
                    parameter = offspring.parameter_dictionary["weights"].index(
                        random.choice(offspring.parameter_dictionary["weights"]))

                    offspring.parameter_dictionary["weights"][parameter] = \
                        ga_random_gen.timeframe_gen()
            new_population.append(offspring)

        return new_population






























