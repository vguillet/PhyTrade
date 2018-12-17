

class GA_tools:
    @staticmethod
    def gen_initial_population(population_size=10):
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        population_lst = []
        for i in range(population_size):
            population_lst.append(Individual())

        return population_lst

    @staticmethod
    def evaluate_population(population_lst, data_slice_info, max_worker_threads=8):
        from PhyTrade.Trading_bots.Tradebot_v3 import Tradebot_v3
        from PhyTrade.Tools.MULTI_THREADING_tools import multi_thread_loops

        performance_lst = []

        # -- Multi-thread evaluation
        # def evaluation_func(item):
        #     performance_lst.append(Tradebot_v3(item.parameter_dictionary, data_slice_info).account.net_worth_history[-1])

        # multi_thread_loops(population_lst, evaluation_func, max_worker_threads=max_worker_threads)

        # -- List based evaluation
        for i in range(len(population_lst)):
            performance_lst.append(Tradebot_v3(population_lst[i].parameter_dictionary, data_slice_info).account.net_worth_history[-1])
            print("Parameter set", i+1, "evaluation completed")

        # performance_lst = MATH().normalise_zero_one(performance_lst)
        return performance_lst

    @staticmethod
    def select_from_population(fitness_evaluation, population, selection_method=0, nb_parents=3):

        # -- Determine fitness ratio
        fitness_ratios = []

        for i in range(len(fitness_evaluation)):
            fitness_ratios.append(fitness_evaluation[i]/sum(fitness_evaluation)*100)

        # -- Select individuals
        parents = []

        if selection_method == 0:
            scanned_fitness_ratios = fitness_ratios

            for i in range(nb_parents):
                individual = scanned_fitness_ratios.index(max(scanned_fitness_ratios))
                parents.append(population[individual])

                population.pop(individual)
                scanned_fitness_ratios.pop(individual)

        return parents

    @staticmethod
    def generate_offsprings(population_size, nb_parents, parents, random_ind, mutation_rate=0.2):
        from PhyTrade.GA_optimisation.GA_random_gen import GA_random_gen
        from PhyTrade.GA_optimisation.Individual_gen import Individual
        import random
        from copy import deepcopy

        ga_random_gen = GA_random_gen

        nb_of_parameters_to_mutate = round(Individual().nb_of_parameters * mutation_rate)

        # -- Save parents to new population
        new_population = []
        for parent in parents:
            new_population.append(parent)

        # -- Generate offsprings from parents with mutations
        cycling = -1
        for i in range(population_size-nb_parents-random_ind):

            cycling += 1
            if cycling >= nb_parents:
                cycling = 0

            offspring = deepcopy(parents[cycling])

            for j in range(nb_of_parameters_to_mutate):
                parameter_type_to_modify = random.choice(list(offspring.parameter_dictionary.keys()))

                if parameter_type_to_modify == "timeframe":
                    parameter = random.choice(list(offspring.parameter_dictionary["timeframe"]))

                    offspring.parameter_dictionary["timeframe"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["timeframe"][parameter])

                elif parameter_type_to_modify == "rsi_standard_upper_thresholds":
                    parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_upper_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_upper_thresholds"][parameter])

                elif parameter_type_to_modify == "rsi_standard_lower_thresholds":
                    parameter = random.choice(list(offspring.parameter_dictionary["rsi_standard_lower_thresholds"]))

                    offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["rsi_standard_lower_thresholds"][parameter])

                elif parameter_type_to_modify == "smoothing_factors":
                    parameter = random.choice(list(offspring.parameter_dictionary["smoothing_factors"]))

                    offspring.parameter_dictionary["smoothing_factors"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["smoothing_factors"][parameter])

                elif parameter_type_to_modify == "amplification_factor":
                    parameter = random.choice(list(offspring.parameter_dictionary["amplification_factor"]))

                    offspring.parameter_dictionary["amplification_factor"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["amplification_factor"][parameter])

                elif parameter_type_to_modify == "weights":
                    parameter = random.choice(list(offspring.parameter_dictionary["weights"]))

                    offspring.parameter_dictionary["weights"][parameter] = \
                        ga_random_gen.timeframe_gen(offspring.parameter_dictionary["weights"][parameter])
            new_population.append(offspring)

        # -- Create random_ind number of random individuals and add to new population
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





























