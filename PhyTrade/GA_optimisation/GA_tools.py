

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
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):

        # -- Determine fitness ratio
        fitness_ratios = fitness_evaluation
        # for i in range(len(fitness_evaluation)):
        #     fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

        # -- Select individuals
        parents = []

        if selection_method == 0:
            scanned_fitness_ratios = fitness_ratios

            for i in range(nb_parents):
                individual = max(scanned_fitness_ratios)
                parents.append(population[fitness_ratios.index(individual)])

                scanned_fitness_ratios.remove(individual)

        return parents

    @staticmethod
    def generate_offsprings(population_size, nb_parents, parents, random_ind, mutation_rate=0.2):
        from PhyTrade.GA_optimisation.GA_random_gen import GA_random_gen
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        import random

        ga_random_gen = GA_random_gen

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        new_population = []
        for parent in parents:
            new_population.append(parent)

        cycling = -1

        for i in range(population_size-nb_parents-random_ind):

            cycling += 1
            if cycling >= nb_parents:
                cycling = 0
            offspring = parents[cycling]

            for j in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                if parameter_type_to_modify == "timeframe":
                    parameter = offspring.parameter_dictionary["timeframe"].index(
                        random.choice(offspring.parameter_dictionary["timeframe"]))

                    offspring.parameter_dictionary["timeframe"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["timeframe"][parameter])

                elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
                    parameter = offspring.parameter_dictionary["rsi_standard_upper_thresholds"].index(
                        random.choice(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter])

                elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
                    parameter = offspring.parameter_dictionary["rsi_standard_lower_thresholds"].index(
                        random.choice(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter])

                elif parameter_type_to_modify == "smoothing_factors":
                    parameter = offspring.parameter_dictionary["smoothing_factors"].index(
                        random.choice(offspring.parameter_dictionary["smoothing_factors"]))

                    offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["smoothing_factors"][parameter])

                elif parameter_type_to_modify == "amplification_factor":
                    parameter = offspring.parameter_dictionary["amplification_factor"].index(
                        random.choice(offspring.parameter_dictionary["amplification_factor"]))

                    offspring.parameter_dictionary["amplification_factor"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["amplification_factor"][parameter])

                elif parameter_type_to_modify == "weights":
                    parameter = offspring.parameter_dictionary["weights"].index(
                        random.choice(offspring.parameter_dictionary["weights"]))

                    offspring.parameter_dictionary["weights"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["weights"][parameter])
            new_population.append(offspring)

        for i in range(random_ind):
            new_population.append(Individual())

        return new_population

    @staticmethod
    def throttle(selected_ind, nb_of_generations, decay_rate):

        selected_ind = selected_ind

        decay_nb = selected_ind/decay_rate

        decay_per_generation = round(nb_of_generations/decay_nb)

        selected_ind = selected_ind-decay_per_generation
        if selected_ind == 0:
            selected_ind = 1

        return selected_ind





























